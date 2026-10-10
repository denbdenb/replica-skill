---
name: replica-architect
description: >-
  Plans technology stack, database schema, and API route architecture from a recon map. Converts data models to SQL with access rules and orders implementation as thin vertical slices. Triggers: plan the clone, design database, stack architecture.
---
# replica-architect

Reads `replica/recon.md` and `replica/features.csv`. Writes
`replica/architecture.md` (template: architecture.md in this folder).

If there is no recon map, stop and run `replica-recon` first. Planning a
clone from memory of what an app does is how you miss half of it.

## Step 1: inspect platform and select stack

First, identify whether the clone is Web, Desktop, Mobile, or CLI/Backend.
Use what the user already knows or what exists in the repository. Do not force
web SaaS patterns (Postgres, Stripe, Vercel) onto desktop, mobile or local tools.

| target platform | recommended stack | data & storage | auth & payments |
| --- | --- | --- | --- |
| **Web App** | Next.js / SvelteKit / Rails + Tailwind | Postgres (Supabase/Neon) or SQLite (Turso) | Supabase/Auth.js; Stripe (if paid) |
| **Desktop App** | WinUI 3 (.NET), WPF, Tauri, Electron | SQLite / local file store | OS credentials; in-app licensing / Stripe |
| **Mobile App** | Android (Compose/Kotlin), iOS (SwiftUI), Flutter | Room (SQLite) / CoreData / DataStore | Credential Manager / RevenueCat / Stores |
| **CLI / Backend** | Python, Go, Node.js, Rust | SQLite / Postgres / JSON | API keys / local config; none |

Write each choice with one line of why. One database. No unnecessary microservices.
The clone does not need the original's architecture, it needs the original's
features. Cloud services (payments, email, hosting) are conditional on the app's needs.

## Step 2: the schema

Turn the inferred data model into SQL. For every table:

- `id uuid primary key default gen_random_uuid()`, `created_at`, `updated_at`
- an owner column (`user_id` or `org_id`) on everything a user owns
- foreign keys with an `on delete` rule decided, not defaulted
- indexes on every foreign key and every column you filter or sort by
- enums or check constraints for status fields
- times as `timestamptz`, always, stored in UTC
- money as integer cents plus a currency column
- access rules: Postgres row level security on Supabase, or one
  authorisation check per query in the data layer. Write which.

For platform-specific schema templates, SQL examples, and storage patterns (Web Postgres RLS vs. Desktop/Mobile SQLite), refer to [schema-guidelines.md](references/schema-guidelines.md).

Then the hard constraints the recon found. Two guests booking the same slot
is a database problem (an exclusion constraint or a unique index), not a UI
problem.

## Step 3: the API

One table per flow from the recon map. For every route or server action:

`method path | what it does | who can call it | input | output | flow`

Plus webhooks in (Stripe, calendar providers) and out, and background jobs
(reminders, sync, cleanup) with their schedule.

Only official, public APIs with the user's own keys. Never the original app's
private endpoints, even if they are visible in a browser.

## Step 4: the parts that bite

Write a line on each that applies: time zones and daylight saving, idempotency
(webhooks arrive twice), race conditions, rate limits, file size limits,
search, realtime, offline, email deliverability, multi-tenancy, GDPR deletion.

## Step 5: build order

1. **Vertical slice.** The core loop end to end, ugly: sign up, do the one
   thing, see the result. Proves the stack.
2. **Must-haves** from `features.csv`, by area.
3. **Should-haves**, then could-haves.
4. **The fixes** replica-entrepreneur finds, once it has run.

Each milestone lists its screens (S-IDs), tables and routes.

## Output

`replica/architecture.md`, the SQL in `replica/schema.sql` or as the first
migration, and a summary: stack in one line, table count, route count, the
three riskiest parts, and the next step: `replica-design` (or continue via `replica-workflow`).
