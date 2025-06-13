"""
@Author = 'Michael Stanley'

============ Change Log ============
2025-Jun-12 = Created.

============ License ============
Copyright (C) 2025 Michael Stanley

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
import pytest
from wmul_rivendell.cli import get_excluded_groups


def test_good_file(fs):
    excluded_groups_file_name = "/temp/excluded_groups.txt"
    fs.create_file(excluded_groups_file_name, contents="Praesent\nmaximus \narcu\reu\norci")
    expected_groups = [
        "Praesent",
        "maximus",
        "arcu",
        "eu",
        "orci" 
    ]

    result = get_excluded_groups(excluded_groups_file_name=excluded_groups_file_name)

    assert result == expected_groups

def test_excludes_blank_line(fs):
    excluded_groups_file_name = "/temp/excluded_groups.txt"
    fs.create_file(excluded_groups_file_name, contents="Praesent\nmaximus \n arcu  \n\r eu\norci")
    expected_groups = [
        "Praesent",
        "maximus",
        "arcu",
        "eu",
        "orci" 
    ]

    result = get_excluded_groups(excluded_groups_file_name=excluded_groups_file_name)

    assert result == expected_groups

def test_raises_value_error_on_empty_file(fs):
    excluded_groups_file_name = "/temp/excluded_groups.txt"
    fs.create_file(excluded_groups_file_name, contents="")

    with pytest.raises(ValueError, match=f"The excluded groups file: {excluded_groups_file_name}, did not contain any desired fields. It appears to be blank or empty. If you wish to include all groups, omit the --exclude_groups option."):
        result = get_excluded_groups(excluded_groups_file_name=excluded_groups_file_name)
