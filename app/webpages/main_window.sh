#!/bin/bash 
if [[ "$OSTYPE" != 'linux-gnu' ]]; then
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://localhost:5000/
fi
if [[ "$OSTYPE" == 'linux-gnu' ]]; then
    google-chrome http://localhost:5000/
fi
sleep 3
python3 server.py
