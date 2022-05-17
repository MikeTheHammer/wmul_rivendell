#!/bin/bash

rdairplay &
sleep 5s
~/wmul_rivendell_venv/bin/wmul_rivendell --log_name /home/rd/load_current_log_line.log --log_level 30 load-current-log-line "WMUL-%m%d" 192.168.1.1 --sql_host 192.168.1.1 --email_address bob@example.com --mail_server 192.168.1.2 --mail_username bob --mail_password "bobspassword"
