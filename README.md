![](https://raw.githubusercontent.com/LuisAlejandro/agoras-actions/develop/branding/banner.svg)

---

Current version: 0.1.0

## Table of contents

* [Twitter Actions](#twitter-actions)

  * [New Twitter post](#new-twitter-post)
  * [Like Twitter post](#like-twitter-post)
  * [Share Twitter post](#share-twitter-post)
  * [Delete Twitter post](#delete-twitter-post)
  * [Last Twitter post from feed](#last-twitter-post-from-feed)
  * [Random Twitter post from feed](#random-twitter-post-from-feed)
  * [Schedule Twitter posts](#schedule-twitter-posts)

* [Facebook Actions](#facebook-actions)

  * [New Facebook post](#new-facebook-post)
  * [Like Facebook post](#like-facebook-post)
  * [Share Facebook post](#share-facebook-post)
  * [Delete Facebook post](#delete-facebook-post)
  * [Last Facebook post from feed](#last-facebook-post-from-feed)
  * [Random Facebook post from feed](#random-facebook-post-from-feed)
  * [Schedule Facebook posts](#schedule-facebook-posts)

* [Instagram Actions](#instagram-actions)

  * [New Instagram post](#new-instagram-post)
  * [Like Instagram post](#like-instagram-post)
  * [Share Instagram post](#share-instagram-post)
  * [Delete Instagram post](#delete-instagram-post)
  * [Last Instagram post from feed](#last-instagram-post-from-feed)
  * [Random Instagram post from feed](#random-instagram-post-from-feed)
  * [Schedule Instagram posts](#schedule-instagram-posts)

* [LinkedIn Actions](#linkedin-actions)
  * [New LinkedIn post](#new-linkedin-post)
  * [Like LinkedIn post](#like-linkedin-post)
  * [Share LinkedIn post](#share-linkedin-post)
  * [Delete LinkedIn post](#delete-linkedin-post)
  * [Last LinkedIn post from feed](#last-linkedin-post-from-feed)
  * [Random LinkedIn post from feed](#random-linkedin-post-from-feed)
  * [Schedule LinkedIn posts](#schedule-linkedin-posts)

## Actions

### Twitter actions

#### New Twitter post

#### Like Twitter post

#### Share Twitter post

#### Delete Twitter post

#### Last Twitter post from feed

#### Random Twitter post from feed

#### Schedule Twitter posts

### Facebook actions

#### New Facebook post

#### Like Facebook post

#### Share Facebook post

#### Delete Facebook post

#### Last Facebook post from feed

##### 🎒 Prep Work

1. Get a facebook permanent access token (explained [here](docs/facebook.rst)) using a facebook account that owns the page where you want to post messages.
2. Find the ID of the page that you want to post messages in (explained [here](docs/facebook.rst)).
3. Find the atom feed URL that contains the posts that you wish to share.

##### 🖥 Workflow Usage

Configure your workflow to use `LuisAlejandro/agoras-actions/lastfb-post-from-feed@0.1.0`,
and provide the atom feed URL you want to use as the `FEED_URL` env variable.

Provide the access token for your Facebook app as the
`FACEBOOK_ACCESS_TOKEN` env variable, set your facebook page ID as
`FACEBOOK_PAGE_ID` (as secrets). Remember, to add secrets go to your repository
`Settings` > `Secrets` > `Actions` > `New repository secret`
for each secret.

For example, create a file `.github/workflows/schedule.yml` on
a github repository with the following content:

```yml
name: Publish last post of feed hourly
on:
  schedule:
    - cron: '0 * * * *'
jobs:
  fbpost:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions/last-fb-post-from-feed@0.1.0
        env:
          FACEBOOK_ACCESS_TOKEN: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
          FACEBOOK_PAGE_ID: ${{ secrets.FACEBOOK_PAGE_ID }}
          FEED_URL: ${{ secrets.FEED_URL }}
```

Publish your changes, activate your actions if disabled and enjoy.

##### ❗ Important notes

* The action is designed to publish a maximum of 1 post per batch, regardless of the actual
number of new posts since the last run. You can alter this behavior by setting a `MAX_COUNT` env
variable with your new value.
* For this action to work properly, it should be run with an hourly cron (`0 * * * *`).
The script is designed to look back and publish all posts (set by `MAX_COUNT`)
since the **last hour**. If you want to change the frecuency of execution, modify the cron
expression and then set a `POST_LOOKBACK` env variable with the cron interval in seconds. For example,
for a `*/5 * * * *` cron (every 5 min), set env `POST_LOOKBACK: 300`.

#### Random Facebook post from feed

#### Schedule Facebook posts

### Instagram actions

#### New Instagram post

#### Like Instagram post

#### Share Instagram post

#### Delete Instagram post

#### Last Instagram post from feed

#### Random Instagram post from feed

#### Schedule Instagram posts

### LinkedIn actions

#### New LinkedIn post

#### Like LinkedIn post

#### Share LinkedIn post

#### Delete LinkedIn post

#### Last LinkedIn post from feed

#### Random LinkedIn post from feed

#### Schedule LinkedIn posts

## Made with 💖 and 🍔

![Banner](https://raw.githubusercontent.com/LuisAlejandro/LuisAlejandro/master/images/author-banner.svg)

> Web [luisalejandro.org](http://luisalejandro.org/) · GitHub [@LuisAlejandro](https://github.com/LuisAlejandro) · Twitter [@LuisAlejandro](https://twitter.com/LuisAlejandro)
