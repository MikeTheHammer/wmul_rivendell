"""
@Author = 'Michael Stanley'

Tests for RivendellAudioImporter.py

============ Change Log ============
2020-Jul-25 = Added GPL notice.

2020-Jul-01 = Created.

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
import pytest
import wmul_test_utils

from collections import namedtuple
from wmul_rivendell import RivendellAudioImporter

run_script_options = namedtuple(
    "run_script_options",
    [
        "use_log_syslog",
        "use_log_filename"
    ]
)
run_script_params, run_script_ids = \
    wmul_test_utils.generate_true_false_matrix_from_namedtuple(run_script_options)


@pytest.fixture(scope="function", params=run_script_params, ids=run_script_ids)
def setup_run_script(request, mocker, caplog):
    params = request.param
    mock_cache_duration = 100
    mock_source_paths = ["mock_source_paths"]

    if params.use_log_syslog:
        mock_rdimport_syslog = True
        mock_rdimport_log_file_name = None
        expected_log_argument = "--log-syslog"
    elif params.use_log_filename:
        mock_rdimport_syslog = False
        mock_rdimport_log_file_name = "mock_rdimport_log_file_name"
        expected_log_argument = f"--log-filename={mock_rdimport_log_file_name}"
    else:
        mock_rdimport_syslog = False
        mock_rdimport_log_file_name = None
        expected_log_argument = None

    mock_arguments = RivendellAudioImporter.ImportRivendellFileWithFileSystemMetadataArguments(
        source_paths=mock_source_paths,
        cache_duration=mock_cache_duration,
        rdimport_syslog=mock_rdimport_syslog,
        rdimport_log_file_name=mock_rdimport_log_file_name
    )

    mock_ttl_cache = "mock_ttl_cache"
    mock_ttl_cache_constructor = mocker.Mock(return_value=mock_ttl_cache)
    mocker.patch("wmul_rivendell.RivendellAudioImporter.cachetools.TTLCache",
                  mock_ttl_cache_constructor)

    mock_returned_files_for_importer = "mock_returned_files_for_importer"

    mock_gather_file_names = mocker.Mock(return_value=(None, mock_returned_files_for_importer))
    mocker.patch("wmul_rivendell.RivendellAudioImporter._gather_file_names",
                 mock_gather_file_names)

    mock_run_importer = mocker.Mock()
    mocker.patch("wmul_rivendell.RivendellAudioImporter._run_importer_on_selected_files",
                 mock_run_importer)

    def mock_sleep_function(dur):
        raise RuntimeError
    mock_sleep = mocker.Mock(side_effect=mock_sleep_function)

    mocker.patch("wmul_rivendell.RivendellAudioImporter.sleep",
                 mock_sleep)

    expected_log_messages = [
        f"With {mock_arguments}",
        "Loop!"
    ]

    with pytest.raises(RuntimeError):
        RivendellAudioImporter.run_script(mock_arguments)

    return wmul_test_utils.make_namedtuple(
        "setup_run_script",
        mock_arguments=mock_arguments,
        mock_ttl_cache_constructor=mock_ttl_cache_constructor,
        mock_cache_duration=mock_cache_duration,
        expected_log_messages=expected_log_messages,
        caplog_text=caplog.text,
        mock_gather_file_names=mock_gather_file_names,
        mock_source_paths=mock_source_paths,
        mock_ttl_cache=mock_ttl_cache,
        mock_run_importer=mock_run_importer,
        mock_returned_files_for_importer=mock_returned_files_for_importer,
        expected_log_argument=expected_log_argument,
        mock_sleep=mock_sleep
    )


def test_run_script(setup_run_script, mocker):
    mock_ttl_cache_constructor_expected_calls = [
        mocker.call(10_000, setup_run_script.mock_cache_duration),
        mocker.call(5, 3600)
    ]

    wmul_test_utils.assert_has_only_these_calls(
        setup_run_script.mock_ttl_cache_constructor, 
        mock_ttl_cache_constructor_expected_calls
    )

    for elm in setup_run_script.expected_log_messages:
        assert elm in setup_run_script.caplog_text

    setup_run_script.mock_gather_file_names.assert_called_once()

    mgfn_call_source_paths, mgfn_call_previously_seen_files, mgfn_call_previously_sent_to_importer_cache = \
        setup_run_script.mock_gather_file_names.call_args[0]

    assert mgfn_call_source_paths == setup_run_script.mock_source_paths
    assert isinstance(mgfn_call_previously_seen_files, dict)
    assert mgfn_call_previously_sent_to_importer_cache == setup_run_script.mock_ttl_cache

    setup_run_script.mock_run_importer.assert_called_once_with(
        setup_run_script.mock_returned_files_for_importer,
        setup_run_script.mock_ttl_cache,
        setup_run_script.expected_log_argument
    )

    setup_run_script.mock_sleep.assert_called_once_with(10)
