![](https://raw.githubusercontent.com/LuisAlejandro/agoras-actions/develop/branding/banner.svg)

---

Current version: 1.1.1

Agoras is a python utility that helps publish and delete posts on the most popular social networks (twitter, facebook, instagram and linkedin).

This repository contains the source code for the Agoras github actions. Its purpose is to serve as a wrapper for the application and provide a simple way to use it in your workflows.

## Usage

The name of the action is `LuisAlejandro/agoras-actions`, and it accepts inputs as parameters. The inputs that you'll need to provide depend on the action you want to execute. For example, to publish a post to facebook, you'll need to provide the access token for your facebook app, the page ID (object ID) where you want to publish the post, the text and the image URL. The full workflow file would look like this:

```yml
name: Publish post to facebook
on:
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@1.1.1
        with:
          network: facebook
          action: post
          status-text: This is a test post
          status-image-url-1: https://placekitten.com/200/300
          facebook-access-token: ZCNqH3bT0as2ZBB...
          facebook-object-id: 8974765243478...
```

The inputs are named after the command line arguments of the Agoras application. You can read more about how to use the application (and subsequently, this action) in the following links:

* [General usage](https://agoras.readthedocs.io/en/latest/usage.html)
* [Using Agoras with Twitter](https://agoras.readthedocs.io/en/latest/twitter.html)
* [Using Agoras with Facebook](https://agoras.readthedocs.io/en/latest/facebook.html)
* [Using Agoras with Instagram](https://agoras.readthedocs.io/en/latest/instagram.html)
* [Using Agoras with LinkedIn](https://agoras.readthedocs.io/en/latest/linkedin.html)

Also, You can find a list of all the available inputs for each action in the [Inputs](#-inputs) section.

## Outputs

This action has one output named `result` that contains the IDs of the posts that were published, liked, shared or deleted. An operation can result in one ID or multiple IDs. Multiple IDs are separated by a comma. An example of an operation that yields multiple IDs would be when publishing with actions `last-from-feed` or `schedule` and `max-count` is set to an integer greater than 1.

To use the output, asign an `id` to the step where you are publishing and then reference the output in the step where you need the IDs like this `${{ steps.your-id-name.outputs.result }}`. An example of how to use the output would be:

```yml
name: Publish post to linkedin and then like it
on:
  workflow_dispatch:
jobs:
  publish-like:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@1.1.1
        id: agoras
        with:
          network: linkedin
          action: post
          status-text: This is a test post
          linkedin-access-token: ZCNqH3bT0as2ZBB...
      - uses: LuisAlejandro/agoras-actions@1.1.1
        with:
          network: linkedin
          action: like
          linkedin-post-id: ${{ steps.agoras.outputs.result }}
          linkedin-access-token: ZCNqH3bT0as2ZBB...
```

## Inputs

* `network`: Social network to use for publishing. Must be one of twitter, facebook, instagram or linkedin.
* `action`: Action to execute. Must be one of like, share, last-from-feed, random-from-feed, schedule, post, delete.
* `twitter-consumer-key`: Twitter consumer key from twitter developer app.
* `twitter-consumer-secret`: Twitter consumer secret from twitter developer app.
* `twitter-oauth-token`: Twitter OAuth token from twitter developer app.
* `twitter-oauth-secret`: Twitter OAuth secret from twitter developer app.
* `tweet-id`: Twitter post ID to like, share or delete.
* `facebook-access-token`: Facebook access token from facebook app.
* `facebook-object-id`: Facebook ID of object where the post is going to be published.
* `facebook-post-id`: Facebook ID of post to be liked, shared or deleted.
* `facebook-profile-id`: Facebook ID of profile where a post will be shared.
* `instagram-access-token`: Facebook access token from facebook app.
* `instagram-object-id`: Instagram ID of profile where the post is going to be published.
* `instagram-post-id`: Instagram ID of post to be liked, shared or deleted.
* `linkedin-access-token`: Your LinkedIn access token.
* `linkedin-post-id`: LinkedIn post ID to like, share or delete.
* `status-text`: Text to be published.
* `status-image-url-1`: First image URL to be published.
* `status-image-url-2`: Second image URL to be published.
* `status-image-url-3`: Third image URL to be published.
* `status-image-url-4`: Fourth image URL to be published.
* `feed-url`: URL of public Atom feed to be parsed.
* `max-count`: Max number of new posts to be published at once.
* `post-lookback`: Only allow posts published
* `max-post-age`: Dont allow publishing of posts older than this number of days.
* `google-sheets-client-email`: A google console project client email corresponding to the private key.
* `google-sheets-private-key`: A google console project private key.
* `google-sheets-id`: The google sheets ID to read schedule entries.
* `google-sheets-name`: The name of the sheet where the schedule is.

## Made with 💖 and 🍔

![Banner](https://raw.githubusercontent.com/LuisAlejandro/LuisAlejandro/master/images/author-banner.svg)

> Web [luisalejandro.org](http://luisalejandro.org/) · GitHub [@LuisAlejandro](https://github.com/LuisAlejandro) · Twitter [@LuisAlejandro](https://twitter.com/LuisAlejandro)
