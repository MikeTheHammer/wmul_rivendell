"""
@Author = 'Michael Stanley'

This script takes the "Cart Data Dump (CSV)" from RD Library and generates statistics about each group.

============ Change Log ============
2025-Jan-17 = Extract statistics, expand generated data.

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
import math
import numpy as np
import pandas as pd
from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import wmul_logger

_logger = wmul_logger.get_logger()

_MAX_TIME = 86_399


@dataclass
class StatisticsLimits:
    smallest_stdev: int = 15
    minimum_population_for_outliers: int = 4
    lower_bound_multiple: float = 1.5
    upper_bound_multiple: float = 3.0

    def to_pandas_series(self):
        return pd.Series(
            {
                "Smallest Standard Deviation": str(timedelta(seconds=int(self.smallest_stdev))),
                "Minimum Population for Outliers": self.minimum_population_for_outliers,
                "Lower Bound Multiple": self.lower_bound_multiple,
                "Upper Bound Multiple": self.upper_bound_multiple
            }
        )
    

class RivendellGroupStatistics:

    def __init__(self, group_name: str, songs_in_group: list, stats_limits: StatisticsLimits):
        self.group_name = group_name
        self.stats_limits = stats_limits
        times_of_this_group = np.array([this_item.length_in_seconds() for this_item in songs_in_group])
        times_of_this_group.sort()
        
        self.number_of_songs = times_of_this_group.size
        self.shortest_song_length = times_of_this_group.min()
        self.longest_song_length = times_of_this_group.max()

        outliers_exluded, outlier_lower_limit, outlier_upper_limit = _remove_outliers(
            times_of_this_group=times_of_this_group, 
            stats_limits=stats_limits
        )

        self.outlier_limits = (round(outlier_lower_limit), round(outlier_upper_limit))
        self.mean = round(outliers_exluded.mean())
        
        stdev = outliers_exluded.std()
        if math.isnan(stdev):
            self.stdev = 0
        else:
            self.stdev = round(stdev)

        if stdev > self.stats_limits.smallest_stdev:
            lower_bound = self.mean - (stats_limits.lower_bound_multiple * stdev)
            if lower_bound < 0:
                self.lower_bound = 0
            else:
                self.lower_bound = RivendellGroupStatistics._nearest_15(lower_bound)
            upper_bound = self.mean + (stats_limits.upper_bound_multiple * stdev)
            self.upper_bound = RivendellGroupStatistics._nearest_15(upper_bound)

            shorter_than_lower_bound = [
                song_length for song_length in times_of_this_group if song_length < self.lower_bound
            ]
            self.number_of_songs_shorter_than_lower_bound = len(shorter_than_lower_bound)

            longer_than_upper_bound = [
                song_length for song_length in times_of_this_group if song_length > self.upper_bound
            ]
            self.number_of_songs_longer_than_upper_bound = len(longer_than_upper_bound)
            total_songs_excluded = self.number_of_songs_shorter_than_lower_bound + \
                self.number_of_songs_longer_than_upper_bound
            percentage_of_songs_excluded = (total_songs_excluded / self.number_of_songs) * 100
            percentage_of_songs_excluded = round(percentage_of_songs_excluded, 1)
            self.percentage_of_songs_excluded = percentage_of_songs_excluded
        else:
            # If STDev is below stats_limits.smallest_stdev, there is not enough variance in the lengths of the songs 
            # for the exclusion to be meaningful and correct.
            self.lower_bound = 0
            self.number_of_songs_shorter_than_lower_bound = 0
            self.upper_bound = _MAX_TIME
            self.number_of_songs_longer_than_upper_bound = 0
            self.percentage_of_songs_excluded = 0
    
    @staticmethod
    def _nearest_15(input_number):
        input_number = round(input_number)
        mod_15 = input_number % 15
        if mod_15 == 0:
            return input_number
        elif mod_15 < 8:
            return input_number - mod_15
        else:
            return input_number + (15 - mod_15)
        
    def to_pandas_series(self):
        lower_outlier_limit, upper_outlier_limit = self.outlier_limits
        lower_outlier_limit = str(timedelta(seconds=int(lower_outlier_limit)))
        upper_outlier_limit = str(timedelta(seconds=int(upper_outlier_limit)))

        return pd.Series(
            {
                "Number of Songs": self.number_of_songs,
                "Shortest Song Length": str(timedelta(seconds=int(self.shortest_song_length))),
                "Longest Song Length": str(timedelta(seconds=int(self.longest_song_length))),
                "Outlier Limits": (lower_outlier_limit, upper_outlier_limit),
                "Mean": str(timedelta(seconds=int(self.mean))),
                "Standard Deviation": str(timedelta(seconds=int(self.stdev))),
                "Lower Bound": str(timedelta(seconds=int(self.lower_bound))),
                "Number of Songs < Lower Bound": self.number_of_songs_shorter_than_lower_bound,
                "Upper Bound": str(timedelta(seconds=int(self.upper_bound))),
                "Number of Songs > Upper Bound": self.number_of_songs_longer_than_upper_bound,
                "Percent of Songs Excluded": self.percentage_of_songs_excluded
            }
        )


def _remove_outliers(times_of_this_group: np.array, stats_limits: StatisticsLimits):
    if ((times_of_this_group.size > stats_limits.minimum_population_for_outliers) and 
        (times_of_this_group.std() >= stats_limits.smallest_stdev)):
        q25, q75 = np.percentile(times_of_this_group, [25, 75])
        iqr = q75 - q25
        iqr_times_1_point_5 = iqr * 1.5
        lower_limit = q25 - iqr_times_1_point_5
        upper_limit = q75 + iqr_times_1_point_5
        outliers_excluded = np.array([this_item for this_item in times_of_this_group if lower_limit < this_item < upper_limit])
        outliers_excluded.sort()
        return outliers_excluded, lower_limit, upper_limit
    else:
        return times_of_this_group, 0, _MAX_TIME


@dataclass
class DatabaseStatistics:
    rivendell_carts: list
    output_filename: Path
    stats_limits: StatisticsLimits
    write_limits: bool

    def _organize_by_rivendell_group(self, unorganized_carts):
        organized_by_rivendell_group = defaultdict(list)

        for rivendell_cart in unorganized_carts:
            organized_by_rivendell_group[rivendell_cart.group_name].append(rivendell_cart)
        
        return organized_by_rivendell_group
    
    def _calculate_statistics_per_group(self, organized_carts):
        statistics_per_group = dict()
        for group_name, songs_in_group in organized_carts.items():
            _logger.debug(f"Working on {group_name}")
            statistics_per_group[group_name] = RivendellGroupStatistics(
                group_name=group_name, 
                songs_in_group=songs_in_group,
                stats_limits=self.stats_limits
            )
        return statistics_per_group

    def _write_csv(self, statistics_per_group):
        df_limits = pd.DataFrame(
            { "Statistics Limits": self.stats_limits.to_pandas_series() }
        )
        df_limits = df_limits.T

        group_names = sorted(statistics_per_group.keys())
        df_data = pd.DataFrame(
            { group_name: statistics_per_group[group_name].to_pandas_series() for group_name in group_names }
        )
        df_data = df_data.T

        with open(str(self.output_filename), newline="", mode="wt", errors="replace") as statistics_output:
            if self.write_limits:
                df_limits.to_csv(statistics_output)
            df_data.to_csv(statistics_output, index_label="Group Name")

    def _write_excel(self, statistics_per_group):
        df_limits = pd.DataFrame(
            { "Statistics Limits": self.stats_limits.to_pandas_series() }
        )
        df_limits = df_limits.T

        group_names = sorted(statistics_per_group.keys())
        df_data = pd.DataFrame(
            { group_name: statistics_per_group[group_name].to_pandas_series() for group_name in group_names }
        )

        df_data = df_data.T
        with pd.ExcelWriter(self.output_filename) as writer:
            if self.write_limits:
                df_limits.to_excel(writer, sheet_name="Limits")
            df_data.to_excel(writer, sheet_name="Data")

    def run_script(self):
        _logger.debug(f"Starting DatabaseStatistics.run_script()")
        organized_by_rivendell_group = self._organize_by_rivendell_group(unorganized_carts=self.rivendell_carts)
        statistics_per_group = self._calculate_statistics_per_group(organized_carts=organized_by_rivendell_group)
        if self.output_filename.suffix == '.xlsx':
            self._write_excel(statistics_per_group)
        else:
            self._write_csv(statistics_per_group=statistics_per_group)
