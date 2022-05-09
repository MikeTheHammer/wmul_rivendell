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
import datetime
import pathlib
import pytest
import wmul_test_utils

from wmul_rivendell import RivendellAudioImporter


@pytest.fixture(scope="function")
def setup_construction(fs):
    mock_file_path = pathlib.Path(r"mock\path\to\file.mp3")
    mock_size = 3_000
    fs.create_file(mock_file_path, st_size=mock_size)
    mock_source_path = pathlib.Path(r"mock\path")
    mock_timestamp = datetime.datetime(year=2020, month=6, day=30, hour=11, minute=5, second=45)

    file_info = RivendellAudioImporter.FileInformation(
        file_path=mock_file_path,
        timestamp=mock_timestamp,
        source_path=mock_source_path
    )

    expected_relative_path = pathlib.Path(r"to\file.mp3")
    expected_str = f"Path: {mock_file_path}, Size: {mock_size}, Timestamp: {mock_timestamp}, " \
                   f"Relative_Path: {expected_relative_path}."
    expected_hash = hash(expected_str)

    return wmul_test_utils.make_namedtuple(
        "setup_construction",
        mock_file_path=mock_file_path,
        mock_size=mock_size,
        mock_timestamp=mock_timestamp,
        file_info=file_info,
        expected_relative_path=expected_relative_path,
        expected_str=expected_str,
        expected_hash=expected_hash
    )


def test_file_path(setup_construction):
    assert setup_construction.mock_file_path == setup_construction.file_info.file_path


def test_file_size(setup_construction):
    assert setup_construction.mock_size == setup_construction.file_info.file_size


def test_timestamp(setup_construction):
    assert setup_construction.mock_timestamp == setup_construction.file_info.timestamp


def test_relative_path(setup_construction):
    assert setup_construction.expected_relative_path == setup_construction.file_info.relative_path


def test_str(setup_construction):
    assert setup_construction.expected_str == str(setup_construction.file_info)


def test_hash(setup_construction):
    assert setup_construction.expected_hash == hash(setup_construction.file_info)


@pytest.fixture(scope="function")
def setup_comparison(fs):
    mock_file_path_string_1 = r"mock\path\to\file1.mp3"
    mock_file_path_1 = pathlib.Path(mock_file_path_string_1)
    mock_size_1 = 3_000
    fs.create_file(mock_file_path_string_1, st_size=mock_size_1)
    mock_source_path_1 = pathlib.Path(r"mock\path")
    mock_timestamp_1 = datetime.datetime(year=2020, month=6, day=30, hour=11, minute=5, second=45)

    mock_file_path_string_3 = r"mock\path\to\file3.mp3"
    mock_file_path_3 = pathlib.Path(mock_file_path_string_3)
    fs.create_file(mock_file_path_string_3, st_size=mock_size_1)

    file_info_1 = RivendellAudioImporter.FileInformation(
        file_path=mock_file_path_1,
        timestamp=mock_timestamp_1,
        source_path=mock_source_path_1
    )

    file_info_2 = RivendellAudioImporter.FileInformation(
        file_path=mock_file_path_1,
        timestamp=mock_timestamp_1,
        source_path=mock_source_path_1
    )

    file_info_3 = RivendellAudioImporter.FileInformation(
        file_path=mock_file_path_3,
        timestamp=mock_timestamp_1,
        source_path=mock_source_path_1
    )

    mock_size_4 = 4_000
    fs.remove_object(mock_file_path_string_1)
    fs.create_file(mock_file_path_string_1, st_size=mock_size_4)

    file_info_4 = RivendellAudioImporter.FileInformation(
        file_path=mock_file_path_1,
        timestamp=mock_timestamp_1,
        source_path=mock_source_path_1
    )

    mock_timestamp_5 = datetime.datetime(year=2020, month=6, day=30, hour=11, minute=10, second=45)

    file_info_5 = RivendellAudioImporter.FileInformation(
        file_path=mock_file_path_1,
        timestamp=mock_timestamp_5,
        source_path=mock_source_path_1
    )

    return wmul_test_utils.make_namedtuple(
        "setup_comparison",
        file_info_1=file_info_1,
        file_info_2=file_info_2,
        file_info_3=file_info_3,
        file_info_4=file_info_4,
        file_info_5=file_info_5
    )


def test_equality(setup_comparison):
    assert setup_comparison.file_info_1 == setup_comparison.file_info_2
    assert setup_comparison.file_info_1 != setup_comparison.file_info_3
    assert setup_comparison.file_info_1 != setup_comparison.file_info_4
    assert setup_comparison.file_info_1 != setup_comparison.file_info_5

    assert setup_comparison.file_info_2 != setup_comparison.file_info_3
    assert setup_comparison.file_info_2 != setup_comparison.file_info_4
    assert setup_comparison.file_info_2 != setup_comparison.file_info_5

    assert setup_comparison.file_info_3 != setup_comparison.file_info_4
    assert setup_comparison.file_info_3 != setup_comparison.file_info_5

    assert setup_comparison.file_info_4 != setup_comparison.file_info_5


def test_less_than(setup_comparison):
    assert not(setup_comparison.file_info_1 < setup_comparison.file_info_2)
    assert setup_comparison.file_info_1 < setup_comparison.file_info_3
    assert setup_comparison.file_info_1 < setup_comparison.file_info_4
    assert setup_comparison.file_info_1 < setup_comparison.file_info_5

    assert not(setup_comparison.file_info_2 < setup_comparison.file_info_1)
    assert setup_comparison.file_info_2 < setup_comparison.file_info_3
    assert setup_comparison.file_info_2 < setup_comparison.file_info_4
    assert setup_comparison.file_info_2 < setup_comparison.file_info_5

    assert not(setup_comparison.file_info_3 < setup_comparison.file_info_1)
    assert not(setup_comparison.file_info_3 < setup_comparison.file_info_2)
    assert not(setup_comparison.file_info_3 < setup_comparison.file_info_4)
    assert not(setup_comparison.file_info_3 < setup_comparison.file_info_5)

    assert not(setup_comparison.file_info_4 < setup_comparison.file_info_1)
    assert not(setup_comparison.file_info_4 < setup_comparison.file_info_2)
    assert setup_comparison.file_info_4 < setup_comparison.file_info_3
    assert setup_comparison.file_info_4 < setup_comparison.file_info_5


@pytest.fixture(scope="function")
def setup_same_size_as(mocker):
    size_1 = 3_000
    size_2 = 4_000
    mock_info_1_a = mocker.Mock(
        file_size=size_1
    )
    mock_info_1_b = mocker.Mock(
        file_size=size_1
    )
    mock_info_2 = mocker.Mock(
        file_size=size_2
    )

    return wmul_test_utils.make_namedtuple(
        "setup_same_size_as",
        mock_info_1_a=mock_info_1_a,
        mock_info_1_b=mock_info_1_b,
        mock_info_2=mock_info_2
    )


def test_same_size_true(setup_same_size_as):
    assert RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_1_a,
                                                               setup_same_size_as.mock_info_1_a)
    assert RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_1_b,
                                                               setup_same_size_as.mock_info_1_b)
    assert RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_2,
                                                               setup_same_size_as.mock_info_2)
    assert RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_1_a,
                                                               setup_same_size_as.mock_info_1_b)
    assert RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_1_b,
                                                               setup_same_size_as.mock_info_1_a)


def test_same_size_false(setup_same_size_as):
    assert not RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_1_a,
                                                                   setup_same_size_as.mock_info_2)
    assert not RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_1_b,
                                                                   setup_same_size_as.mock_info_2)
    assert not RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_2,
                                                                   setup_same_size_as.mock_info_1_a)
    assert not RivendellAudioImporter.FileInformation.same_size_as(setup_same_size_as.mock_info_2,
                                                                   setup_same_size_as.mock_info_1_b)


@pytest.fixture(scope="function")
def setup_new_info_much_newer(mocker):
    five_ten_timestamp = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=5, second=10)
    five_thirty_timestamp = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=5, second=30)
    five_fifty_timestamp = datetime.datetime(year=2020, month=6, day=30, hour=12, minute=5, second=50)

    five_ten_info = mocker.Mock(
        timestamp=five_ten_timestamp
    )
    five_thirty_info = mocker.Mock(
        timestamp=five_thirty_timestamp
    )
    five_fifty_info = mocker.Mock(
        timestamp=five_fifty_timestamp
    )

    minimum_difference = 30

    return wmul_test_utils.make_namedtuple(
        "setup_new_info_much_newer",
        five_ten_info=five_ten_info,
        five_thirty_info=five_thirty_info,
        five_fifty_info=five_fifty_info,
        minimum_difference=minimum_difference
    )


def test_five_ten_and_five_thirty(setup_new_info_much_newer):
    assert not RivendellAudioImporter.FileInformation.new_info_much_newer(
        setup_new_info_much_newer.five_ten_info,
        setup_new_info_much_newer.five_thirty_info,
        setup_new_info_much_newer.minimum_difference
    )

    assert not RivendellAudioImporter.FileInformation.new_info_much_newer(
        setup_new_info_much_newer.five_thirty_info,
        setup_new_info_much_newer.five_ten_info,
        setup_new_info_much_newer.minimum_difference
    )


def test_five_ten_and_five_fifty(setup_new_info_much_newer):
    assert RivendellAudioImporter.FileInformation.new_info_much_newer(
        setup_new_info_much_newer.five_ten_info,
        setup_new_info_much_newer.five_fifty_info,
        setup_new_info_much_newer.minimum_difference
    )

    assert not RivendellAudioImporter.FileInformation.new_info_much_newer(
        setup_new_info_much_newer.five_fifty_info,
        setup_new_info_much_newer.five_ten_info,
        setup_new_info_much_newer.minimum_difference
    )


@pytest.fixture(scope="function", params=[False, True], ids=["No Log Argument", "Has Log Argument"])
def setup_generate_importer_command_no_group(fs, caplog, request):
    has_log_argument = request.param
    mock_file_path = pathlib.Path(r"/source/mock_filename.mp3")
    fs.create_file(mock_file_path)
    mock_time_stamp = datetime.datetime.now()
    mock_source_path = pathlib.Path(r"/source")

    mock_file_for_importer = RivendellAudioImporter.FileInformation(
        mock_file_path, mock_time_stamp, mock_source_path
    )

    if has_log_argument:
        mock_log_argument = "mock_log_argument"
    else:
        mock_log_argument = ""

    result_value = mock_file_for_importer.generate_importer_command(mock_log_argument)

    expected_log_messages = [
        f"With {mock_file_for_importer}",
        f"This file does not have a group. {str(mock_file_path)}"
    ]

    return wmul_test_utils.make_namedtuple(
        "setup_generate_importer_command_no_group",
        result_log_messages=caplog.messages,
        result_value=result_value,
        expected_log_messages=expected_log_messages
    )


def test_generate_importer_command_no_group_log_message_correct(setup_generate_importer_command_no_group):
    assert sorted(setup_generate_importer_command_no_group.expected_log_messages) == \
           sorted(setup_generate_importer_command_no_group.result_log_messages)


def test_importer_command_no_group_return_value_correct(setup_generate_importer_command_no_group):
    assert setup_generate_importer_command_no_group.result_value is None


@pytest.fixture(scope="function", params=[False, True], ids=["No Log Argument", "Has Log Argument"])
def setup_generate_importer_command_group_no_sched_code(fs, caplog, request):
    has_log_argument = request.param
    mock_group = "mock_group"
    mock_file_path_str = f"\\source\\{mock_group}\\mock_filename.mp3"
    mock_file_path = pathlib.Path(mock_file_path_str)
    fs.create_file(mock_file_path)
    mock_time_stamp = datetime.datetime.now()
    mock_source_path = pathlib.Path(r"/source")

    mock_file_for_importer = RivendellAudioImporter.FileInformation(
        mock_file_path, mock_time_stamp, mock_source_path
    )

    if has_log_argument:
        mock_log_argument = "mock_log_argument"
        expected_result = [
            "--autotrim-level=0",
            "--normalization-level=0",
            "--title-from-cartchunk-cutid",
            "--delete-source",
            f'--set-string-description="mock_filename.mp3"',
            '--verbose',
            mock_log_argument,
            mock_group,
            mock_file_path_str
        ]
    else:
        mock_log_argument = ""
        expected_result = [
            "--autotrim-level=0",
            "--normalization-level=0",
            "--title-from-cartchunk-cutid",
            "--delete-source",
            f'--set-string-description="mock_filename.mp3"',
            '--verbose',
            mock_group,
            mock_file_path_str
        ]

    result_value = mock_file_for_importer.generate_importer_command(mock_log_argument)

    expected_log_messages = [
        f"With {mock_file_for_importer}",
        "No scheduler codes."
    ]

    return wmul_test_utils.make_namedtuple(
        "setup_generate_importer_command_group_no_sched_code",
        result_log_messages=caplog.messages,
        expected_log_messages=expected_log_messages,
        result_value=result_value,
        expected_result=expected_result,
    )


def test_file_information_generate_importer_command_group_no_sched_code_log_message_correct(
        setup_generate_importer_command_group_no_sched_code):
    assert sorted(setup_generate_importer_command_group_no_sched_code.expected_log_messages) == \
           sorted(setup_generate_importer_command_group_no_sched_code.result_log_messages)


def test_file_information_generate_importer_command_group_return_value_correct(
        setup_generate_importer_command_group_no_sched_code):

    assert setup_generate_importer_command_group_no_sched_code.result_value == \
           setup_generate_importer_command_group_no_sched_code.expected_result


@pytest.fixture(scope="function", params=[False, True], ids=["No Log Argument", "Has Log Argument"])
def setup_generate_importer_command_group_sched_codes(fs, caplog, request):
    has_log_argument = request.param
    mock_group = "mock_group"
    mock_sched_code_1 = "mock_sched_code_1"
    mock_sched_code_2 = "mock_sched_code_2"
    mock_file_path_str = f"\\source\\{mock_group}\\{mock_sched_code_1}\\{mock_sched_code_2}\\mock_filename.mp3"
    mock_file_path = pathlib.Path(mock_file_path_str)
    fs.create_file(mock_file_path)
    mock_time_stamp = datetime.datetime.now()
    mock_source_path = pathlib.Path(r"/source")

    mock_file_for_importer = RivendellAudioImporter.FileInformation(
        mock_file_path, mock_time_stamp, mock_source_path
    )

    if has_log_argument:
        mock_log_argument = "mock_log_arguemnt"
        expected_result = [
            f"--add-scheduler-code={mock_sched_code_1}",
            f"--add-scheduler-code={mock_sched_code_2}",
            "--autotrim-level=0",
            "--normalization-level=0",
            "--title-from-cartchunk-cutid",
            "--delete-source",
            f'--set-string-description="mock_filename.mp3"',
            "--verbose",
            mock_log_argument,
            mock_group,
            mock_file_path_str
        ]
    else:
        mock_log_argument = ""
        expected_result = [
            f"--add-scheduler-code={mock_sched_code_1}",
            f"--add-scheduler-code={mock_sched_code_2}",
            "--autotrim-level=0",
            "--normalization-level=0",
            "--title-from-cartchunk-cutid",
            "--delete-source",
            f'--set-string-description="mock_filename.mp3"',
            "--verbose",
            mock_group,
            mock_file_path_str
        ]

    result_value = mock_file_for_importer.generate_importer_command(mock_log_argument)

    expected_log_messages = [
        f"With {mock_file_for_importer}",
        "Has scheduler codes."
    ]

    return wmul_test_utils.make_namedtuple(
        "setup_generate_importer_command_group_sched_codes",
        result_log_messages=caplog.messages,
        expected_log_messages=expected_log_messages,
        result_value=result_value,
        expected_result=expected_result
    )


def test_generate_importer_command_group_sched_codes_log_message_correct(
        setup_generate_importer_command_group_sched_codes):
    assert sorted(setup_generate_importer_command_group_sched_codes.expected_log_messages) == \
           sorted(setup_generate_importer_command_group_sched_codes.result_log_messages)


def test_generate_importer_command_group_sched_codes_return_value_correct(
        setup_generate_importer_command_group_sched_codes):

    assert setup_generate_importer_command_group_sched_codes.result_value == \
           setup_generate_importer_command_group_sched_codes.expected_result


def test__failed(fs):
    mock_file_path = pathlib.Path("\\source\\mock_group\\mock_filename.mp3")
    fs.create_file(mock_file_path)
    mock_time_stamp = datetime.datetime.now()
    mock_source_path = pathlib.Path(r"\\source")

    mock_file_info = RivendellAudioImporter.FileInformation(
        mock_file_path, mock_time_stamp, mock_source_path
    )

    mock_suffix = "_mock_suffix"

    mock_file_info._failed(mock_suffix)

    expected_file = pathlib.Path("\\source\\mock_group\\mock_filename.mp3_mock_suffix")
    assert expected_file.exists()
    assert not mock_file_path.exists()


@pytest.fixture(scope="function")
def setup_failed_with_reason(fs, mocker):
    mock_failed = mocker.Mock()

    mocker.patch("wmul_rivendell.RivendellAudioImporter.FileInformation._failed",
                 mock_failed)

    mock_file_path = pathlib.Path("\\source\\mock_group\\mock_filename.mp3")
    fs.create_file(mock_file_path)
    mock_time_stamp = datetime.datetime.now()
    mock_source_path = pathlib.Path(r"\\source")

    mock_file_info = RivendellAudioImporter.FileInformation(
        mock_file_path, mock_time_stamp, mock_source_path
    )

    return wmul_test_utils.make_namedtuple(
        "setup_failed_with_reason",
        mock_file_info=mock_file_info,
        mock_failed=mock_failed
    )


def test_failed_rdimport(setup_failed_with_reason):
    setup_failed_with_reason.mock_file_info.failed_rdimport()
    setup_failed_with_reason.mock_failed.assert_called_once_with("_RDIMPORT_FAILED")


def test_failed_group(setup_failed_with_reason):
    setup_failed_with_reason.mock_file_info.failed_group()
    setup_failed_with_reason.mock_failed.assert_called_once_with("_NO_GROUP_FAILED")
