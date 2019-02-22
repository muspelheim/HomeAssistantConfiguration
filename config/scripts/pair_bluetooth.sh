#!/bin/sh

bluetoothctl << EOF
agent on
default-agent
connect C9:20:4C:20:5C:C4
EOF
