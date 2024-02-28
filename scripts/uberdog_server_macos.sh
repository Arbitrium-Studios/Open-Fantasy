#!/bin/sh
cd ../

# Define some constants for our AI server:
MAX_CHANNELS=999999
STATESERVER=4002
ASTRON_IP="127.0.0.1:7199"
EVENTLOGGER_IP="127.0.0.1:7198"
BASE_CHANNEL=${BASE_CHANNEL:-1000000}

while [ true ]
do
python3 -m toontown.uberdog.UDStart --base-channel $BASE_CHANNEL --max-channels $MAX_CHANNELS --stateserver $STATESERVER --messagedirector-ip $ASTRON_IP --eventlogger-ip $EVENTLOGGER_IP
done