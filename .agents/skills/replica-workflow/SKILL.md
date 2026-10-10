---
name: replica-workflow
description: >-
  Master orchestrator for the 11-skill Replica pack: assesses project platform, coordinates execution stages, manages artifact checkpoints in replica/state.md, and enforces quality verification gates. Triggers: run replica workflow, clone project plan.
---

# replica-workflow

Master coordinator for the 11-skill Replica pack in Google Antigravity 2.0.
Coordinates clean-room reconstruction: reverse-engineer behavior, build fresh code,
test thoroughly, analyze user complaints, rebrand, and prepare deployment.

## Safeguards and Authorization

- **Clean room**: Use public sources only. No private APIs, scraped logins, or copied code.
- **Explicit authorization**: Never deploy live, purchase domains, provision paid cloud services, or mutate external accounts without explicit user consent.

## Execution Modes and Stage Map

Select the execution mode based on project goals:
1. **Quick (UI & Core Flow)**: Recon -> Architecture -> Design -> Build -> Diff.
2. **Standard (Full Product)**: Quick + Backend + Test + Entrepreneur + Brand.
3. **Full (Go-To-Market)**: Standard + Launch + Deploy.

| Stage | Specialist Skill | Primary Artifact | Quality Gate |
|---|---|---|---|
| 1. Recon | `replica-recon` | `replica/recon.md`, `features.csv` | Feature IDs and priorities set |
| 2. Architecture | `replica-architect` | `replica/architecture.md` | Data model and vertical slice chosen |
| 3. Design | `replica-design` | `replica/design/tokens.json` | Contrast check exits 0 |
| 4. Build | `replica-build` | Shell & screen source code | Core vertical slice interactive |
| 5. Backend | `replica-backend` (Conditional) | `replica/backend.md`, migrations | Auth & local secrets verified |
| 6. Test | `replica-test` | `replica/test-plan.md`, `bugs.md` | Zero open S1/S2 bugs |
| 7. Diff | `replica-diff` | `replica/parity.md` | Parity score and layout edge-diff |
| 8. Entrepreneur | `replica-entrepreneur` | `replica/feedback.md`, `fixes.md` | Verbatim linked user quotes |
| 9. Brand | `replica-brand` | `replica/brand.json`, tokens | Rebrand sweep check exits 0 |
| 10. Launch | `replica-launch` (Conditional) | `replica/launch/listing.json` | Store listing lint exits 0 |
| 11. Deploy | `replica-deploy` (Conditional) | `replica/deploy.md` | Preflight checklist complete |

Skip cloud backend for client-only desktop/mobile apps. Skip store listing for web SaaS or internal tools.

## Operating Rules

1. **Assess Platform First**: Identify target environment (Web, Windows, Android, macOS, CLI) and existing tech stack before selecting patterns.
2. **Check State Before Acting**: Read `replica/state.md` to identify completed stages. Verify claimed artifacts exist before continuing.
3. **Selective Instruction Loading**: Do not preload all skills. Read only the specific `SKILL.md` needed for the active stage.
4. **Enforce Stage Gates**: Never declare a stage complete without running its verification check. Record results in `replica/state.md`.
5. **Completion Report**: When all target stages pass, provide a concise summary containing target platform, completed stages, parity score, verification status, and next user actions.
