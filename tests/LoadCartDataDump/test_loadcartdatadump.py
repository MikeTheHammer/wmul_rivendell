"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-May-25 = Created. Most of this module was refactored from 
                tests/FilterCartReportForMusicScheduler/
                test_filtercartreportformusicscheduler.py when the code under 
                test was refactored into LoadCartDataDump.

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
import pytest
import wmul_test_utils

from wmul_rivendell.LoadCartDataDump import LoadCartDataDump, RivendellCart, CartType

@pytest.fixture(scope="function")
def setup_standard_cart_filter(cart_source_file_contents):
    mock_rivendell_cart_data_filename = "mock_rivendell_cart_data_filename"

    cart_filter = LoadCartDataDump(
        rivendell_cart_data_filename=mock_rivendell_cart_data_filename,
        include_macros=False,
        excluded_group_list=[],
        include_all_cuts=False
    )

    return wmul_test_utils.make_namedtuple(
        "setup_standard_cart_filter",
        cart_filter=cart_filter,
        cart_source_file_contents=\
            cart_source_file_contents.source_file_contents,
    )


def test__load_rivendell_carts_file_does_not_exist(
        fs, 
        setup_standard_cart_filter
    ):

    cart_filter = setup_standard_cart_filter.cart_filter
    import pathlib
    rivendell_cart_data_filename = pathlib.Path(r"\fakepath\fakefile.csv")
    assert not rivendell_cart_data_filename.exists()

    output_file_path = pathlib.Path(r"\fakepath\fake_output_file.csv")

    cart_filter.rivendell_cart_data_filename = rivendell_cart_data_filename
    cart_filter.output_filename = output_file_path

    with pytest.raises(OSError) as oserror:
        cart_filter._load_rivendell_carts()


@pytest.fixture(scope="function")
def cart_source_file_contents():
    """Source file contents should parse to rivendell_cart_1_1, rivendell_cart_5_1, rivendell_cart_5071_1, and 
       rivendell_cart_100249_1 in the defined_carts fixture."""

    source_file_contents = \
        'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '1,1,audio,TEMPORIBUS,perferendis optio adipisci odit,nesciunt repellendus,,1951,,,,saepe architecto sequi alias,,,facere odio magnam odit,,,,perferendis pariatur eligendi dolorem,,000001_001.wav,:07,,,,,,,,,,,2010s\r\n' \
        '2,1,audio,TEMPORIBUS,saepe recusandae deleniti laborum,quisquam natus,,1965,,,,enim ut qui veniam,,,omnis voluptatum accusantium saepe,,,,praesentium eaque deleniti tempore,,000002_001.wav,:07,,,,,,,,,,,2010s\r\n' \
        '2,2,audio,TEMPORIBUS,aperiam sed totam reiciendis,recusandae nesciunt,,1962,,,,fugiat saepe quam libero,,,repellat non in fuga,,,,deserunt repellat odit velit,,000002_002.wav,:11,,,,,,,,,,,2010s\r\n' \
        '6,2,audio,TEMPORIBUS,tempora libero earum repudiandae,modi quo,,1953,,,,iure nobis illum quia,,,fugiat beatae perspiciatis dicta,,,,tempore voluptates tenetur dolorem,,000006_002.wav,:11,,,,,,,,,,,2010s\r\n' \
        '101,1,audio,TEMPORIBUS,aliquam omnis quisquam enim,nobis sit,,2003,,,,culpa quas minus reiciendis,,,ipsam cumque nulla harum,,,,deserunt natus quidem at,,000101_001.wav,:05,,,,,,,,,,,2010s\r\n' \
        '500,1,audio,VOLUPTATIB,voluptate commodi neque aperiam,reiciendis rem,,1969,,,,assumenda quasi maxime cum,,,doloremque provident dolorum mollitia,,,,ut praesentium sit quidem,,000500_001.wav,:08,,,,,,,,,,,2010s\r\n' \
        '970000,1,macro,ALIQUAM,quasi necessitatibus quo vero,sapiente fuga,,1994,,,,distinctio culpa perspiciatis quam,,,explicabo magni temporibus provident,,,,adipisci officia impedit dolores,,,:00,,,,,,,,,,,2010s\r\n' \
        '970001,1,macro,ALIQUAM,porro eos dolores fuga,rem dolor,,2015,,,,omnis molestias nesciunt cumque,,,adipisci quidem consequuntur quia,,,,provident perspiciatis quisquam ea,,,:00,,,,,,,,,,,2010s\r\n'
    
    return wmul_test_utils.make_namedtuple(
        "cart_source_file_contents",
        source_file_contents=source_file_contents
    )


@pytest.fixture(scope="function")
def defined_rivendell_carts():
    rivendell_cart_1_1 = RivendellCart(cart_number='1', cut_number='1', type=CartType.Audio, group_name='TEMPORIBUS', title='perferendis optio adipisci odit', artist='nesciunt repellendus', album='', year='1951', isrc='', isci='', label='', client='saepe architecto sequi alias', agency='', publisher='', composer='facere odio magnam odit', conductor='', song_id='', user_defined='', description='perferendis pariatur eligendi dolorem', outcue='', filename='000001_001.wav', length=':07', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
    rivendell_cart_2_1 = RivendellCart(cart_number='2', cut_number='1', type=CartType.Audio, group_name='TEMPORIBUS', title='saepe recusandae deleniti laborum', artist='quisquam natus', album='', year='1965', isrc='', isci='', label='', client='enim ut qui veniam', agency='', publisher='', composer='omnis voluptatum accusantium saepe', conductor='', song_id='', user_defined='', description='praesentium eaque deleniti tempore', outcue='', filename='000002_001.wav', length=':07', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
    rivendell_cart_2_2 = RivendellCart(cart_number='2', cut_number='2', type=CartType.Audio, group_name='TEMPORIBUS', title='aperiam sed totam reiciendis', artist='recusandae nesciunt', album='', year='1962', isrc='', isci='', label='', client='fugiat saepe quam libero', agency='', publisher='', composer='repellat non in fuga', conductor='', song_id='', user_defined='', description='deserunt repellat odit velit', outcue='', filename='000002_002.wav', length=':11', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
    rivendell_cart_6_2 = RivendellCart(cart_number='6', cut_number='2', type=CartType.Audio, group_name='TEMPORIBUS', title='tempora libero earum repudiandae', artist='modi quo', album='', year='1953', isrc='', isci='', label='', client='iure nobis illum quia', agency='', publisher='', composer='fugiat beatae perspiciatis dicta', conductor='', song_id='', user_defined='', description='tempore voluptates tenetur dolorem', outcue='', filename='000006_002.wav', length=':11', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
    rivendell_cart_101_1 = RivendellCart(cart_number='101', cut_number='1', type=CartType.Audio, group_name='TEMPORIBUS', title='aliquam omnis quisquam enim', artist='nobis sit', album='', year='2003', isrc='', isci='', label='', client='culpa quas minus reiciendis', agency='', publisher='', composer='ipsam cumque nulla harum', conductor='', song_id='', user_defined='', description='deserunt natus quidem at', outcue='', filename='000101_001.wav', length=':05', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
    rivendell_cart_500_1 = RivendellCart(cart_number='500', cut_number='1', type=CartType.Audio, group_name='VOLUPTATIB', title='voluptate commodi neque aperiam', artist='reiciendis rem', album='', year='1969', isrc='', isci='', label='', client='assumenda quasi maxime cum', agency='', publisher='', composer='doloremque provident dolorum mollitia', conductor='', song_id='', user_defined='', description='ut praesentium sit quidem', outcue='', filename='000500_001.wav', length=':08', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
    rivendell_cart_970000_1 = RivendellCart(cart_number='970000', cut_number='1', type=CartType.Macro, group_name='ALIQUAM', title='quasi necessitatibus quo vero', artist='sapiente fuga', album='', year='1994', isrc='', isci='', label='', client='distinctio culpa perspiciatis quam', agency='', publisher='', composer='explicabo magni temporibus provident', conductor='', song_id='', user_defined='', description='adipisci officia impedit dolores', outcue='', filename='', length=':00', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
    rivendell_cart_970001_1 = RivendellCart(cart_number='970001', cut_number='1', type=CartType.Macro, group_name='ALIQUAM', title='porro eos dolores fuga', artist='rem dolor', album='', year='2015', isrc='', isci='', label='', client='omnis molestias nesciunt cumque', agency='', publisher='', composer='adipisci quidem consequuntur quia', conductor='', song_id='', user_defined='', description='provident perspiciatis quisquam ea', outcue='', filename='', length=':00', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='2010s')
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


def test__load_rivendell_carts(fs, setup_standard_cart_filter, 
                               defined_rivendell_carts):
    cart_filter = setup_standard_cart_filter.cart_filter
    import pathlib
    rivendell_cart_data_filename = pathlib.Path(r"\fakepath\source_file.csv")
    assert not rivendell_cart_data_filename.exists()

    output_file_path = pathlib.Path(r"\fakepath\output_file.csv")

    fs.create_file(
        rivendell_cart_data_filename, 
        contents=setup_standard_cart_filter.cart_source_file_contents
    )

    cart_filter.rivendell_cart_data_filename = rivendell_cart_data_filename
    cart_filter.output_filename = output_file_path

    result_carts = cart_filter._load_rivendell_carts()

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
        defined_rivendell_carts.rivendell_cart_970000_1,
        defined_rivendell_carts.rivendell_cart_970001_1
    ]
    x = 1
    assert result_carts == expected_carts


def test__remove_macro_carts_no_carts(setup_standard_cart_filter):
    rivendell_carts = []
    expected_carts = []
    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_macro_carts(rivendell_carts=rivendell_carts)
    assert list(result_carts) == expected_carts


def test__remove_macro_carts_all_audio_carts(setup_standard_cart_filter, 
                                             defined_rivendell_carts):
    rivendell_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1
    ]

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_macro_carts(rivendell_carts=rivendell_carts)
    assert expected_carts == list(result_carts)


def test__remove_macro_carts_mixed_carts(setup_standard_cart_filter, 
                                         defined_rivendell_carts):
    rivendell_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
        defined_rivendell_carts.rivendell_cart_970000_1,
        defined_rivendell_carts.rivendell_cart_970001_1
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1
    ]

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_macro_carts(rivendell_carts=rivendell_carts)
    assert expected_carts == list(result_carts)


def test__remove_macro_carts_all_macro_carts(setup_standard_cart_filter, 
                                             defined_rivendell_carts):
    rivendell_carts = [
        defined_rivendell_carts.rivendell_cart_970000_1,
        defined_rivendell_carts.rivendell_cart_970001_1
    ]
    expected_carts = []

    result_carts = setup_standard_cart_filter.cart_filter.\
        _remove_macro_carts(rivendell_carts=rivendell_carts)
    assert expected_carts == list(result_carts)


def test__remove_extra_cuts_no_cuts(setup_standard_cart_filter):
    rivendell_carts = []
    result_carts = setup_standard_cart_filter.cart_filter.\
        _remove_extra_cuts(rivendell_carts=rivendell_carts)

    assert len(result_carts) == 0
    assert result_carts is not rivendell_carts


def test__remove_extra_cuts_no_extra_cuts(setup_standard_cart_filter, defined_rivendell_carts):
    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
    ]

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_extra_cuts(rivendell_carts=rivendell_carts_for_test)

    assert list(result_carts) == expected_carts


def test__remove_extra_cuts_extra_cuts_in_order(setup_standard_cart_filter, 
                                                defined_rivendell_carts):
    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
    ]

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_extra_cuts(rivendell_carts=rivendell_carts_for_test)

    assert list(result_carts) == expected_carts


def test__remove_extra_cuts_extra_cuts_out_of_order(setup_standard_cart_filter, 
                                                    defined_rivendell_carts):
    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
    ]

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_extra_cuts(rivendell_carts=rivendell_carts_for_test)

    assert list(result_carts) == expected_carts


def test__remove_excluded_groups_empty_list(setup_standard_cart_filter, defined_rivendell_carts):
    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
    ]

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_excluded_groups(rivendell_carts=rivendell_carts_for_test)

    assert list(result_carts) == expected_carts


def test__remove_excluded_groups_no_carts_from_groups(setup_standard_cart_filter, defined_rivendell_carts):
    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
    ]

    excluded_groups = ["POSSIMUS", "INCIDUNT"]
    setup_standard_cart_filter.cart_filter.excluded_group_list = excluded_groups

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_excluded_groups(rivendell_carts=rivendell_carts_for_test)

    assert list(result_carts) == expected_carts


def test__remove_excluded_groups_some_carts_from_groups(setup_standard_cart_filter, defined_rivendell_carts):
    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
    ]

    expected_carts = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
    ]

    excluded_groups = ["POSSIMUS", "INCIDUNT", "VOLUPTATIB"]
    setup_standard_cart_filter.cart_filter.excluded_group_list = excluded_groups

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_excluded_groups(rivendell_carts=rivendell_carts_for_test)

    assert list(result_carts) == expected_carts


def test__remove_excluded_groups_all_carts_from_groups(setup_standard_cart_filter, defined_rivendell_carts):
    rivendell_carts_for_test = [
        defined_rivendell_carts.rivendell_cart_1_1,
        defined_rivendell_carts.rivendell_cart_2_1,
        defined_rivendell_carts.rivendell_cart_2_2,
        defined_rivendell_carts.rivendell_cart_6_2,
        defined_rivendell_carts.rivendell_cart_101_1,
        defined_rivendell_carts.rivendell_cart_500_1,
    ]

    expected_carts = [
    ]

    excluded_groups = ["POSSIMUS", "INCIDUNT", "VOLUPTATIB", "TEMPORIBUS", "EXPLICABO"]
    setup_standard_cart_filter.cart_filter.excluded_group_list = excluded_groups

    result_carts = setup_standard_cart_filter.cart_filter\
        ._remove_excluded_groups(rivendell_carts=rivendell_carts_for_test)

    assert list(result_carts) == expected_carts


load_carts_params, rload_carts_ids = wmul_test_utils\
    .generate_true_false_matrix_from_list_of_strings(
        "load_carts_options",
        [
            "include_macros",
            "include_all_cuts",
            "exclude_groups"
        ]
    )


@pytest.fixture(scope="function", params=load_carts_params, ids=rload_carts_ids)
def setup_run_script(request, caplog, mocker):
    params = request.param
    mock_rivendell_cart_data_filename = "mock_rivendell_cart_data_filename"

    mock_rivendell_carts = ["mock_rivendell_carts"]
    mock_load_rivendell_carts = mocker.Mock(return_value=mock_rivendell_carts)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._load_rivendell_carts",
        mock_load_rivendell_carts
    )

    mock_rivendell_carts_without_excluded_groups = ["mock_rivendell_carts_without_excluded_groups"]
    mock_remove_excluded_groups = mocker.Mock(return_value=mock_rivendell_carts_without_excluded_groups)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._remove_excluded_groups",
        mock_remove_excluded_groups
    )

    mock_rivendell_carts_without_macros = ["mock_rivendell_carts_without_macros"]
    mock_remove_macro_carts = mocker.Mock(return_value=mock_rivendell_carts_without_macros)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._remove_macro_carts",
        mock_remove_macro_carts
    )

    mock_rivendell_carts_without_extra_cuts = ["mock_rivendell_carts_without_extra_cuts"]
    mock_remove_extra_cuts = mocker.Mock(return_value=mock_rivendell_carts_without_extra_cuts)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._remove_extra_cuts",
        mock_remove_extra_cuts
    )

    cart_filter = LoadCartDataDump(
        rivendell_cart_data_filename=mock_rivendell_cart_data_filename,
        include_macros=params.include_macros,
        excluded_group_list=params.exclude_groups,
        include_all_cuts=params.include_all_cuts
    )

    results = cart_filter.load_carts()

    return wmul_test_utils.make_namedtuple(
        "setup_load_carts",
        params=params,
        mock_load_rivendell_carts=mock_load_rivendell_carts,
        mock_rivendell_carts=mock_rivendell_carts,
        mock_rivendell_carts_without_excluded_groups=mock_rivendell_carts_without_excluded_groups,
        mock_remove_excluded_groups=mock_remove_excluded_groups,
        mock_remove_macro_carts=mock_remove_macro_carts,
        mock_rivendell_carts_without_macros=mock_rivendell_carts_without_macros,
        mock_remove_extra_cuts=mock_remove_extra_cuts,
        mock_rivendell_carts_without_extra_cuts=mock_rivendell_carts_without_extra_cuts,
        results=results,
        caplog_text=caplog.text
    )


def test_run_script_load_rivendell_carts_called_correctly(setup_run_script):
    setup_run_script.mock_load_rivendell_carts.assert_called_once_with()


def test_run_script_remove_macro_carts_called_correctly(setup_run_script):
    if setup_run_script.params.include_macros:
        setup_run_script.mock_remove_macro_carts.assert_not_called()
    else:
        if setup_run_script.params.exclude_groups:
            setup_run_script.mock_remove_macro_carts.assert_called_once_with(setup_run_script.mock_rivendell_carts_without_excluded_groups)
        else:
            setup_run_script.mock_remove_macro_carts.assert_called_once_with(setup_run_script.mock_rivendell_carts)


def test_run_script_remove_extra_cuts_called_correctly(setup_run_script):
    if setup_run_script.params.include_all_cuts:
        setup_run_script.mock_remove_extra_cuts.assert_not_called()
    else:
        if setup_run_script.params.include_macros:
            if setup_run_script.params.exclude_groups:
                setup_run_script.mock_remove_extra_cuts.assert_called_once_with(setup_run_script.mock_rivendell_carts_without_excluded_groups)
                pass
            else:
                setup_run_script.mock_remove_extra_cuts.assert_called_once_with(setup_run_script.mock_rivendell_carts)
        else:
            setup_run_script.mock_remove_extra_cuts.assert_called_once_with(
                setup_run_script.mock_rivendell_carts_without_macros
            )


def test_run_script_returns_correct_item(setup_run_script):
    if not setup_run_script.params.include_all_cuts:
        assert setup_run_script.results == setup_run_script.mock_rivendell_carts_without_extra_cuts
    elif not setup_run_script.params.include_macros:
        assert setup_run_script.results == setup_run_script.mock_rivendell_carts_without_macros
    elif setup_run_script.params.exclude_groups:
        assert setup_run_script.results == setup_run_script.mock_rivendell_carts_without_excluded_groups
    else:
        assert setup_run_script.results == setup_run_script.mock_rivendell_carts
