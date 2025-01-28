"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-Jan-20 = Change license from GPLv2 to GPLv3.

2023-Jan-19 = Created.

============ License ============
Copyright (C) 2023, 2025 Michael Stanley

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
from click.testing import CliRunner
import pytest

from wmul_rivendell import cli
from wmul_test_utils import generate_true_false_matrix_from_list_of_strings

filter_cart_report_params, filter_cart_report_ids = \
    generate_true_false_matrix_from_list_of_strings(
        "filter_cart_report",
        [
            "include_macros",
            "include_all_cuts",
            "use_trailing_comma",
            "exclude_groups"
        ]

    )

@pytest.mark.parametrize("params", filter_cart_report_params, ids=filter_cart_report_ids)
def test_filter_cart_report(fs, params, mocker, caplog):
    mock_rivendell_cart_filename = "/test/mock_rivendell_cart_filename.txt"
    fs.create_file(mock_rivendell_cart_filename)
    mock_output_filename = "/test/mock_output_filename"
    mock_desired_fields_filename = "/test/desired.txt"

    desired_fields_file_contents = "Cart_number\nGroup_Name\nTitle\nArtist\nAlbum\nYear\nLength\nUser_Defined\nSched_Codes\n"
    expected_desired_fields = [
        "Cart_number", 
        "Group_Name",
        "Title",
        "Artist",
        "Album",
        "Year",
        "Length",
        "User_Defined",
        "Sched_Codes"
    ]

    fs.create_file(mock_desired_fields_filename, 
                   contents=desired_fields_file_contents)

    mock_rivendell_carts = "mock_rivendell_carts"
    mock_load_carts = mocker.Mock(return_value=mock_rivendell_carts)

    mock_load_cart_data_dump_object = mocker.Mock(load_carts=mock_load_carts)
    mock_load_cart_data_dump_constructor = mocker.patch(
        "wmul_rivendell.cli.LoadCartDataDump",
        return_value=mock_load_cart_data_dump_object,
        autospec=True
    )

    mock_filter_cart_report_object = mocker.Mock()

    mock_filter_cart_report_constructor = mocker.patch(
        "wmul_rivendell.cli.FilterCartReportForMusicScheduler",
        return_value=mock_filter_cart_report_object,
        autospec=True
    )

    cli_args = [
            mock_rivendell_cart_filename,
            mock_output_filename,
            mock_desired_fields_filename
        ]
    
    if params.include_macros:
        cli_args.append("--include_macros")
    
    if params.include_all_cuts:
        cli_args.append("--include_all_cuts")

    if params.use_trailing_comma:
        cli_args.append("--use_trailing_comma")

    if params.exclude_groups:
        exclude_groups_file_contents = "LAUDANTIUM\nASPERIORES\n"
        mock_exclude_groups_filename = "/test/mock_exclude_groups_filename.txt"
        fs.create_file(mock_exclude_groups_filename, contents=exclude_groups_file_contents)
        cli_args.append("--excluded_groups_file_name")
        cli_args.append(mock_exclude_groups_filename)
        expected_exclude_groups = ["LAUDANTIUM", "ASPERIORES"]
    else:
        expected_exclude_groups = []

    runner = CliRunner()
    result = runner.invoke(
        cli.filter_cart_report,
        cli_args
    )

    assert result.exit_code == 0

    mock_load_cart_data_dump_constructor.assert_called_once_with(
        rivendell_cart_data_filename=mock_rivendell_cart_filename,
        include_macros=params.include_macros,
        include_all_cuts=params.include_all_cuts,
        excluded_group_list=expected_exclude_groups,
    )

    mock_load_carts.assert_called_once_with()

    mock_filter_cart_report_constructor.assert_called_once_with(
        rivendell_carts=mock_rivendell_carts,
        output_filename=mock_output_filename,
        desired_field_list=expected_desired_fields,
        use_trailing_comma=params.use_trailing_comma
    )

    mock_filter_cart_report_object.run_script.assert_called_once_with()
