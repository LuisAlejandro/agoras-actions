![](https://raw.githubusercontent.com/LuisAlejandro/agoras-actions/develop/branding/banner.svg)

---

Current version: 2.0.1

> **Breaking change:** Version 2.0 aligns with [Agoras 2.0](https://agoras.luisalejandro.org/en/latest/migration.html). Input names, authentication, and CLI routing changed. See [docs/MIGRATION-v2.md](docs/MIGRATION-v2.md) before upgrading from 1.x. Each agoras-actions release pins the matching Agoras PyPI version (e.g. `@2.0.1` uses `agoras==2.0.1`).

Agoras is a Python utility for publishing and managing posts on social networks (X, Facebook, Instagram, LinkedIn, Discord, YouTube, TikTok, Threads, Telegram, and WhatsApp).

This repository wraps Agoras as a GitHub Action for use in workflows.

## Usage

The action is `LuisAlejandro/agoras-actions`. Required inputs are `network` and `action`. Other inputs depend on the platform and action.

### Post to Facebook (OAuth unattended)

```yml
name: Publish post to Facebook
on:
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@2.0.1
        with:
          network: facebook
          action: post
          text: This is a test post
          image-1: https://placekitten.com/200/300
          facebook-client-id: ${{ secrets.FB_CLIENT_ID }}
          facebook-client-secret: ${{ secrets.FB_CLIENT_SECRET }}
          facebook-refresh-token: ${{ secrets.FB_REFRESH_TOKEN }}
          facebook-object-id: ${{ secrets.FB_PAGE_ID }}
```

### Post to X

```yml
- uses: LuisAlejandro/agoras-actions@2.0.1
  with:
    network: x
    action: post
    text: Hello from GitHub Actions
    x-consumer-key: ${{ secrets.X_CONSUMER_KEY }}
    x-consumer-secret: ${{ secrets.X_CONSUMER_SECRET }}
    x-oauth-token: ${{ secrets.X_OAUTH_TOKEN }}
    x-oauth-secret: ${{ secrets.X_OAUTH_SECRET }}
```

Documentation:

* [Agoras documentation](https://agoras.luisalejandro.org/)
* [Agoras migration guide](https://agoras.luisalejandro.org/en/latest/migration.html)
* [agoras-actions v2 migration](docs/MIGRATION-v2.md)
* [Platform arguments and env vars](https://agoras.luisalejandro.org/en/latest/reference/platform-arguments-envvars.html)
* [Contributing](CONTRIBUTING.md)

## Local development

Build and start the development container:

```bash
make image
make start
```

Run quality checks (release preflight uses the same targets):

```bash
make lint
make format
make test
```

Open a shell in the container:

```bash
make console
```

Copy `.env.example` to `secrets.env` and fill in credentials for `make functional-test` when exercising live APIs.

### Building the Docker image locally

Build the GitHub Action runtime image (from `docker/Dockerfile`):

```bash
make docker-image
```

The root `Dockerfile` powers day-to-day development (`make image`, `make start`, `make lint`, `make test`).

## Outputs

The `result` output contains comma-separated post IDs from publish, like, share, or delete operations.

```yml
- uses: LuisAlejandro/agoras-actions@2.0.1
  id: agoras
  with:
    network: linkedin
    action: post
    text: Test post
    linkedin-client-id: ${{ secrets.LI_CLIENT_ID }}
    linkedin-client-secret: ${{ secrets.LI_CLIENT_SECRET }}
    linkedin-refresh-token: ${{ secrets.LI_REFRESH_TOKEN }}
    linkedin-object-id: ${{ secrets.LI_OBJECT_ID }}
- uses: LuisAlejandro/agoras-actions@2.0.1
  with:
    network: linkedin
    action: like
    post-id: ${{ steps.agoras.outputs.result }}
    linkedin-client-id: ${{ secrets.LI_CLIENT_ID }}
    linkedin-client-secret: ${{ secrets.LI_CLIENT_SECRET }}
    linkedin-refresh-token: ${{ secrets.LI_REFRESH_TOKEN }}
    linkedin-object-id: ${{ secrets.LI_OBJECT_ID }}
```

## Inputs

### Control

* `network` — Platform: `x`, `facebook`, `instagram`, `linkedin`, `discord`, `youtube`, `tiktok`, `threads`, `telegram`, `whatsapp` (`twitter` maps to `x`)
* `action` — `post`, `like`, `share`, `delete`, `video`, `authorize`, `template`, `last-from-feed`, `random-from-feed`, `schedule`

### Content

* `text`, `link`, `image-1` … `image-4`, `post-id`, `profile-id`
* `video-url`, `video-title`, `video-description`, `video-type`, `video-caption`
* `title`, `description`, `category-id`, `privacy`, `keywords`

### Feed and schedule

* `feed-url`, `max-count`, `post-lookback`, `max-post-age`
* `sheets-id`, `sheets-name`, `sheets-client-email`, `sheets-private-key`

### Platform credentials

Prefixed inputs per platform (e.g. `x-consumer-key`, `facebook-client-id`, `facebook-refresh-token`). See [action.yml](action.yml) and [docs/MIGRATION-v2.md](docs/MIGRATION-v2.md) for the full list.

## Examples

### LinkedIn post with link preview

```yml
on:
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@2.0.1
        with:
          network: linkedin
          action: post
          text: New blog post
          link: https://luisalejandro.org/blog
          linkedin-client-id: ${{ secrets.LI_CLIENT_ID }}
          linkedin-client-secret: ${{ secrets.LI_CLIENT_SECRET }}
          linkedin-refresh-token: ${{ secrets.LI_REFRESH_TOKEN }}
          linkedin-object-id: ${{ secrets.LI_OBJECT_ID }}
```

### Feed publish (cron)

```yml
on:
  schedule:
    - cron: '0 * * * *'
jobs:
  feed:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@2.0.1
        with:
          network: x
          action: last-from-feed
          feed-url: https://example.com/feed.xml
          max-count: 1
          post-lookback: 3600
          x-consumer-key: ${{ secrets.X_CONSUMER_KEY }}
          x-consumer-secret: ${{ secrets.X_CONSUMER_SECRET }}
          x-oauth-token: ${{ secrets.X_OAUTH_TOKEN }}
          x-oauth-secret: ${{ secrets.X_OAUTH_SECRET }}
```

## Made with 💖 and 🍔

![Banner](https://raw.githubusercontent.com/LuisAlejandro/LuisAlejandro/master/images/author-banner.svg)

> Web [luisalejandro.org](http://luisalejandro.org/) · GitHub [@LuisAlejandro](https://github.com/LuisAlejandro) · X [@LuisAlejandro](https://twitter.com/LuisAlejandro)
