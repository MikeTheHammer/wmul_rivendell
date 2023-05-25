"""
@Author = 'Michael Stanley'

This script takes the "Cart Data Dump (CSV)" from RD Library and eliminates data fields that the music scheduler
cannot use. It does this because some music schedulers, such as Natural Music 5, cannot import the full data dump.

============ Change Log ============
2023-May-25 = Refactor to remove RivendellCart, CartType, and the logic for 
                loading and filtering the carts into LoadCartDataDump. This 
                refactoring will allow DatabaseStatistics to re-use the code.

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
from wmul_rivendell.LoadCartDataDump import LoadCartDataDump

import wmul_logger

_logger = wmul_logger.get_logger()


@dataclass
class FilterCartReportForMusicScheduler:
    rivendell_carts: list
    output_filename: Path
    desired_field_list: list
    use_trailing_comma: bool

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
        
        music_scheduler_carts = self._remove_unwanted_fields(self.rivendell_carts)
        self._export_carts_to_csv(music_scheduler_carts)


class TrailingCommaDialect(csv.excel):
    lineterminator = ',\r\n'


csv.register_dialect("TrailingComma", TrailingCommaDialect)
