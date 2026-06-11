![](https://raw.githubusercontent.com/LuisAlejandro/agoras-actions/develop/branding/banner.svg)

---

Current version: 1.1.3

**Agoras Actions** is a [GitHub Action](https://github.com/features/actions) that wraps the [Agoras](https://github.com/LuisAlejandro/agoras) CLI. Use it in workflows to publish, schedule, like, share, and delete posts on Twitter, Facebook, Instagram, and LinkedIn without installing Agoras on the runner.

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development and contribution guidelines. Release history is in [HISTORY.md](HISTORY.md).

## Usage

The action name is `LuisAlejandro/agoras-actions`. Pass Agoras CLI options as action inputs (kebab-case in workflows, matching `action.yml`).

Example: publish a post to Facebook:

```yml
name: Publish post to facebook
on:
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@1.1.3
        with:
          network: facebook
          action: post
          status-text: This is a test post
          status-image-url-1: https://placekitten.com/200/300
          facebook-access-token: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
          facebook-object-id: ${{ secrets.FACEBOOK_OBJECT_ID }}
```

Inputs mirror Agoras command-line arguments. See the Agoras docs for network-specific behavior:

- [General usage](https://agoras.readthedocs.io/en/latest/usage.html)
- [Twitter](https://agoras.readthedocs.io/en/latest/twitter.html)
- [Facebook](https://agoras.readthedocs.io/en/latest/facebook.html)
- [Instagram](https://agoras.readthedocs.io/en/latest/instagram.html)
- [LinkedIn](https://agoras.readthedocs.io/en/latest/linkedin.html)

All inputs are listed in [Inputs](#inputs) below and in [`action.yml`](action.yml).

## Outputs

The action exposes one output, `result`, containing post IDs from publish, like, share, or delete operations. One operation may return multiple IDs (comma-separated), for example when using `last-from-feed` or `schedule` with `max-count` greater than 1.

Assign an `id` to the step and reference the output in a later step:

```yml
name: Publish post to linkedin and then like it
on:
  workflow_dispatch:
jobs:
  publish-like:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@1.1.3
        id: agoras
        with:
          network: linkedin
          action: post
          status-text: This is a test post
          linkedin-access-token: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
      - uses: LuisAlejandro/agoras-actions@1.1.3
        with:
          network: linkedin
          action: like
          linkedin-post-id: ${{ steps.agoras.outputs.result }}
          linkedin-access-token: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
```

## Inputs

| Input | Description |
|-------|-------------|
| `network` | Social network: `twitter`, `facebook`, `instagram`, or `linkedin`. |
| `action` | Operation: `like`, `share`, `last-from-feed`, `random-from-feed`, `schedule`, `post`, or `delete`. |
| `status-text` | Text to publish. |
| `status-link` | Link to publish (embeds URL preview where supported). |
| `status-image-url-1` … `status-image-url-4` | Image URLs to attach. |
| `feed-url` | Public Atom feed URL for feed-driven actions. |
| `max-count` | Maximum new posts to publish in one run. |
| `post-lookback` | Only allow posts published within this window (seconds). |
| `max-post-age` | Do not publish posts older than this many days. |
| `twitter-consumer-key` / `twitter-consumer-secret` | Twitter app credentials. |
| `twitter-oauth-token` / `twitter-oauth-secret` | Twitter user OAuth credentials. |
| `tweet-id` | Twitter post ID for like, share, or delete. |
| `facebook-access-token` | Facebook app access token. |
| `facebook-object-id` | Facebook page or object ID for publishing. |
| `facebook-post-id` | Facebook post ID for like, share, or delete. |
| `facebook-profile-id` | Facebook profile ID when sharing to a profile. |
| `instagram-access-token` | Instagram (Facebook app) access token. |
| `instagram-object-id` | Instagram profile ID for publishing. |
| `instagram-post-id` | Instagram post ID for like, share, or delete. |
| `linkedin-access-token` | LinkedIn access token. |
| `linkedin-post-id` | LinkedIn post ID for like, share, or delete. |
| `google-sheets-client-email` | Google service account email for schedule action. |
| `google-sheets-private-key` | Google service account private key. |
| `google-sheets-id` | Spreadsheet ID for schedule entries. |
| `google-sheets-name` | Sheet name containing the schedule. |

## Examples

Publish to LinkedIn with a link preview:

```yml
on:
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@1.1.3
        with:
          network: linkedin
          action: post
          status-text: This is a test post
          status-link: https://luisalejandro.org/blog/posts/nuevo-blog
          linkedin-access-token: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
```

Publish to Facebook with multiple images:

```yml
on:
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@1.1.3
        with:
          network: facebook
          action: post
          status-text: This is a test post
          status-image-url-1: https://pbs.twimg.com/media/Ej3d42zXsAEfDCr?format=jpg
          status-image-url-2: https://pbs.twimg.com/media/Ej3d42zXsAEfDCr?format=jpg
          status-image-url-3: https://pbs.twimg.com/media/Ej3d42zXsAEfDCr?format=jpg
          status-image-url-4: https://pbs.twimg.com/media/Ej3d42zXsAEfDCr?format=jpg
          facebook-access-token: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
          facebook-object-id: ${{ secrets.FACEBOOK_OBJECT_ID }}
```

Publish the latest feed item to Facebook on a schedule:

```yml
on:
  schedule:
    - cron: 0 * * * *
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@1.1.3
        with:
          network: facebook
          action: last-from-feed
          feed-url: https://luisalejandro.org/blog/posts/feed.xml
          max-count: 1
          post-lookback: 3600
          facebook-access-token: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
          facebook-object-id: ${{ secrets.FACEBOOK_OBJECT_ID }}
```

## Local development

Integration tests run Agoras inside Docker against credentials in `secrets.env`:

```bash
make image
make start
cp .env.example secrets.env   # edit with test credentials
make functional-test
```

Use `make console` for an interactive shell in the container. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contributor workflow.

## Made with 💖 and 🍔

![Banner](https://raw.githubusercontent.com/LuisAlejandro/LuisAlejandro/master/images/author-banner.svg)

> Web [luisalejandro.org](http://luisalejandro.org/) · GitHub [@LuisAlejandro](https://github.com/LuisAlejandro) · Twitter [@LuisAlejandro](https://twitter.com/LuisAlejandro)
