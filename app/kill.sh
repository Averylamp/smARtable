#!/bin/bash
ps aux | grep -i server.py | awk '{print $2}' | xargs kill
