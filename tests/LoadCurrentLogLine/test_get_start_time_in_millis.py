"""
@Author = 'Michael Stanley'

Describe this file.

============ Change Log ============
2021-Mar-11 = Created.

============ License ============
Copyright (C) 2021 Michael Stanley

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
from wmul_rivendell.LoadCurrentLogLine import _get_start_time_in_millis
from datetime import datetime


def test_zero_time():
    time_under_test = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)

    expected_time_in_millis = 0
    result_time_in_millis = _get_start_time_in_millis(time_under_test)

    assert expected_time_in_millis == result_time_in_millis


def test_3_50_20_am():
    time_under_test = datetime(year=2020, month=1, day=1, hour=3, minute=50, second=20)

    expected_time_in_millis = 13_820_000
    result_time_in_millis = _get_start_time_in_millis(time_under_test)

    assert expected_time_in_millis == result_time_in_millis


def test_3_50_20_pm():
    time_under_test = datetime(year=2020, month=1, day=1, hour=15, minute=50, second=20)

    expected_time_in_millis = 57_020_000
    result_time_in_millis = _get_start_time_in_millis(time_under_test)

    assert expected_time_in_millis == result_time_in_millis


def test_two_days_same_hour_same_millis():
    first_time_under_test = datetime(year=2020, month=1, day=1, hour=15, minute=50, second=0)
    second_time_under_test = datetime(year=2020, month=1, day=2, hour=15, minute=50, second=0)

    first_time_in_millis = _get_start_time_in_millis(first_time_under_test)
    second_time_in_millis = _get_start_time_in_millis(second_time_under_test)

    assert first_time_in_millis == second_time_in_millis
