"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-Feb-27 = Catch crashes that occur when renaming a bad file and the file 
              is locked by another user.

2023-Jan-20 = Back-insert items into change log.
              Change license from GPLv2 to GPLv3.

2022-Jun-09 = Improve the crash handling when the problem is a network burp.

2022-May-16 = Fix bug in subprocess due to back-porting behind Python 3.7. 
              Python 3.6 does not have the subprocess.run capture_output param.

2022-May-05 = Make .wav case-insensitive.

2021-May-26 = Added recovery from certain network burps.

2020-Oct-15 = Added ability to tell rdimport where to log.
              Now renamed files as _FAILED when rdimport rejects them.
              Improve own logging.

2020-Jun-30 = Created.

============ License ============
Copyright (C) 2020-2023 Michael Stanley

This file is part of wmul_rivendell.

wmul_rivendell is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free 
Software Foundation, either version 3 of the License, or (at your option) any 
later version.

wmul_rivendell is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
wmul_rivendell. If not, see <https://www.gnu.org/licenses/>. 
"""
from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path
from time import sleep
import datetime
import cachetools
import subprocess

import wmul_logger

_logger = wmul_logger.get_logger()


@total_ordering
class FileInformation:

    def __init__(self, file_path: Path, timestamp: datetime.datetime, source_path: Path):
        self.file_path = file_path
        self.file_size = file_path.stat().st_size
        self.timestamp = timestamp
        self.relative_path = file_path.relative_to(source_path)

    def __str__(self):
        return f"Path: {self.file_path}, Size: {self.file_size}, Timestamp: {self.timestamp}, " \
               f"Relative_Path: {self.relative_path}."

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(str(self))

    def same_size_as(self, other):
        return self.file_size == other.file_size

    def new_info_much_newer(self, second_file, minimum_difference):
        difference = self.timestamp - second_file.timestamp
        return difference < datetime.timedelta(seconds=-minimum_difference)

    def generate_importer_command(self, log_argument):
        _logger.debug(f"With {self}")
        relative_path = self.relative_path
        relative_path_parts = relative_path.parts
        len_of_relative_path_parts = len(relative_path_parts)
        if len_of_relative_path_parts == 1:
            _logger.debug(f"This file does not have a group. {str(self.file_path)}")
            return None
        elif len_of_relative_path_parts == 2:
            _logger.debug("No scheduler codes.")
            group_folder, file_path = relative_path_parts
            scheduler_codes_options = []
        else:
            _logger.debug("Has scheduler codes.")
            group_folder, *scheduler_code_folders, file_path = relative_path_parts
            scheduler_codes_options = [f'--add-scheduler-code={scheduler_code}'
                                       for scheduler_code in scheduler_code_folders]

        import_command = [
            *scheduler_codes_options,
            "--autotrim-level=0",
            "--normalization-level=0",
            "--title-from-cartchunk-cutid",
            "--delete-source",
            f'--set-string-description="{self.file_path.name}"',
            "--verbose"
        ]

        if log_argument:
            import_command.append(log_argument)

        import_command.extend(
            [group_folder, str(self.file_path)]
        )
        return import_command

    def _failed(self, new_suffix):
        old_suffix = self.file_path.suffix
        new_path = self.file_path.with_suffix(old_suffix + new_suffix)
        try: 
            self.file_path.rename(new_path)
        except OSError as ose:
            _logger.debug(ose)
            if ose.errno == 16: # Device or Resource Busy (Someone else has the file locked).
                return
            else:
                raise

    def failed_rdimport(self):
        self._failed("_RDIMPORT_FAILED")

    def failed_group(self):
        self._failed("_NO_GROUP_FAILED")


@dataclass
class ImportRivendellFileWithFileSystemMetadataArguments:
    source_paths: list
    cache_duration: int
    rdimport_syslog: bool
    rdimport_log_file_name: str


def _gather_file_names(source_paths, previously_seen_files, previously_sent_to_importer_cache):
    _logger.debug(f"With Source Paths: {source_paths}\t Previously Seen Files: {previously_seen_files}\t "
                  f"and {previously_sent_to_importer_cache}")
    files_seen_this_time = {}
    files_for_importer = []
    datetime_now = datetime.datetime.now()
    _logger.debug(f"Datetime resolved: {datetime_now}")
    for source_path in source_paths:
        _logger.debug(f"Working on {source_path}")
        files_seen_this_time_this_path, files_for_importer_this_path = \
            _gather_names_from_this_path(previously_seen_files, datetime_now, source_path,
                                         previously_sent_to_importer_cache)
        files_seen_this_time.update(files_seen_this_time_this_path)
        files_for_importer.extend(files_for_importer_this_path)
    _logger.debug(f"Returning Files_seen_this_time: {files_seen_this_time} and Files_for_importer: {files_for_importer}")
    return files_seen_this_time, files_for_importer


def _gather_names_from_this_path(previously_seen_files, datetime_now, source_path, previously_sent_to_importer_cache):
    _logger.debug(
        f"With Previously Seen Files: {previously_seen_files}, Datetime_now: {datetime_now}, "
        f"Source Path: {source_path}, and Previously Sent to Importer Cache: {previously_sent_to_importer_cache}"
    )
    matching_file_paths = source_path.rglob("*.[Ww][Aa][Vv]")
    files_seen_this_time = {}
    files_for_importer = []
    for file_path in matching_file_paths:
        _logger.debug(f"Working on {file_path}")
        if file_path not in previously_sent_to_importer_cache:
            _logger.debug(f"Have not sent {file_path} to the importer in the previous "
                          f"{previously_sent_to_importer_cache.ttl} seconds")
            seen_this_time, for_importer = _check_this_file(previously_seen_files, file_path, datetime_now, source_path)
            if seen_this_time:
                _logger.debug(f"Seen this time! {file_path}")
                files_seen_this_time[file_path] = seen_this_time
            elif for_importer:
                _logger.info(f"For importer! {file_path}")
                files_for_importer.append(for_importer)
            else:
                _logger.debug(f"Not for seen this time or importer! {file_path}")
        else:
            _logger.debug(f"Sent a file with this name to the importer within the previous "
                          f"{previously_sent_to_importer_cache.ttl} seconds! {file_path}")
    _logger.debug(f"Returning files_seen_this_time: {files_seen_this_time} and files_for_importer {files_for_importer}")
    return files_seen_this_time, files_for_importer


def _check_this_file(previously_seen_files, file_path, datetime_now, source_path):
    _logger.debug(f"With {previously_seen_files}, {file_path}, {datetime_now}, {source_path}")
    if file_path.is_file():
        _logger.debug("Is File!")
        this_version = FileInformation(file_path=file_path, timestamp=datetime_now, source_path=source_path)
        previously_seen_version = previously_seen_files.get(file_path)
        _logger.debug(f"Previously seen version: {previously_seen_version}")
        if _previous_seen_and_same_size(previously_seen_version, this_version):
            _logger.debug("Previously seen and same size!")
            return _for_importer_or_seen_this_time(previously_seen_version, this_version)
        else:
            _logger.debug("New file or new size!")
            return this_version, None
    else:
        _logger.debug("Is not a file!")
        return None, None


def _for_importer_or_seen_this_time(previously_seen_version, this_version):
    _logger.debug(f"With {previously_seen_version}, {this_version}")
    if previously_seen_version.new_info_much_newer(this_version, 30):
        _logger.debug("This one is much newer!")
        return None, this_version
    else:
        _logger.debug("This one is not new enough!")
        return previously_seen_version, None


def _previous_seen_and_same_size(previously_seen_version, new_version):
    _logger.debug(f"With {previously_seen_version}, and {new_version}")
    return previously_seen_version and previously_seen_version.same_size_as(new_version)


def _run_importer_on_selected_files(files_for_importer, previously_sent_to_importer_cache, log_argument):
    for file_for_importer in files_for_importer:
        _logger.info(f"Sending to the importer: {file_for_importer.file_path}")
        importer_command = file_for_importer.generate_importer_command(log_argument)
        _logger.info(f"Importer command: {importer_command}")
        if not importer_command:
            file_for_importer.failed_group()
        previously_sent_to_importer_cache[file_for_importer.file_path] = True
        results = subprocess.run(["rdimport", *importer_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if results.returncode == 0:
            if ((b"is not readable or not a recognized format, skipping..." in results.stdout) or 
                (b"Unable to open " in results.stdout)):
                _logger.error(f"Error on {importer_command[-1]}, {results.args}, {results.stderr}, {results.stdout}")
                file_for_importer.failed_rdimport()
            else:
                _logger.debug(f"Success! {importer_command[-1]}, {results.args}, {results.stderr}, {results.stdout}")
        else:
            _logger.error(f"Error on {importer_command[-1]}, {results.args}, {results.stderr}, {results.stdout}")
            file_for_importer.failed_rdimport()


def run_script(arguments):
    _logger.debug(f"With {arguments}")
    previously_seen_files = {}
    previously_sent_to_importer_cache = cachetools.TTLCache(10_000, arguments.cache_duration)

    if arguments.rdimport_syslog:
        log_argument = "--log-syslog"
    elif arguments.rdimport_log_file_name:
        log_argument = f"--log-filename={arguments.rdimport_log_file_name}"
    else:
        log_argument = None

    _logger.info(f"With log_argument: {log_argument}")

    while True:
        exception_cache = cachetools.TTLCache(5, 3600)
        try:
            _logger.debug("Loop!")
            previously_seen_files, files_for_importer = _gather_file_names(
                arguments.source_paths,
                previously_seen_files,
                previously_sent_to_importer_cache
            )
            _run_importer_on_selected_files(files_for_importer, previously_sent_to_importer_cache, log_argument)
            sleep(10)
        except BlockingIOError as bio:
            _logger.debug(bio)
            exception_cache[datetime.datetime.now()] = True
            if exception_cache.currsize > 3:
                raise
            sleep(300)
        except OSError as ose:
            _logger.debug(ose)
            if ose.errno == 112:
                exception_cache[datetime.datetime.now()] = True
                if exception_cache.currsize > 3:
                    raise
                sleep(300)
            else:
                raise
