"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-Jan-20 = Change license from GPLv2 to GPLv3.

2022-May-16 = Fix a bug caused by backporting behind Python 3.7, which does 
                not have the subprocess.run capture_output param.

2020-Oct-08 = Created.

============ License ============
Copyright (C) 2020, 2022-2023 Michael Stanley

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

from wmul_rivendell import RivendellAudioImporter


@pytest.fixture(scope="function")
def setup__run_importer_on_selected_files(caplog, mocker):
    mock_file_1_command = "mock_file_1_command"
    mock_file_2_command = "mock_file_2_command"
    mock_file_3_command = "mock_file_3_command"
    mock_file_4_command = "mock_file_4_command"

    mock_file_1_file_path = "mock_file_1_file_path"
    mock_file_2_file_path = "mock_file_2_file_path"
    mock_file_3_file_path = "mock_file_3_file_path"
    mock_file_4_file_path = "mock_file_4_file_path"

    mock_file_1_failed = mocker.Mock()
    mock_file_2_failed = mocker.Mock()
    mock_file_3_failed = mocker.Mock()
    mock_file_4_failed = mocker.Mock()

    mock_file_1 = mocker.Mock(
        generate_importer_command=mocker.Mock(return_value=[mock_file_1_command]),
        file_path=mock_file_1_file_path,
        rdimport_failed=mock_file_1_failed
    )
    mock_file_2 = mocker.Mock(
        generate_importer_command=mocker.Mock(return_value=[mock_file_2_command]),
        file_path=mock_file_2_file_path,
        rdimport_failed=mock_file_2_failed
    )
    mock_file_3 = mocker.Mock(
        generate_importer_command=mocker.Mock(return_value=[mock_file_3_command]),
        file_path=mock_file_3_file_path,
        rdimport_failed=mock_file_3_failed
    )
    mock_file_4 = mocker.Mock(
        generate_importer_command=mocker.Mock(return_value=[mock_file_4_command]),
        file_path=mock_file_4_file_path,
        rdimport_failed=mock_file_4_failed
    )

    mock_files_for_importer = [mock_file_1, mock_file_2, mock_file_3, mock_file_4]

    mock_previously_sent_to_importer = {}

    mock_log_arguement = "mock_log_argument"

    file_4_stdout = b'blah blah is not readable or not a recognized format, skipping... blah blah'

    def mock_subprocess_run_function(args, stdout, stderr):
        if args[1] == mock_file_2_command:
            return mocker.Mock(returncode=-1, args=args, stdout=b'', stderr=b'')
        elif args[1] == mock_file_4_command:
            return mocker.Mock(
                returncode=0,
                args=args,
                stdout=file_4_stdout,
                stderr=b''
            )
        else:
            return mocker.Mock(returncode=0, args=args, stdout=b'', stderr=b'')

    mock_subprocess_run = mocker.Mock(side_effect=mock_subprocess_run_function)
    mocker.patch("wmul_rivendell.RivendellAudioImporter.subprocess.run",
                 mock_subprocess_run)

    mock_subprocess_pipe = "mock_suprocess_pipe"
    mocker.patch("wmul_rivendell.RivendellAudioImporter.subprocess.PIPE",
                 mock_subprocess_pipe)

    RivendellAudioImporter._run_importer_on_selected_files(
        mock_files_for_importer,
        mock_previously_sent_to_importer,
        mock_log_arguement
    )

    expected_calls = [
        mocker.call(["rdimport", mock_file_1_command], stderr=mock_subprocess_pipe, stdout=mock_subprocess_pipe),
        mocker.call(["rdimport", mock_file_2_command], stderr=mock_subprocess_pipe, stdout=mock_subprocess_pipe),
        mocker.call(["rdimport", mock_file_3_command], stderr=mock_subprocess_pipe, stdout=mock_subprocess_pipe),
        mocker.call(["rdimport", mock_file_4_command], stderr=mock_subprocess_pipe, stdout=mock_subprocess_pipe)
    ]

    expected_previously_sent_to_importer = {
        mock_file_1_file_path: True,
        mock_file_2_file_path: True,
        mock_file_3_file_path: True,
        mock_file_4_file_path: True
    }

    expected_log_entries = [
        f"Sending to the importer: {mock_file_1_file_path}",
        f"Importer command: ['{mock_file_1_command}']",
        f"Success! {mock_file_1_command}, ['rdimport', '{mock_file_1_command}'], b'', b''",
        f"Sending to the importer: {mock_file_2_file_path}",
        f"Importer command: ['{mock_file_2_command}']",
        f"Error on {mock_file_2_command}, ['rdimport', '{mock_file_2_command}'], b'', b''",
        f"Sending to the importer: {mock_file_3_file_path}",
        f"Importer command: ['{mock_file_3_command}']",
        f"Success! {mock_file_3_command}, ['rdimport', '{mock_file_3_command}'], b'', b''",
        f"Sending to the importer: {mock_file_4_file_path}",
        f"Importer command: ['{mock_file_4_command}']",
        f"Error on {mock_file_4_command}, ['rdimport', '{mock_file_4_command}'], b'', {file_4_stdout}",
    ]

    return wmul_test_utils.make_namedtuple(
        "setup__run_importer_on_selected_files",
        mock_files_for_importer=mock_files_for_importer,
        mock_previously_sent_to_importer=mock_previously_sent_to_importer,
        mock_log_arguement=mock_log_arguement,
        mock_subprocess_run=mock_subprocess_run,
        expected_calls=expected_calls,
        expected_previously_sent_to_importer=expected_previously_sent_to_importer,
        expected_log_entries=expected_log_entries,
        result_log_entries=caplog.messages
    )


def test_generate_importer_command_called_correctly(
        setup__run_importer_on_selected_files):
    for mock_file in setup__run_importer_on_selected_files.mock_files_for_importer:
        mock_file.generate_importer_command.assert_called_once_with(
            setup__run_importer_on_selected_files.mock_log_arguement
        )


def test_cache_correct(setup__run_importer_on_selected_files):
    assert setup__run_importer_on_selected_files.mock_previously_sent_to_importer == \
           setup__run_importer_on_selected_files.expected_previously_sent_to_importer


def test_subprocess_called_correctly(setup__run_importer_on_selected_files):
    setup__run_importer_on_selected_files.mock_subprocess_run.assert_has_calls(
        setup__run_importer_on_selected_files.expected_calls)

    assert setup__run_importer_on_selected_files.mock_subprocess_run.call_count == \
           len(setup__run_importer_on_selected_files.expected_calls)


def test_logging_correct(setup__run_importer_on_selected_files):
    assert sorted(setup__run_importer_on_selected_files.expected_log_entries) == \
           sorted(setup__run_importer_on_selected_files.result_log_entries)
