# The Replica skill

> [!NOTE]
> **Google Antigravity 2.0 Port**: This repository is a native port of the original [Replica skill pack for Claude by Jake Schincariol](https://github.com/Jakeschincariol/replica-skill). It adapts all 11 skills for Google Antigravity 2.0, standardizes Python utilities to run from the project root across Windows/macOS/Linux without external dependencies, makes workflows platform-aware (Web, Windows Desktop, Android APK, iOS, CLI), and adds a dedicated `replica-workflow` orchestrator.
>
> **Инструкция на русском языке**: Подробное руководство по использованию и архитектуре проекта доступно в файле [GUIDE_RU.md](file:///GUIDE_RU.md).

Eleven modular skills plus one master orchestrator for Google Antigravity 2.0 that clone any app. Free, MIT, no signup, no API key, nothing to connect.

One reverse-engineers the app you want to clone. One rebuilds it. One tests it for bugs. And one is the Entrepreneur: it reads what the app's users hate and fixes it in yours, so you have an app you can sell.

In between, the others plan the stack and the database, rebuild the design system, wire up auth and payments, score your clone against the original, give it a name and a brand of its own, write the landing page and the store listing, and put it live on your domain. `replica-workflow` coordinates all of them.

**It rebuilds what an app does, never what it owns.** Features and flows, clean-room style. Not its code, its logo, its copy or its content. The fine print is at the bottom, and the skills enforce it.

## Install in Google Antigravity 2.0

### Option A: Global Install (All Projects & Chats)
Install once to make Replica available across all workspaces on your machine:

**Windows (PowerShell):**
```powershell
git clone https://github.com/denbdenb/replica-skill.git
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini\config\skills"
Copy-Item -Recurse -Force replica-skill\.agents\skills\* "$env:USERPROFILE\.gemini\config\skills\"
```

**macOS / Linux (Bash):**
```bash
git clone https://github.com/denbdenb/replica-skill.git
mkdir -p ~/.gemini/config/skills
cp -r replica-skill/.agents/skills/* ~/.gemini/config/skills/
```

### Option B: Workspace Install (Single Project)
Install locally in a specific project's `.agents/skills/` folder:

**Windows (PowerShell):**
```powershell
git clone https://github.com/denbdenb/replica-skill.git
New-Item -ItemType Directory -Force -Path ".agents\skills"
Copy-Item -Recurse -Force replica-skill\.agents\skills\* .agents\skills\
```

**macOS / Linux (Bash):**
```bash
git clone https://github.com/denbdenb/replica-skill.git
mkdir -p .agents/skills
cp -r replica-skill/.agents/skills/* .agents/skills/
```

The utilities require Python 3.8 or newer (`python` on Windows, `python3` on Unix). Standard library only: nothing to pip install.

## The skills

| Skill | What it does |
| --- | --- |
| `replica-workflow` | Master orchestrator: assesses platform, coordinates stages, verifies quality gates, tracks state in `replica/`. |
| `replica-recon` | Reverse-engineers any app: screens, flows, components, data model from public pages, docs, and screenshots. |
| `replica-architect` | Plans the stack, database schema and API for your clone across Web, Desktop, Mobile, or CLI. |
| `replica-design` | Rebuilds the design system: colours, type, spacing, components. As tokens, with WCAG contrast verification. |
| `replica-build` | Rebuilds the app screen by screen from the recon map: shell first, vertical slice, full states. |
| `replica-backend` | Auth, database, payments and integrations (conditional on app requirements). |
| `replica-test` | Tests every flow for bugs using platform-appropriate harnesses (Playwright, FlaUI, Compose UI, pytest). |
| `replica-diff` | Compares your clone against the original: feature parity score, missing list, and layout diff. |
| `replica-entrepreneur` | Reads what users hate in real reviews and turns it into fixes and a positioning angle. |
| `replica-brand` | Names and rebrands your version so it is yours, verified by an automated brand sweep. |
| `replica-launch` | Landing page, pricing, and app store listing linter (for mobile/store apps). |
| `replica-deploy` | Preflight gate (tests, parity, sweep clean) and deployment instructions. |

## How to use it

Start with the orchestrator, or run any individual skill:

```
replica-workflow
```

Or execute stage-by-stage:
```
recon -> architect -> design -> build -> backend -> test -> diff -> entrepreneur -> brand -> launch -> deploy
```

Outputs live in your project's `replica/` directory:
- `replica/recon.md` and `replica/features.csv`
- `replica/architecture.md`
- `replica/design/tokens.json` and `replica/design/components.md`
- `replica/build-log.md` and `replica/clone-screens/`
- `replica/backend.md`
- `replica/test-plan.md` and `replica/bugs.md`
- `replica/parity.md` and `replica/diffs/`
- `replica/reviews.csv`, `replica/feedback.md`, and `replica/fixes.md`
- `replica/brand.md` and `replica/brand.json`
- `replica/launch/`
- `replica/deploy.md`

## The tools

Six standard-library Python tools. None touch the network. Optimized for streaming, minimal memory footprint, and fast execution.

```bash
# Layout diff: ignores colour, compares structure (PNG)
python .agents/skills/replica-diff/imgdiff.py original.png clone.png --out replica/diffs/diff.png

# Feature parity score and missing list in build order
python .agents/skills/replica-diff/parity.py replica/features.csv

# Ranks what real users hate from reviews CSV with linked quotes
python .agents/skills/replica-entrepreneur/reviews.py replica/reviews.csv --out replica/feedback.md

# WCAG 2.2 contrast checker on design tokens
python .agents/skills/replica-design/contrast.py replica/design/tokens.json

# Brand sweep: finds original names, domains and colours in code
python .agents/skills/replica-brand/sweep.py . --avoid "Original App"

# Store listing linter for App Store and Google Play limits and trademarks
python .agents/skills/replica-launch/listing.py replica/launch/listing.json
```

### Token and Context Optimization Flags

All six utilities support flags specifically designed to minimize agent context consumption:
- `--summary`: Emits a single concise summary line (saves 70% to 90% of output tokens when an agent invokes CLI tools).
- `--compact-json`: Emits unindented single-line JSON, stripping unnecessary whitespace.

## Performance and Token Optimization

The Antigravity 2.0 port includes an extensive optimization suite (see [TOKEN_OPTIMIZATION.md](file:///TOKEN_OPTIMIZATION.md)):
- **Discovery Metadata (-48.8%)**: Condensed all 12 skill descriptions to ~180-260 characters, saving ~700 tokens on every agent turn.
- **Progressive Disclosure**: Platform-specific schemas and deep heuristics moved into `references/` directories, loaded conditionally only when needed.
- **Workflow Orchestration (-57.5%)**: Streamlined `replica-workflow` into a compact 410-word decision engine using a standardized `replica/state.md` checkpoint.
- **Memory & Speed**: 4.0x peak RAM reduction in `imgdiff.py` (~23 MB vs ~95 MB), 40x speedup in `reviews.py` date parsing, sRGB lookup tables in `contrast.py`, and streaming line-by-line checks in `sweep.py`.

Run test suite:
```bash
python -m unittest discover -s tests -v
```

## Fine print

**It rebuilds functionality and UX patterns, clean-room style.** It studies what the app does and how people move through it, then writes everything fresh. It never copies the target's source code, proprietary assets, logos, trademarks, copy or private APIs.

**It only reads what you are allowed to read.** Public pages and your own account. It never scrapes behind a login or against a site's terms, never logs into anyone else's account, and never gets past a paywall. If your account's terms forbid using it to build a competitor, it says so and sticks to public sources.

**It always rebrands before launch.** New name, new palette, new logo, new words. `replica-deploy` will not ship until the sweep is clean.

**"Clone any app" means the features and the flow.** Not the content, the network or the licences an app owns. You can rebuild a music app's player, playlists and sharing. You cannot clone its catalogue.

**No guarantee of a "perfect" clone.** Results depend on how complex the app is. A booking tool is weeks. A spreadsheet engine is not. `replica-recon` sizes it honestly before you start, and `replica-diff` gives you a real number, not a vibe.

**The Entrepreneur never makes things up.** No invented reviews, quotes or numbers. Every claim has a link, and the sample size is stated.

**Check before you sell.** Run the trademark checks `replica-brand` lists, read the terms of anything you used, and talk to a lawyer before launch if there is money on the line. This is not legal advice.

## Credit

- **Original Claude Skill Pack**: Designed and created by Jake Schincariol ([opusjake.ai](https://opusjake.ai), [Original Repository](https://github.com/Jakeschincariol/replica-skill)).
- **Google Antigravity 2.0 Port**: Ported by denb ([denbdenb](https://github.com/denbdenb)). Adds native `.agents/skills/` packaging, cross-platform execution on Windows/macOS/Linux, multi-platform app support (Web, Windows Desktop, Android APK, iOS, CLI), and workflow orchestration (`replica-workflow`).

## License

MIT. Take it, change it, ship it.
