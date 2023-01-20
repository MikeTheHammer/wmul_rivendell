"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-Jan-20 = Change license from GPLv2 to GPLv3.

2020-Oct-08 = Created.

============ License ============
Copyright (C) 2020, 2023 Michael Stanley

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


_check_this_file_test_options = namedtuple(
    "_check_this_file_test_options",
    [
        "is_file",
        "previously_seen_and_same_size",
        "for_importer"
    ]
)
_check_this_file_test_params, _check_this_file_test_ids = \
    wmul_test_utils.generate_true_false_matrix_from_namedtuple(_check_this_file_test_options)


@pytest.fixture(scope="function", params=_check_this_file_test_params, ids=_check_this_file_test_ids)
def setup__check_this_file(request, mocker):
    param = request.param

    mock_file_path_is_file = mocker.Mock(return_value=param.is_file)
    mock_file_path = mocker.Mock(
        is_file=mock_file_path_is_file
    )

    mock_datetime_now = "mock_datetime_now"
    mock_source_path = "mock_source_path"

    mock_previously_seen_version = "mock_previously_seen_version"
    mock_previously_seen_files = {
        mock_file_path: mock_previously_seen_version
    }

    mock_this_version = "mock_this_version"
    mock_file_information = mocker.Mock(return_value=mock_this_version)
    mocker.patch("wmul_rivendell.RivendellAudioImporter.FileInformation",
                 mock_file_information)

    def mock__previous_seen_and_same_size_function(psv, tv):
        return param.previously_seen_and_same_size
    mock__previous_seen_and_same_size = mocker.Mock(side_effect=mock__previous_seen_and_same_size_function)
    mocker.patch("wmul_rivendell.RivendellAudioImporter._previous_seen_and_same_size",
                 mock__previous_seen_and_same_size)

    def mock__for_importer_or_seen_this_time_function(psv, tv):
        if param.for_importer:
            return None, tv
        else:
            return psv, None
    mock__for_importer_or_seen_this_time = mocker.Mock(side_effect=mock__for_importer_or_seen_this_time_function)
    mocker.patch("wmul_rivendell.RivendellAudioImporter._for_importer_or_seen_this_time",
                 mock__for_importer_or_seen_this_time)

    result_version, result_for_importer = RivendellAudioImporter._check_this_file(
        mock_previously_seen_files, mock_file_path, mock_datetime_now, mock_source_path
    )

    return wmul_test_utils.make_namedtuple(
        "setup__check_this_file",
        param=param,
        mock_file_path_is_file=mock_file_path_is_file,
        mock_file_path=mock_file_path,
        mock_datetime_now=mock_datetime_now,
        mock_source_path=mock_source_path,
        mock_previously_seen_version=mock_previously_seen_version,
        mock_this_version=mock_this_version,
        mock_file_information=mock_file_information,
        mock__previous_seen_and_same_size=mock__previous_seen_and_same_size,
        mock__for_importer_or_seen_this_time=mock__for_importer_or_seen_this_time,
        result_version=result_version,
        result_for_importer=result_for_importer
    )


def test_file_path_is_file_called_correctly(setup__check_this_file):
    setup__check_this_file.mock_file_path_is_file.assert_called_once_with()


def test_file_information_called_correctly(setup__check_this_file):
    if setup__check_this_file.param.is_file:
        setup__check_this_file.mock_file_information.assert_called_once_with(
            file_path=setup__check_this_file.mock_file_path,
            timestamp=setup__check_this_file.mock_datetime_now,
            source_path=setup__check_this_file.mock_source_path
        )
    else:
        setup__check_this_file.mock_file_information.assert_not_called()


def test__previous_seen_called_correctly(setup__check_this_file):
    if setup__check_this_file.param.is_file:
        setup__check_this_file.mock__previous_seen_and_same_size.assert_called_once_with(
            setup__check_this_file.mock_previously_seen_version,
            setup__check_this_file.mock_this_version
        )
    else:
        setup__check_this_file.mock__previous_seen_and_same_size.assert_not_called()


def test__for_importer_called_correctly(setup__check_this_file):
    if setup__check_this_file.param.is_file:
        if setup__check_this_file.param.previously_seen_and_same_size:
            setup__check_this_file.mock__for_importer_or_seen_this_time.assert_called_once_with(
                setup__check_this_file.mock_previously_seen_version,
                setup__check_this_file.mock_this_version
            )
        else:
            setup__check_this_file.mock__for_importer_or_seen_this_time.assert_not_called()
    else:
        setup__check_this_file.mock__for_importer_or_seen_this_time.assert_not_called()


def test__version_correct(setup__check_this_file):
    if setup__check_this_file.param.is_file:
        if setup__check_this_file.param.previously_seen_and_same_size:
            if setup__check_this_file.param.for_importer:
                assert setup__check_this_file.result_version is None
            else:
                assert setup__check_this_file.result_version == setup__check_this_file.mock_previously_seen_version
        else:
            assert setup__check_this_file.result_version == setup__check_this_file.mock_this_version
    else:
        assert setup__check_this_file.result_version is None


def test_for_importer_correct(setup__check_this_file):
    if setup__check_this_file.param.is_file:
        if setup__check_this_file.param.previously_seen_and_same_size:
            if setup__check_this_file.param.for_importer:
                assert setup__check_this_file.result_for_importer == setup__check_this_file.mock_this_version
            else:
                assert setup__check_this_file.result_for_importer is None
        else:
            assert setup__check_this_file.result_for_importer is None
    else:
        assert setup__check_this_file.result_for_importer is None
