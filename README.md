![](https://raw.githubusercontent.com/LuisAlejandro/agoras-actions/develop/branding/banner.svg)

---

Current version: 2.0.5

> **Breaking change:** Version 2.0 aligns with [Agoras 2.0](https://agoras.luisalejandro.org/en/latest/migration.html). Input names, authentication, and CLI routing changed. See [docs/MIGRATION-v2.md](docs/MIGRATION-v2.md) before upgrading from 1.x. Each agoras-actions release pins the matching Agoras PyPI version (e.g. `@2.0.5` uses `agoras==2.0.5`).

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
      - uses: LuisAlejandro/agoras-actions@2.0.5
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
- uses: LuisAlejandro/agoras-actions@2.0.5
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
make build
```

The root `Dockerfile` powers day-to-day development (`make image`, `make start`, `make lint`, `make test`).

## Outputs

The `result` output contains comma-separated post IDs from publish, like, share, or delete operations.

```yml
- uses: LuisAlejandro/agoras-actions@2.0.5
  id: agoras
  with:
    network: linkedin
    action: post
    text: Test post
    linkedin-client-id: ${{ secrets.LI_CLIENT_ID }}
    linkedin-client-secret: ${{ secrets.LI_CLIENT_SECRET }}
    linkedin-refresh-token: ${{ secrets.LI_REFRESH_TOKEN }}
    linkedin-object-id: ${{ secrets.LI_OBJECT_ID }}
- uses: LuisAlejandro/agoras-actions@2.0.5
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

* `network` — Platform for social actions: `x`, `facebook`, … (`twitter` maps to `x`). Optional when `action` is `refresh-credentials`.
* `action` — `post`, `like`, `share`, `delete`, `video`, `template`, `refresh-credentials`
* `github-secret-update-token`, `platforms`, `*-refresh-token-secret-name` — see [Credential refresh](#credential-refresh-github-secrets)

### Content

* `text`, `link`, `image-1` … `image-4`, `post-id`, `profile-id`
* `video-url`, `video-title`, `video-description`, `video-type`, `video-caption`
* `title`, `description`, `category-id`, `privacy`, `keywords`

### Platform credentials

Prefixed inputs per platform (e.g. `x-consumer-key`, `facebook-client-id`, `facebook-refresh-token`). The action maps these to Agoras environment variables internally (e.g. `FACEBOOK_CLIENT_ID`, `TWITTER_CONSUMER_KEY`). See [action.yml](action.yml) and [Platform arguments and env vars](https://agoras.luisalejandro.org/en/latest/reference/platform-arguments-envvars.html) for the full list.

> [!TIP]
> Standard LinkedIn apps usually return a 60-day access token and no refresh token. For standard apps, use `linkedin-access-token` instead of `linkedin-refresh-token`.

`authorize`, `last-from-feed`, `random-from-feed`, and `schedule` are **not** supported by this action. Run `agoras <network> authorize` or `agoras utils …` locally when you need those flows.

## Examples

### LinkedIn post with link preview

```yml
on:
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@2.0.5
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

## Credential refresh (GitHub secrets)

OAuth providers may rotate long-lived refresh tokens. Use the standalone `refresh-credentials` action on a schedule (or `workflow_dispatch`) to refresh tokens and write rotated values back to **your** repository secrets.

**Requirements**

* A PAT or GitHub App installation token with **repository secrets write** permission (`AGORAS_SECRET_UPDATE_TOKEN` or any secret you map to `github-secret-update-token`).
* Per-platform `*-refresh-token-secret-name` inputs that name the GitHub secret to update (arbitrary names — they do not have to match action input names).
* Full unattended credentials for each platform (same inputs as posting, e.g. `facebook-client-id`, `facebook-refresh-token`, …).

**Limitations**

* Updated secrets apply to **future** workflow runs only; the same job cannot read newly written secrets.
* Repository secrets only (not org/environment secrets in v1).
* Supports YouTube, Facebook, Instagram, LinkedIn, TikTok, and Threads. X, Discord, Telegram, and WhatsApp are out of scope.

**Example (scheduled refresh)**

```yml
name: Refresh social OAuth tokens
on:
  schedule:
    - cron: '0 6 * * 1'
  workflow_dispatch:

concurrency:
  group: refresh-oauth-tokens
  cancel-in-progress: false

jobs:
  refresh:
    runs-on: ubuntu-22.04
    steps:
      - uses: LuisAlejandro/agoras-actions@2.0.5
        with:
          action: refresh-credentials
          github-secret-update-token: ${{ secrets.AGORAS_SECRET_UPDATE_TOKEN }}
          facebook-client-id: ${{ secrets.FB_CLIENT_ID }}
          facebook-client-secret: ${{ secrets.FB_CLIENT_SECRET }}
          facebook-refresh-token: ${{ secrets.FB_REFRESH_TOKEN }}
          facebook-object-id: ${{ secrets.FB_PAGE_ID }}
          facebook-refresh-token-secret-name: FB_REFRESH_TOKEN
```

Use `platforms: facebook,linkedin` to limit which platforms run. Optional `network` adds another filter when set.

**Security:** Restrict this workflow to `schedule` / `workflow_dispatch` on your default branch. Do not run secret-write steps on fork PRs. If OAuth refresh succeeds but GitHub write fails, update the secret manually before the next post.

## Made with 💖 and 🍔

![Banner](https://raw.githubusercontent.com/LuisAlejandro/LuisAlejandro/master/images/author-banner.svg)

> Web [luisalejandro.org](http://luisalejandro.org/) · GitHub [@LuisAlejandro](https://github.com/LuisAlejandro) · X [@LuisAlejandro](https://twitter.com/LuisAlejandro)
