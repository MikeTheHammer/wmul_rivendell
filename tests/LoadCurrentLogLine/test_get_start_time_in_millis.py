"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-Jan-20 = Change license from GPLv2 to GPLv3.

2021-Mar-11 = Created.

============ License ============
Copyright (C) 2021, 2023 Michael Stanley

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
