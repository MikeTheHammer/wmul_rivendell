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
Copyright (C) 2021, 2023, 2025 Michael Stanley

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

from wmul_rivendell.FilterCartReportForMusicScheduler import ConvertDatabaseToCSV
from wmul_rivendell.LoadCartDataDump import RivendellCart, CartType


cart_filter_params, cart_filter_ids = \
    wmul_test_utils.generate_true_false_matrix_from_list_of_strings(
        "cart_filter_params", ["fix_bad_header"]
    )

@pytest.fixture(scope="function", params=cart_filter_params, 
    ids=cart_filter_ids )
def setup_standard_cart_filter(mocker):
    mock_output_filename = mocker.Mock()
    mock_rivendell_carts = mocker.Mock()

    cart_filter = ConvertDatabaseToCSV(
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
    rivendell_cart_1_1 = RivendellCart(cart_number='1', cut_number='1', type=CartType.Audio, group_name='TEMPORIBUS', title='perferendis optio adipisci odit', artist='nesciunt repellendus', album='', year='1951', isrc='', isci='', label='', client='saepe architecto sequi alias', agency='', publisher='', composer='facere odio magnam odit', conductor='', song_id='', user_defined='', description='perferendis pariatur eligendi dolorem', outcue='', filename='000001_001.wav', length=':07', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    rivendell_cart_2_1 = RivendellCart(cart_number='2', cut_number='1', type=CartType.Audio, group_name='TEMPORIBUS', title='saepe recusandae deleniti laborum', artist='quisquam natus', album='', year='1965', isrc='', isci='', label='', client='enim ut qui veniam', agency='', publisher='', composer='omnis voluptatum accusantium saepe', conductor='', song_id='', user_defined='', description='praesentium eaque deleniti tempore', outcue='', filename='000002_001.wav', length=':07', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    rivendell_cart_2_2 = RivendellCart(cart_number='2', cut_number='2', type=CartType.Audio, group_name='TEMPORIBUS', title='aperiam sed totam reiciendis', artist='recusandae nesciunt', album='', year='1962', isrc='', isci='', label='', client='fugiat saepe quam libero', agency='', publisher='', composer='repellat non in fuga', conductor='', song_id='', user_defined='', description='deserunt repellat odit velit', outcue='', filename='000002_002.wav', length=':11', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    rivendell_cart_6_2 = RivendellCart(cart_number='6', cut_number='2', type=CartType.Audio, group_name='TEMPORIBUS', title='tempora libero earum repudiandae', artist='modi quo', album='', year='1953', isrc='', isci='', label='', client='iure nobis illum quia', agency='', publisher='', composer='fugiat beatae perspiciatis dicta', conductor='', song_id='', user_defined='', description='tempore voluptates tenetur dolorem', outcue='', filename='000006_002.wav', length=':11', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    rivendell_cart_101_1 = RivendellCart(cart_number='101', cut_number='1', type=CartType.Audio, group_name='TEMPORIBUS', title='aliquam omnis quisquam enim', artist='nobis sit', album='', year='2003', isrc='', isci='', label='', client='culpa quas minus reiciendis', agency='', publisher='', composer='ipsam cumque nulla harum', conductor='', song_id='', user_defined='', description='deserunt natus quidem at', outcue='', filename='000101_001.wav', length=':05', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    rivendell_cart_500_1 = RivendellCart(cart_number='500', cut_number='1', type=CartType.Audio, group_name='VOLUPTATIB', title='voluptate commodi neque aperiam', artist='reiciendis rem', album='', year='1969', isrc='', isci='', label='', client='assumenda quasi maxime cum', agency='', publisher='', composer='doloremque provident dolorum mollitia', conductor='', song_id='', user_defined='', description='ut praesentium sit quidem', outcue='', filename='000500_001.wav', length=':08', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    rivendell_cart_970000_1 = RivendellCart(cart_number='970000', cut_number='1', type=CartType.Macro, group_name='ALIQUAM', title='quasi necessitatibus quo vero', artist='sapiente fuga', album='', year='1994', isrc='', isci='', label='', client='distinctio culpa perspiciatis quam', agency='', publisher='', composer='explicabo magni temporibus provident', conductor='', song_id='', user_defined='', description='adipisci officia impedit dolores', outcue='', filename='', length=':00', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    rivendell_cart_970001_1 = RivendellCart(cart_number='970001', cut_number='1', type=CartType.Macro, group_name='ALIQUAM', title='porro eos dolores fuga', artist='rem dolor', album='', year='2015', isrc='', isci='', label='', client='omnis molestias nesciunt cumque', agency='', publisher='', composer='adipisci quidem consequuntur quia', conductor='', song_id='', user_defined='', description='provident perspiciatis quisquam ea', outcue='', filename='', length=':00', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
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
    rc_1_1_group_name = "TEMPORIBUS"
    rc_1_1_title = "perferendis optio adipisci odit"

    rc_1_1 = OrderedDict()
    rc_1_1[cart_number_field_name] = rc_1_1_cart_number
    rc_1_1[cut_number_field_name] = rc_1_1_cut_number
    rc_1_1[group_name_field_name] = rc_1_1_group_name
    rc_1_1[title_field_name] = rc_1_1_title

    rc_1_1_line = rc_1_1_cart_number + "," + rc_1_1_cut_number + "," + rc_1_1_group_name + "," + rc_1_1_title

    rc_6_2_cart_number = '6'
    rc_6_2_cut_number = '2'
    rc_6_2_group_name = "TEMPORIBUS"
    rc_6_2_title = "tempora libero earum repudiandae"

    rc_6_2 = OrderedDict()
    rc_6_2[cart_number_field_name] = rc_6_2_cart_number
    rc_6_2[cut_number_field_name] = rc_6_2_cut_number
    rc_6_2[group_name_field_name] = rc_6_2_group_name
    rc_6_2[title_field_name] = rc_6_2_title

    rc_6_2_line = rc_6_2_cart_number + "," + rc_6_2_cut_number + "," + rc_6_2_group_name + "," + rc_6_2_title

    rc_101_1_cart_number = '101'
    rc_101_1_cut_number = '1'
    rc_101_1_group_name = "LEGATEMPORIBUSL_ID"
    rc_101_1_title = "aliquam omnis quisquam enim"

    rc_101_1 = OrderedDict()
    rc_101_1[cart_number_field_name] = rc_101_1_cart_number
    rc_101_1[cut_number_field_name] = rc_101_1_cut_number
    rc_101_1[group_name_field_name] = rc_101_1_group_name
    rc_101_1[title_field_name] = rc_101_1_title

    rc_101_1_line = rc_101_1_cart_number + "," + rc_101_1_cut_number + "," + rc_101_1_group_name + "," + rc_101_1_title

    rc_500_1_cart_number = '500'
    rc_500_1_cut_number = '1'
    rc_500_1_group_name = "VOLUPTATIB"
    rc_500_1_title = "voluptate commodi neque aperiam"

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

    cart_filter._export_carts(music_scheduler_carts)

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

    cart_filter._export_carts(music_scheduler_carts)

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
    mock_output_filename = mocker.Mock()
    mock_rivendell_carts = mocker.Mock()

    mock_music_scheduler_carts = "mock_music_scheduler_cuts"
    mock_remove_unwanted_fields = mocker.Mock(return_value=mock_music_scheduler_carts)
    mocker.patch(
        "wmul_rivendell.FilterCartReportForMusicScheduler.ConvertDatabaseToCSV._remove_unwanted_fields",
        mock_remove_unwanted_fields
    )

    mock_export_carts = mocker.Mock()
    mocker.patch(
        "wmul_rivendell.FilterCartReportForMusicScheduler.ConvertDatabaseToCSV._export_carts",
        mock_export_carts
    )

    cart_filter = ConvertDatabaseToCSV(
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
        mock_export_carts=mock_export_carts,
        caplog_text=caplog.text
    )


def test_run_script_remove_unwanted_fields_called_correctly(setup_run_script):
    setup_run_script.mock_remove_unwanted_fields.assert_called_once_with(
        setup_run_script.mock_rivendell_carts
    )


def test_run_script_export_carts_to_csv_called_correctly(setup_run_script):
    setup_run_script.mock_export_carts.assert_called_once_with(setup_run_script.mock_music_scheduler_carts)
