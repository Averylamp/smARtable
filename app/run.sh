#!/bin/bash
ps aux | grep -i server.py | awk '{print $2}' | xargs kill
sleep 1
python3 server.py &
sleep 5
if [[ "$OSTYPE" != 'linux-gnu' ]]; then
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://localhost:5000/blank &
fi
if [[ "$OSTYPE" == 'linux-gnu' ]]; then
    google-chrome http://localhost:5000/blank &
fi
sleep 4
curl http://localhost:5000/set_backgrounds/
sleep 2
./webpages/calibrate_window.sh
python3 calibration.py

