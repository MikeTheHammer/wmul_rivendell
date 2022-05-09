"""
@Author = 'Michael Stanley'

============ Change Log ============
2020-Oct-07 = Created.

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
import cachetools
import pytest
import wmul_test_utils

from wmul_rivendell import RivendellAudioImporter


@pytest.fixture(scope="function")
def setup__gather_names_from_this_path(mocker, caplog):
    mock_previously_seen_files = "mock_previously_seen_files"
    mock_datetime_now = "mock_datetime_now"

    mock_source_path_1 = "mock_source_path_1"
    mock_source_path_2 = "mock_source_path_2"
    mock_source_path_3 = "mock_source_path_3"
    mock_source_path_4 = "mock_source_path_4"

    mock_ttl = 40_000
    mock_previously_sent_to_importer_cache = cachetools.TTLCache(
        10_000,
        mock_ttl
    )
    mock_previously_sent_to_importer_cache[mock_source_path_4] = True

    mock_source_path_rglob = [
        mock_source_path_1,
        mock_source_path_2,
        mock_source_path_3,
        mock_source_path_4
    ]

    mock_source_path_rglob_function = mocker.Mock(return_value=mock_source_path_rglob)

    mock_source_path = mocker.Mock(rglob=mock_source_path_rglob_function)

    mock_seen_this_time = mocker.Mock(return_value=True)

    def mock__check_this_file_function(psf, fp, dtn, sp):
        if fp == mock_source_path_1:
            return None, mock_source_path_1
        elif fp == mock_source_path_2:
            return None, None
        elif fp == mock_source_path_3:
            return mock_seen_this_time, None
        else:
            raise ValueError("file path not valid")

    mock__check_this_file = mocker.Mock(side_effect=mock__check_this_file_function)

    mocker.patch("wmul_rivendell.RivendellAudioImporter._check_this_file", mock__check_this_file)

    expected_files_seen_this_time = {mock_source_path_3: mock_seen_this_time}
    expected_files_for_importer = [mock_source_path_1]

    result_files_seen_this_time, result_files_for_importer = \
        RivendellAudioImporter._gather_names_from_this_path(
            mock_previously_seen_files,
            mock_datetime_now,
            mock_source_path,
            mock_previously_sent_to_importer_cache
        )

    expected_calls = [
        mocker.call(mock_previously_seen_files, mock_source_path_rglob[0], mock_datetime_now, mock_source_path),
        mocker.call(mock_previously_seen_files, mock_source_path_rglob[1], mock_datetime_now, mock_source_path),
        mocker.call(mock_previously_seen_files, mock_source_path_rglob[2], mock_datetime_now, mock_source_path)
    ]

    expected_log_messages = [
        f"With Previously Seen Files: {mock_previously_seen_files}, Datetime_now: {mock_datetime_now}, "
        f"Source Path: {mock_source_path}, and Previously Sent to Importer Cache: "
        f"{mock_previously_sent_to_importer_cache}",

        f"Working on {mock_source_path_1}",
        f"Working on {mock_source_path_2}",
        f"Working on {mock_source_path_3}",
        f"Working on {mock_source_path_4}",
        f"Have not sent {mock_source_path_1} to the importer in the previous {mock_ttl} seconds",
        f"Have not sent {mock_source_path_2} to the importer in the previous {mock_ttl} seconds",
        f"Have not sent {mock_source_path_3} to the importer in the previous {mock_ttl} seconds",
        f"Seen this time! {mock_source_path_3}",
        f"For importer! {mock_source_path_1}",
        f"Not for seen this time or importer! {mock_source_path_2}",
        f"Sent a file with this name to the importer within the previous {mock_ttl} seconds! {mock_source_path_4}",
        f"Returning files_seen_this_time: {expected_files_seen_this_time} and "
        f"files_for_importer {expected_files_for_importer}"
    ]

    return wmul_test_utils.make_namedtuple(
        "setup__gather_names_from_this_path",
        mock_source_path_rglob_function=mock_source_path_rglob_function,
        mock__check_this_file=mock__check_this_file,
        expected_files_seen_this_time=expected_files_seen_this_time,
        expected_files_for_importer=expected_files_for_importer,
        result_files_seen_this_time=result_files_seen_this_time,
        result_files_for_importer=result_files_for_importer,
        expected_calls=expected_calls,
        expected_log_messages=expected_log_messages,
        result_log_messages=caplog.messages
    )


def test_source_path_rglob_called_correctly(setup__gather_names_from_this_path):
    setup__gather_names_from_this_path.mock_source_path_rglob_function.assert_called_once_with("*.[Ww][Aa][Vv]")


def test__check_this_file_called_correctly(setup__gather_names_from_this_path):
    setup__gather_names_from_this_path.mock__check_this_file.assert_has_calls(
        setup__gather_names_from_this_path.expected_calls)

    assert setup__gather_names_from_this_path.mock__check_this_file.call_count == \
           len(setup__gather_names_from_this_path.expected_calls)


def test_files_seen_this_time_correct(setup__gather_names_from_this_path):
    assert setup__gather_names_from_this_path.expected_files_seen_this_time == \
           setup__gather_names_from_this_path.result_files_seen_this_time


def test_files_for_importer_correct(setup__gather_names_from_this_path):
    assert setup__gather_names_from_this_path.expected_files_for_importer == \
           setup__gather_names_from_this_path.result_files_for_importer


def test_log_messages_correct(setup__gather_names_from_this_path):
    assert sorted(setup__gather_names_from_this_path.expected_log_messages) == \
           sorted(setup__gather_names_from_this_path.result_log_messages)
