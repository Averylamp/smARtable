#!/bin/bash
ps aux | grep -i server.py | awk '{print $2}' | xargs kill
sleep 1
python3 server.py &
sleep 5
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://localhost:5000/blank &
sleep 4
curl http://localhost:5000/set_backgrounds/
sleep 2
./webpages/calibrate_window.sh
python3 calibration.py

