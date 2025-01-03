"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-Jan-20 = Change license from GPLv2 to GPLv3.

2020-Oct-07 = Created.

============ License ============
Copyright (C) 2020, 2023 Michael Stanley

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
import cachetools
import datetime
import pathlib
import pytest
import wmul_test_utils

from wmul_rivendell import RivendellAudioImporter


@pytest.fixture(scope="function")
def setup__gather_file_names(mocker, caplog):
    mock_source_path_1 = "mock_source_path_1"
    mock_source_path_2 = "mock_source_path_2"
    mock_source_paths = [
        mock_source_path_1,
        mock_source_path_2
    ]
    mock_previously_seen_files = "mock_previously_seen_files"

    mock_previously_sent_to_importer_cache = "mock_previously_sent_to_importer_cache"

    mock_datetime_datetime_now = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=5, second=10)

    mock_datetime_datetime_now_function = mocker.Mock(
        return_value=mock_datetime_datetime_now
    )
    mocker.patch("wmul_rivendell.RivendellAudioImporter.datetime.datetime",
                 now=mock_datetime_datetime_now_function)

    mock_files_seen_this_time_this_path_source_path_1 = {
        "mock_key_1": "mock_value_1",
        "mock_key_2": "mock_value_2"
    }
    mock_files_seen_this_time_this_path_source_path_2 = {
        "mock_key_3": "mock_value_3",
        "mock_key_4": "mock_value_4"
    }

    expected_files_seen_this_time = {
        **mock_files_seen_this_time_this_path_source_path_1,
        **mock_files_seen_this_time_this_path_source_path_2
    }

    mock_files_for_importer_this_path_source_path_1 = {
        "mock_file_1",
        "mock_file_2"
    }

    mock_files_for_importer_this_path_source_path_2 = {
        "mock_file_1",
        "mock_file_2"
    }

    expected_files_for_importer = [
        *mock_files_for_importer_this_path_source_path_1,
        *mock_files_for_importer_this_path_source_path_2
    ]

    def mock__gather_names_from_this_path_function(psf, dtn, sp, pstic):
        if sp == mock_source_path_1:
            return mock_files_seen_this_time_this_path_source_path_1, mock_files_for_importer_this_path_source_path_1
        elif sp == mock_source_path_2:
            return mock_files_seen_this_time_this_path_source_path_2, mock_files_for_importer_this_path_source_path_2

    mock__gather_names_from_this_path = mocker.Mock(
        side_effect= mock__gather_names_from_this_path_function
    )

    mocker.patch("wmul_rivendell.RivendellAudioImporter._gather_names_from_this_path",
                 mock__gather_names_from_this_path)

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_file_names(
            mock_source_paths,
            mock_previously_seen_files,
            mock_previously_sent_to_importer_cache
        )

    expected_calls = [
        mocker.call(mock_previously_seen_files, mock_datetime_datetime_now, mock_source_paths[0],
                    mock_previously_sent_to_importer_cache),

        mocker.call(mock_previously_seen_files, mock_datetime_datetime_now, mock_source_paths[1],
                    mock_previously_sent_to_importer_cache),
    ]

    expected_log_messages = [
        f"With Source Paths: {mock_source_paths}\t Previously Seen Files: {mock_previously_seen_files}\t and "
        f"{mock_previously_sent_to_importer_cache}",

        f"Datetime resolved: {mock_datetime_datetime_now}",
        f"Working on {mock_source_path_1}",
        f"Working on {mock_source_path_2}",

        f"Returning Files_seen_this_time: {expected_files_seen_this_time} and "
        f"Files_for_importer: {expected_files_for_importer}"
    ]

    return wmul_test_utils.make_namedtuple(
        "setup__gather_file_names",
        mock_datetime_datetime_now_function=mock_datetime_datetime_now_function,
        expected_files_seen_this_time=expected_files_seen_this_time,
        expected_files_for_importer=expected_files_for_importer,
        mock__gather_names_from_this_path=mock__gather_names_from_this_path,
        result_files_seen_this_time=result_files_seen_this_time,
        result_files_for_importer=result_files_for_importer,
        expected_calls=expected_calls,
        expected_log_messages=expected_log_messages,
        result_log_messages=caplog.messages
    )


def test_datetime_datetime_now_called_correctly(setup__gather_file_names):
    setup__gather_file_names.mock_datetime_datetime_now_function.assert_called_once_with()


def test__gather_names_called_correctly(setup__gather_file_names):
    setup__gather_file_names.mock__gather_names_from_this_path.assert_has_calls(
        setup__gather_file_names.expected_calls)

    assert setup__gather_file_names.mock__gather_names_from_this_path.call_count == \
           len(setup__gather_file_names.expected_calls)


def test_files_seen_this_time_correct(setup__gather_file_names):
    assert setup__gather_file_names.expected_files_seen_this_time == \
           setup__gather_file_names.result_files_seen_this_time


def test_files_for_importer_correct(setup__gather_file_names):
    assert sorted(setup__gather_file_names.expected_files_for_importer) == \
           sorted(setup__gather_file_names.result_files_for_importer)


def test_log_messages_correct(setup__gather_file_names):
    assert sorted(setup__gather_file_names.expected_log_messages) == \
           sorted(setup__gather_file_names.result_log_messages)


def test__gather_file_names_end_to_end(fs, mocker):
    source_path_1 = pathlib.Path(r"\source\group1")
    source_path_2 = pathlib.Path(r"\source\group2")

    fs.create_dir(source_path_1)
    fs.create_dir(source_path_2)

    file_1_1_path = source_path_1 / "file1.wav"
    file_1_2_path = source_path_1 / "file2.wav"
    file_1_3_path = source_path_1 / "file3.wav"
    file_2_3_path = source_path_2 / "file3.wav"
    file_2_4_path = source_path_2 / "file4.wav"
    file_2_5_path = source_path_2 / "file5.wav"

    initial_size = 1_000
    intermediate_size = 5_000
    final_size = 10_000

    file_1_1_fake_file = fs.create_file(file_1_1_path, st_size=final_size)
    file_1_2_fake_file = fs.create_file(file_1_2_path, st_size=initial_size)
    file_1_3_fake_file = fs.create_file(file_1_3_path, st_size=intermediate_size)
    file_2_3_fake_file = fs.create_file(file_2_3_path, st_size=intermediate_size)
    file_2_4_fake_file = fs.create_file(file_2_4_path, st_size=intermediate_size)
    file_2_5_fake_file = fs.create_file(file_2_5_path, st_size=initial_size)

    first_pass_mock_datetime_datetime_now = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=5, second=10)
    second_pass_mock_datetime_datetime_now = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=5, second=30)
    third_pass_mock_datetime_datetime_now = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=5, second=50)
    fourth_pass_mock_datetime_datetime_now = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=6, second=10)
    fifth_pass_mock_datetime_datetime_now = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=6, second=30)
    sixth_pass_mock_datetime_datetime_now = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=6, second=50)

    patched_datetime_datetime = mocker.patch("wmul_rivendell.RivendellAudioImporter.datetime.datetime",
                                             now=lambda: first_pass_mock_datetime_datetime_now)

    source_paths = [source_path_1, source_path_2]
    previously_seen_files = {}
    previously_sent_to_importer_cache = cachetools.TTLCache(maxsize=10_000, ttl=180, timer=lambda: 1)

    # First pass. Should see all six files in files_seen_this_time and no files in files_for_importer.

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_file_names(
            source_paths=source_paths,
            previously_seen_files=previously_seen_files,
            previously_sent_to_importer_cache=previously_sent_to_importer_cache
        )

    first_pass_expected_files_seen_this_time_file_paths = [
        file_1_1_path,
        file_1_2_path,
        file_1_3_path,
        file_2_3_path,
        file_2_4_path,
        file_2_5_path
    ]

    first_pass_expected_files_for_importer = []

    assert sorted(result_files_seen_this_time.keys()) == \
           sorted(first_pass_expected_files_seen_this_time_file_paths)
    assert sorted(result_files_for_importer) == sorted(first_pass_expected_files_for_importer)

    # Second pass. Should still see all six files in files_seen_this_time and no files in files_for_importer.

    file_1_2_fake_file.st_size = intermediate_size
    file_1_3_fake_file.st_size = final_size
    file_2_3_fake_file.st_size = final_size
    file_2_4_fake_file.st_size = final_size
    file_2_5_fake_file.st_size = intermediate_size

    patched_datetime_datetime.now = lambda: second_pass_mock_datetime_datetime_now

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_file_names(
            source_paths=source_paths,
            previously_seen_files=result_files_seen_this_time,
            previously_sent_to_importer_cache=previously_sent_to_importer_cache
        )

    second_pass_expected_files_seen_this_time_file_paths = [
        file_1_1_path,
        file_1_2_path,
        file_1_3_path,
        file_2_3_path,
        file_2_4_path,
        file_2_5_path
    ]

    second_pass_expected_files_for_importer = []

    assert sorted(result_files_seen_this_time.keys()) == \
           sorted(second_pass_expected_files_seen_this_time_file_paths)
    assert sorted(result_files_for_importer) == sorted(second_pass_expected_files_for_importer)

    # Third pass. Should see all but file_1_1 seen_this_time and should see file_1_1 for importer.

    file_1_2_fake_file.st_size = final_size
    file_2_5_fake_file.st_size = final_size

    patched_datetime_datetime.now = lambda: third_pass_mock_datetime_datetime_now

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_file_names(
            source_paths=source_paths,
            previously_seen_files=result_files_seen_this_time,
            previously_sent_to_importer_cache=previously_sent_to_importer_cache
        )

    result_files_for_importer_file_paths = [file_item.file_path for file_item in result_files_for_importer]

    third_pass_expected_files_seen_this_time_file_paths = [
        file_1_2_path,
        file_1_3_path,
        file_2_3_path,
        file_2_4_path,
        file_2_5_path
    ]

    third_pass_expected_files_for_importer_file_paths = [file_1_1_path]

    assert sorted(result_files_seen_this_time.keys()) == \
           sorted(third_pass_expected_files_seen_this_time_file_paths)
    assert sorted(result_files_for_importer_file_paths) == \
           sorted(third_pass_expected_files_for_importer_file_paths)

    # Fourth pass. Should see 1_2 and 2_5 seen_this_time. Should see file_1_3, 2_3, and 2_4 for importer.

    previously_sent_to_importer_cache[file_1_1_path] = True

    patched_datetime_datetime.now = lambda: fourth_pass_mock_datetime_datetime_now

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_file_names(
            source_paths=source_paths,
            previously_seen_files=result_files_seen_this_time,
            previously_sent_to_importer_cache=previously_sent_to_importer_cache
        )

    result_files_for_importer_file_paths = [file_item.file_path for file_item in result_files_for_importer]

    fourth_pass_expected_files_seen_this_time_file_paths = [
        file_1_2_path,
        file_2_5_path
    ]

    fourth_pass_expected_files_for_importer_file_paths = [
        file_1_3_path,
        file_2_3_path,
        file_2_4_path
    ]

    assert sorted(result_files_seen_this_time.keys()) == \
           sorted(fourth_pass_expected_files_seen_this_time_file_paths)
    assert sorted(result_files_for_importer_file_paths) == \
           sorted(fourth_pass_expected_files_for_importer_file_paths)

    previously_sent_to_importer_cache[file_1_3_path] = True
    previously_sent_to_importer_cache[file_2_3_path] = True
    previously_sent_to_importer_cache[file_2_4_path] = True

    # Fifth pass. Should not see any seen_this_time Should see 1_2 and 2_5 to importer.

    patched_datetime_datetime.now = lambda: fifth_pass_mock_datetime_datetime_now

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_file_names(
            source_paths=source_paths,
            previously_seen_files=result_files_seen_this_time,
            previously_sent_to_importer_cache=previously_sent_to_importer_cache
        )

    result_files_for_importer_file_paths = [file_item.file_path for file_item in result_files_for_importer]

    fifth_pass_expected_files_seen_this_time_file_paths = []

    fifth_pass_expected_files_for_importer_file_paths = [
        file_1_2_path,
        file_2_5_path
    ]

    assert sorted(result_files_seen_this_time.keys()) == \
           sorted(fifth_pass_expected_files_seen_this_time_file_paths)
    assert sorted(result_files_for_importer_file_paths) == \
           sorted(fifth_pass_expected_files_for_importer_file_paths)

    previously_sent_to_importer_cache[file_1_2_path] = True
    previously_sent_to_importer_cache[file_2_5_path] = True

    # Sixth pass. Should not see any seen_this_time or files_for_importer.

    patched_datetime_datetime.now = lambda: sixth_pass_mock_datetime_datetime_now

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_file_names(
            source_paths=source_paths,
            previously_seen_files=result_files_seen_this_time,
            previously_sent_to_importer_cache=previously_sent_to_importer_cache
        )

    result_files_for_importer_file_paths = [file_item.file_path for file_item in result_files_for_importer]

    sixth_pass_expected_files_seen_this_time_file_paths = []
    sixth_pass_expected_files_for_importer_file_paths = []

    assert sorted(result_files_seen_this_time.keys()) == \
           sorted(sixth_pass_expected_files_seen_this_time_file_paths)
    assert sorted(result_files_for_importer_file_paths) == \
           sorted(sixth_pass_expected_files_for_importer_file_paths)

