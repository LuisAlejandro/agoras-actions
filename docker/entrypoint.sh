#!/usr/bin/env bash

# Exit early if there are errors and be verbose
set -exuo pipefail

if [ "${1}" == "test" ]; then
    echo "Container built successfully, exiting"
    exit 0
fi

python3 /execute.py "$@" | tee /output.log

RESULT="$(cat /output.log | jq -r '.id' | xargs printf '%s,')"

echo "result=${RESULT%%,}" >> $GITHUB_OUTPUT
