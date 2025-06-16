"""
@Author = 'Michael Stanley'

This script takes the "Cart Data Dump (CSV)" from RD Library and eliminates data fields that the music scheduler
cannot use. It does this because some music schedulers, such as Natural Music 5, cannot import the full data dump.

============ Change Log ============
2025-Jan-03 = Change the way the trailing comma is added. Python 3.13 doesn't allow a comma to be included in the line 
              terminator. Instead, a dummy additional field is added to the end of the record.

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
Copyright (C) 2020-2023, 2025 Michael Stanley

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
import pandas as pd
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from wmul_rivendell.LoadCartDataDump import RivendellCart


import wmul_logger

_logger = wmul_logger.get_logger()


@dataclass
class ConvertDatabaseBase:
    rivendell_carts: list[RivendellCart]
    output_filename: Path
    desired_field_list: list[str]

    def _remove_unwanted_fields(self, rivendell_carts):
        trimmed_carts = []
        for cart in rivendell_carts:
            this_trimmed_cart  = OrderedDict()
            for desired_field in self.desired_field_list:
                this_trimmed_cart[desired_field] = getattr(cart, desired_field.lower(), "INVALID FIELD NAME IN DESIRED FIELDS FILE")
            trimmed_carts.append(this_trimmed_cart)
        return trimmed_carts

    def _export_carts(self, trimmed_carts):
        pass

    def run_script(self):
        _logger.debug(f"Starting run_script with {self}")
        music_scheduler_carts = self._remove_unwanted_fields(self.rivendell_carts)
        self._export_carts(music_scheduler_carts)


@dataclass
class ConvertDatabaseToCSV(ConvertDatabaseBase):
    use_trailing_comma: bool

    def _export_carts(self, trimmed_carts):
        fieldnames = list(trimmed_carts[0].keys())
        if self.use_trailing_comma:
            fieldnames.append("Placeholder")
        with open(str(self.output_filename), newline="", mode="wt", errors="replace") as music_scheduler_file:
            natural_music_writer = csv.DictWriter(music_scheduler_file, fieldnames,
                                                  dialect="excel")
            natural_music_writer.writerows(trimmed_carts)


@dataclass
class ConvertDatabaseToExcel(ConvertDatabaseBase):
    def _export_carts(self, trimmed_carts):
        df_data = pd.DataFrame(trimmed_carts)
        with pd.ExcelWriter(self.output_filename) as writer:
            df_data.to_excel(writer, sheet_name="Data")
