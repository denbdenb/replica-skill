# Recon Heuristics and Sizing Guidelines

Reference material for `replica-recon`. Load this reference when sizing a clone project
or classifying non-clonable assets and edge case behaviors.

## 1. Project Sizing Guidelines

Estimate scope based on screen count, unique entities, and asynchronous integration:

- **Small (S - Weekend build)**: 3-5 screens, 1-2 entities, no payment gateway, client-only state or simple local SQLite.
- **Medium (M - 2-3 weeks)**: 6-12 screens, 3-6 entities, single auth provider, standard CRUD flows, simple transactional emails.
- **Large (L - Multi-month build)**: 15+ screens, multi-tenancy, real-time collaboration, complex webhooks, subscription billing, background worker queues.
- **Extra Large (XL - Rescope)**: Broad platforms (e.g. entire Salesforce, entire Figma). Rescope down to the core loop.

## 2. Non-Clonable Assets (Clean-room Boundary)

Always mark these categories as `skip` in `features.csv`:
- Proprietary dataset catalogs (copyrighted media catalogs, curated databases).
- Live two-sided network effects (existing registered users and marketplace liquidity).
- Proprietary machine learning models or internal weights.
- Exclusive partner contracts and regulated licenses (banking charters, telecom carrier agreements).
