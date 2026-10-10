# Migration Report: Porting replica-skill to Google Antigravity 2.0

## Executive Summary

The 11-skill Replica pack ([Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill)) was successfully ported to **Google Antigravity 2.0**. The port preserves the original clean-room reverse-engineering methodology, standard-library Python utilities, data templates, MIT license, and creator credits.

A 12th skill, `replica-workflow`, was added to serve as a focused orchestrator coordinating the 11 modular skills, tracking workflow state in `replica/`, skipping unnecessary stages based on platform assessment, and enforcing quality verification gates.

---

## 1. Audit Findings

### 1.1 Claude-Specific Assumptions and Metadata
- **Plugin Manifests**: The repository contained `.claude-plugin/plugin.json` and `marketplace.json`, which assumed Claude Code plugin installations and pointed skills to the repository root (`"skills": "./"`).
- **Slash Commands**: Skill documentation and workflow transitions assumed Claude-specific slash commands (`/replica-recon`, `/replica-architect`, etc.).
- **Direct Agent Mentions**: Skills directly named "Claude" in operational guidelines (e.g., `replica-backend/SKILL.md` line 22: *"Claude never signs up for services... Claude writes .env.example"*).
- **Installation Guidance**: `README.md` directed users to `/plugin marketplace add...` and `~/.claude/skills/`.

### 1.2 Path Resolution and Execution Inconsistencies
- **Broken Relative Script Invocations**:
  - `replica-brand/SKILL.md` instructed running `python3 ../replica-design/contrast.py replica/design/tokens.json`, which failed when executed from the project root.
  - `replica-deploy/SKILL.md` referenced `python3 ../replica-diff/parity.py` and referenced `~/.claude/skills/`.
- **Interpreter Assumptions**: All scripts used `#!/usr/bin/env python3` and documentation specified `python3`. On Windows systems, `python3` resolves to a Windows Store stub and fails with exit code 1; `python` or `py` is required.
- **Output Directory Creation**: Utilities taking output path flags (such as `--out replica/feedback.md` or `--out replica/diffs/diff.png`) assumed parent directories already existed, raising `FileNotFoundError` if `replica/` or subdirectories were missing.

### 1.3 Image Format Handling in `imgdiff.py`
- `imgdiff.py` only checked for the 8-byte PNG signature `b"\x89PNG\r\n\x1a\n"`. When provided JPEGs, WebPs, GIFs, BMPs, or SVGs, it raised a generic error (`"is not a PNG"`).
- The interlaced PNG error message gave macOS-only advice (`"(on a Mac: sips -s format png in.png --out out.png)"`).

### 1.4 Architectural and Platform Assumptions
- `replica-architect` hardcoded web SaaS defaults (Next.js App Router, Supabase/Neon PostgreSQL, Stripe Checkout, Resend email, Vercel hosting).
- `replica-design` assumed CSS custom properties and Tailwind CSS theme mapping.
- `replica-test` assumed Playwright with axe-core.
- `replica-deploy` assumed Vercel deployment, DNS A/CNAME records, and mobile App Store/Google Play publishing.
- For desktop applications (e.g. WinUI 3, WPF), native mobile applications (Android Jetpack Compose, iOS SwiftUI), or CLI tools, these web SaaS defaults imposed unnecessary dependencies.

### 1.5 Unit Test Assumptions
- `tests/_load.py` imported scripts directly from root `<folder>/<name>.py`.
- `tests/test_repo.py` asserted that 11 skills lived directly at the repository root and checked `.claude-plugin/plugin.json` and Claude README copy.
- `tests/test_contrast_listing.py` and `tests/test_parity.py` referenced template files at root paths.

---

## 2. Structural Changes and Native Layout

### 2.1 Workspace Skills Directory (`.agents/skills/`)
All skills now reside under `.agents/skills/`, matching Antigravity 2.0 workspace customization discovery rules:

```
replica-skill/
├── .agents/
│   └── skills/
│       ├── replica-workflow/          [Orchestrator Skill]
│       │   └── SKILL.md
│       ├── replica-recon/             [Stage 1]
│       │   ├── SKILL.md
│       │   ├── recon-map.md
│       │   └── features.csv
│       ├── replica-architect/         [Stage 2]
│       │   ├── SKILL.md
│       │   └── architecture.md
│       ├── replica-design/            [Stage 3]
│       │   ├── SKILL.md
│       │   ├── contrast.py
│       │   └── tokens.json
│       ├── replica-build/             [Stage 4]
│       │   └── SKILL.md
│       ├── replica-backend/           [Stage 5]
│       │   └── SKILL.md
│       ├── replica-test/              [Stage 6]
│       │   ├── SKILL.md
│       │   ├── bug-report.md
│       │   ├── e2e.example.spec.ts
│       │   └── test-plan.md
│       ├── replica-diff/              [Stage 7]
│       │   ├── SKILL.md
│       │   ├── imgdiff.py
│       │   └── parity.py
│       ├── replica-entrepreneur/      [Stage 8]
│       │   ├── SKILL.md
│       │   ├── reviews.py
│       │   └── themes.json
│       ├── replica-brand/             [Stage 9]
│       │   ├── SKILL.md
│       │   └── sweep.py
│       ├── replica-launch/            [Stage 10]
│       │   ├── SKILL.md
│       │   ├── listing.py
│       │   └── listing.example.json
│       └── replica-deploy/            [Stage 11]
│           ├── SKILL.md
│           └── preflight.md
├── tests/
│   ├── _load.py
│   ├── test_contrast_listing.py
│   ├── test_imgdiff.py
│   ├── test_parity.py
│   ├── test_repo.py
│   ├── test_reviews.py
│   └── test_sweep.py
├── ANTIGRAVITY_MIGRATION.md
├── README.md
├── LICENSE
└── .gitignore
```

### 2.2 Preserving Skill Isolation and Metadata
- Every skill maintains valid YAML frontmatter with `name` matching the folder name and detailed third-person descriptions.
- Sibling templates, schemas, and helper scripts remain directly beside their respective `SKILL.md`.
- `.claude-plugin/` metadata is omitted from `.agents/`.

---

## 3. Cross-Platform Python Utility Refactoring

All 6 utilities continue to rely strictly on the Python Standard Library (no pip dependencies required):

1. **`imgdiff.py`**:
   - Added magic-byte image signature detection in `read_png()`. Unsupported formats (JPEG, WebP, GIF, BMP, TIFF, SVG) now trigger explicit, actionable errors indicating the detected format and conversion instructions.
   - Replaced macOS-specific `sips` interlacing advice with cross-platform guidance.
   - Updated `write_png()` to auto-create parent directories when writing diff images.
2. **`reviews.py`**:
   - Updated `load_themes()` to resolve `themes.json` relative to `__file__`.
   - Updated `--out` file writing to auto-create parent directories (e.g. `replica/`).
3. **`sweep.py`**:
   - Added `.agents`, `.agent`, and `.claude` to `SKIP_DIRS` to avoid false-positive brand hits on installed skill files while thoroughly checking project source code.
4. **Standardized Root Invocations**:
   - All skills updated to document commands callable directly from the project root:
     - `python .agents/skills/replica-diff/parity.py replica/features.csv`
     - `python .agents/skills/replica-diff/imgdiff.py original.png clone.png --out replica/diffs/diff.png`
     - `python .agents/skills/replica-design/contrast.py replica/design/tokens.json`
     - `python .agents/skills/replica-entrepreneur/reviews.py replica/reviews.csv --out replica/feedback.md`
     - `python .agents/skills/replica-brand/sweep.py . --config replica/brand.json`
     - `python .agents/skills/replica-launch/listing.py replica/launch/listing.json`

---

## 4. Platform-Aware Workflow Design

Workflows now explicitly accommodate multi-platform development without imposing web SaaS defaults:

| Dimension | Web App | Desktop App (Windows/macOS) | Mobile App (Android/iOS) | CLI / Backend |
| --- | --- | --- | --- | --- |
| **Stack Selection** | Next.js, SvelteKit, Rails | WinUI 3 (.NET), WPF, Tauri, Electron | Kotlin Compose, SwiftUI, Flutter | Python, Go, Node, Rust |
| **Data Layer** | PostgreSQL, SQLite (Turso) | Local SQLite, File storage | Room (SQLite), CoreData | SQLite, JSON, Postgres |
| **Design Tokens** | CSS vars, Tailwind | WinUI XAML ResourceDictionary | Compose Color/Typography, SwiftUI | ANSI styles / Terminal theme |
| **Testing Harness** | Playwright, axe-core | FlaUI, WinApp CLI, UI Automation | Compose UI test, ADB, XCUITest | pytest, unittest, CLI harness |
| **Monetization** | Stripe Billing, LemonSqueezy | In-app license, Microsoft Store | App Store IAP, Google Play Billing | None / SaaS subscription |
| **Deployment** | Vercel, Fly, Cloudflare | MSIX, InnoSetup, DMG, GitHub Release | TestFlight, Google Play Console | PyPI, Docker image, GitHub Release |

---

## 5. Master Orchestrator (`replica-workflow`)

A dedicated `replica-workflow` skill was authored at `.agents/skills/replica-workflow/SKILL.md`:
- **Platform Assessment**: Inspects project type and repository state in Step 0.
- **Selective Execution**: Bypasses irrelevant stages (e.g., skips App Store listing for desktop apps or web tools; skips cloud backend for local-first apps).
- **Anti-Duplication**: Reads existing files in `replica/` before executing each stage, preventing rework.
- **Verification Gates**: Enforces programmatic gates:
  - Contrast check exit code 0 (`contrast.py`)
  - Parity must-haves completed (`parity.py`)
  - Clean brand sweep exit code 0 (`sweep.py`)
  - Clean store listing exit code 0 (`listing.py`)
  - Clean automated tests and zero open S1/S2 bugs

---

## 6. Validation and Test Results

### 6.1 Automated Unit Test Suite
Ran complete unit test suite with:
```pwsh
python -m unittest discover -s tests -v
```
**Results: 58 passed, 0 failed, 0 errors in 0.941s.**

Detailed test breakdown:
- `test_contrast_listing.py`: 12 tests passed (contrast calculations, flattening, AA thresholds, listing limits, avoid flag, shipped templates).
- `test_imgdiff.py`: 15 tests passed (PNG decoding, filters, pixel/layout modes, retina scaling, height delta, and newly added explicit unsupported format tests).
- `test_parity.py`: 11 tests passed (weighted scoring, must-have tracking, build order, area grouping, visual score folding, shipped template).
- `test_repo.py`: 5 tests passed (12 skills in `.agents/skills/`, valid YAML frontmatter, no Claude plugin in `.agents`, README reel copy, no em-dashes).
- `test_reviews.py`: 10 tests passed (theme loading, date/rating parsing, quote extraction, duplicate handling, source weighting).
- `test_sweep.py`: 5 tests passed (identifier matches, hex color normalization, path matching, replica inclusion, skip directories).

### 6.2 CLI Verification Matrix

| Utility | Command Tested | Input | Exit Code | Observed Behavior | Status |
| --- | --- | --- | --- | --- | --- |
| `contrast.py` | `--help` | N/A | 0 | Displayed usage instructions | **PASSED** |
| `contrast.py` | CLI pair check | `#000000 #ffffff` | 0 | Contrast ratio 21.00:1 (AAA pass) | **PASSED** |
| `contrast.py` | CLI pair check | `#aaaaaa #ffffff` | 1 | Contrast ratio 2.32:1 (AA fail) | **PASSED** |
| `contrast.py` | Missing file | `nonexistent.xyz` | 2 | Reported FileNotFoundError cleanly | **PASSED** |
| `listing.py` | `--help` | N/A | 0 | Displayed usage instructions | **PASSED** |
| `listing.py` | Shipped example | `listing.example.json` | 0 | Analyzed store limits; 0 errors, 1 warning | **PASSED** |
| `listing.py` | Missing file | `nonexistent.json` | 2 | Reported FileNotFoundError cleanly | **PASSED** |
| `parity.py` | `--help` | N/A | 0 | Displayed usage instructions | **PASSED** |
| `parity.py` | Shipped matrix | `features.csv` | 0 | Parsed 17 features, reported 9 must-haves | **PASSED** |
| `parity.py` | `--fail-under 99.9` | `features.csv` | 1 | Failed gate when score below threshold | **PASSED** |
| `parity.py` | Missing file | `nonexistent.csv` | 2 | Reported FileNotFoundError cleanly | **PASSED** |
| `imgdiff.py` | `--help` | N/A | 0 | Displayed usage instructions | **PASSED** |
| `imgdiff.py` | Non-PNG input | `sample.jpg` (JPEG header) | 2 | Explicitly reported JPEG format and conversion advice | **PASSED** |
| `sweep.py` | `--help` | N/A | 0 | Displayed usage instructions | **PASSED** |
| `sweep.py` | Brand hits | `sweep . --avoid Calendly` | 1 | Detected 15 test fixtures in test suite | **PASSED** |
| `sweep.py` | Clean sweep | `sweep . --avoid Random` | 0 | Clean report: 0 matches found | **PASSED** |
| `reviews.py` | `--help` | N/A | 0 | Displayed usage instructions | **PASSED** |
| `reviews.py` | Valid CSV + `--out` | `temp_reviews.csv` | 0 | Parsed reviews and created output markdown | **PASSED** |
| `reviews.py` | Missing file | `nonexistent.csv` | 2 | Reported FileNotFoundError cleanly | **PASSED** |

### 6.3 Repository Invariants
- **No Em-Dashes**: Verified via static search across all `.md`, `.py`, `.json`, `.ts`, and `.csv` files. Zero instances of `\u2014`.
- **License**: Preserved verbatim MIT license and copyright notice for Jake Schincariol.

---

## 7. File Inventory

### 7.1 Preserved Verbatim
- `LICENSE`
- `.gitignore`
- `replica-recon/recon-map.md` (moved to `.agents/skills/replica-recon/recon-map.md`)
- `replica-recon/features.csv` (moved to `.agents/skills/replica-recon/features.csv`)
- `replica-architect/architecture.md` (moved to `.agents/skills/replica-architect/architecture.md`)
- `replica-design/tokens.json` (moved to `.agents/skills/replica-design/tokens.json`)
- `replica-test/bug-report.md` (moved to `.agents/skills/replica-test/bug-report.md`)
- `replica-test/e2e.example.spec.ts` (moved to `.agents/skills/replica-test/e2e.example.spec.ts`)
- `replica-test/test-plan.md` (moved to `.agents/skills/replica-test/test-plan.md`)
- `replica-entrepreneur/themes.json` (moved to `.agents/skills/replica-entrepreneur/themes.json`)
- `replica-launch/listing.example.json` (moved to `.agents/skills/replica-launch/listing.example.json`)
- `replica-deploy/preflight.md` (moved to `.agents/skills/replica-deploy/preflight.md`)
- `.claude-plugin/plugin.json` (kept outside `.agents/` for reference)
- `.claude-plugin/marketplace.json` (kept outside `.agents/` for reference)

### 7.2 Modified Files
- `.agents/skills/replica-recon/SKILL.md` (updated next-step links)
- `.agents/skills/replica-architect/SKILL.md` (platform-aware stack options, skill links)
- `.agents/skills/replica-design/SKILL.md` (multi-platform token mappings, script paths)
- `.agents/skills/replica-design/contrast.py` (verified standard library compatibility)
- `.agents/skills/replica-build/SKILL.md` (platform-agnostic accessibility, skill links)
- `.agents/skills/replica-backend/SKILL.md` (agent reference updates, conditional backend scope)
- `.agents/skills/replica-test/SKILL.md` (multi-platform test harnesses, skill links)
- `.agents/skills/replica-diff/SKILL.md` (root execution paths, skill links)
- `.agents/skills/replica-diff/imgdiff.py` (explicit image format detection, cross-platform advice, directory auto-creation)
- `.agents/skills/replica-diff/parity.py` (verified root execution)
- `.agents/skills/replica-entrepreneur/SKILL.md` (root execution paths, skill links)
- `.agents/skills/replica-entrepreneur/reviews.py` (output directory auto-creation)
- `.agents/skills/replica-brand/SKILL.md` (root execution paths, skill links)
- `.agents/skills/replica-brand/sweep.py` (skip `.agents` and `.claude` directories)
- `.agents/skills/replica-launch/SKILL.md` (conditional store listing, root execution paths)
- `.agents/skills/replica-launch/listing.py` (verified root execution)
- `.agents/skills/replica-deploy/SKILL.md` (agent reference updates, root preflight execution paths, multi-platform distribution)
- `tests/_load.py` (loads from `.agents/skills/` with fallback)
- `tests/test_contrast_listing.py` (updated template file paths)
- `tests/test_imgdiff.py` (added tests for JPEG, WebP, BMP, and SVG error handling)
- `tests/test_parity.py` (updated template file paths)
- `tests/test_repo.py` (updated to test `.agents/skills/`, 12 skills, and Antigravity structure)
- `README.md` (updated with Antigravity 2.0 instructions, Windows/Linux install commands, and 12-skill documentation)

### 7.3 Added Files
- `.agents/skills/replica-workflow/SKILL.md` (master orchestrator skill)
- `ANTIGRAVITY_MIGRATION.md` (this migration document)

### 7.4 Omitted Files from `.agents/`
- `.claude-plugin/` directory intentionally omitted from `.agents/` to maintain clean Antigravity 2.0 customization discovery.
