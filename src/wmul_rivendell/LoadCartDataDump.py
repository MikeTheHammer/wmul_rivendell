"""
@Author = 'Michael Stanley'

This script takes the "Cart Data Dump (CSV)" from RD Library and converts it 
into Python data.


============ Change Log ============
2023-May-25 = Created. This module was originally part of 
                FilterCartReportForMusicSchedule and was refactored into this
                module so that DatabaseStatistics could re-use the code.

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
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from os import SEEK_SET
from pathlib import Path

import wmul_logger

_logger = wmul_logger.get_logger()



class CartType(Enum):
    Audio = 1
    Macro = 2

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


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
        _logger.debug(source_dict)
        if source_dict["TYPE"] == "audio":
            cart_type = CartType.Audio
        else:
            cart_type = CartType.Macro

        description=source_dict["DESCRIPTION"]
        if isinstance(description, str):
            description = description.strip()

        outcue=source_dict["OUTCUE"]
        if isinstance(outcue, str):
            outcue = outcue.strip()

        return cls(
            cart_number=source_dict["CART_NUMBER"],
            cut_number=source_dict["CUT_NUMBER"],
            type=cart_type,
            group_name=source_dict["GROUP_NAME"],
            title=source_dict["TITLE"].strip(),
            artist=source_dict["ARTIST"].strip(),
            album=source_dict["ALBUM"].strip(),
            year=source_dict["YEAR"].strip(),
            isrc=source_dict["ISRC"].strip(),
            isci=source_dict["ISCI"].strip(),
            label=source_dict["LABEL"].strip(),
            client=source_dict["CLIENT"].strip(),
            agency=source_dict["AGENCY"].strip(),
            publisher=source_dict["PUBLISHER"].strip(),
            composer=source_dict["COMPOSER"].strip(),
            conductor=source_dict["CONDUCTOR"].strip(),
            song_id=source_dict["SONG_ID"].strip(),
            user_defined=source_dict["USER_DEFINED"].strip(),
            description=description,
            outcue=outcue,
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

    def length_in_seconds(self):
        _logger.info(self)
        length = self.length
        if length.count(":") > 1:
            hours, minutes, seconds = length.split(":")
            hours = int(hours)
        else:
            minutes, seconds = self.length.split(":")
            hours = 0

        if minutes:
            minutes = int(minutes)
        else:
            minutes = 0
        seconds = int(seconds)

        return (hours * 3600) + (minutes * 60) + seconds


def _fix_rivendell_csv_file(rivendell_source_file):
    text_buffer = StringIO()

    file_iterator = iter(rivendell_source_file)
    expected_fields = next(file_iterator)
    text_buffer.write(expected_fields)

    line_buffer = StringIO(expected_fields)
    line_parsed_as_csv = list(csv.reader(line_buffer))[0]

    count_of_expected_fields = len(line_parsed_as_csv)

    try:
        while True:
            text_line = next(file_iterator)
            text_line_buffer = StringIO(text_line)
            text_line_parsed_as_csv = list(csv.reader(text_line_buffer))[0]
            
            while len(text_line_parsed_as_csv) < count_of_expected_fields:
                text_line = text_line.strip()
                next_line = next(file_iterator)
                text_line = text_line + " " + next_line
                text_line_buffer = StringIO(text_line)
                text_line_parsed_as_csv = list(csv.reader(text_line_buffer))[0]

                if len(text_line_parsed_as_csv) > count_of_expected_fields:
                    raise ValueError(f"There are errors in the csv file that cannot be automatically fixed. {text_line_buffer.getvalue()}")
            text_buffer.write(text_line_buffer.getvalue())
    except StopIteration:
        text_buffer.seek(0, SEEK_SET)
        return text_buffer


@dataclass
class LoadCartDataDump:
    rivendell_cart_data_filename: Path
    excluded_group_list: list
    include_macros: bool
    include_all_cuts: bool

    def _load_rivendell_carts(self):
        with open(str(self.rivendell_cart_data_filename), newline="", mode="rt", errors="replace") as \
                rivendell_source_file:
            rivendell_fixed_data = _fix_rivendell_csv_file(rivendell_source_file)
            rivendell_reader = csv.DictReader(rivendell_fixed_data)
            rivendell_carts = [RivendellCart.from_dict(rivendell_cart) for rivendell_cart in rivendell_reader]
        return rivendell_carts

    def _remove_excluded_groups(self, rivendell_carts):
        return (rivendell_cart for rivendell_cart in rivendell_carts if
                rivendell_cart.group_name not in self.excluded_group_list)

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

    def load_carts(self):
        _logger.debug(f"Starting load_carts with {self}")
        rivendell_carts = self._load_rivendell_carts()

        if self.excluded_group_list:
            rivendell_carts = self._remove_excluded_groups(rivendell_carts)
        if not self.include_macros:
            rivendell_carts = self._remove_macro_carts(rivendell_carts)
        if not self.include_all_cuts:
            rivendell_carts = self._remove_extra_cuts(rivendell_carts)

        return rivendell_carts
