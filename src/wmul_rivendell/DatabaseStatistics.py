"""
@Author = 'Michael Stanley'

This script takes the "Cart Data Dump (CSV)" from RD Library and generates statistics about each group.

============ Change Log ============
2025-Jan-03 = Created.

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
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import statistics

import wmul_logger

_logger = wmul_logger.get_logger()

@dataclass
class DatabaseStatistics:
    rivendell_carts: list
    output_filename: Path

    def _organize_by_rivendell_group(self, unorganized_carts):
        organized_by_rivendell_group = defaultdict(list)

        for rivendell_cart in unorganized_carts:
            organized_by_rivendell_group[rivendell_cart.group_name].append(rivendell_cart)
        
        return organized_by_rivendell_group
    
    def _calculate_statistics_per_group(self, organized_carts):
        statistics_per_group = dict()
        for group_name, group_list in organized_carts.items():
            statistics_per_group[group_name] = self._calculate_statistics_of_this_group(group_list=group_list)
        return statistics_per_group
        
    def _calculate_statistics_of_this_group(self, group_list):
        times_of_this_group = [this_item.length_in_seconds() for this_item in group_list]
        mean_this_group = round(statistics.mean(times_of_this_group))
        stdev_this_group = round(statistics.pstdev(times_of_this_group, mu=mean_this_group))
        two_stdev_this_group = 2 * stdev_this_group
        lower_bound = mean_this_group - two_stdev_this_group
        upper_bound = mean_this_group + two_stdev_this_group
        return mean_this_group, stdev_this_group, lower_bound, upper_bound 

    def _write_csv(self, statistics_per_group):
        group_names = statistics_per_group.keys()
        group_names = sorted(group_names)
        with open(str(self.output_filename), newline="", mode="wt", errors="replace") as statistics_output:
            statistics_writer = csv.writer(statistics_output)
            statistics_writer.writerow(["Group Name", "Mean", "Standard Deviation", "Lower Bound", "Upper Bound"])
            for group in group_names:
                group_mean, group_stdev, group_lower_bound, group_upper_bound = statistics_per_group[group]
                statistics_writer.writerow([group, group_mean, group_stdev, group_lower_bound, group_upper_bound])

    def run_script(self):
        _logger.debug(f"with {locals()}")
        organized_by_rivendell_group = self._organize_by_rivendell_group(unorganized_carts=self.rivendell_carts)
        statistics_per_group = self._calculate_statistics_per_group(organized_carts=organized_by_rivendell_group)
        self._write_csv(statistics_per_group)
