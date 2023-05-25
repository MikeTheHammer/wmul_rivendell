"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-May-25 = Created. Most of this module was refactored from 
                tests/FilterCartReportForMusicScheduler/
                test_filtercartreportformusicscheduler.py when the code under 
                test was refactored into LoadCartDataDump.

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
import pytest
import wmul_test_utils

from wmul_rivendell.LoadCartDataDump import LoadCartDataDump, RivendellCart, CartType


cart_filter_params, cart_filter_ids = \
    wmul_test_utils.generate_true_false_matrix_from_list_of_strings(
        "cart_filter_params", ["fix_bad_header"]
    )

@pytest.fixture(scope="function", params=cart_filter_params, 
    ids=cart_filter_ids )
def setup_standard_cart_filter(cart_source_file_contents, request):
    mock_rivendell_cart_data_filename = "mock_rivendell_cart_data_filename"
    fix_bad_header = request.param.fix_bad_header

    cart_filter = LoadCartDataDump(
        rivendell_cart_data_filename=mock_rivendell_cart_data_filename,
        fix_header=fix_bad_header,
        include_macros=False,
        excluded_group_list=[],
        include_all_cuts=False
    )

    return wmul_test_utils.make_namedtuple(
        "setup_standard_cart_filter",
        cart_filter=cart_filter,
        cart_source_file_contents=\
            cart_source_file_contents.source_file_contents,
        fix_bad_header=fix_bad_header,
        use_bad_header=cart_source_file_contents.use_bad_header
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


cart_source_file_contents_params, cart_source_file_ids = \
    wmul_test_utils.generate_true_false_matrix_from_list_of_strings(
        "cart_source_file_contents_options", ["use_bad_header"]
    )

@pytest.fixture(scope="function", params=cart_source_file_contents_params, 
    ids=cart_source_file_ids )
def cart_source_file_contents(request):
    """Source file contents should parse to rivendell_cart_1_1 and 
        rivendell_cart_6_2 in the defined_carts fixture. """

    use_bad_header = request.param.use_bad_header

    if use_bad_header:
        """ This has the bad header that is present in Rivendell 3.6.4 - 3.6.6 """
        
        source_file_contents = \
            'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,"FILENAME,LENGTH",START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\n' \
            '1,1,audio,"LEGAL_ID","Alternative","Legal ID","","","","","","","","","","","","","We Are Marshall (Cheer)","","000001_001.wav",:07,0,7523,7079,7497,-1,-1,-1,-1,-1,-1,""\n' \
            '6,2,audio,"ALTERNATIV","Flashback","Legal ID","","","","","","","","","","","","","Every Hour Commercial Free","","000006_002.wav",:11,0,11023,-1,-1,-1,-1,-1,-1,-1,-1,""\n'
    else:
        source_file_contents = \
            'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\n' \
            '1,1,audio,"LEGAL_ID","Alternative","Legal ID","","","","","","","","","","","","","We Are Marshall (Cheer)","","000001_001.wav",:07,0,7523,7079,7497,-1,-1,-1,-1,-1,-1,""\n' \
            '6,2,audio,"ALTERNATIV","Flashback","Legal ID","","","","","","","","","","","","","Every Hour Commercial Free","","000006_002.wav",:11,0,11023,-1,-1,-1,-1,-1,-1,-1,-1,""\n'
    
    return wmul_test_utils.make_namedtuple(
        "cart_source_file_contents",
        use_bad_header=use_bad_header,
        source_file_contents=source_file_contents
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

    if (setup_standard_cart_filter.use_bad_header and 
            not setup_standard_cart_filter.fix_bad_header):
        with pytest.raises(KeyError) as ke:
            result_carts = cart_filter._load_rivendell_carts()
            assert "KeyError: 'FILENAME'" in str(ke)
    else:
        result_carts = cart_filter._load_rivendell_carts()

        expected_carts = [
            defined_rivendell_carts.rivendell_cart_1_1,
            defined_rivendell_carts.rivendell_cart_6_2
        ]

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

    excluded_groups = ["STREETBEAT", "SG_MISC"]
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
    ]

    excluded_groups = ["STREETBEAT", "SG_MISC", "ALT_IMAGE"]
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

    excluded_groups = ["STREETBEAT", "SG_MISC", "ALT_IMAGE", "LEGAL_ID", "ALTERNATIV"]
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
            "fix_header",
            "exclude_groups"
        ]
    )


@pytest.fixture(scope="function", params=load_carts_params, ids=rload_carts_ids)
def setup_run_script(request, caplog, mocker):
    params = request.param
    mock_rivendell_cart_data_filename = "mock_rivendell_cart_data_filename"

    mock_rivendell_carts = "mock_rivendell_carts"
    mock_load_rivendell_carts = mocker.Mock(return_value=mock_rivendell_carts)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._load_rivendell_carts",
        mock_load_rivendell_carts
    )

    mock_rivendell_carts_without_excluded_groups = "mock_rivendell_carts_without_excluded_groups"
    mock_remove_excluded_groups = mocker.Mock(return_value=mock_rivendell_carts_without_excluded_groups)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._remove_excluded_groups",
        mock_remove_excluded_groups
    )

    mock_rivendell_carts_without_macros = "mock_rivendell_carts_without_macros"
    mock_remove_macro_carts = mocker.Mock(return_value=mock_rivendell_carts_without_macros)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._remove_macro_carts",
        mock_remove_macro_carts
    )

    mock_rivendell_carts_without_extra_cuts = "mock_rivendell_carts_without_extra_cuts"
    mock_remove_extra_cuts = mocker.Mock(return_value=mock_rivendell_carts_without_extra_cuts)
    mocker.patch(
        "wmul_rivendell.LoadCartDataDump.LoadCartDataDump._remove_extra_cuts",
        mock_remove_extra_cuts
    )

    cart_filter = LoadCartDataDump(
        rivendell_cart_data_filename=mock_rivendell_cart_data_filename,
        fix_header=params.fix_header,
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
