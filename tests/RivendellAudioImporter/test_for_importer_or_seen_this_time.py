"""
@Author = 'Michael Stanley'

============ Change Log ============
2020-Oct-08 = Created.

============ License ============
Copyright (C) 2020 Michael Stanley

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
import wmul_test_utils

from collections import namedtuple
from wmul_rivendell import RivendellAudioImporter


_for_importer_or_seen_this_time_options = namedtuple(
    "_for_importer_or_seen_this_time_options",
    [
        "new_info_newer"
    ]
)
_for_importer_or_seen_this_time_params, _for_importer_or_seen_this_time_ids = \
    wmul_test_utils.generate_true_false_matrix_from_namedtuple(_for_importer_or_seen_this_time_options)


@pytest.fixture(scope="function", params=_for_importer_or_seen_this_time_params,
                ids=_for_importer_or_seen_this_time_ids)
def setup__for_importer_or_seen_this_time(request, mocker):
    param = request.param

    mock_new_info_much_newer = mocker.Mock(return_value=param.new_info_newer)
    mock_previously_seen_version = mocker.Mock(new_info_much_newer=mock_new_info_much_newer)
    mock_this_version = "mock_this_version"

    result_previous_version, result_this_version = \
        RivendellAudioImporter._for_importer_or_seen_this_time(
            mock_previously_seen_version,
            mock_this_version
        )

    return wmul_test_utils.make_namedtuple(
        "setup__for_importer_or_seen_this_time",
        param=param,
        mock_new_info_much_newer=mock_new_info_much_newer,
        mock_previously_seen_version=mock_previously_seen_version,
        mock_this_version=mock_this_version,
        result_previous_version=result_previous_version,
        result_this_version=result_this_version
    )


def test_new_info_much_newer_called_correctly(setup__for_importer_or_seen_this_time):
    setup__for_importer_or_seen_this_time.mock_new_info_much_newer.assert_called_once_with(
        setup__for_importer_or_seen_this_time.mock_this_version, 30)


def test_correct_file_path_returned(setup__for_importer_or_seen_this_time):
    if setup__for_importer_or_seen_this_time.param.new_info_newer:
        assert setup__for_importer_or_seen_this_time.result_this_version == \
               setup__for_importer_or_seen_this_time.mock_this_version
    else:
        assert setup__for_importer_or_seen_this_time.result_this_version is None


def test_correct_previously_seen_version_returned(setup__for_importer_or_seen_this_time):
    if setup__for_importer_or_seen_this_time.param.new_info_newer:
        assert setup__for_importer_or_seen_this_time.result_previous_version is None
    else:
        assert setup__for_importer_or_seen_this_time.result_previous_version == \
               setup__for_importer_or_seen_this_time.mock_previously_seen_version

