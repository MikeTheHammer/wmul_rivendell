"""
@Author = 'Michael Stanley'

============ Change Log ============
2025-Jun-17 = Created.

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
from wmul_rivendell.cli import get_items_from_file


def test_good_file(fs):
    file_name = "/temp/items.txt"
    fs.create_file(file_name, contents="Praesent\nmaximus \narcu\reu\norci")
    expected_items = [
        "Praesent",
        "maximus",
        "arcu",
        "eu",
        "orci" 
    ]

    result = get_items_from_file(file_name=file_name)

    assert result == expected_items


def test_excludes_blank_line(fs):
    file_name = "/temp/items.txt"
    fs.create_file(file_name, contents="Praesent\nmaximus \n arcu  \n\r eu\norci")
    expected_fields = [
        "Praesent",
        "maximus",
        "arcu",
        "eu",
        "orci" 
    ]

    result = get_items_from_file(file_name=file_name)

    assert result == expected_fields


def test_raises_value_error_on_empty_file(fs):
    file_name = "/temp/items.txt"
    fs.create_file(file_name, contents="")

    with pytest.raises(ValueError, match=f"The file: {file_name}, did not contain any items. It appears to be blank or empty."):
        result = get_items_from_file(file_name=file_name)


def test_returns_empty_list_on_no_file():
    result = get_items_from_file(None)
    assert result == []
