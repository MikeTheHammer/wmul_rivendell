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
from pathlib import Path
from wmul_rivendell.cli import convert_cart_database
from wmul_test_utils import assert_has_only_these_calls

def test_convert_cart_database(mocker):
    mock_rivendell_cart_filename = mocker.Mock()
    mock_output_filename = "/temp/mock_output_filename.txt"
    expected_output_filename = Path(mock_output_filename)
    mock_desired_fields_filename = mocker.Mock()
    mock_desired_fields = mocker.Mock()
    mock_include_macros = mocker.Mock()
    mock_include_all_cuts = mocker.Mock()
    mock_excluded_groups_filename = mocker.Mock()
    mock_excluded_groups = mocker.Mock()
    mock_run_script = mocker.Mock()
    mock_converter_object = mocker.Mock(run_script=mock_run_script)
    mock_converter_function = mocker.Mock(return_value=mock_converter_object)

    def get_items_from_file(file_name):
        if file_name == mock_desired_fields_filename:
            return mock_desired_fields
        elif file_name == mock_excluded_groups_filename:
            return mock_excluded_groups
        else:
            assert False, f"An unexpected file_name was passed to get_items_from_file: {file_name}"


    mock_get_items_from_file = mocker.patch(
        "wmul_rivendell.cli.get_items_from_file", 
        mocker.Mock(side_effect=get_items_from_file)
    )

    mock_rivendell_carts = mocker.Mock()

    mock_load_carts_function = mocker.Mock(return_value=mock_rivendell_carts)

    mock_lcdd_object = mocker.Mock(load_carts=mock_load_carts_function)

    mock_load_cart_data_dump = mocker.patch(
        "wmul_rivendell.cli.LoadCartDataDump",
        mocker.Mock(return_value=mock_lcdd_object)
    )

    expected_get_items_calls = [
        mocker.call(file_name=mock_desired_fields_filename),
        mocker.call(file_name=mock_excluded_groups_filename)
    ]

    convert_cart_database(
        rivendell_cart_filename=mock_rivendell_cart_filename,
        output_filename=mock_output_filename,
        desired_fields_filename=mock_desired_fields_filename,
        include_macros=mock_include_macros,
        include_all_cuts=mock_include_all_cuts,
        excluded_groups_file_name=mock_excluded_groups_filename,
        converter=mock_converter_function
    )

    assert_has_only_these_calls(
        mock=mock_get_items_from_file,
        calls=expected_get_items_calls
    )

    mock_load_cart_data_dump.assert_called_once_with(
        rivendell_cart_data_filename=mock_rivendell_cart_filename,
        include_all_cuts=mock_include_all_cuts,
        include_macros=mock_include_macros,
        excluded_group_list=mock_excluded_groups
    )

    mock_load_carts_function.assert_called_once_with()

    mock_converter_function.assert_called_once_with(
        rivendell_carts=mock_rivendell_carts,
        desired_field_list=mock_desired_fields,
        output_filename=expected_output_filename
    )

    mock_run_script.assert_called_once_with()
