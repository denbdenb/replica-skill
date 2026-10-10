---
name: replica-deploy
description: >-
  Prepares production deployment across web, desktop, or mobile platforms: enforces preflight verification gates, DNS/hosting setup, env configurations, and release packaging. Triggers: deploy clone, production release, publish app, ship live.
---
# replica-deploy

Reads everything in `replica/`. Writes `replica/deploy.md` (the checklist in
`preflight.md` in this folder, filled in).

## The rules

- **Nothing goes live without the user's go.** Show the preflight results and
  ask.
- **The user buys and signs in.** The agent never buys a domain, enters a card,
  types a password or pastes a live key. The agent writes the exact DNS records,
  env var names and commands; the user does the account steps.
- **Not until it is rebranded.** The sweep must be clean. No exceptions.

## Step 1: preflight

Run every check and paste the results into `deploy.md`:

```bash
npx playwright test                                                        # or native test suite (dotnet test, ./gradlew test, pytest)
python .agents/skills/replica-diff/parity.py replica/features.csv           # must-haves done
python .agents/skills/replica-brand/sweep.py . --config replica/brand.json  # exit 0: clean
python .agents/skills/replica-launch/listing.py replica/launch/listing.json # if shipping to app stores
npm run build                                                              # or native build/publish (dotnet publish, ./gradlew assembleRelease)
```

Plus by hand: no open S1 or S2 bugs, privacy policy and terms pages live
(listing every processor), cookie banner if you use non-essential cookies in
the EU or UK, account deletion works, the favicon, titles and OG image are
yours.

Any failure stops the deploy. Say which and why.

## Step 2: production services

- A **separate production project** for the database (never the dev one),
  backups on, migrations run by the deploy, not by hand.
- Env vars set in the host for production, matching `.env.example`. Live
  keys only here.
- **Stripe**: switch to live mode, recreate products and prices, add the
  production webhook endpoint and its signing secret, test one real
  purchase and refund it.
- **OAuth**: add the production domain to every provider's redirect URIs and
  authorised origins. Google scopes that need verification must be approved,
  or only test users can sign in.
- **Email**: the sending domain verified with the provider.

## Step 3: host and domain

Default: Vercel for Next.js, Cloudflare Pages, Netlify, or Fly.io. Connect the repo
so `main` deploys and pull requests receive preview URLs.

For full DNS record templates (A, CNAME, SPF, DKIM, DMARC) and distribution packaging
workflows (Windows MSIX, macOS DMG, Android AAB, iOS App Store, Docker), consult
[platform-deployment.md](references/platform-deployment.md).

## Step 4: watch it

Error tracking (Sentry or the host's), uptime checks on the home page and the
core flow's API, logs kept, analytics (a privacy-friendly one avoids the
cookie banner), and an alert to the user's email or phone. Then do the core
flow on the live site yourself, and ask the user to do it on their phone.

## Output

`replica/deploy.md` with every check and its result, the live URL, the DNS
records set, and what to watch in the first week. The clone is now an app
with your name on it.
