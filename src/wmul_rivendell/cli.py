"""
@Author = 'Michael Stanley'

Describe this file.

============ Change Log ============
2020-Jun-26 = Created.

============ License ============
Copyright (C) 2020 Michael Stanley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import click
import datetime

from pathlib import Path

from wmul_rivendell.FilterCartReportForMusicScheduler import FilterCartReportForMusicScheduler
from wmul_rivendell.LoadCurrentLogLine import LoadCurrentLogLineArguments, run_script as load_current_log_lines
from wmul_rivendell.RivendellAudioImporter import \
    ImportRivendellFileWithFileSystemMetadataArguments, run_script as import_rivendell_file
import wmul_emailer
import wmul_logger


_logger = wmul_logger.get_logger()


class RequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.required_if = kwargs.pop('required_if')
        assert self.required_if, "'required_if' parameter required"
        kwargs['help'] = f"{kwargs.get('help', '')} NOTE: This argument is required if {self.required_if} " \
                         f"is supplied".strip()
        super(RequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.required_if in opts

        if other_present:
            if not we_are_present:
                raise click.UsageError(f"Illegal usage: {self.name} is required when {self.required_if} is supplied")
            else:
                self.prompt = None

        return super(RequiredIf, self).handle_parse_result(ctx, opts, args)


class MXWith(click.Option):
    def __init__(self, *args, **kwargs):
        self.mx_with = kwargs.pop('mx_with')
        assert self.mx_with, "'mx_with' parameter required"
        kwargs['help'] = f"{kwargs.get('help', '')} NOTE: This argument is mutually exclusive with " \
                         f"{self.mx_with}.".strip()
        super(MXWith, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.mx_with in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(f"Illegal usage: {self.name} is mutually exclusive with {self.mx_with}.")
            else:
                self.prompt = None

        return super(MXWith, self).handle_parse_result(ctx, opts, args)


@click.group()
@click.version_option()
@click.option('--log_name', type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True), default=None,
              required=False, help="The path to the log file.")
@click.option('--log_level', type=click.IntRange(10, 50, clamp=True), required=False, default=30,
              help="The log level: 10: Debug, 20: Info, 30: Warning, 40: Error, 50: Critical. "
                   "Intermediate values (E.G. 32) are permitted, but will essentially be rounded up (E.G. Entering 32 "
                   "is the same as entering 40. Logging messages lower than the log level will not be written to the "
                   "log. E.G. If 30 is input, then all Debug, Info, and Verbose messages will be silenced.")
def wmul_rivendell_cli(log_name, log_level):
    if log_name:
        global _logger
        _logger = wmul_logger.setup_logger(file_name=log_name, log_level=log_level)
        import pkg_resources  # part of setuptools
        version = pkg_resources.require("wmul_rivendell")[0].version
        _logger.warning(f"Version: {version}")
        _logger.warning("In command_line_interface")


@wmul_rivendell_cli.command()
@click.argument('rivendell_cart_filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
                nargs=1)
@click.argument('output_filename', type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True),
                nargs=1)
@click.argument('desired_fields_filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
                nargs=1)
@click.option('--include_macros', is_flag=True, help="Include macro carts in the output file.")
@click.option('--include_all_cuts', is_flag=True,
              help="Include all the individual cuts in the output file. If this is left unset, then the output file "
                   "will only include the lowest numbered cut in each cart.")
@click.option('--use_trailing_comma', is_flag=True,
              help="Include a comma at the end of each line. Required by some scheduling software, such as Natural "
                   "Music, to see the final field.")
@click.option('--fix_header', is_flag=True, 
              help="Whether to fix the header bug in Rivendell 3.6.4 - 3.6.6.")
def filter_cart_report(rivendell_cart_filename, output_filename, desired_fields_filename, include_macros,
                       include_all_cuts, use_trailing_comma, fix_header):
    _logger.debug(f"With {locals()}")

    with open(desired_fields_filename, "rt") as desired_fields_reader:
        desired_fields = [desired_field.strip("\n\r") for desired_field in desired_fields_reader]

    x = FilterCartReportForMusicScheduler(
        rivendell_cart_data_filename=rivendell_cart_filename,
        output_filename=output_filename,
        desired_field_list=desired_fields,
        include_macros=include_macros,
        include_all_cuts=include_all_cuts,
        use_trailing_comma=use_trailing_comma,
        fix_header=fix_header
    )
    x.run_script()


@wmul_rivendell_cli.command()
@click.argument('log_name_format', type=str, nargs=1)
@click.argument('rivendell_host', type=str, nargs=1)
@click.option('--sql_host', type=str, nargs=1, default="localhost",
              help="The host name to the SQL database. Usually localhost. Default: localhost.")
@click.option('--sql_user', type=str, nargs=1, default="rduser",
              help="The username for the SQL database. Usually rduser. Default: rduser.")
@click.option('--sql_pass', type=str, nargs=1, default="letmein",
              help="The password for the SQL database. Usually letmein. Default: letmein.")
@click.option('--sql_database_name', type=str, nargs=1, default="Rivendell",
              help="The Database name of the SQL database. Usually Rivendell. Default: Rivendell.")
@click.option('--use_date', type=click.DateTime(formats=["%Y-%m-%d", "%y-%m-%d"]), nargs=1,
              help="The date of the log to be loaded. Format is YY-MM-DD or YYYY-MM-DD. If this option is omitted, "
                   "the system date of the system running the script will be used.")
@click.option('--use_time',
              type=click.DateTime(formats=["%I:%M:%S %p", "%I:%M %p", "%I %p", "%H:%M:%S", "%H:%M", "%H"]),
              nargs=1, help="The time of the log line to be loaded. The script will find the line closest to, but "
                            "before that time. Valid formats are HH:MM:SS AM, HH:MM AM, HH AM, HH:MM:SS, HH:MM, and HH."
                            "If AM/PM are present, HH will be 12-hour. If AM/PM are absent, HH will be 24-hour. IF MM "
                            "and/or SS are omitted, they will be set to 00. If this option is omitted,"
                            "the system time of the system running the script will be used.")
@click.option('--dry_run', is_flag=True,
              help="For testing purposes. Prints out the log line that is selected, but does not load it.")
@click.option('--start_immediately', is_flag=True,
              help="Starts the selected log line immediately. If not set, the selected log line will be 'made next'.")
@click.option('--days_back', type=int, nargs=1, default=7,
              help="Maximum number of days back in time to go. If a log is not available for the given day, the script"
                   " will try to load the previous day's log. It will keep going back in time up to and including "
                   "this many days. This option is for cases where it is preferred to load and replay an old log "
                   "rather than no log. If no logs can be found for those dates, it will try to load the default log, "
                   "if provided. Set this value to 0 to not attempt previous days' logs. Defaults to 7.")
@click.option('--default_log', type=str, nargs=1,
              help="The full name of the last-ditch log to try to load if day based logs fail.")
@click.option('--log_machine', type=int, nargs=1, default=1,
              help="The log machine on which to load the playlist. Defaults to 1 (Main Log).")
@click.option("--email_address", type=str, multiple=True,
              help="The e-mail address to which the report should be sent.")
@click.option("--mail_server", type=str, cls=RequiredIf, required_if="email_address",
              help="The address of the e-mail SMTP server to use.")
@click.option("--mail_port", type=int, default=25, help="The port of the e-mail server. Defaults to 25")
@click.option("--mail_username", type=str, cls=RequiredIf, required_if="email_address",
              help="The username to authenticate with the e-mail server.")
@click.option("--mail_password", type=str, cls=RequiredIf, required_if="email_address",
              help="The password to authenticate with the e-mail server.")
def load_current_log_line(log_name_format, rivendell_host, sql_host, sql_user, sql_pass, sql_database_name, use_date,
                          use_time, dry_run, start_immediately, days_back, default_log, log_machine, email_address,
                          mail_server, mail_port, mail_username, mail_password):
    _logger.debug(f"With {locals()}")

    if email_address:
        emailer = wmul_emailer.EmailSender(
            server_host=mail_server,
            port=mail_port,
            user_name=mail_username,
            password=mail_password,
            destination_email_addresses=email_address,
            from_email_address='rivendell@wmul-nas-4'
        )
    else:
        emailer = None

    if use_date:
        use_date = use_date.date()
    else:
        use_date = datetime.datetime.now().date()

    if use_time:
        use_time = use_time.time()
    else:
        use_time = datetime.datetime.now().time()

    use_datetime = datetime.datetime.combine(date=use_date, time=use_time)

    x = LoadCurrentLogLineArguments(
        log_datetime=use_datetime,
        rivendell_host=rivendell_host,
        sql_host=sql_host,
        sql_user=sql_user,
        sql_pass=sql_pass,
        sql_database_name=sql_database_name,
        log_name_format=log_name_format,
        dry_run=dry_run,
        start_immediately=start_immediately,
        days_back=days_back,
        default_log=default_log,
        log_machine=log_machine,
        emailer=emailer
    )

    load_current_log_lines(x)


@wmul_rivendell_cli.command()
@click.argument('source_paths', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True), nargs=-1)
@click.option('--cache_duration', type=int, default=180,
              help="How long (in seconds) this importer will remember a given file name after sending it to the "
                   "Rivendell importer. For this duration, this importer will ignore any other files with this name. "
                   "Defaults to 180 seconds (3 minutes).")
@click.option('--rdimport_syslog', is_flag=True, cls=MXWith, mx_with='rdimport_log_file_name',
              help="Tell rdimport to log to syslog.")
@click.option('--rdimport_log_file_name',
              type=click.Path(file_okay=True, dir_okay=False, readable=True, writable=True), cls=MXWith,
              mx_with="rdimport_syslog",  help="Tell rdimport to log to this filename.")
def import_with_file_system_metadata(source_paths, cache_duration, rdimport_syslog, rdimport_log_file_name):
    _logger.debug(f"With {locals()}")
    source_paths = [Path(sp) for sp in source_paths]

    if rdimport_log_file_name:
        rdimport_log_file_name = str(rdimport_log_file_name)
    else:
        rdimport_log_file_name = ""

    args = ImportRivendellFileWithFileSystemMetadataArguments(
        source_paths=source_paths,
        cache_duration=cache_duration,
        rdimport_syslog=rdimport_syslog,
        rdimport_log_file_name=rdimport_log_file_name
    )
    try:
        import_rivendell_file(arguments=args)
    except Exception as e:
        _logger.exception(f"Final crash: {e}")
