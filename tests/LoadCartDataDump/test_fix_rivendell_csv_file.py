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
    return \
        'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '599159,1,audio,aliquid,Inventore neque dignissimos repellendus.,Reprehenderit officiis cum.,,,,,,,,,,,,Laudantium asperiores veritatis quia facere in consequuntur.,Fugit eligendi perferendis itaque placeat optio.,,,,,,,,,,,,,,2010s\r\n' \
        '139437,1,audio,odit,Quisquam voluptatem voluptas nostrum.,Aliquid a consequatur.,,,,,,,,,,,,Modi quo dolores pariatur iste.,Aperiam nesciunt sapiente culpa dolore impedit alias.,,,,,,,,,,,,,,2010s\r\n' \
        '520726,1,audio,incidunt,Repellendus omnis modi sequi.,Corrupti necessitatibus fugiat.,,,,,,,,,,,,Corrupti vitae quo ipsam voluptatem deleniti expedita voluptas.,Doloribus earum nulla debitis blanditiis iste cumque.,,,,,,,,,,,,,,2010s\r\n' \
        '680237,1,audio,doloribus,Quod laboriosam expedita ipsa.,A quae ex.,,,,,,,,,,,,Doloribus ea illo culpa ullam libero.,Qui voluptatibus earum laboriosam libero.,,,,,,,,,,,,,,2010s\r\n' \
        '174387,1,audio,porro,Perferendis tempore consequatur molestiae.,Expedita harum praesentium.,,,,,,,,,,,,"Ipsam voluptas impedit alias a modi amet.",Corrupti non rerum reiciendis.,,,,,,,,,,,,,,2010s\r\n' \
        '146066,1,audio,officia,Similique quo ullam exercitationem.,Ea ratione itaque.,,,,,,,,,,,,Officiis tenetur corrupti dolores nulla porro.,Nemo occaecati ad blanditiis eos sed doloribus enim.,,,,,,,,,,,,,,2010s\r\n' \
        '93372,1,audio,aperiam,Nisi mollitia voluptates autem.,Repellendus cum labore.,,,,,,,,,,,,Nisi ullam deleniti expedita aspernatur deserunt.,Voluptates placeat est vitae sint.,,,,,,,,,,,,,,2010s\r\n' \
        '787912,1,audio,voluptate,Repudiandae quam ipsum quia.,Dignissimos nisi blanditiis.,,,,,,,,,,,,Ab incidunt illum fugit repellat dicta quo reiciendis.,Expedita facere incidunt deserunt.,,,,,,,,,,,,,,2010s\r\n' \
        '785851,1,audio,id,Iure eos libero tenetur.,Illo odit expedita.,,,,,,,,,,,,Laboriosam ipsum labore laboriosam porro.,Reiciendis illo recusandae vitae voluptatibus quam.,,,,,,,,,,,,,,2010s\r\n' \
        '68669,1,audio,saepe,Sed saepe accusamus eveniet.,Eum qui nostrum.,,,,,,,,,,,,Non dolores est nam repellendus.,Dolore quia veritatis.,,,,,,,,,,,,,,2010s\r\n' 

def test_no_extra_new_lines(fs, expected_result):
    source_file_contents = \
        'CART_NUMBER,CUT_NUMBER,TYPE,GROUP_NAME,TITLE,ARTIST,ALBUM,YEAR,ISRC,ISCI,LABEL,CLIENT,AGENCY,PUBLISHER,COMPOSER,CONDUCTOR,SONG_ID,USER_DEFINED,DESCRIPTION,OUTCUE,FILENAME,LENGTH,START_POINT,END_POINT,SEGUE_START_POINT,SEGUE_END_POINT,HOOK_START_POINT,HOOK_END_POINT,TALK_START_POINT,TALK_END_POINT,FADEUP_POINT,FADEDOWN_POINT,SCHED_CODES\r\n' \
        '599159,1,audio,aliquid,Inventore neque dignissimos repellendus.,Reprehenderit officiis cum.,,,,,,,,,,,,Laudantium asperiores veritatis quia facere in consequuntur.,Fugit eligendi perferendis itaque placeat optio.,,,,,,,,,,,,,,2010s\r\n' \
        '139437,1,audio,odit,Quisquam voluptatem voluptas nostrum.,Aliquid a consequatur.,,,,,,,,,,,,Modi quo dolores pariatur iste.,Aperiam nesciunt sapiente culpa dolore impedit alias.,,,,,,,,,,,,,,2010s\r\n' \
        '520726,1,audio,incidunt,Repellendus omnis modi sequi.,Corrupti necessitatibus fugiat.,,,,,,,,,,,,Corrupti vitae quo ipsam voluptatem deleniti expedita voluptas.,Doloribus earum nulla debitis blanditiis iste cumque.,,,,,,,,,,,,,,2010s\r\n' \
        '680237,1,audio,doloribus,Quod laboriosam expedita ipsa.,A quae ex.,,,,,,,,,,,,Doloribus ea illo culpa ullam libero.,Qui voluptatibus earum laboriosam libero.,,,,,,,,,,,,,,2010s\r\n' \
        '174387,1,audio,porro,Perferendis tempore consequatur molestiae.,Expedita harum praesentium.,,,,,,,,,,,,"Ipsam voluptas impedit alias a modi amet.",Corrupti non rerum reiciendis.,,,,,,,,,,,,,,2010s\r\n' \
        '146066,1,audio,officia,Similique quo ullam exercitationem.,Ea ratione itaque.,,,,,,,,,,,,Officiis tenetur corrupti dolores nulla porro.,Nemo occaecati ad blanditiis eos sed doloribus enim.,,,,,,,,,,,,,,2010s\r\n' \
        '93372,1,audio,aperiam,Nisi mollitia voluptates autem.,Repellendus cum labore.,,,,,,,,,,,,Nisi ullam deleniti expedita aspernatur deserunt.,Voluptates placeat est vitae sint.,,,,,,,,,,,,,,2010s\r\n' \
        '787912,1,audio,voluptate,Repudiandae quam ipsum quia.,Dignissimos nisi blanditiis.,,,,,,,,,,,,Ab incidunt illum fugit repellat dicta quo reiciendis.,Expedita facere incidunt deserunt.,,,,,,,,,,,,,,2010s\r\n' \
        '785851,1,audio,id,Iure eos libero tenetur.,Illo odit expedita.,,,,,,,,,,,,Laboriosam ipsum labore laboriosam porro.,Reiciendis illo recusandae vitae voluptatibus quam.,,,,,,,,,,,,,,2010s\r\n' \
        '68669,1,audio,saepe,Sed saepe accusamus eveniet.,Eum qui nostrum.,,,,,,,,,,,,Non dolores est nam repellendus.,Dolore quia veritatis.,,,,,,,,,,,,,,2010s\r\n' 
    
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
        '599159,1,audio,aliquid,Inventore neque dignissimos repellendus.,Reprehenderit officiis cum.,,,,,,,,,,,,Laudantium asperiores veritatis quia facere in consequuntur.,Fugit eligendi perferendis itaque placeat optio.,,,,,,,,,,,,,,2010s\r\n' \
        '139437,1,audio,odit,Quisquam voluptatem voluptas nostrum.,Aliquid a consequatur.,,,,,,,,,,,,Modi quo dolores pariatur iste.,Aperiam nesciunt sapiente culpa dolore impedit alias.,,,,,,,,,,,,,,2010s\r\n' \
        '520726,1,audio,incidunt,Repellendus omnis modi sequi.,Corrupti necessitatibus fugiat.,,,,,,,,,,,,Corrupti vitae quo ipsam voluptatem deleniti expedita voluptas.,Doloribus earum nulla debitis blanditiis iste cumque.,,,,,,,,,,,,,,2010s\r\n' \
        '680237,1,audio,doloribus,Quod laboriosam expedita ipsa.,A quae ex.,,,,,,,,,,,,Doloribus ea illo culpa ullam libero.,Qui voluptatibus earum laboriosam libero.,,,,,,,,,,,,,,2010s\r\n' \
        '174387,1,audio,porro,Perferendis tempore consequatur molestiae.,Expedita harum praesentium.,,,,,,,,,,,,"Ipsam voluptas impedit\r\nalias a modi amet.",Corrupti non rerum reiciendis.,,,,,,,,,,,,,,2010s\r\n' \
        '146066,1,audio,officia,Similique quo ullam exercitationem.,Ea ratione itaque.,,,,,,,,,,,,Officiis tenetur corrupti dolores nulla porro.,Nemo occaecati ad blanditiis eos sed doloribus enim.,,,,,,,,,,,,,,2010s\r\n' \
        '93372,1,audio,aperiam,Nisi mollitia voluptates autem.,Repellendus cum labore.,,,,,,,,,,,,Nisi ullam deleniti expedita aspernatur deserunt.,Voluptates placeat est vitae sint.,,,,,,,,,,,,,,2010s\r\n' \
        '787912,1,audio,voluptate,Repudiandae quam ipsum quia.,Dignissimos nisi blanditiis.,,,,,,,,,,,,Ab incidunt illum fugit repellat dicta quo reiciendis.,Expedita facere incidunt deserunt.,,,,,,,,,,,,,,2010s\r\n' \
        '785851,1,audio,id,Iure eos libero tenetur.,Illo odit expedita.,,,,,,,,,,,,Laboriosam ipsum labore laboriosam porro.,Reiciendis illo recusandae vitae voluptatibus quam.,,,,,,,,,,,,,,2010s\r\n' \
        '68669,1,audio,saepe,Sed saepe accusamus eveniet.,Eum qui nostrum.,,,,,,,,,,,,Non dolores est nam repellendus.,Dolore quia veritatis.,,,,,,,,,,,,,,2010s\r\n' 
         
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
        '599159,1,audio,aliquid,Inventore neque dignissimos repellendus.,Reprehenderit officiis cum.,,,,,,,,,,,,Laudantium asperiores veritatis quia facere in consequuntur.,Fugit eligendi perferendis itaque placeat optio.,,,,,,,,,,,,,,2010s\r\n' \
        '139437,1,audio,odit,Quisquam voluptatem voluptas nostrum.,Aliquid a consequatur.,,,,,,,,,,,,Modi quo dolores pariatur iste.,Aperiam nesciunt sapiente culpa dolore impedit alias.,,,,,,,,,,,,,,2010s\r\n' \
        '520726,1,audio,incidunt,Repellendus omnis modi sequi.,Corrupti necessitatibus fugiat.,,,,,,,,,,,,Corrupti vitae quo ipsam voluptatem deleniti expedita voluptas.,Doloribus earum nulla debitis blanditiis iste cumque.,,,,,,,,,,,,,,2010s\r\n' \
        '680237,1,audio,doloribus,Quod laboriosam expedita ipsa.,A quae ex.,,,,,,,,,,,,Doloribus ea illo culpa ullam libero.,Qui voluptatibus earum laboriosam libero.,,,,,,,,,,,,,,2010s\r\n' \
        '174387,1,audio,porro,Perferendis tempore consequatur molestiae.,Expedita harum praesentium.,,,,,,,,,,,,"Ipsam voluptas impedit\r\nalias a modi amet.",Corrupti non rerum reiciendis.,,,,,,,,,,,,,,2010s\r\n' \
        '146066,1,audio,officia,Similique quo ullam exercitationem.,Ea ratione itaque.,,,,,,,,,,,,Officiis tenetur corrupti\r\ndolores nulla porro.,Nemo occaecati ad blanditiis eos sed doloribus enim.,,,,,,,,,,,,,,2010s\r\n' \
        '93372,1,audio,aperiam,Nisi mollitia voluptates autem.,Repellendus cum labore.,,,,,,,,,,,,Nisi ullam deleniti expedita aspernatur deserunt.,Voluptates placeat est vitae sint.,,,,,,,,,,,,,,2010s\r\n' \
        '787912,1,audio,voluptate,Repudiandae quam ipsum quia.,Dignissimos nisi blanditiis.,,,,,,,,,,,,Ab incidunt illum fugit repellat dicta quo reiciendis.,Expedita facere incidunt deserunt.,,,,,,,,,,,,,,2010s\r\n' \
        '785851,1,audio,id,Iure eos libero tenetur.,Illo odit expedita.,,,,,,,,,,,,Laboriosam ipsum labore laboriosam porro.,Reiciendis illo recusandae vitae voluptatibus quam.,,,,,,,,,,,,,,2010s\r\n' \
        '68669,1,audio,saepe,Sed saepe accusamus eveniet.,Eum qui nostrum.,,,,,,,,,,,,Non dolores est nam repellendus.,Dolore quia veritatis.,,,,,,,,,,,,,,2010s\r\n' 

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
        '599159,1,audio,aliquid,Inventore neque dignissimos repellendus.,Reprehenderit officiis cum.,,,,,,,,,,,,Laudantium asperiores veritatis quia facere in consequuntur.,Fugit eligendi perferendis itaque placeat optio.,,,,,,,,,,,,,,2010s\r\n' \
        '139437,1,audio,odit,Quisquam voluptatem voluptas nostrum.,Aliquid a consequatur.,,,,,,,,,,,,Modi quo dolores pariatur iste.,Aperiam nesciunt sapiente culpa dolore impedit alias.,,,,,,,,,,,,,,2010s\r\n' \
        '520726,1,audio,incidunt,Repellendus omnis modi sequi.,Corrupti necessitatibus fugiat.,,,,,,,,,,,,Corrupti vitae quo ipsam voluptatem deleniti expedita voluptas.,Doloribus earum nulla debitis blanditiis iste cumque.,,,,,,,,,,,,,,2010s\r\n' \
        '680237,1,audio,doloribus,Quod laboriosam expedita ipsa.,A quae ex.,,,,,,,,,,,,Doloribus ea illo culpa ullam libero.,Qui voluptatibus earum laboriosam libero.,,,,,,,,,,,,,,2010s\r\n' \
        '174387,1,audio,porro,Perferendis tempore consequatur molestiae.,Expedita harum praesentium.,,,,,,,,,,,,"Ipsam voluptas impedit\r\nalias a modi amet.",Corrupti non rerum reiciendis.,,,,,,,,,,,,,,2010s\r\n' \
        '146066,1,audio,officia,Similique\r\nquo ullam exercitationem.,Ea ratione itaque.,,,,,,,,,,,,Officiis tenetur corrupti\r\ndolores nulla porro.,Nemo occaecati ad blanditiis eos sed doloribus enim.,,,,,,,,,,,,,,2010s\r\n' \
        '93372,1,audio,aperiam,Nisi mollitia voluptates autem.,Repellendus cum labore.,,,,,,,,,,,,Nisi ullam deleniti expedita aspernatur deserunt.,Voluptates placeat est vitae sint.,,,,,,,,,,,,,,2010s\r\n' \
        '787912,1,audio,voluptate,Repudiandae quam ipsum quia.,Dignissimos nisi blanditiis.,,,,,,,,,,,,Ab incidunt illum fugit repellat dicta quo reiciendis.,Expedita facere incidunt deserunt.,,,,,,,,,,,,,,2010s\r\n' \
        '785851,1,audio,id,Iure eos libero tenetur.,Illo odit expedita.,,,,,,,,,,,,Laboriosam ipsum labore laboriosam porro.,Reiciendis illo recusandae vitae voluptatibus quam.,,,,,,,,,,,,,,2010s\r\n' \
        '68669,1,audio,saepe,Sed saepe accusamus eveniet.,Eum qui nostrum.,,,,,,,,,,,,Non dolores est nam repellendus.,Dolore quia veritatis.,,,,,,,,,,,,,,2010s\r\n' 
    
    file_name = pathlib.Path(r"\fakepath\source_file.csv")

    fs.create_file(
        file_name,
        contents=source_file_contents
    )

    with open(file_name, newline="", mode="rt", errors="replace") as rivendell_file:
        result = _fix_rivendell_csv_file(rivendell_source_file=rivendell_file)

    assert expected_result == result.getvalue()