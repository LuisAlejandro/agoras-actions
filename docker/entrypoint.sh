#!/usr/bin/env bash

# Do not use -x: action args include platform credentials and would leak to logs.
set -euo pipefail

if [ "${1}" == "test" ]; then
    echo "Container built successfully, exiting"
    exit 0
fi

REFRESH_MODE=false
for arg in "$@"; do
    case "${arg}" in
        action=refresh-credentials|action=\"refresh-credentials\")
            REFRESH_MODE=true
            ;;
    esac
done

if [ "${REFRESH_MODE}" = true ]; then
    python3 /execute.py "$@"
    exit $?
fi

python3 /execute.py "$@" | tee /output.log

RESULT="$(cat /output.log | jq -r '.id' | xargs printf '%s,')"

echo "result=${RESULT%%,}" >> $GITHUB_OUTPUT
