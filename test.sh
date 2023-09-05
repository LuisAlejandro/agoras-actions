source secrets.env

python3 docker/execute.py \
    network="twitter" \
    action="post" \
    status-text="${STATUS_TEXT}" \
    status-link="${STATUS_LINK}" \
    status-image-url-1="${STATUS_IMAGE_URL_1}" \
    status-image-url-2="${STATUS_IMAGE_URL_2}" \
    status-image-url-3="${STATUS_IMAGE_URL_3}" \
    status-image-url-4="${STATUS_IMAGE_URL_4}" \
    tweet-id="${TWEET_ID}" \
    facebook-post-id="${FACEBOOK_POST_ID}" \
    linkedin-post-id="${LINKEDIN_POST_ID}" \
    instagram-post-id="${INSTAGRAM_POST_ID}" \
    feed-url="${FEED_URL}" \
    max-count="${MAX_COUNT}" \
    post-lookback="${POST_LOOKBACK}" \
    max-post-age="${MAX_POST_AGE}" \
    twitter-consumer-key="${TWITTER_CONSUMER_KEY}" \
    twitter-consumer-secret="${TWITTER_CONSUMER_SECRET}" \
    twitter-oauth-token="${TWITTER_OAUTH_TOKEN}" \
    twitter-oauth-secret="${TWITTER_OAUTH_SECRET}" \
    facebook-access-token="${FACEBOOK_ACCESS_TOKEN}" \
    facebook-object-id="${FACEBOOK_OBJECT_ID}" \
    facebook-profile-id="${FACEBOOK_PROFILE_ID}" \
    instagram-access-token="${INSTAGRAM_ACCESS_TOKEN}" \
    instagram-object-id="${INSTAGRAM_OBJECT_ID}" \
    linkedin-access-token="${LINKEDIN_ACCESS_TOKEN}" \
    google-sheets-client-email="${GOOGLE_SHEETS_CLIENT_EMAIL}" \
    google-sheets-private-key="${GOOGLE_SHEETS_PRIVATE_KEY}" \
    google-sheets-id="${GOOGLE_SHEETS_ID}" \
    google-sheets-name="${GOOGLE_SHEETS_NAME}"