"""
@Author = 'Michael Stanley'

I am reasonably certain that this was based on Open Source Radio's 'load-log-skip-to-current-line':
https://github.com/opensourceradio/ram/blob/e112952d87a64d92d564ab9693d37c9e63740607/usr/local/bin/load-log-skip-to-current-time .
However, I did not document my source at the time I originally wrote this.

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
from dataclasses import dataclass
from datetime import datetime, timedelta
from mysql.connector import Error

import mysql.connector
import subprocess
import wmul_emailer
import wmul_logger

_logger = wmul_logger.get_logger()


@dataclass
class LoadCurrentLogLineArguments:
    log_datetime: datetime
    sql_host: str
    sql_user: str
    sql_pass: str
    sql_database_name: str
    log_name_format: str
    rivendell_host: str
    dry_run: bool
    start_immediately: bool
    days_back: int
    default_log: str
    log_machine: int
    emailer: wmul_emailer.EmailSender


def _get_start_time_in_millis(log_datetime):
    desired_time = log_datetime.time()
    hours_in_millis = desired_time.hour * 3_600_000
    minutes_in_millis = desired_time.minute * 60_000
    seconds_in_millis = desired_time.second * 1000
    return hours_in_millis + minutes_in_millis + seconds_in_millis


def _get_desired_log_line(arguments, desired_start_time_in_millis):
    connection = mysql.connector.connect(
        host=arguments.sql_host,
        database=arguments.sql_database_name,
        user=arguments.sql_user,
        password=arguments.sql_pass
    )
    working_datetime = arguments.log_datetime
    working_days_back = arguments.days_back
    log_name = None
    desire_log_line = None
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            while desire_log_line is None:
                log_name = working_datetime.strftime(arguments.log_name_format)
                desire_log_line = _query_database_for_log_line(
                    log_name=log_name,
                    desired_start_time_in_millis=desired_start_time_in_millis,
                    cursor=cursor
                )
                if desire_log_line is None:
                    if working_days_back > 0:
                        working_datetime -= timedelta(days=1)
                        working_days_back -= 1
                    elif arguments.default_log:
                        log_name = arguments.default_log
                        desire_log_line = _get_default_log(cursor, log_name, desired_start_time_in_millis)
                    else:
                        _log_possibilities_exhausted()
                        break
    except Error as e:
        _logger.error("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            _logger.debug("MySQL connection is closed")
    return desire_log_line, log_name


def _get_default_log(cursor, log_name, desired_start_time_in_millis):
    record = _query_database_for_log_line(
        log_name=log_name,
        desired_start_time_in_millis=desired_start_time_in_millis,
        cursor=cursor
    )
    if record is None:
        _log_possibilities_exhausted()
    return record


def _log_possibilities_exhausted():
    _logger.critical("All log possibilities exhausted.")


def _query_database_for_log_line(log_name, desired_start_time_in_millis, cursor):
    sql_statement = "SELECT count, cart_number, start_time FROM LOG_LINES WHERE log_name = %s AND start_time " \
                    ">= 0 ORDER BY count ASC LIMIT 1;"
    cursor.execute(sql_statement, (log_name,))
    first_line = cursor.fetchone()
    if first_line is None:
        _logger.debug(f"There are no log lines with Log Name: {log_name}")
        return None
    if desired_start_time_in_millis == 0:
        return first_line

    sql_statement = "SELECT count, cart_number, start_time FROM LOG_LINES WHERE log_name = %s AND " \
                    "start_time > 0 AND start_time <= %s ORDER BY count DESC LIMIT 1;"
    cursor.execute(sql_statement, (log_name, desired_start_time_in_millis))
    line_closest_to_time = cursor.fetchone()
    if line_closest_to_time is None:
        return first_line
    else:
        return line_closest_to_time


def _build_rml_command(desired_log_line, log_name, start_immediately, log_machine):
    load_log_command = f"LL {log_machine} {log_name} {desired_log_line[0]} ! "
    if start_immediately:
        start_immediately_command = f"PN {log_machine} !"
    else:
        start_immediately_command = ""
    set_mode_automatic_command = f"PM 2 {log_machine} ! "
    return f"{load_log_command} {start_immediately_command} {set_mode_automatic_command}"


def _send_command_to_rivendell(rml_command, rivendell_host):
    try:
        rml_process = subprocess.run(
            ["rmlsend", f"--to-host={rivendell_host}", rml_command],
            capture_output=True,
            check=True
        )
        _logger.debug(f"Sending command to Rivendell succeeded. {rml_process}")
        return str(rml_process)
    except subprocess.CalledProcessError as e:
        _logger.critical("Sending command to Rivendell failed.")
        _logger.critical(e)
        return "Sending command to Rivendell failed."


def _send_email(arguments, log_name, desired_log_line, send_command_result):
    if arguments.emailer:
        email_subject = "[WMUL RIVENDELL] Workstation Loaded a Log from Script"
        email_body = f"Rivendell Workstation {arguments.rivendell_host} loaded a log from script.\n" \
                     f"The script was passed in the following arguments.\n" \
                     f"Datetime: {arguments.log_datetime.strftime('%Y-%m-%d  %H:%M:%S')}\n" \
                     f"Days Back: {arguments.days_back}\n" \
                     f"Default_Log: {arguments.default_log}\n" \
                     f"Log Machine: {arguments.log_machine}\n" \
                     f"Start Immediately: {arguments.start_immediately}\n\n" \
                     f"It tried to load {log_name}, and jump to line {desired_log_line[0]} with cart " \
                     f"{desired_log_line[1]} and start time {timedelta(milliseconds=int(desired_log_line[2]))}.\n" \
                     f"The result was: {send_command_result}"

        arguments.emailer.send_email(
            email_body=email_body,
            email_subject=email_subject,
        )


def run_script(arguments):
    _logger.debug(f"In run_script with {arguments}")
    desired_start_time_in_millis = _get_start_time_in_millis(arguments.log_datetime)
    _logger.info(f"Found desired_start_time_in_millis: {desired_start_time_in_millis}")
    desired_log_line, log_name = _get_desired_log_line(arguments, desired_start_time_in_millis)
    _logger.info(f"Found desired_log_line {desired_log_line} and log_name {log_name}")
    if desired_log_line:
        rml_command = _build_rml_command(desired_log_line, log_name, arguments.start_immediately, arguments.log_machine)
        _logger.info(f"Found rml_command: {rml_command}")
        if arguments.dry_run:
            print(f"Would have loaded log: {log_name} on host: {arguments.rivendell_host}, jumped to line "
                  f"{desired_log_line}, started_immediately: {arguments.start_immediately}, "
                  f"using the command: {rml_command}")
            return
        send_command_result = _send_command_to_rivendell(rml_command, arguments.rivendell_host)
    else:
        if arguments.dry_run:
            print(f"Unable to find a log line to load.")
            return
        send_command_result = "Could not run command, exhausted all possibilities"
    _send_email(arguments, log_name, desired_log_line, send_command_result)

