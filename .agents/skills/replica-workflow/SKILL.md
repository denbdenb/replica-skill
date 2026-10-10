---
name: replica-workflow
description: >-
  Coordinates and orchestrates the Replica pack skills (recon, architect,
  design, build, backend, test, diff, entrepreneur, brand, launch, deploy) to
  clone an application cleanly and methodically. Inspects the target platform
  (web, desktop, mobile, CLI), tracks progress in replica/, skips redundant
  stages, prevents duplicate work, and enforces quality verification gates
  before advancing. Use when the user wants to start, plan, track, resume, or
  run an end-to-end clone workflow.
---

# replica-workflow

Master coordinator for the Replica skill pack in Google Antigravity 2.0.

Replica clones an existing application's functionality and UX patterns using
a clean-room methodology: reverse-engineer public behavior, rebuild fresh code,
test thoroughly, uncover what users dislike about the original, and rebrand it
into your own product.

This workflow coordinates the 11 specialized skills, preserves incremental state
in `replica/`, avoids duplicating work, and enforces quality gates at every stage.

## Clean-room safeguards

Before initiating any workflow, enforce these non-negotiable safeguards:

1. **Public sources only**: Never access unauthorized accounts, scrape behind
   logins, or bypass paywalls.
2. **No private APIs or decompiled code**: Do not copy JavaScript bundles, reverse
   engineer binaries, or inspect private network calls. Use public documentation.
3. **Write fresh**: Every line of code, stylesheet, copy string, and asset is
   created originally.
4. **No live automated mutations**: Never purchase domains, deploy to live
   production, or bill cards without explicit user action.

## Pipeline Overview

```
Stage 1: Recon          -> replica/recon.md, replica/features.csv
Stage 2: Architecture   -> replica/architecture.md, schema
Stage 3: Design         -> replica/design/tokens.json, components.md (gate: contrast)
Stage 4: Build          -> Shell, vertical slice, screens, replica/build-log.md
Stage 5: Backend        -> (Conditional) Auth, DB, APIs, replica/backend.md
Stage 6: Test           -> replica/test-plan.md, test specs, replica/bugs.md
Stage 7: Diff           -> replica/parity.md (gate: parity & imgdiff)
Stage 8: Entrepreneur   -> replica/reviews.csv, feedback.md, fixes.md
Stage 9: Brand          -> replica/brand.md, brand.json (gate: sweep clean)
Stage 10: Launch        -> (Conditional) Landing, pricing, listing.json (gate: listing)
Stage 11: Deploy        -> (Conditional) replica/deploy.md preflight gate
```

## Step 0: Project and Platform Assessment

Before recommending architecture or tools, inspect the environment:

1. **Target Platform**:
   - **Web**: Next.js, Vite/React, SvelteKit, Nuxt, Rails, etc.
   - **Desktop**: Windows WinUI 3, WPF, macOS SwiftUI/AppKit, Electron, Tauri.
   - **Mobile**: Android (Jetpack Compose / Kotlin), iOS (SwiftUI / Swift), Flutter, Expo.
   - **Backend / CLI**: Python, Node, Go, Rust.
2. **Existing Workspace State**:
   - Check if `replica/` exists in the project root.
   - Read existing artifacts to resume without repeating completed stages.
3. **Conditionality Matrix**:
   - Client-only desktop or offline mobile app? Skip cloud backend and Stripe billing unless requested.
   - Open-source tool or web SaaS? Skip App Store and Google Play store listing linting.
   - Internal tool? Skip landing page and public marketing stages.

## Stage Coordination and Verification Gates

For each stage, invoke the modular skill or guide the user through its steps:

### 1. Recon (`replica-recon`)
- **Inputs**: Public URLs, documentation, screenshots, feature lists.
- **Outputs**: `replica/recon.md`, `replica/features.csv`, `replica/screens/`.
- **Gate**: Feature matrix has stable IDs, areas, priorities (must/should/could), and initial status `no`.

### 2. Architecture (`replica-architect`)
- **Inputs**: `replica/recon.md`, `replica/features.csv`.
- **Outputs**: `replica/architecture.md`, data schema.
- **Platform awareness**: Match tech stack to target platform (e.g. Room/SQLite for mobile/desktop, Postgres for web).
- **Gate**: Core loop vertical slice identified; data model mapped with indexes and constraints.

### 3. Design System (`replica-design`)
- **Inputs**: Screenshots in `replica/screens/`, recon component list.
- **Outputs**: `replica/design/tokens.json`, `components.md`.
- **Verification Gate**:
  ```bash
  python .agents/skills/replica-design/contrast.py replica/design/tokens.json
  ```
  Must exit 0 (zero AA contrast failures).

### 4. Implementation (`replica-build`)
- **Inputs**: Architecture plan, design tokens, component specs.
- **Outputs**: App shell, vertical slice, screen implementations, `replica/build-log.md`.
- **Gate**: All must-have screens implemented with all states (empty, loading, error, success).

### 5. Backend Services (`replica-backend` - Conditional)
- **Inputs**: `replica/architecture.md`.
- **Outputs**: Migrations, API routes, auth, webhooks, `replica/backend.md`.
- **Gate**: Authorisation checks enforced; secrets kept strictly in local environment variables.

### 6. Verification and Testing (`replica-test`)
- **Inputs**: Flow definitions from recon map.
- **Outputs**: `replica/test-plan.md`, test suites, `replica/bugs.md`.
- **Platform awareness**: Playwright for web, FlaUI/WinApp for Windows, Compose UI tests for Android.
- **Gate**: Zero open S1 (critical) or S2 (major) bugs.

### 7. Parity and Visual Diff (`replica-diff`)
- **Inputs**: Updated `replica/features.csv`, screenshots.
- **Verification Gate**:
  ```bash
  python .agents/skills/replica-diff/parity.py replica/features.csv
  python .agents/skills/replica-diff/imgdiff.py original.png clone.png --out replica/diffs/diff.png
  ```
  Must-haves completed; layout structures aligned.

### 8. User Voice and Differentiation (`replica-entrepreneur`)
- **Inputs**: Real user feedback in `replica/reviews.csv`.
- **Outputs**: `replica/feedback.md`, `replica/fixes.md`.
- **Verification Gate**:
  ```bash
  python .agents/skills/replica-entrepreneur/reviews.py replica/reviews.csv --out replica/feedback.md
  ```
  Every quote verbatim and linked; fixes added to `features.csv` with `original: no`.

### 9. Rebrand and Identity (`replica-brand`)
- **Inputs**: Positioning angle from `fixes.md`.
- **Outputs**: `replica/brand.md`, `replica/brand.json`, new design tokens.
- **Verification Gate**:
  ```bash
  python .agents/skills/replica-brand/sweep.py . --config replica/brand.json
  ```
  Must exit 0 (clean sweep: no original names, domains, or brand colors remaining).

### 10. Store and Launch Preparation (`replica-launch` - Conditional)
- **Inputs**: `replica/brand.json`, `replica/fixes.md`.
- **Outputs**: `replica/launch/` marketing assets, `listing.json`.
- **Verification Gate**:
  ```bash
  python .agents/skills/replica-launch/listing.py replica/launch/listing.json
  ```
  Must exit 0 (zero errors in metadata limits and trademark checks).

### 11. Deployment Preflight (`replica-deploy` - Conditional)
- **Inputs**: Full `replica/` directory.
- **Outputs**: `replica/deploy.md` filled preflight checklist.
- **Verification Gate**:
  All automated tests green, sweep clean, listing valid, production configuration ready.

## Managing Workflow State

To inspect current progress at any time, run:

```bash
python .agents/skills/replica-diff/parity.py replica/features.csv
```

When resuming work, check which files already exist in `replica/` and continue from the first incomplete stage.
