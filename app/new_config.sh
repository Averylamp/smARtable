#!/bin/bash
if [[ "$OSTYPE" != 'linux-gnu' ]]; then
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=file:///Users/avery/Developer/projects/smARtable/app/templates/blank_index.html &
fi
if [[ "$OSTYPE" == 'linux-gnu' ]]; then
    google-chrome file:///Users/avery/Developer/projects/smARtable/app/templates/blank_index.html &
fi
python3 calibration.py