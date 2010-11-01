#!/usr/bin/sh
# CURRENT SYSTEM USES UAS PARSER AND USER_AGENT.PY PARSER FROM BROWSERSCOPE
# This generates somewhat curated data
python csv_parse.py
python xml_parse.py
python merge_data.py
