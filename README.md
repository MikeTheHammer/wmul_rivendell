# Description

This project provides several utility scripts to help in the use of Rivendell
Radio Automation 4.0+

It may also work with Rivendell 3, but I am no longer guaranteeing that.

`Filter Cart Report For Music Scheduler` takes the Rivendell Cart Data Dump
(.csv) and filters out the fields, cart types, and cuts that are not needed by
external scheduling software.

`Database Statistics` takes the Rivendell Cart Data Dump (.csv) and provides
statistical information about each group. Currently, it generates the Number
of Songs, Shortest Song Length, Longest Song Length, Outlier Limits, Mean,
Standard Deviation, Lower Bound (a variable multiple of standard deviations
below the mean), and  upper bound (a variable multiple of standard deviations
above the mean).

`Load Current Log Line` selects which log to use and which line in the log
to use based on the current date and time.

`Import With File System Metadata` uses the folder structure to find the
group and scheduler code(s) to which a file should be imported.

## Table of Contents

- [Installation - Linux](#installation---linux)
- [Installation - Windows](#installation---windows)
- [Usage](#usage)
  - [Filter Cart Report For Music Scheduler](#filter-cart-report-for-music-scheduler)
  - [Database Statistics](#database-statistics)
  - [Load Current Log Line](#load-current-log-line)
    - [Running Load Current Log Line at Startup](#running-load-current-log-line-at-startup)
  - [Import With File System Metadata](#import-with-file-system-metadata)
    - [Running Import With File System Metadata as a Service](#running-import-with-file-system-metadata-as-a-service)
  - [Logging](#logging)

## Installation - Linux

1. If you are using Ubuntu or Mint, you will need to install `python3-venv`.

    a. Ubuntu 22.04 Jammy Jellyfish or Mint 21.X (Vanessa, Vera, Victoria, or
    Virginia)  

    ```bash
    sudo apt-get update
    sudo apt-get install python3.10-venv
    ```

    b. Ubuntu 24.04 Noble Numbat or Mint 22.X (Wilma, Xia)

    ```bash
    sudo apt-get update
    sudo apt-get install python3.12-venv
    ```

2. Go to your home directory.

    ```bash
    cd ~
    ```

3. Create a Python Virtual Environment for this module. Putting it into a
virtual environment will prevent this module from interfering with or
receiving interference from other Python 3 modules on your system.

    ```bash
    python3 -m venv wmul_rivendell_venv
    ```

4. Activate the virtual environment.

    ```bash
    source wmul_rivendell_venv/bin/activate
    ```

5. Update pip, because the packaged version is already out of date.

    ```bash
    pip3 install --upgrade pip
    ```

6. pip install this package.

    ```bash
    pip3 install wmul_rivendell
    ```

## Installation - Windows

While `Load Current Log Line` and `Rivendell Audio Importer` are only usable on
the same machine as the Rivendell install, `Filter Cart Report For Music
Scheduler` and `Database Statistics` can be run on a Windows machine as well.
(Presumably the same machine as the music scheduler software.)

1. Download and install a recent version of Python 3 from <https://www.python.org/downloads/> .
This software has been tested with Python 3.8-3.13.

    a. Check `Install Launcher for all users (recommended)` and `Add Python
    3.11 to PATH`. (Or whichever Python version you are installing.)  
    b. Click `Customize Installation`.  
    c. Make certain that `pip` is checked.  
    d. Click `Next`.  
    e. Make certain that `Install for all users` is checked.  
    f. Click `Install`.  
    g. Confirm the UAC dialog when it appears.  
    h. Once the install is complete, click `Close`.  

2. Open a Windows Powershell terminal.

3. Change to the root of the C: drive.

    ```powershell
    cd \
    ```

4. Create a Python Virtual Environment for this module. Putting it into a
virtual environment will prevent this module from interfering with or
receiving interference from other Python 3 modules on your system.

    ```powershell
    python3 -m venv wmul_rivendell_venv
    ```

5. Activate the virtual environment.

    ```powershell
    .\wmul_rivendell_venv\Scripts\Activate.ps1
    ```

6. Update pip, because the version packaged with the Python installer is a
bit old almost as soon as the installer is released.

    ```powershell
    pip install --upgrade pip
    ```

7. pip install this package.

    ```powershell
    pip3 install wmul_rivendell
    ```

## Usage

While these four scripts are bundled together because of their common goal of
assisting the Rivendell experience, they are really four different scripts with
four different usages. (Granted, the information from `Database Statistics`
will be helpful inside your music scheduler.)

### Filter Cart Report For Music Scheduler

This script takes the Rivendell Cart Data Dump (.csv) and filters out the
fields, cart types, and cuts that are not needed by external scheduling
software.

(In particular, Natural Music 5 has trouble importing the full Cart Data Dump.
It seems to be due to the number of fields. The Cart Data Dump includes 33
fields and Natural Music 5 seems to only be able to handle 32.)

This script can optionally remove MACRO carts from the data dump and reduce
the entry for each cart down to a single cut.

This script can optionally remove any cuts belonging to specified groups. Use
the `--excluded_groups_file_name [FILENAME]` option. The `FILENAME` should
contain a list of group names that are to be excluded from the output file.
Each group name should be on a separate line. Any cuts belonging to any of
those groups will be exluded from the output. Useful for keeping your
non-music cuts out of your music scheduler.

1. To begin, you will need to create a text file containing the field names
that you want to keep. Each field needs to be on its own line. Field names are
case-insensitive. Two example files are in the github repo:
<https://github.com/MikeTheHammer/wmul_rivendell/tree/main/example_files/>.

    `all_fields.txt` is every field included in Cart Data Dump.
`desired_fields.txt` is an example of a file containing only the desired
fields. Use `Notepad` on Windows, or `Text Editor` on Linux.

2. Use RD Library to create a Cart Data Dump (.csv) file and save it.

3. Run the filter script.

    Usage: `wmul_rivendell [LOGGING] filter-cart-report RIVENDELL_CART_FILENAME
     OUTPUT_FILENAME  DESIRED_FIELDS_FILENAME [OPTIONS]` .

    a. **RIVENDELL_CART_FILENAME** is the name of the Cart Data Dump file.  
    b. **OUTPUT_FILENAME** is the name of the file to which the script should
    write. This is the file that you will load into your music scheduler.
    (If a file with this name already exists, it will be overwritten.)  
    c. **DESIRED_FIELDS_FILENAME** is the name of the file containing the list
    of desired fields. This is the file you created in step 1.  
    d. There are four **[OPTIONS]**:  

    - **--include_macros** If this flag is set, MACROS will be included
        in the output.  
    - **--include_all_cuts** If this flag is set, all the cuts will be
    included in the output. If this flag is left off, only the lowest
    numbered cut will be output.  
    - **--use_trailing_comma** If this flag is set, each line of the
    output file will include a comma at the end. If your music scheduler
    cannot see the final field, try this setting. Natural Music 5 needs
    this flag.  
    - **--excluded_groups_file_name [FILENAME]** Allows you to supply a
    filename with a list of groups to exclude. Any cuts belonging to any
    of those groups will be exluded from the output. Useful for keeping
    your non-music cuts out of your music scheduler.

    e. For an explanation of **[LOGGING]**, see [Logging](#logging).

    **Example:**
    `wmul_rivendell --log_name "~/filter_cart_report.log" --log_level 30
    filter-cart-report "~/cart_data_dump.csv"
    "~/cart_data_for_music_scheduler.csv" "~/desired_fields.txt"
    --use_trailing_comma`

### Database Statistics

This script takes the Rivendell Cart Data Dump (.csv), optionally filters out
specified groups, and generates statistical information about each group.
Currently, it generates the Number of Songs, Shortest Song Length, Longest
Song Length, Outlier Limits, Mean, Standard Deviation, Lower Bound (a variable
multiple of standard deviations below the mean), number of songs shorter than
the lower bound, upper bound (a variable multiple of standard deviations above
the mean), number of songs longer than the upper bound, and the percent of
songs excluded.

Within each group, it first checks the population standard deviation and
population size. If both values are above the set limits, it will remove the
statistical outliers, using the interquartile range method. However, if either
value is below the set limits, this step will be skipped. The default value is
15 seconds for smallest standard deviation and 4 for minimum population. These
values can be changed with command-line options with `--smallest_stdev` and
`--minimum_population`

After removing the statistical outliers, it calculates the mean and standard
deviation. If the new standard deviation is above the set limit, it will
calculate the lower and upper bound. The lower bound is calculated by
multiplying the standard deviation by a multiple and subtracting that from the
mean. The upper bound is calculated by multiplying the standard deviation by a
different multiple and adding that to the mean. The bounds are then rounded off
to the nearest 15 seconds. If the new standard deviation is below the limit,
it will set the bounds to 0, and 86_399 (23:59:59).

**Example:**  
Given:  

> Mean: 3:00  
Standard Deviation: 0:30  
Lower Bound Multiple: 1.5  
Upper Bound Multiple: 3.0  

The calculated results will be:  

> Lower Bound: 2:15  
Upper Bound: 4:30

The lower bound multiple defaults to 1.5 and the upper bound multiple defaults
to 3.0. Both can be changed at the command-line with `--lower_bound_multiple`
and `--upper_bound_mulitple`.

This script can optionally include all cuts inside a cart when making the
calculations. Otherwise, it will base its calculations on the lowest numbered
cut in each cart. Use `--include_all_cuts`.

This script can optionally exclude specified groups and not calculate
statistics for those groups. Use `--excluded_groups_file_name [FILENAME]`. The
`FILENAME` should contain a list of group names that are to be excluded from
the output file. Each group name should be on a separate line. These groups
will be excluded when calculating database statistics. Useful for
focusing on your music groups.  

The script can be provided with new values for the statistical limits: smallest
standard deviation, minimum population, lower bound multiple, and upper bound
multiple.

The script can optionally include the values for the statistical limits in the
output file. Use `--write_limits`. (Useful when exploring different values.)

By default, the script will only output the Number of Songs, Lower Bound, and
Upper Bound. It can optionally include the Shortest Song Length, Longest Song
Length, Outlier Limits, Mean, Standard Deviation, number of songs shorter than
the lower bound, number of songs longer than the upper bound, and the percent
of songs excluded. Use `--write_full_statistics`.

Usage: `wmul_rivendell [LOGGING] database-statistics RIVENDELL_CART_FILENAME  
OUTPUT_FILENAME   [OPTIONS]`

1. **RIVENDELL_CART_FILENAME** is the name of the Cart Data Dump file.
2. **OUTPUT_FILENAME** is the name of the file to which the script should
write. If a file with this name already exists, it will be renamed with "_old"
 at the end.)
3. There are eight **[OPTIONS]**:

    a. **--include_all_cuts** If this flag is set, all the cuts will be
    included in the output. If this flag is left off, only the lowest numbered
    cut will be output.  
    b. **--excluded_groups_file_name [FILENAME]** Allows you to supply a
    filename with a list of groups to exclude. Useful for focusing on your
    music groups.  
    c. **--smallest_stdev** The smallest standard deviation (in seconds)
    permitted for calculating outliers, and upper and lower bounds for
    excluding songs. If the group population standard deviation is less than
    this number, then no outliers will be excluded. If the population
    (excluding outliers) standard deviation is less than this number, then no
    lower and upper boundes will be calculated. This limit helps avoid odd
    behaviour when a group is mostly the same length. E.G. a group containing
    only 30 second spots. Default is 15.  
    d. **--minimum_population** The smallest population for calculating
    outliers. If the population of the group is smaller than or equal to this
    number, then outliers will not be calculated and excluded. Default is 4.  
    e. **--lower_bound_multiple** The standard deviation will be multiplied by
    this number and subtracted from the mean to generate the lower bound.
    Default is 1.5.  
    f. **--upper_bound_multiple** The standard deviation will be multiplied by
    this number and added to the mean to generate the upper bound. Default is
    3.0.  
    g. **--write_limits** If this flag is set, the statistics limits
    (smallest_stdev, minimum_population, lower_bound_multiple, and
    upper_bound_multiple) will be written to the file.  
    h. **--write_full_statistics** If this flag is set, the full set of
    statistics will be written. If not set, only the summary statistics
    (Number of Songs, Lower Bound, Upper Bound) will be written.  
4. For an explanation of **[LOGGING]**, see [Logging](#logging).

### Load Current Log Line

This script will compute the log name for today, connect to the Rivendell
database and find the line in that log that is closest to (but before) the
current time. It can also compute this information for a provided date and
time. It then sends an RML "LL" (Load Log) command to load that log on that
line. Optionally it can send an e-mail showing that log and line were loaded.

This script must run on a system that has Rivendell installed since it
depends on the `rmlsend` module. It's primary use-case is to start the
Rivendell log in the correct place after a reboot; therefore, you will almost
certainly want to install it on your main on-air machine.

I am reasonably certain that this was based on Open Source Radio's
`load-log-skip-to-current-line`:
<https://github.com/opensourceradio/ram/blob/e112952d87a64d92d564ab9693d37c9e63740607/usr/local/bin/load-log-skip-to-current-time> .
However, I did not document my source at the time I originally wrote this
script.  

Usage: `wmul_rivendell [LOGGING] load-current-log-line LOG_NAME_FORMAT
RIVENDELL_HOST [OPTIONS]`

1. **LOG_NAME_FORMAT**: The format of the log name. This will be the same text
string that is in `RD Admin | Manage Services | [Service] | Log Name Template`.
E.G. `WMUL-%m%d"

2. **RIVENDELL_HOST**: The hostname or IP address of the host that is running RD AirPlay.

3. There are sixteen **[OPTIONS]**:

    a. **--sql_host**: The host name to the SQL database. Usually localhost.
    Default: localhost.  
    b. **--sql_user**: The username for the SQL database. Usually rduser.
    Default: rduser.  
    c. **--sql_pass**: The password for the SQL database. Usually letmein.
    Default: letmein.  
    d. **--sql_database_name**: The Database name of the SQL database.
    Usually Rivendell. Default: Rivendell.  
    e. **--use_date**: The date of the log to be loaded. Format is YY-MM-DD or
    YYYY-MM-DD. If this option is omitted, the system date of the system
    running the script will be used.  
    f. **--use_time**: The time of the log line to be loaded. The script will
    find the line closest to, but before that time. Valid formats are
    HH:MM:SS AM, HH:MM AM, HH AM, HH:MM:SS, HH:MM, and HH. If AM/PM are
    present, HH will be 12-hour. If AM/PM are absent, HH will be 24-hour.
    IF MM and/or SS are omitted, they will be set to 00. If this option is
    omitted, the system time of the system running the script will be used.  
    g. **--dry_run**: For testing purposes. Prints out the log line that is
    selected, but does not load it.  
    h. **--start_immediately**: Starts the selected log line immediately. If
    not set, the selected log line will be "made next".  
    i. **--days_back**: Maximum number of days back in time to go. If a log is
    not available for the given day, the script will try to load the previous
    day's log. It will keep going back in time up to and including this many
    days. This option is for cases where it is preferred to load and replay an
    old log rather than no log.  If no logs can be found for those dates, it
    will try to load the default log, if provided. Set this value to 0 to not
    attempt previous days' logs. Defaults to 7.  
    j. **--default_log**: The full name of the last-ditch log to try to load if
    day-based logs fail. (A future version will allow for different default logs
    for each day of the week.)  
    k. **--log_machine**: The log machine on which to load the playlist.
    Defaults to 1 (Main Log).  
    l. **--email_address**: The e-mail address to which the report should be
    sent.  
    m. **--mail_server**: The address of the e-mail SMTP server to use. This
    argument is required if email_address is supplied.  
    n. **--mail_port**: The port of the e-mail server. Defaults to 25.  
    o. **--mail_username**: The username to authenticate with the e-mail
    server.  
    p. **--mail_password**: The password to authenticate with the e-mail
    server.  

4. For an explanation of **[LOGGING]**, see [Logging](#logging).

Example: `wmul_rivendell --log_name "~/load_current_log_line.log" --log_level 30 load-current-log-line "WMUL-%m%d" 192.168.1.1 --sql_host 192.168.1.1 --email_address bob@example.com --mail_server 192.168.1.2 --mail_username bob --mail_password bobspassword`

#### Running Load Current Log Line at Startup

This section explains how to setup a shell script to start RD AirPlay and run
this script at startup.

1. Copy the example shell script from the github repo to a text editor.
`Text Editor` is installed by default on Ubuntu / Mint. The sample shell script
is at: <https://github.com/MikeTheHammer/wmul_rivendell/blob/main/example_files/start_rivendell_and_load_current_log.sh> .

2. Edit the shell script.

    a. The first line of this script `rdairplay &` starts RD AirPlay as a
    separate process.  
    b. The second line `sleep 5s` causes the shell script to sleep for 5
    seconds. Sleeping gives time for RD AirPlay to load completely before the
    next part of the shell script runs. The 5 second pause works on my machine,
    which is a Core i7 9700 with an M.2 SSD. A lower performance machine may
    need a longer sleep.  
    c. The third line is the meat and potatoes of the shell script. Alter this
    line as needed to match the settings on your system.

3. `Save` the file and exit your text editor.

4. In a terminal window, enter
`chmod 700 start_rivendell_and_load_current_log.sh` to make the shell script
executable.

5. In xfce, open `Applications | Settings | Session and Startup`.

6. Select the `Application Autostart` tab.

7. Click `Add`.

8. Give the entry a name, such as "Start RD AirPlay and load current log".
Optionally, give the entry a description.

9. Click the folder icon next to the `Command` box.

10. `start_rivendell_and_load_current_log.sh` should be in the "Recently Used"
folder. If not, navigate to the "rd" home directory.

11. Select `start_rivendell_and_load_current_log.sh` and then click `OK.

12. Click `OK` again. This script should now run each time the `rd` user logs
in.

### Import With File System Metadata

This script is different than the others. It is intended to run as a service.
It continuously scans a directory and all of its subdirectories. When it
detects a .wav file, it derives the Rivendell group and scheduler code(s) from
the names of the subfolders. It then calls rdimport on the file and with the
derived group and scheduler code(s).

This script is the almost the equivalent of being able to configure a dropbox
with the Metadata Pattern of `%g/%i.wav` . (There is no metadata wildcard for
scheduler codes.)

This script must run on a system that has Rivendell installed since it depends
on the `rdimport` module.

**Examples:**

- `/Rivendell Import/FLASHBACK/Queen - Save Me.wav` - Will be imported into
the "FLASHBACK" group, with no scheduler codes.

- `/Rivendell Import/FLASHBACK/1980/Queen - Save Me.wav` - Will be imported
into the "FLASHBACK" group, with the "1980" scheduler code.

- `/Rivendell Import/FLASHBACK/1980/Vinyl/Queen - Save Me.wav` - Will be
imported into the "FLASHBACK" group, with the "1980" and "Vinyl" scheduler
codes.

Note: This script makes no attempt to verify that the group or scheduler
code(s) are valid before calling `rdimport`.

**Limitations:**

- This importer will only detect .wav files.

- The rdimport options: "--autotrim-level=0", "--normalization-level=0",
"--title-from-cartchunk-cutid", "--delete-source", "--verbose" are hardcoded.

- The rdimport option: "--set-string-description=" is hardcoded to the
filename. E.G. `--set-string-description="Queen - Save Me.wav"` .

These limitations may be removed in future versions.

**Usage:**

``wmul_rivendell [LOGGING] import-with-file-system-metadata SOURCE_PATHS [OPTIONS]``

1. **SOURCE_PATHS**: One or more system paths to search for files. Each
subdirectory off each source path will be recursively searched. Any file in the
root directory will be ignored since it doesn't have a group.  

2. There are three **[OPTIONS]**:

    a. **--cache_duration**: How long (in seconds) this importer will remember
    a given file name after sending it to the Rivendell importer. For this
    duration, this importer will ignore any other files with this name.
    Defaults to 180 seconds (3 minutes).  
    b. **--rdimport_syslog**: Tell rdimport to log to syslog. Mutually
    Exclusive with **--rdimport_log_file_name**.
    c. **--rdimport_log_file_name**: Tell rdimport to log to this filename.
    Mutually Exclusive with **--rdimport_syslog**.

3. For an explanation of **[LOGGING]**, see [Logging](#logging).

**Example:**  
`wmul_rivendell --log_name "/home/rd/import_with_file_system_metadata.log"
--log_level 30 import-with-file-system-metadata "/mnt/Rivendell Import Folder/"`

#### Running Import With File System Metadata as a Service

You almost certainly want to run `Import With File System Metadata` as a
ervice that will load and restart automatically. An example `.service` file is
at: <https://github.com/MikeTheHammer/wmul_rivendell/blob/main/example_files/wmul_rivendell_importer.service> .

1. Login as a user with `sudo` permission.

2. Copy the example to a text editor. Save the file as
`wmul_rivendell_importer.service` in your home folder.

3. Alter the line starting with `ExecStart=/home/rd/wmul_rivendell_venv/bin/wmul_rivendell`
as needed to match the settings on your system.

4. Copy file to the `/lib/systemd/system/` directory.

    ```bash
    sudo cp /home/rd/wmul_rivendell_importer.service /lib/systemd/system/
    ```

5. Make the service file executable.

    ```bash
    sudo chmod 644 /lib/systemd/system/wmul_rivendell_importer.service
    ```

6. Enable the service.

    ```bash
    sudo systemctl daemon-reload

    sudo systemctl enable wmul_rivendell_importer.service

    sudo systemctl start wmul_rivendell_importer.service
    ```

### Logging

**--log_name** is the path to the log file.

**--log_level** is the log level: 10: Debug, 20: Info, 30: Warning, 40: Error,
50: Critical. Intermediate values (E.G. 32) are permitted, but will be rounded
up (E.G. Entering 32 is the same as entering 40. Logging messages lower than
the log level will not be written to the log. E.G. If 30 is input, then all
Debug, and Info messages will be silenced.

To utilize this module's logging feature for debugging, the log directives
need to be included between the `wmul_rivendell` command and the specific
script command. (This is a limitation of python's click module.)

**Example:**  
`wmul_rivendell --log_name "/home/rd/filter_cart_report.log" --log_level 30
filter-cart-report [filter-cart-report-args]`

(A future version may modify this.)
