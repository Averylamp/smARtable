#!/bin/bash 
if [[ "$OSTYPE" != 'linux-gnu' ]]; then
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://localhost:5000/blank
fi
if [[ "$OSTYPE" == 'linux-gnu' ]]; then
    google-chrome http://localhost:5000/blank
fi
