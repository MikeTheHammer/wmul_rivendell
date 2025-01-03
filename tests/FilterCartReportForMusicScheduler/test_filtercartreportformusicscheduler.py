"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-Jan-20 = Change license from GPLv2 to GPLv3.

2023-Jan-11 = Added tests that deal with a bug introduced in version 3.6.4. 
              The bug causes the header for the "FILENAME" and "LENGTH" to be 
              combined. Only the headers are combined, the actual data is 
              properly separated.

2021-Jan-29 = Created.

============ License ============
Copyright (C) 2021, 2023 Michael Stanley

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
from collections import OrderedDict
import pytest
import wmul_test_utils

from wmul_rivendell.FilterCartReportForMusicScheduler import FilterCartReportForMusicScheduler
from wmul_rivendell.LoadCartDataDump import RivendellCart, CartType


cart_filter_params, cart_filter_ids = \
    wmul_test_utils.generate_true_false_matrix_from_list_of_strings(
        "cart_filter_params", ["fix_bad_header"]
    )

@pytest.fixture(scope="function", params=cart_filter_params, 
    ids=cart_filter_ids )
def setup_standard_cart_filter():
    mock_output_filename = "mock_output_filename"
    mock_rivendell_carts = "mock_rivendell_carts"

    cart_filter = FilterCartReportForMusicScheduler(
        rivendell_carts=mock_rivendell_carts,
        output_filename=mock_output_filename,
        desired_field_list=[],
        use_trailing_comma=False
    )

    return wmul_test_utils.make_namedtuple(
        "setup_standard_cart_filter",
        mock_output_filename=mock_output_filename,
        mock_rivendell_carts=mock_rivendell_carts,
        cart_filter=cart_filter
    )

@pytest.fixture(scope="function")
def defined_rivendell_carts():
    rivendell_cart_1_1 = RivendellCart(
        cart_number='1',
        cut_number='1',
        type=CartType.Audio,
        group_name="LEGAL_ID",
        title="Alternative",
        artist="Legal ID",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="",
        agency="",
        publisher="",
        composer="",
        conductor="",
        song_id="",
        user_defined="",
        description="We Are Marshall (Cheer)",
        outcue="",
        filename="000001_001.wav",
        length=':07',
        start_point="0",
        end_point="7523",
        segue_start_point="7079",
        segue_end_point="7497",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    rivendell_cart_2_1 = RivendellCart(
        cart_number='2',
        cut_number='1',
        type=CartType.Audio,
        group_name="LEGAL_ID",
        title="Streetbeat",
        artist="Legal ID",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="",
        agency="",
        publisher="",
        composer="",
        conductor="",
        song_id="",
        user_defined="",
        description="We Are Marshall (Cheer)",
        outcue="",
        filename="000002_001.wav",
        length=':07',
        start_point="0",
        end_point="7523",
        segue_start_point="7079",
        segue_end_point="7497",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    rivendell_cart_2_2 = RivendellCart(
        cart_number='2',
        cut_number='2',
        type=CartType.Audio,
        group_name="ALTERNATIV",
        title="Streetbeat",
        artist="Legal ID",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="",
        agency="",
        publisher="",
        composer="",
        conductor="",
        song_id="",
        user_defined="",
        description="Every Hour Commercial Free",
        outcue="",
        filename="000002_002.wav",
        length=':11',
        start_point="0",
        end_point="11023",
        segue_start_point="-1",
        segue_end_point="-1",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    rivendell_cart_6_2 = RivendellCart(
        cart_number='6',
        cut_number='2',
        type=CartType.Audio,
        group_name="ALTERNATIV",
        title="Flashback",
        artist="Legal ID",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="",
        agency="",
        publisher="",
        composer="",
        conductor="",
        song_id="",
        user_defined="",
        description="Every Hour Commercial Free",
        outcue="",
        filename="000006_002.wav",
        length=':11',
        start_point="0",
        end_point="11023",
        segue_start_point="-1",
        segue_end_point="-1",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    rivendell_cart_101_1 = RivendellCart(
        cart_number='101',
        cut_number='1',
        type=CartType.Audio,
        group_name="ALT_IMAGE",
        title="Student Broadcast Voice",
        artist="Dry Legal ID",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="",
        agency="",
        publisher="",
        composer="Imported from WOAFR: LID/0006",
        conductor="",
        song_id="",
        user_defined="",
        description="Student Broadcast Voice",
        outcue="",
        filename="000101_001.wav",
        length=':05',
        start_point="0",
        end_point="5825",
        segue_start_point="-1",
        segue_end_point="-1",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    rivendell_cart_500_1 = RivendellCart(
        cart_number='500',
        cut_number='1',
        type=CartType.Audio,
        group_name="ALT_IMAGE",
        title="Cutting Edge Alt Music",
        artist="Alternative Sweeper",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="",
        agency="",
        publisher="",
        composer="Imported from WOAFR: AIM/0001",
        conductor="",
        song_id="",
        user_defined="",
        description="Cutting Edge Alt Music",
        outcue="",
        filename="000500_001.wav",
        length=':08',
        start_point="0",
        end_point="8176",
        segue_start_point="-1",
        segue_end_point="-1",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    rivendell_cart_970000_1 = RivendellCart(
        cart_number='970000',
        cut_number='1',
        type=CartType.Macro,
        group_name="MACROS",
        title="START NEXT",
        artist="WMUL-FM",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="Mike Stanley",
        agency="",
        publisher="",
        composer="",
        conductor="",
        song_id="",
        user_defined="",
        description="",
        outcue="",
        filename="",
        length=':00',
        start_point="-1",
        end_point="-1",
        segue_start_point="-1",
        segue_end_point="-1",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    rivendell_cart_970001_1 = RivendellCart(
        cart_number='970000',
        cut_number='1',
        type=CartType.Macro,
        group_name="MACROS",
        title="BBFN",
        artist="WMUL-FM",
        album="",
        year="",
        isrc="",
        isci="",
        label="",
        client="Mike Stanley",
        agency="",
        publisher="",
        composer="",
        conductor="",
        song_id="",
        user_defined="",
        description="",
        outcue="",
        filename="",
        length=':00',
        start_point="-1",
        end_point="-1",
        segue_start_point="-1",
        segue_end_point="-1",
        hook_start_point="-1",
        hook_end_point="-1",
        talk_start_point="-1",
        talk_end_point="-1",
        fadeup_point="-1",
        fadedown_point="-1",
        sched_codes=""
    )
    return wmul_test_utils.make_namedtuple(
        "defined_carts",
        rivendell_cart_1_1=rivendell_cart_1_1,
        rivendell_cart_2_1=rivendell_cart_2_1,
        rivendell_cart_2_2=rivendell_cart_2_2,
        rivendell_cart_6_2=rivendell_cart_6_2,
        rivendell_cart_101_1=rivendell_cart_101_1,
        rivendell_cart_500_1=rivendell_cart_500_1,
        rivendell_cart_970000_1=rivendell_cart_970000_1,
        rivendell_cart_970001_1=rivendell_cart_970001_1
    )


all_fields = [
        "cart_number",
        "cut_number",
        "type",
        "group_name",
        "title",
        "artist",
        "album",
        "year",
        "isrc",
        "isci",
        "label",
        "client",
        "agency",
        "publisher",
        "composer",
        "conductor",
        "song_id",
        "user_defined",
        "description",
        "outcue",
        "filename",
        "length",
        "start_point",
        "end_point",
        "segue_start_point",
        "segue_end_point",
        "hook_start_point",
        "hook_end_point",
        "talk_start_point",
        "talk_end_point",
        "fadeup_point",
        "fadedown_point",
        "sched_codes"
]


desired_field_list_parameters = [
    all_fields,
    [
        "cart_number",
        "cut_number",
        "type",
        "group_name",
        "title",
        "artist",
        "song_id",
        "user_defined",
        "description",
        "outcue",
        "filename",
        "length",
        "start_point",
        "end_point",
        "talk_start_point",
        "talk_end_point",
        "fadeup_point",
        "fadedown_point",
        "sched_codes"
    ],
    [
        "cart_number",
        "cut_number",
        "type"
    ]
]


@pytest.mark.parametrize("desired_field_list", desired_field_list_parameters)
def test__remove_unwanted_fields_fields_removed(
        setup_standard_cart_filter, 
        defined_rivendell_carts, 
        desired_field_list
    ):

    cart_filter = setup_standard_cart_filter.cart_filter

    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1
    ]

    cart_filter.desired_field_list = desired_field_list

    result_carts = cart_filter._remove_unwanted_fields(
        rivendell_carts=rivendell_carts_for_test
    )

    assert len(result_carts) == len(rivendell_carts_for_test)

    for rc in result_carts:
        assert desired_field_list == list(rc.keys())


def test__remove_unwanted_fields_fields_copied_correctly(
        setup_standard_cart_filter, 
        defined_rivendell_carts
    ):

    cart_filter = setup_standard_cart_filter.cart_filter

    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1
    ]
    cart_filter.desired_field_list = all_fields

    result_carts = cart_filter._remove_unwanted_fields(
        rivendell_carts=rivendell_carts_for_test
    )

    assert len(result_carts) == len(rivendell_carts_for_test)

    cart_under_test = rivendell_carts_for_test[0]

    result_cart = result_carts[0]
    result_cart_keys = result_cart.keys()

    invalid_field_name = "INVALID FIELD NAME"

    for field in all_fields:
        assert field in result_cart_keys
        original_value_of_field = getattr(cart_under_test, field, 
                                          invalid_field_name)
        assert original_value_of_field != invalid_field_name
        assert result_cart[field] == original_value_of_field


@pytest.fixture()
def defined_music_scheduler_carts():
    cart_number_field_name = "cart_number"
    cut_number_field_name = "cut_number"
    group_name_field_name = "group_name"
    title_field_name = "title"

    rc_1_1_cart_number = '1'
    rc_1_1_cut_number = '1'
    rc_1_1_group_name = "LEGAL_ID"
    rc_1_1_title = "Alternative"

    rc_1_1 = OrderedDict()
    rc_1_1[cart_number_field_name] = rc_1_1_cart_number
    rc_1_1[cut_number_field_name] = rc_1_1_cut_number
    rc_1_1[group_name_field_name] = rc_1_1_group_name
    rc_1_1[title_field_name] = rc_1_1_title

    rc_1_1_line = rc_1_1_cart_number + "," + rc_1_1_cut_number + "," + rc_1_1_group_name + "," + rc_1_1_title

    rc_6_2_cart_number = '6'
    rc_6_2_cut_number = '2'
    rc_6_2_group_name = "LEGAL_ID"
    rc_6_2_title = "Flashback"

    rc_6_2 = OrderedDict()
    rc_6_2[cart_number_field_name] = rc_6_2_cart_number
    rc_6_2[cut_number_field_name] = rc_6_2_cut_number
    rc_6_2[group_name_field_name] = rc_6_2_group_name
    rc_6_2[title_field_name] = rc_6_2_title

    rc_6_2_line = rc_6_2_cart_number + "," + rc_6_2_cut_number + "," + rc_6_2_group_name + "," + rc_6_2_title

    rc_101_1_cart_number = '101'
    rc_101_1_cut_number = '1'
    rc_101_1_group_name = "LEGAL_ID"
    rc_101_1_title = "Student Broadcast Voice"

    rc_101_1 = OrderedDict()
    rc_101_1[cart_number_field_name] = rc_101_1_cart_number
    rc_101_1[cut_number_field_name] = rc_101_1_cut_number
    rc_101_1[group_name_field_name] = rc_101_1_group_name
    rc_101_1[title_field_name] = rc_101_1_title

    rc_101_1_line = rc_101_1_cart_number + "," + rc_101_1_cut_number + "," + rc_101_1_group_name + "," + rc_101_1_title

    rc_500_1_cart_number = '500'
    rc_500_1_cut_number = '1'
    rc_500_1_group_name = "ALT_IMAGE"
    rc_500_1_title = "Cutting Edge Alt Music"

    rc_500_1 = OrderedDict()
    rc_500_1[cart_number_field_name] = rc_500_1_cart_number
    rc_500_1[cut_number_field_name] = rc_500_1_cut_number
    rc_500_1[group_name_field_name] = rc_500_1_group_name
    rc_500_1[title_field_name] = rc_500_1_title

    rc_500_1_line = rc_500_1_cart_number + "," + rc_500_1_cut_number + "," + rc_500_1_group_name + "," + rc_500_1_title

    return wmul_test_utils.make_namedtuple(
        "defined_music_scheduler_carts",
        rc_1_1=rc_1_1,
        rc_1_1_line=rc_1_1_line,
        rc_6_2=rc_6_2,
        rc_6_2_line=rc_6_2_line,
        rc_101_1=rc_101_1,
        rc_101_1_line=rc_101_1_line,
        rc_500_1=rc_500_1,
        rc_500_1_line=rc_500_1_line
    )


def test__export_carts_to_csv_trailing_comma(fs, setup_standard_cart_filter, 
                                             defined_music_scheduler_carts):
    cart_filter = setup_standard_cart_filter.cart_filter

    import pathlib
    output_file_path = pathlib.Path(r"\fake_output_file.csv")
    assert not output_file_path.exists()

    cart_filter.output_filename = output_file_path
    cart_filter.use_trailing_comma = True

    music_scheduler_carts = [
        defined_music_scheduler_carts.rc_1_1,
        defined_music_scheduler_carts.rc_6_2,
        defined_music_scheduler_carts.rc_101_1,
        defined_music_scheduler_carts.rc_500_1
    ]

    cart_filter._export_carts_to_csv(music_scheduler_carts)

    assert output_file_path.exists()

    expected_file_contents = \
        defined_music_scheduler_carts.rc_1_1_line + ",\r\n" + \
        defined_music_scheduler_carts.rc_6_2_line + ",\r\n" + \
        defined_music_scheduler_carts.rc_101_1_line + ",\r\n" + \
        defined_music_scheduler_carts.rc_500_1_line + ",\r\n"

    result_file_contents = open(output_file_path, newline="", mode="rt", 
                                errors="replace").read()

    assert expected_file_contents == result_file_contents


def test__export_carts_to_csv_no_trailing_comma(fs, setup_standard_cart_filter, 
                                                defined_music_scheduler_carts):
    cart_filter = setup_standard_cart_filter.cart_filter

    import pathlib
    output_file_path = pathlib.Path(r"\fake_output_file.csv")
    assert not output_file_path.exists()

    cart_filter.output_filename = output_file_path
    cart_filter.use_trailing_comma = False

    music_scheduler_carts = [
        defined_music_scheduler_carts.rc_1_1,
        defined_music_scheduler_carts.rc_6_2,
        defined_music_scheduler_carts.rc_101_1,
        defined_music_scheduler_carts.rc_500_1
    ]

    cart_filter._export_carts_to_csv(music_scheduler_carts)

    assert output_file_path.exists()

    expected_file_contents = \
        defined_music_scheduler_carts.rc_1_1_line + "\r\n" + \
        defined_music_scheduler_carts.rc_6_2_line + "\r\n" + \
        defined_music_scheduler_carts.rc_101_1_line + "\r\n" + \
        defined_music_scheduler_carts.rc_500_1_line + "\r\n"

    result_file_contents = open(output_file_path, newline="", mode="rt", 
                                errors="replace").read()

    assert expected_file_contents == result_file_contents


@pytest.fixture(scope="function")
def setup_run_script(caplog, mocker):
    mock_output_filename = "mock_output_filename"

    mock_rivendell_carts = "mock_rivendell_carts"

    mock_music_scheduler_carts = "mock_music_scheduler_cuts"
    mock_remove_unwanted_fields = mocker.Mock(return_value=mock_music_scheduler_carts)
    mocker.patch(
        "wmul_rivendell.FilterCartReportForMusicScheduler.FilterCartReportForMusicScheduler._remove_unwanted_fields",
        mock_remove_unwanted_fields
    )

    mock_export_carts_to_csv = mocker.Mock()
    mocker.patch(
        "wmul_rivendell.FilterCartReportForMusicScheduler.FilterCartReportForMusicScheduler._export_carts_to_csv",
        mock_export_carts_to_csv
    )

    cart_filter = FilterCartReportForMusicScheduler(
        rivendell_carts=mock_rivendell_carts,
        output_filename=mock_output_filename,
        desired_field_list=[],
        use_trailing_comma=True
    )

    cart_filter.run_script()

    return wmul_test_utils.make_namedtuple(
        "setup_run_script",
        mock_rivendell_carts=mock_rivendell_carts,
        mock_remove_unwanted_fields=mock_remove_unwanted_fields,
        mock_music_scheduler_carts=mock_music_scheduler_carts,
        mock_export_carts_to_csv=mock_export_carts_to_csv,
        caplog_text=caplog.text
    )


def test_run_script_remove_unwanted_fields_called_correctly(setup_run_script):
    setup_run_script.mock_remove_unwanted_fields.assert_called_once_with(
        setup_run_script.mock_rivendell_carts
    )


def test_run_script_export_carts_to_csv_called_correctly(setup_run_script):
    setup_run_script.mock_export_carts_to_csv.assert_called_once_with(setup_run_script.mock_music_scheduler_carts)


