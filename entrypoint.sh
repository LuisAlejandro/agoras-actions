#!/usr/bin/env bash

if [ "${1}" == "bash" ]; then
    bash
elif [ "${1}" == "daemon" ]; then
    tail -f /dev/null
else
    python3 /action.py ${1}
fi
