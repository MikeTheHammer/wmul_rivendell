"""
@Author = 'Michael Stanley'

This script takes the "Cart Data Dump (CSV)" from RD Library and eliminates data fields that the music scheduler
cannot use. It does this because some music schedulers, such as Natural Music 5, cannot import the full data dump.

============ Change Log ============
2023-Jan-20 = Back-insert items into change log.
              Change license from GPLv2 to GPLv3.

2023-Jan-19 = Modify to accomodate a bug in Rivendell 3.6.4-3.6.6 where two 
                fields in the header are malformed.

2022-May-06 = Update documentation.

2021-May-26 = Change RivendellCart to keep cart_number, cut_number, and year as
                strings. 
              Refactor from_csv to from_dict, to more accurately reflect the 
                way it works.
              Refactor to make the removal of macro carts into a method, for
                easier unit testing.

2020-Jun-25 = Created.

============ License ============
Copyright (C) 2020-2023 Michael Stanley

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
import csv
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from pathlib import Path

import wmul_logger

_logger = wmul_logger.get_logger()


class CartType(Enum):
    Audio = 1
    Macro = 2


@dataclass
class RivendellCart:
    cart_number: str
    cut_number: str
    type: CartType
    group_name: str
    title: str
    artist: str
    album: str
    year: str
    isrc: str
    isci: str
    label: str
    client: str
    agency: str
    publisher: str
    composer: str
    conductor: str
    song_id: str
    user_defined: str
    description: str
    outcue: str
    filename: str
    length: str
    start_point: str
    end_point: str
    segue_start_point: str
    segue_end_point: str
    hook_start_point: str
    hook_end_point: str
    talk_start_point: str
    talk_end_point: str
    fadeup_point: str
    fadedown_point: str
    sched_codes: str

    @classmethod
    def from_dict(cls, source_dict):
        if source_dict["TYPE"] == "audio":
            cart_type = CartType.Audio
        else:
            cart_type = CartType.Macro

        return cls(
            cart_number=source_dict["CART_NUMBER"],
            cut_number=source_dict["CUT_NUMBER"],
            type=cart_type,
            group_name=source_dict["GROUP_NAME"],
            title=source_dict["TITLE"],
            artist=source_dict["ARTIST"],
            album=source_dict["ALBUM"],
            year=source_dict["YEAR"],
            isrc=source_dict["ISRC"],
            isci=source_dict["ISCI"],
            label=source_dict["LABEL"],
            client=source_dict["CLIENT"],
            agency=source_dict["AGENCY"],
            publisher=source_dict["PUBLISHER"],
            composer=source_dict["COMPOSER"],
            conductor=source_dict["CONDUCTOR"],
            song_id=source_dict["SONG_ID"],
            user_defined=source_dict["USER_DEFINED"],
            description=source_dict["DESCRIPTION"],
            outcue=source_dict["OUTCUE"],
            filename=source_dict["FILENAME"],
            length=source_dict["LENGTH"],
            start_point=source_dict["START_POINT"],
            end_point=source_dict["END_POINT"],
            segue_start_point=source_dict["SEGUE_START_POINT"],
            segue_end_point=source_dict["SEGUE_END_POINT"],
            hook_start_point=source_dict["HOOK_START_POINT"],
            hook_end_point=source_dict["HOOK_END_POINT"],
            talk_start_point=source_dict["TALK_START_POINT"],
            talk_end_point=source_dict["TALK_END_POINT"],
            fadeup_point=source_dict["FADEUP_POINT"],
            fadedown_point=source_dict["FADEDOWN_POINT"],
            sched_codes=source_dict["SCHED_CODES"]
        )


@dataclass
class FilterCartReportForMusicScheduler:
    rivendell_cart_data_filename: Path
    output_filename: Path
    desired_field_list: list
    include_macros: bool
    include_all_cuts: bool
    use_trailing_comma: bool
    fix_header: bool

    def _load_rivendell_carts(self):
        with open(str(self.rivendell_cart_data_filename), newline="", mode="rt", errors="replace") as \
                rivendell_source_file:
            if self.fix_header:
                source_file = rivendell_source_file.readlines()
                first_line = source_file[0]
                first_line = first_line.replace('"', '')
                new_contents = "\n".join([first_line, *source_file[1:]])
                string_buffer = StringIO(initial_value=new_contents)
            else:
                string_buffer = StringIO(initial_value=rivendell_source_file.read())
            
            rivendell_reader = csv.DictReader(string_buffer)
            rivendell_carts = [RivendellCart.from_dict(rivendell_cart) for rivendell_cart in rivendell_reader]
        return rivendell_carts

    def _remove_macro_carts(self, rivendell_carts):
        return (rivendell_cart for rivendell_cart in rivendell_carts if not rivendell_cart.type == CartType.Macro)

    def _remove_extra_cuts(self, rivendell_carts):
        carts_grouped_by_cart_number = dict()
        for cart in rivendell_carts:
            if cart.cart_number in carts_grouped_by_cart_number:
                if cart.cut_number < carts_grouped_by_cart_number[cart.cart_number].cut_number:
                    carts_grouped_by_cart_number[cart.cart_number] = cart
            else:
                carts_grouped_by_cart_number[cart.cart_number] = cart
        return carts_grouped_by_cart_number.values()

    def _remove_unwanted_fields(self, rivendell_carts):
        music_scheduler_carts = []
        for cart in rivendell_carts:
            music_scheduler_cart = OrderedDict()
            for desired_field in self.desired_field_list:
                music_scheduler_cart[desired_field] = getattr(cart, desired_field.lower(), "INVALID FIELD NAME")
            music_scheduler_carts.append(music_scheduler_cart)
        return music_scheduler_carts

    def _export_carts_to_csv(self, music_scheduler_carts):
        if self.use_trailing_comma:
            dialect = "TrailingComma"
        else:
            dialect = "excel"
        with open(str(self.output_filename), newline="", mode="wt", errors="replace") as music_scheduler_file:
            natural_music_writer = csv.DictWriter(music_scheduler_file, music_scheduler_carts[0].keys(),
                                                  dialect=dialect)
            natural_music_writer.writerows(music_scheduler_carts)

    def run_script(self):
        _logger.debug(f"Starting run_script with {self}")
        rivendell_carts = self._load_rivendell_carts()

        if not self.include_macros:
            rivendell_carts = self._remove_macro_carts(rivendell_carts)
        if not self.include_all_cuts:
            rivendell_carts = self._remove_extra_cuts(rivendell_carts)

        music_scheduler_carts = self._remove_unwanted_fields(rivendell_carts)
        self._export_carts_to_csv(music_scheduler_carts)


class TrailingCommaDialect(csv.excel):
    lineterminator = ',\r\n'


csv.register_dialect("TrailingComma", TrailingCommaDialect)
