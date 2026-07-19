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

# Prefer last JSON object line; use .ids[] when present else .id
JSON_LINE="$(grep -E '^\{.*\}$' /output.log | tail -n 1 || true)"
if [ -z "${JSON_LINE}" ]; then
  echo "No JSON result from Agoras" >&2
  exit 1
fi
RESULT="$(printf '%s\n' "${JSON_LINE}" | jq -r 'if (.ids | type) == "array" then (.ids | join(",")) else .id end')"
echo "result=${RESULT}" >> "$GITHUB_OUTPUT"
