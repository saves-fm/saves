# Deploying

The web app (`apps/web`, a Worker serving the Vite build as static assets) and the API (`apps/api`) run on Cloudflare Workers in Matthew's Cloudflare account. Each has a `staging` and a `production` environment in its `wrangler.toml`.

| What | When | Where |
|---|---|---|
| Staging | Every push to `main` | [saves-web-staging](https://saves-web-staging.matthewsullivan21.workers.dev) · [saves-api-staging](https://saves-api-staging.matthewsullivan21.workers.dev/v1/health) |
| PR previews | Every push to a PR from this repo | `pr-<number>-saves-web-staging…` and `pr-<number>-saves-api-staging…`, linked in a PR comment |
| Production | The v1.0.0 launch | saves.fm (once the domain is set up, #9) |

PR previews are uploaded as Worker *versions* with a preview alias, so they never take staging's traffic. PRs from forks get CI but no preview, since they can't read the deploy secret.

## Setup (once)

The workflow (`.github/workflows/deploy.yml`) needs two things in the repo's settings:

1. **`CLOUDFLARE_ACCOUNT_ID` variable**: the account ID, already set.
2. **`CLOUDFLARE_API_TOKEN` secret**: a Cloudflare API token that can deploy Workers.
   - Create it at dash.cloudflare.com → **My Profile** → **API Tokens** → **Create Token** → **Edit Cloudflare Workers** template → **Use template**. Under *Account Resources* pick **Matthew Sullivan**, under *Zone Resources* pick **All zones**, then **Continue to summary** → **Create Token**.
   - Add it without pasting it anywhere else: `gh secret set CLOUDFLARE_API_TOKEN -R saves-fm/saves` (it prompts for the value).

Until the secret exists, the Deploy workflow skips with a notice instead of failing.

## By hand

```bash
pnpm --filter @saves/api deploy:staging
pnpm --filter @saves/web deploy:staging   # builds first
```

## Secrets

Secrets are set per environment with Wrangler, from the clipboard so they never land in a file or the shell history:

```bash
cd apps/api
pbpaste | npx wrangler secret put RA_WEB_API_KEY --env staging      # Matthew's personal RA key
pbpaste | npx wrangler secret put RA_WEB_API_KEY --env production   # the savesfm service-account key
printf 'RA_WEB_API_KEY=%s\n' "$(pbpaste)" > .dev.vars              # local, gitignored
```

If `secret put --env staging` fails with "the latest version of your Worker isn't currently deployed", a PR preview uploaded a newer version than the one staging runs. Redeploy staging from `main` first (`pnpm --filter @saves/api deploy:staging`), then set the secret.
