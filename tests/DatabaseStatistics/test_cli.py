"""
@Author = 'Michael Stanley'

============ Change Log ============
2025-Jan-03 = Created

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
from click.testing import CliRunner
import pytest

from wmul_rivendell import cli
from wmul_test_utils import generate_true_false_matrix_from_list_of_strings

database_statistic_params, database_statistic_ids = \
    generate_true_false_matrix_from_list_of_strings(
        "database_statistic",
        [
            "include_all_cuts",
            "exclude_groups"
        ]

    )

@pytest.mark.parametrize("params", database_statistic_params, ids=database_statistic_ids)
def test_database_statistics(fs, params, mocker, caplog):
    mock_rivendell_cart_filename = "/test/mock_rivendell_cart_filename.txt"
    fs.create_file(mock_rivendell_cart_filename)
    mock_output_filename = "/test/mock_output_filename"

    mock_rivendell_carts = "mock_rivendell_carts"
    mock_load_carts = mocker.Mock(return_value=mock_rivendell_carts)

    mock_load_cart_data_dump_object = mocker.Mock(load_carts=mock_load_carts)
    mock_load_cart_data_dump_constructor = mocker.patch(
        "wmul_rivendell.cli.LoadCartDataDump",
        return_value=mock_load_cart_data_dump_object,
        autospec=True
    )

    mock_database_statistics_object = mocker.Mock()

    mock_database_statistics_constructor = mocker.patch(
        "wmul_rivendell.cli.DatabaseStatistics",
        return_value=mock_database_statistics_object,
        autospec=True
    )

    cli_args = [
            mock_rivendell_cart_filename,
            mock_output_filename,
        ]

    if params.include_all_cuts:
        cli_args.append("--include_all_cuts")

    if params.exclude_groups:
        exclude_groups_file_contents = "ALTERNATIV\nSG_MISC\n"
        mock_exclude_groups_filename = "/test/mock_exclude_groups_filename.txt"
        fs.create_file(mock_exclude_groups_filename, contents=exclude_groups_file_contents)
        cli_args.append("--excluded_groups_file_name")
        cli_args.append(mock_exclude_groups_filename)
        expected_exclude_groups = ["ALTERNATIV", "SG_MISC"]
    else:
        expected_exclude_groups = []

    runner = CliRunner()
    result = runner.invoke(
        cli.database_statistics,
        cli_args
    )

    assert result.exit_code == 0

    mock_load_cart_data_dump_constructor.assert_called_once_with(
        rivendell_cart_data_filename=mock_rivendell_cart_filename,
        include_macros=False,
        include_all_cuts=params.include_all_cuts,
        excluded_group_list=expected_exclude_groups,
    )

    mock_load_carts.assert_called_once_with()

    mock_database_statistics_constructor.assert_called_once_with(
        rivendell_carts=mock_rivendell_carts,
        output_filename=mock_output_filename,
    )

    mock_database_statistics_object.run_script.assert_called_once_with()
