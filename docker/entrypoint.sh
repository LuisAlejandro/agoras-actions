#!/usr/bin/env bash




if [ "${1}" == "bash" ]; then
    bash

elif [ "${1}" == "new-tw-post" ]; then
    agoras publish
        --network twitter \
        --action post \
        --twitter-consumer-key ${2} \
        --twitter-consumer-secret ${3} \
        --twitter-oauth-token ${4} \
        --twitter-oauth-secret ${5} \
        --status-text ${6} \
        --status-image-url-1 ${7} \
        --status-image-url-2 ${8} \
        --status-image-url-3 ${9} \
        --status-image-url-4 ${10}

elif [ "${1}" == "new-fb-post" ]; then
    agoras publish
        --network facebook \
        --action post \
        --facebook-access-token ${2} \
        --facebook-object-id ${3} \
        --status-text ${4} \
        --status-image-url-1 ${5} \
        --status-image-url-2 ${6} \
        --status-image-url-3 ${7} \
        --status-image-url-4 ${9}

elif [ "${1}" == "new-ig-post" ]; then
    agoras publish
        --network instagram \
        --action post \
        --instagram-access-token ${2} \
        --instagram-object-id ${3} \
        --status-text ${4} \
        --status-image-url-1 ${5} \
        --status-image-url-2 ${6} \
        --status-image-url-3 ${7} \
        --status-image-url-4 ${9}

elif [ "${1}" == "new-li-post" ]; then
    agoras publish
        --network linkedin \
        --action post \
        --linkedin-username ${2} \
        --linkedin-password ${3} \
        --status-text ${4} \
        --status-image-url-1 ${5} \
        --status-image-url-2 ${6} \
        --status-image-url-3 ${7} \
        --status-image-url-4 ${9}

elif [ "${1}" == "tweet-like" ]; then
    agoras publish
        --network twitter \
        --action like \
        --twitter-consumer-key ${2} \
        --twitter-consumer-secret ${3} \
        --twitter-oauth-token ${4} \
        --twitter-oauth-secret ${5} \
        --tweet-id ${6}

elif [ "${1}" == "tweet-share" ]; then
    agoras publish
        --network twitter \
        --action share \
        --twitter-consumer-key ${2} \
        --twitter-consumer-secret ${3} \
        --twitter-oauth-token ${4} \
        --twitter-oauth-secret ${5} \
        --tweet-id ${6}

elif [ "${1}" == "tweet-last-post-from-feed" ]; then
    agoras publish
        --network twitter \
        --action last-from-feed \
        --twitter-consumer-key ${2} \
        --twitter-consumer-secret ${3} \
        --twitter-oauth-token ${4} \
        --twitter-oauth-secret ${5} \
        --feed-url ${6} \
        --max-count ${7} \
        --post-lookback ${8}

elif [ "${1}" == "tweet-random-post-from-feed" ]; then
    agoras publish
        --network twitter \
        --action random-from-feed \
        --twitter-consumer-key ${2} \
        --twitter-consumer-secret ${3} \
        --twitter-oauth-token ${4} \
        --twitter-oauth-secret ${5} \
        --feed-url ${6} \
        --max-post-age ${7}

elif [ "${1}" == "tweet-spreadsheet-schedule" ]; then
    agoras publish
        --network twitter \
        --action schedule \
        --twitter-consumer-key ${2} \
        --twitter-consumer-secret ${3} \
        --twitter-oauth-token ${4} \
        --twitter-oauth-secret ${5} \
        --google-sheets-id ${6} \
        --google-sheets-client-email ${7} \
        --google-sheets-private-key ${8}

else
    tail -f /dev/null
fi
