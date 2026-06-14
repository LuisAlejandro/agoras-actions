# Agoras 2.0 → agoras-actions 2.0 Migration Guide

## Executive summary

agoras-actions **2.0.0** is a **breaking release** aligned with [Agoras 2.0](https://docs.agoras.io/migration). The action no longer calls the legacy `agoras publish` command. It routes to native Agoras 2.0 CLI commands:

- **Platform actions:** `agoras <platform> <action>` (e.g. `agoras x post`)
- **Feed automation:** `agoras utils feed-publish`
- **Scheduling:** `agoras utils schedule-run`

Input names changed to match v2 CLI flags. OAuth platforms no longer accept direct access-token inputs (`facebook-access-token` was removed in Agoras 2.0).

---

## Feature catalog (new in v2)

### New platforms

| Platform | Actions |
|----------|---------|
| **x** (formerly twitter) | authorize, post, video, like, share, delete |
| **facebook** | authorize, post, video, like, share, delete |
| **instagram** | authorize, post, video |
| **linkedin** | authorize, post, video, like, share, delete |
| **discord** | authorize, post, video, delete |
| **youtube** | authorize, video, like, delete |
| **tiktok** | authorize, post, video |
| **threads** | authorize, post, video, share |
| **telegram** | authorize, post, video, delete |
| **whatsapp** | authorize, post, video, template |

### New actions exposed by agoras-actions

| Action | CLI target | Notes |
|--------|------------|-------|
| `video` | `<platform> video` | All video-capable platforms |
| `authorize` | `<platform> authorize` | Interactive OAuth; limited use in GHA |
| `template` | `whatsapp template` | WhatsApp only |

### Unchanged automation actions (new CLI routing)

| GHA `action` | Agoras 2.0 CLI |
|--------------|----------------|
| `last-from-feed` | `agoras utils feed-publish --mode last` |
| `random-from-feed` | `agoras utils feed-publish --mode random` |
| `schedule` | `agoras utils schedule-run` |

### Packaging (Agoras 2.0)

Agoras 2.0 splits into five PyPI packages (`agoras-common`, `agoras-media`, `agoras-core`, `agoras-platforms`, `agoras`). The Docker image installs the `agoras` meta-package. Python **3.10+** required (3.9 dropped).

---

## Deprecation catalog

| v1.1.3 item | v2 status | agoras-actions 2.0 |
|-------------|-----------|-------------------|
| `agoras publish` | Deprecated in Agoras (removed in v3.0) | **Removed** from `execute.py` |
| `network: twitter` | Deprecated → `x` | Accepted; mapped to `x` internally |
| `twitter-consumer-key` etc. | → `x-consumer-key` / `--consumer-key` | Renamed inputs |
| `status-text`, `status-link`, `status-image-url-N` | → `text`, `link`, `image-N` | Renamed inputs |
| `tweet-id`, `facebook-post-id`, etc. | → unified `post-id` | Single `post-id` input |
| `facebook-access-token` | **Removed** in Agoras 2.0 | **Removed**; use OAuth refresh token |
| `instagram-access-token` | **Removed** | **Removed**; use OAuth refresh token |
| `linkedin-access-token` | **Removed** | **Removed**; use OAuth refresh token |
| `google-sheets-*` | → `sheets-*` in CLI | Renamed to `sheets-*` (legacy names still mapped in `execute.py`) |

---

## Gap matrix (v1.1.3 → v2.0)

| Area | v1.1.3 | v2.0 |
|------|--------|------|
| CLI entry | `publish --network --action` | Platform or utils subcommands |
| Networks | 4 | 10 (+ twitter alias) |
| Auth (Facebook) | `facebook-access-token` | `facebook-client-id`, `facebook-client-secret`, `facebook-refresh-token`, `facebook-object-id` |
| Content params | `status-text` | `text` |
| Post IDs | Per-network (`tweet-id`, etc.) | Unified `post-id` |
| Output | `jq -r '.id'` | Unchanged (`{"id":"..."}` JSON lines) |
| Docker agoras pin | `agoras==1.1.3` | Bundled from `agoras` BuildKit context at build time; PyPI pin when 2.0 ships |

---

## User migration guide

### X post (was Twitter)

**Before (1.1.3):**

```yaml
- uses: LuisAlejandro/agoras-actions@1.1.3
  with:
    network: twitter
    action: post
    status-text: Hello!
    twitter-consumer-key: ${{ secrets.X_CONSUMER_KEY }}
    twitter-consumer-secret: ${{ secrets.X_CONSUMER_SECRET }}
    twitter-oauth-token: ${{ secrets.X_OAUTH_TOKEN }}
    twitter-oauth-secret: ${{ secrets.X_OAUTH_SECRET }}
```

**After (2.0.0):**

```yaml
- uses: LuisAlejandro/agoras-actions@2.0.0
  with:
    network: x
    action: post
    text: Hello!
    x-consumer-key: ${{ secrets.X_CONSUMER_KEY }}
    x-consumer-secret: ${{ secrets.X_CONSUMER_SECRET }}
    x-oauth-token: ${{ secrets.X_OAUTH_TOKEN }}
    x-oauth-secret: ${{ secrets.X_OAUTH_SECRET }}
```

### Facebook post (OAuth unattended)

**Before:**

```yaml
- uses: LuisAlejandro/agoras-actions@1.1.3
  with:
    network: facebook
    action: post
    status-text: Deployed!
    facebook-access-token: ${{ secrets.FB_TOKEN }}
    facebook-object-id: ${{ secrets.FB_PAGE_ID }}
```

**After:**

```yaml
- uses: LuisAlejandro/agoras-actions@2.0.0
  with:
    network: facebook
    action: post
    text: Deployed!
    facebook-client-id: ${{ secrets.FB_CLIENT_ID }}
    facebook-client-secret: ${{ secrets.FB_CLIENT_SECRET }}
    facebook-refresh-token: ${{ secrets.FB_REFRESH_TOKEN }}
    facebook-object-id: ${{ secrets.FB_PAGE_ID }}
```

### Feed publish

```yaml
- uses: LuisAlejandro/agoras-actions@2.0.0
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

### Schedule run

```yaml
- uses: LuisAlejandro/agoras-actions@2.0.0
  with:
    network: ''
    action: schedule
    sheets-id: ${{ secrets.SHEETS_ID }}
    sheets-name: Schedule
    sheets-client-email: ${{ secrets.SHEETS_CLIENT_EMAIL }}
    sheets-private-key: ${{ secrets.SHEETS_PRIVATE_KEY }}
```

---

## Input reference (GHA input → CLI flag → env var)

### Common content

| GHA input | Platform CLI | Env var |
|-----------|--------------|---------|
| `text` | `--text` | `STATUS_TEXT` |
| `link` | `--link` | `STATUS_LINK` |
| `image-1` … `image-4` | `--image-1` … `--image-4` | `STATUS_IMAGE_URL_1` … `4` |
| `post-id` | `--post-id` | Platform-specific (e.g. `TWEET_ID`) |

### X

| GHA input | Platform CLI | Env var |
|-----------|--------------|---------|
| `x-consumer-key` | `--consumer-key` | `TWITTER_CONSUMER_KEY` |
| `x-consumer-secret` | `--consumer-secret` | `TWITTER_CONSUMER_SECRET` |
| `x-oauth-token` | `--oauth-token` | `TWITTER_OAUTH_TOKEN` |
| `x-oauth-secret` | `--oauth-secret` | `TWITTER_OAUTH_SECRET` |

Utils commands (`feed-publish`, `schedule-run`) use prefixed `--x-*` flags; `execute.py` passes prefixed names for utils actions.

### Facebook (OAuth unattended)

| GHA input | Platform CLI | Env var |
|-----------|--------------|---------|
| `facebook-client-id` | `--client-id` | `FACEBOOK_CLIENT_ID` |
| `facebook-client-secret` | `--client-secret` | `FACEBOOK_CLIENT_SECRET` |
| `facebook-app-id` | `--app-id` | `FACEBOOK_APP_ID` |
| `facebook-object-id` | `--object-id` | `FACEBOOK_OBJECT_ID` |
| `facebook-refresh-token` | (env only) | `FACEBOOK_REFRESH_TOKEN` |

See [Agoras platform arguments reference](https://docs.agoras.io/reference/platform-arguments-envvars.html) for Discord, YouTube, TikTok, Threads, Telegram, and WhatsApp.

---

## Implementation checklist (maintainers)

1. [x] Rewrite [`docker/execute.py`](../docker/execute.py) with `build_argv()` router
2. [x] Expand [`action.yml`](../action.yml) inputs for all platforms
3. [x] Bundle Agoras 2.0 source in [`docker/Dockerfile`](../docker/Dockerfile) via BuildKit `agoras` context
4. [x] Bump version to 2.0.0 in `setup.cfg`, `README.md`, `push.yml`
5. [x] Align dev [`Dockerfile`](../Dockerfile) and [`Makefile`](../Makefile) with same Agoras version
6. [x] Add unit tests in [`docker/test_execute.py`](../docker/test_execute.py)
7. [x] Add PR Docker build smoke test in [`.github/workflows/pr.yml`](../.github/workflows/pr.yml)
8. [ ] Release: tag `2.0.0`, push GHCR image, GitHub release notes

---

## Verification matrix

| Network | Action | Smoke test |
|---------|--------|------------|
| x | post | `build_argv` unit test |
| facebook | post | Manual with OAuth secrets |
| instagram | post | Manual with OAuth secrets |
| linkedin | post | Manual with OAuth secrets |
| discord | post | Manual with bot token |
| youtube | video | Manual with OAuth secrets |
| tiktok | post | Manual with OAuth secrets |
| threads | post | Manual with OAuth secrets |
| telegram | post | Manual with bot token |
| whatsapp | post | Manual with API token |
| x | last-from-feed | `build_argv` unit test |
| (any) | schedule | `build_argv` unit test |
| x | like (multi ID) | Comma-separated `post-id` loop |

Run unit tests:

```bash
cd docker && python3 -m unittest test_execute.py -v
```

Run Docker smoke test (requires sibling `agoras` checkout — 2.0 is not on PyPI yet):

```bash
make docker-image AGORAS_SRC=../agoras
docker run --rm ghcr.io/luisalejandro/agoras-actions:2.0.0 test
```

Or directly:

```bash
docker buildx build \
  --build-context agoras=../agoras \
  -f docker/Dockerfile \
  docker \
  -t agoras-actions:test \
  --load
docker run --rm agoras-actions:test test
```

CI (`push.yml`, `pr.yml`) checks out `LuisAlejandro/agoras` and passes it as the `agoras` BuildKit context. Use the `agoras_ref` workflow input on manual dispatch to pin a branch, tag, or commit.

When `agoras>=2.0.0` is published to PyPI, replace the `COPY --from=agoras` block in `docker/Dockerfile` with `RUN pip3 install "agoras>=2.0.0,<3.0.0"`.

---

## Known limitations

- **`authorize` in GHA:** Interactive browser OAuth does not work headless in CI. Use unattended credentials (refresh tokens + client IDs) or pre-authorize locally and mount token storage (not supported in default image).
- **Agoras 2.0 not on PyPI:** The production image bundles agoras source at build time via the `agoras` BuildKit context. It does not install from PyPI or `git+https://…@develop`.
- **WhatsApp output:** Uses `{"id": "..."}` via `_output_status`; same `entrypoint.sh` parsing applies.

---

## Risk register

| Risk | Mitigation |
|------|------------|
| Facebook/Instagram/LinkedIn workflows break | Migration examples + OAuth env var docs |
| Breaking input names | Major version 2.0.0 + this document |
| Dev/prod skew | Dev Dockerfile pins same Agoras source as production |
| No integration CI | PR workflow builds Docker image; unit tests for routing |

---

## Appendix: Agoras source references

| Topic | Path in agoras repo |
|-------|---------------------|
| Platform registry | `packages/cli/src/agoras/cli/registry.py` |
| CLI entry | `packages/cli/src/agoras/cli/main.py` |
| Feed utils | `packages/cli/src/agoras/cli/utils/feed.py` |
| Schedule utils | `packages/cli/src/agoras/cli/utils/schedule.py` |
| Migration docs | `docs/migration/` |
| Env var reference | `docs/reference/platform-arguments-envvars.rst` |
| JSON output | `packages/core/src/agoras/core/interfaces.py` |
