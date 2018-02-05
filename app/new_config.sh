#!/bin/bash
export CUR_DIR=$(pwd)
if [[ "$OSTYPE" != 'linux-gnu' ]]; then
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=file://$CUR_DIR/templates/static_calibrate.html &
fi
if [[ "$OSTYPE" == 'linux-gnu' ]]; then
    google-chrome file://$CUR_DIR/templates/static_calibrate.html
fi
python3 calibration.py
