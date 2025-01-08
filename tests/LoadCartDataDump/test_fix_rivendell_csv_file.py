"""
@Author = 'Michael Stanley'

============ Change Log ============
2025-Jan-08 = Created. 

============ License ============
Copyright (C) 2025 Michael Stanley

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
import pathlib
import pytest
import wmul_test_utils

from wmul_rivendell.LoadCartDataDump import _fix_rivendell_csv_file


@pytest.fixture(scope="function")
def expected_result():
    return 'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '1,1,audio,LEGAL_ID,Alternative,Legal ID,,,,,,,,,,,,,We Are Marshall (Cheer),,000001_001.wav,:07,0,7523,7079,7497,-1,-1,-1,-1,-1,-1,\r\n' \
        '5,1,audio,LEGAL_ID,Jazz,Legal ID,,,,,,,,,,,,,From the Campus of Marshall University,,000005_001.wav,:04,0,4806,-1,-1,-1,-1,-1,-1,-1,-1,\r\n' \
        '5071,1,audio,PSA_E_30,Arm Chair Officials,Interscholastic Athletics,,,,,,David Adkins,,,,,,"NFHS, NIAAA, WVSSAC 2023","""1_Armchair Officials 30_WV.wav""",,005071_001.wav,:30,0,30000,30000,30001,-1,-1,0,0,-1,-1,\r\n' \
        '5075,1,audio,PSA_E_30,Mentally Healthy Nation,Post Covid Mental Health,,,,,,David Adkins,,,,,,American Psychiatric Association 2023,"""PSNRAPA1E30_01.wav""",,005075_001.wav,:30,0,30000,30000,-1,-1,-1,0,0,-1,-1,\r\n' \
        '100249,1,audio,ALTERNATIV,Calm Is Intention Devouring Its Frailty,Morning Teleportation,,2017,,,,,,,Imported from WOAFR: A17/0370,,,,Calm Is Intention Devouring Its Frailty,,100249_001.wav,4:17,0,257000,252000,257000,-1,-1,0,3000,-1,-1,2015s\r\n'


def test_no_extra_new_lines(fs, expected_result):
    source_file_contents = \
        'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '1,1,audio,LEGAL_ID,Alternative,Legal ID,,,,,,,,,,,,,We Are Marshall (Cheer),,000001_001.wav,:07,0,7523,7079,7497,-1,-1,-1,-1,-1,-1,\r\n' \
        '5,1,audio,LEGAL_ID,Jazz,Legal ID,,,,,,,,,,,,,From the Campus of Marshall University,,000005_001.wav,:04,0,4806,-1,-1,-1,-1,-1,-1,-1,-1,\r\n' \
        '5071,1,audio,PSA_E_30,Arm Chair Officials,Interscholastic Athletics,,,,,,David Adkins,,,,,,"NFHS, NIAAA, WVSSAC 2023","""1_Armchair Officials 30_WV.wav""",,005071_001.wav,:30,0,30000,30000,30001,-1,-1,0,0,-1,-1,\r\n' \
        '5075,1,audio,PSA_E_30,Mentally Healthy Nation,Post Covid Mental Health,,,,,,David Adkins,,,,,,American Psychiatric Association 2023,"""PSNRAPA1E30_01.wav""",,005075_001.wav,:30,0,30000,30000,-1,-1,-1,0,0,-1,-1,\r\n' \
        '100249,1,audio,ALTERNATIV,Calm Is Intention Devouring Its Frailty,Morning Teleportation,,2017,,,,,,,Imported from WOAFR: A17/0370,,,,Calm Is Intention Devouring Its Frailty,,100249_001.wav,4:17,0,257000,252000,257000,-1,-1,0,3000,-1,-1,2015s\r\n'
    
    file_name = pathlib.Path(r"\fakepath\source_file.csv")

    fs.create_file(
        file_name,
        contents=source_file_contents
    )

    with open(file_name, newline="", mode="rt", errors="replace") as rivendell_file:
        result = _fix_rivendell_csv_file(rivendell_source_file=rivendell_file)

    assert expected_result == result.getvalue()


def test_one_with_extra_new_line(fs, expected_result):
    source_file_contents = \
        'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '1,1,audio,LEGAL_ID,Alternative,Legal ID,,,,,,,,,,,,,We Are Marshall (Cheer),,000001_001.wav,:07,0,7523,7079,7497,-1,-1,-1,-1,-1,-1,\r\n' \
        '5,1,audio,LEGAL_ID,Jazz,Legal ID,,,,,,,,,,,,,From the Campus of Marshall University,,000005_001.wav,:04,0,4806,-1,-1,-1,-1,-1,-1,-1,-1,\r\n' \
        '5071,1,audio,PSA_E_30,Arm Chair Officials,Interscholastic Athletics,,,,,,David Adkins,,,,,,"NFHS, NIAAA, WVSSAC\r\n2023","""1_Armchair Officials 30_WV.wav""",,005071_001.wav,:30,0,30000,30000,30001,-1,-1,0,0,-1,-1,\r\n' \
        '5075,1,audio,PSA_E_30,Mentally Healthy Nation,Post Covid Mental Health,,,,,,David Adkins,,,,,,American Psychiatric Association 2023,"""PSNRAPA1E30_01.wav""",,005075_001.wav,:30,0,30000,30000,-1,-1,-1,0,0,-1,-1,\r\n' \
        '100249,1,audio,ALTERNATIV,Calm Is Intention Devouring Its Frailty,Morning Teleportation,,2017,,,,,,,Imported from WOAFR: A17/0370,,,,Calm Is Intention Devouring Its Frailty,,100249_001.wav,4:17,0,257000,252000,257000,-1,-1,0,3000,-1,-1,2015s\r\n'
     
    file_name = pathlib.Path(r"\fakepath\source_file.csv")

    fs.create_file(
        file_name,
        contents=source_file_contents
    )

    with open(file_name, newline="", mode="rt", errors="replace") as rivendell_file:
        result = _fix_rivendell_csv_file(rivendell_source_file=rivendell_file)

    assert expected_result == result.getvalue()

def test_two_with_extra_new_line(fs, expected_result):
    source_file_contents = \
        'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '1,1,audio,LEGAL_ID,Alternative,Legal ID,,,,,,,,,,,,,We Are Marshall (Cheer),,000001_001.wav,:07,0,7523,7079,7497,-1,-1,-1,-1,-1,-1,\r\n' \
        '5,1,audio,LEGAL_ID,Jazz,Legal ID,,,,,,,,,,,,,From the Campus of Marshall University,,000005_001.wav,:04,0,4806,-1,-1,-1,-1,-1,-1,-1,-1,\r\n' \
        '5071,1,audio,PSA_E_30,Arm Chair Officials,Interscholastic Athletics,,,,,,David Adkins,,,,,,"NFHS, NIAAA, WVSSAC\r\n2023","""1_Armchair Officials 30_WV.wav""",,005071_001.wav,:30,0,30000,30000,30001,-1,-1,0,0,-1,-1,\r\n' \
        '5075,1,audio,PSA_E_30,Mentally Healthy Nation,Post Covid Mental Health,,,,,,David Adkins,,,,,,American Psychiatric Association\r\n2023,"""PSNRAPA1E30_01.wav""",,005075_001.wav,:30,0,30000,30000,-1,-1,-1,0,0,-1,-1,\r\n' \
        '100249,1,audio,ALTERNATIV,Calm Is Intention Devouring Its Frailty,Morning Teleportation,,2017,,,,,,,Imported from WOAFR: A17/0370,,,,Calm Is Intention Devouring Its Frailty,,100249_001.wav,4:17,0,257000,252000,257000,-1,-1,0,3000,-1,-1,2015s\r\n'
    
    file_name = pathlib.Path(r"\fakepath\source_file.csv")

    fs.create_file(
        file_name,
        contents=source_file_contents
    )

    with open(file_name, newline="", mode="rt", errors="replace") as rivendell_file:
        result = _fix_rivendell_csv_file(rivendell_source_file=rivendell_file)

    assert expected_result == result.getvalue()


def test_multiple_extra_new_line(fs, expected_result):
    source_file_contents = \
        'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '1,1,audio,LEGAL_ID,Alternative,Legal ID,,,,,,,,,,,,,We Are Marshall (Cheer),,000001_001.wav,:07,0,7523,7079,7497,-1,-1,-1,-1,-1,-1,\r\n' \
        '5,1,audio,LEGAL_ID,Jazz,Legal ID,,,,,,,,,,,,,From the Campus of Marshall University,,000005_001.wav,:04,0,4806,-1,-1,-1,-1,-1,-1,-1,-1,\r\n' \
        '5071,1,audio,PSA_E_30,Arm Chair\r\nOfficials,Interscholastic Athletics,,,,,,David Adkins,,,,,,"NFHS, NIAAA, WVSSAC\r\n2023","""1_Armchair Officials 30_WV.wav""",,005071_001.wav,:30,0,30000,30000,30001,-1,-1,0,0,-1,-1,\r\n' \
        '5075,1,audio,PSA_E_30,Mentally Healthy Nation,Post Covid Mental Health,,,,,,David Adkins,,,,,,American Psychiatric Association\r\n2023,"""PSNRAPA1E30_01.wav""",,005075_001.wav,:30,0,30000,30000,-1,-1,-1,0,0,-1,-1,\r\n' \
        '100249,1,audio,ALTERNATIV,Calm Is Intention Devouring Its Frailty,Morning Teleportation,,2017,,,,,,,Imported from WOAFR: A17/0370,,,,Calm Is Intention Devouring Its Frailty,,100249_001.wav,4:17,0,257000,252000,257000,-1,-1,0,3000,-1,-1,2015s\r\n'
    
    file_name = pathlib.Path(r"\fakepath\source_file.csv")

    fs.create_file(
        file_name,
        contents=source_file_contents
    )

    with open(file_name, newline="", mode="rt", errors="replace") as rivendell_file:
        result = _fix_rivendell_csv_file(rivendell_source_file=rivendell_file)

    assert expected_result == result.getvalue()