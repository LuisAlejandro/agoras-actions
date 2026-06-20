source secrets.env

python3 docker/execute.py \
    network="x" \
    action="post" \
    text="${STATUS_TEXT}" \
    link="${STATUS_LINK}" \
    image-1="${STATUS_IMAGE_URL_1}" \
    image-2="${STATUS_IMAGE_URL_2}" \
    image-3="${STATUS_IMAGE_URL_3}" \
    image-4="${STATUS_IMAGE_URL_4}" \
    post-id="${TWEET_ID}" \
    feed-url="${FEED_URL}" \
    max-count="${MAX_COUNT}" \
    post-lookback="${POST_LOOKBACK}" \
    max-post-age="${MAX_POST_AGE}" \
    x-consumer-key="${TWITTER_CONSUMER_KEY}" \
    x-consumer-secret="${TWITTER_CONSUMER_SECRET}" \
    x-oauth-token="${TWITTER_OAUTH_TOKEN}" \
    x-oauth-secret="${TWITTER_OAUTH_SECRET}" \
    facebook-client-id="${FACEBOOK_CLIENT_ID}" \
    facebook-client-secret="${FACEBOOK_CLIENT_SECRET}" \
    facebook-refresh-token="${FACEBOOK_REFRESH_TOKEN}" \
    facebook-object-id="${FACEBOOK_OBJECT_ID}" \
    facebook-profile-id="${FACEBOOK_PROFILE_ID}" \
    instagram-client-id="${INSTAGRAM_CLIENT_ID}" \
    instagram-client-secret="${INSTAGRAM_CLIENT_SECRET}" \
    instagram-refresh-token="${INSTAGRAM_REFRESH_TOKEN}" \
    instagram-object-id="${INSTAGRAM_OBJECT_ID}" \
    linkedin-client-id="${LINKEDIN_CLIENT_ID}" \
    linkedin-client-secret="${LINKEDIN_CLIENT_SECRET}" \
    linkedin-refresh-token="${LINKEDIN_REFRESH_TOKEN}" \
    linkedin-object-id="${LINKEDIN_OBJECT_ID}" \
    sheets-client-email="${GOOGLE_SHEETS_CLIENT_EMAIL}" \
    sheets-private-key="${GOOGLE_SHEETS_PRIVATE_KEY}" \
    sheets-id="${GOOGLE_SHEETS_ID}" \
    sheets-name="${GOOGLE_SHEETS_NAME}"
