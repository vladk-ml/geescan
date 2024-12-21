#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set display for X11 forwarding if not using WSLg
if [ -z "$DISPLAY" ]; then
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    export LIBGL_ALWAYS_INDIRECT=1
fi

# Run the application
python main.py
