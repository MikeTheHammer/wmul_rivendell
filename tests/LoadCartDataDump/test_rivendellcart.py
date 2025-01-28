"""
@Author = 'Michael Stanley'

============ Change Log ============
2023-May-25 = Moved from tests/FilterCartReportForMusicScheduler when the 
                code under test was refactored into LoadCartDataDump.

2023-Jan-20 = Change license from GPLv2 to GPLv3.

2020-Oct-21 = Created.

============ License ============
Copyright (C) 2020, 2023, 2025 Michael Stanley

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
from collections import namedtuple
from wmul_rivendell.LoadCartDataDump import CartType, RivendellCart
import pytest
import wmul_test_utils

from_dict_options = namedtuple(
    "from_dict_options",
    [
        "audio_cart"
    ]
)


from_dict_params, from_dict_ids = wmul_test_utils.generate_true_false_matrix_from_namedtuple(from_dict_options)


@pytest.fixture(scope="function", params=from_dict_params, ids=from_dict_ids)
def setup_from_dict(request):
    if request.param.audio_cart:
        expected_type = CartType.Audio
        type_for_dict = "audio"
    else:
        expected_type = CartType.Macro
        type_for_dict = "macro"

    expected_cart_number = '638525'
    expected_cut_number = '1'
    expected_group_name = '"EXPLICABO"'
    expected_title = 'perferendis enim harum repudiandae'
    expected_artist = 'nisi ipsum'
    expected_album = 'molestiae aut'
    expected_year = '"2017"'
    expected_isrc = 'atque ratione'
    expected_isci = 'consequuntur eligendi'
    expected_label = 'occaecati vero'
    expected_client = 'amet fugiat'
    expected_agency = 'possimus corrupti'
    expected_publisher = 'soluta rerum'
    expected_composer = '"placeat sed'
    expected_conductor = 'enim architecto'
    expected_song_id = 'suscipit veritatis'
    expected_user_defined = 'accusamus reprehenderit'
    expected_description = 'repellat consectetur'
    expected_outcue = 'maiores incidunt'
    expected_filename = 'recusandae unde'
    expected_length = '7:14'
    expected_length_in_seconds = 434
    expected_start_point = 'repudiandae totam'
    expected_end_point = 'aut iste'
    expected_segue_start_point = 'dignissimos tenetur'
    expected_segue_end_point = 'molestiae doloremque'
    expected_hook_start_point = 'doloribus cupiditate'
    expected_hook_end_point = 'reprehenderit perspiciatis'
    expected_talk_start_point = 'similique dolorum'
    expected_talk_end_point = 'dolorem nostrum'
    expected_fadeup_point = 'assumenda praesentium'
    expected_fadedown_point = 'minus vitae'
    expected_sched_codes = 'non officia'

    source_dict = {
        "CART_NUMBER": expected_cart_number,
        "CUT_NUMBER": expected_cut_number,
        "TYPE": type_for_dict,
        "GROUP_NAME": expected_group_name,
        "TITLE": expected_title,
        "ARTIST": expected_artist,
        "ALBUM": expected_album,
        "YEAR": expected_year,
        "ISRC": expected_isrc,
        "ISCI": expected_isci,
        "LABEL": expected_label,
        "CLIENT": expected_client,
        "AGENCY": expected_agency,
        "PUBLISHER": expected_publisher,
        "COMPOSER": expected_composer,
        "CONDUCTOR": expected_conductor,
        "SONG_ID": expected_song_id,
        "USER_DEFINED": expected_user_defined,
        "DESCRIPTION": expected_description,
        "OUTCUE": expected_outcue,
        "FILENAME": expected_filename,
        "LENGTH": expected_length,
        "START_POINT": expected_start_point,
        "END_POINT": expected_end_point,
        "SEGUE_START_POINT": expected_segue_start_point,
        "SEGUE_END_POINT": expected_segue_end_point,
        "HOOK_START_POINT": expected_hook_start_point,
        "HOOK_END_POINT": expected_hook_end_point,
        "TALK_START_POINT": expected_talk_start_point,
        "TALK_END_POINT": expected_talk_end_point,
        "FADEUP_POINT": expected_fadeup_point,
        "FADEDOWN_POINT": expected_fadedown_point,
        "SCHED_CODES": expected_sched_codes
    }

    result_rivendell_cart = RivendellCart.from_dict(source_dict=source_dict)

    return wmul_test_utils.make_namedtuple(
        "setup_from_dict__audio",
        expected_cart_number=expected_cart_number,
        expected_cut_number=expected_cut_number,
        expected_type=expected_type,
        expected_group_name=expected_group_name,
        expected_title=expected_title,
        expected_artist=expected_artist,
        expected_album=expected_album,
        expected_year=expected_year,
        expected_isrc=expected_isrc,
        expected_isci=expected_isci,
        expected_label=expected_label,
        expected_client=expected_client,
        expected_agency=expected_agency,
        expected_publisher=expected_publisher,
        expected_composer=expected_composer,
        expected_conductor=expected_conductor,
        expected_song_id=expected_song_id,
        expected_user_defined=expected_user_defined,
        expected_description=expected_description,
        expected_outcue=expected_outcue,
        expected_filename=expected_filename,
        expected_length=expected_length,
        expected_length_in_seconds=expected_length_in_seconds,
        expected_start_point=expected_start_point,
        expected_end_point=expected_end_point,
        expected_segue_start_point=expected_segue_start_point,
        expected_segue_end_point=expected_segue_end_point,
        expected_hook_start_point=expected_hook_start_point,
        expected_hook_end_point=expected_hook_end_point,
        expected_talk_start_point=expected_talk_start_point,
        expected_talk_end_point=expected_talk_end_point,
        expected_fadeup_point=expected_fadeup_point,
        expected_fadedown_point=expected_fadedown_point,
        expected_sched_codes=expected_sched_codes,
        result_rivendell_cart=result_rivendell_cart
    )


def test_from_dict_cart_number_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_cart_number == result_rivendell_cart.cart_number


def test_from_dict_cut_number_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_cut_number == result_rivendell_cart.cut_number


def test_from_dict_type_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_type == result_rivendell_cart.type


def test_from_dict_group_name_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_group_name == result_rivendell_cart.group_name


def test_from_dict_title_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_title == result_rivendell_cart.title


def test_from_dict_artist_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_artist == result_rivendell_cart.artist


def test_from_dict_album_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_album == result_rivendell_cart.album


def test_from_dict_year_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_year == result_rivendell_cart.year


def test_from_dict_isrc_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_isrc == result_rivendell_cart.isrc


def test_from_dict_isci_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_isci == result_rivendell_cart.isci


def test_from_dict_label_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_label == result_rivendell_cart.label


def test_from_dict_client_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_client == result_rivendell_cart.client


def test_from_dict_agency_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_agency == result_rivendell_cart.agency


def test_from_dict_publisher_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_publisher == result_rivendell_cart.publisher


def test_from_dict_composer_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_composer == result_rivendell_cart.composer


def test_from_dict_conductor_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_conductor == result_rivendell_cart.conductor


def test_from_dict_song_id_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_song_id == result_rivendell_cart.song_id


def test_from_dict_user_defined_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_user_defined == result_rivendell_cart.user_defined


def test_from_dict_description_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_description == result_rivendell_cart.description


def test_from_dict_outcue_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_outcue == result_rivendell_cart.outcue


def test_from_dict_filename_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_filename == result_rivendell_cart.filename


def test_from_dict_length_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_length == result_rivendell_cart.length


def test_from_dict_start_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_start_point == result_rivendell_cart.start_point


def test_from_dict_end_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_end_point == result_rivendell_cart.end_point


def test_from_dict_segue_start_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_segue_start_point == result_rivendell_cart.segue_start_point


def test_from_dict_segue_end_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_segue_end_point == result_rivendell_cart.segue_end_point


def test_from_dict_hook_start_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_hook_start_point == result_rivendell_cart.hook_start_point


def test_from_dict_hook_end_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_hook_end_point == result_rivendell_cart.hook_end_point


def test_from_dict_talk_start_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_talk_start_point == result_rivendell_cart.talk_start_point


def test_from_dict_talk_end_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_talk_end_point == result_rivendell_cart.talk_end_point


def test_from_dict_fadeup_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_fadeup_point == result_rivendell_cart.fadeup_point


def test_from_dict_fadedown_point_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_fadedown_point == result_rivendell_cart.fadedown_point


def test_from_dict_sched_codes_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_sched_codes == result_rivendell_cart.sched_codes

def test_length_in_seconds_correct(setup_from_dict):
    result_rivendell_cart = setup_from_dict.result_rivendell_cart
    assert setup_from_dict.expected_length_in_seconds == result_rivendell_cart.length_in_seconds()

def test_length_in_seconds_longer_than_one_hour():
    source_dict = {
        "CART_NUMBER": '100340',
        "CUT_NUMBER": '1',
        "TYPE": "audio",
        "GROUP_NAME": '"ALTERNATIV"',
        "TITLE": '"Do You Want Love"',
        "ARTIST": '"Dave Depper"',
        "ALBUM": '""',
        "YEAR": '"2017"',
        "ISRC": '""',
        "ISCI": '""',
        "LABEL": '""',
        "CLIENT": '""',
        "AGENCY": '""',
        "PUBLISHER": '""',
        "COMPOSER": '"Imported from WOAFR: A17/0461"',
        "CONDUCTOR": '""',
        "SONG_ID": '""',
        "USER_DEFINED": '""',
        "DESCRIPTION": '"Do You Want Love"',
        "OUTCUE": '""',
        "FILENAME": '"100340_001.wav"',
        "LENGTH": '1:07:14',
        "START_POINT": '0',
        "END_POINT": '434000',
        "SEGUE_START_POINT": '432000',
        "SEGUE_END_POINT": '434000',
        "HOOK_START_POINT": '-1',
        "HOOK_END_POINT": '-1',
        "TALK_START_POINT": '0',
        "TALK_END_POINT": '40000',
        "FADEUP_POINT": '-1',
        "FADEDOWN_POINT": '-1',
        "SCHED_CODES": '"2015s"'
    }

    result_rivendell_cart = RivendellCart.from_dict(source_dict=source_dict)

    expected_length_in_seconds = 4034

    assert result_rivendell_cart.length_in_seconds() == expected_length_in_seconds
