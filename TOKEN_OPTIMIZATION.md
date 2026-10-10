# Token, Context, Memory and Performance Optimization
## Replica Skill Pack for Google Antigravity 2.0

### Executive Summary

This document details the comprehensive optimization of the Replica Skill Pack for Google Antigravity 2.0. The goal of this optimization is to minimize token consumption across agent interactions, decrease peak Python memory utilization, speed up CLI execution, and provide progressive disclosure without sacrificing functionality, code quality, or test coverage.

All changes were implemented using only Python 3.12 standard library features (zero third-party dependencies). The test suite was expanded from 58 to 72 unit tests, verifying full backward compatibility, identical mathematical and detection results, and complete repository invariants (including zero em-dashes).

---

### Phase 1: Baseline Measurements and Architecture Audit

**Environment:** Windows 11, Python 3.12.10 (Standard Library only), Git

#### 1. Baseline Skill Size and Metadata Metrics

Antigravity 2.0 loads skill discovery metadata (`name` and `description` from YAML frontmatter) into the active agent system prompt context on every request. The full instruction body of each `SKILL.md` is only ingested when an agent explicitly triggers the skill.

| Skill | Total Lines | Total Words | Total Chars | Desc Chars | Desc Words | Body Words | Body Lines |
|---|---|---|---|---|---|---|---|
| `replica-architect` | 109 | 759 | 4,800 | 478 | 81 | 672 | 99 |
| `replica-backend` | 93 | 659 | 4,248 | 427 | 65 | 588 | 84 |
| `replica-brand` | 110 | 709 | 4,459 | 494 | 83 | 620 | 100 |
| `replica-build` | 89 | 649 | 3,935 | 418 | 70 | 573 | 80 |
| `replica-deploy` | 102 | 716 | 4,540 | 481 | 78 | 632 | 92 |
| `replica-design` | 102 | 631 | 4,221 | 480 | 75 | 550 | 92 |
| `replica-diff` | 93 | 631 | 4,310 | 459 | 75 | 550 | 83 |
| `replica-entrepreneur` | 112 | 805 | 4,968 | 589 | 102 | 697 | 101 |
| `replica-launch` | 101 | 683 | 4,402 | 432 | 67 | 610 | 91 |
| `replica-recon` | 134 | 933 | 5,533 | 502 | 90 | 837 | 124 |
| `replica-test` | 90 | 579 | 3,646 | 460 | 75 | 498 | 80 |
| `replica-workflow` | 161 | 891 | 7,489 | 480 | 66 | 819 | 151 |
| **TOTAL** | **1,296** | **8,645** | **58,551** | **5,700** | **927** | **7,646** | **1,177** |

- **Discovery Metadata Baseline:** 5,700 characters (~927 words). Estimated passive system prompt overhead: ~1,300 to 1,450 tokens on every invocation.
- **Instruction Body Baseline:** 7,646 words across all 12 skills.
- **Orchestrator Baseline (`replica-workflow`):** 819 words in body, duplicating commands and stage workflows.

#### 2. Baseline Python Utility Benchmarks

Measured using Python `tracemalloc` and `time.perf_counter()` over 5 repetitions per benchmark on Windows 11 (Python 3.12.10):

| Utility | Test Fixture Description | Baseline Avg Runtime | Baseline Peak Memory | Result / Accuracy |
|---|---|---|---|---|
| `contrast.py` | 500 rounds of 8x8 color pairs (32,000 WCAG calculations) | 764.59 ms | 126.5 KB | 100% compliant |
| `reviews.py` | 5,000 date strings (ISO, partial, malformed, trailing time) | 245.59 ms | 337.4 KB | 100% match |
| `sweep.py` | Synthetic repo of 100 JS files x 500 lines (50,000 lines), 3 names, 2 domains, 2 hex colors | 1,076.34 ms | 865.6 KB | 2,600 hits |
| `imgdiff.py` | Pure-Python layout comparison of two 480x800 RGB PNG screenshots | 9,011.08 ms | 94,998.0 KB (~92.8 MB) | Score 78.7 |

---

### Phase 2: Skill Frontmatter Optimization

Each skill description in YAML frontmatter was revised to be concise, distinctive, and focused on key semantic trigger terms while removing verbose conversational lists and redundant instructions. Target bounds were set to 180 to 260 characters (hard validation bounds: 150 to 350 characters).

#### Before vs. After Frontmatter Description Comparison

| Skill | Baseline Chars | Baseline Words | Optimized Chars | Optimized Words | Reduction % |
|---|---|---|---|---|---|
| `replica-architect` | 478 | 81 | 245 | 36 | -48.7% |
| `replica-backend` | 427 | 65 | 236 | 28 | -44.7% |
| `replica-brand` | 494 | 83 | 237 | 33 | -52.0% |
| `replica-build` | 418 | 70 | 239 | 33 | -42.8% |
| `replica-deploy` | 481 | 78 | 241 | 29 | -49.9% |
| `replica-design` | 480 | 75 | 243 | 31 | -49.4% |
| `replica-diff` | 459 | 75 | 242 | 30 | -47.3% |
| `replica-entrepreneur` | 589 | 102 | 242 | 33 | -58.9% |
| `replica-launch` | 432 | 67 | 248 | 31 | -42.6% |
| `replica-recon` | 502 | 90 | 247 | 29 | -50.8% |
| `replica-test` | 460 | 75 | 246 | 34 | -46.5% |
| `replica-workflow` | 480 | 66 | 250 | 30 | -47.9% |
| **TOTAL** | **5,700** | **927** | **2,916** | **377** | **-48.8%** |

**Token Impact:**
- Metadata character count decreased from 5,700 chars to 2,916 chars (-2,784 characters).
- Metadata word count decreased from 927 words to 377 words (-550 words).
- **Estimated Savings:** ~680 to 750 tokens saved from the agent system prompt on **every single interaction turn**.

---

### Phase 3: `replica-workflow` Orchestrator Refactoring

The master orchestrator (`.agents/skills/replica-workflow/SKILL.md`) was refactored to focus strictly on decision routing, state tracking, and quality gate enforcement, eliminating duplicate procedures fully documented in specialist skills:

- **Baseline Body Size:** 819 words (151 lines, 7,489 characters).
- **Optimized Body Size:** 410 words (43 lines, 3,181 characters).
- **Context Reduction:** **-50.0% words (-57.5% characters)**.
- **Retained Safeguards:**
  1. Platform assessment (Web, Desktop, Mobile, CLI).
  2. Execution modes (Quick, Standard, Full).
  3. Conditional stage skipping.
  4. Artifact inspection before stage execution (no duplicate work).
  5. Mandatory quality gates (test suite green, clean brand sweep, parity thresholds, zero critical bugs).
  6. Explicit user approval requirement before live deployment or destructive actions.
  7. Standardized project checkpoint format (`replica/state.md`).

---

### Phase 4: Progressive Disclosure and State Checkpoints

Large platform-specific implementation guidelines and secondary reference examples were moved into dedicated `references/` directories beside their respective skills, with explicit conditional loading rules:

1. **`replica-architect/references/schema-guidelines.md`**: PostgreSQL RLS policies vs. Desktop/Mobile local SQLite practices.
2. **`replica-test/references/platform-testing.md`**: Testing patterns for Web (Playwright), Desktop (FlaUI / WinApp CLI), Mobile (Compose UI), and CLI (pytest).
3. **`replica-deploy/references/platform-deployment.md`**: Production DNS configuration, desktop MSIX/DMG packaging, mobile App Store/Google Play publishing, and containerization.
4. **`replica-recon/references/recon-heuristics.md`**: Deep app sizing heuristics (S/M/L/XL) and clean-room asset boundary definitions.
5. **`replica-workflow/state-template.md`**: Standard 100 to 200 word project state checkpoint (`replica/state.md`) recording current stage, completed stages, key architectural decisions, verification status, and blockers.

**Instruction Body Savings:**
Across all 12 skills, total instruction body words decreased from 7,646 words down to 6,895 words (-751 words), saving ~1,000 tokens when skills are viewed, while preserving deep technical details on demand.

---

### Phase 5: `sweep.py` Stream Processing and Exclusions

**File:** `.agents/skills/replica-brand/sweep.py`

#### Changes:
1. Replaced memory-buffering `fh.readlines()` with line-by-line generator streaming (`for line in fh:`).
2. Added safe compiler and IDE artifact exclusions to `SKIP_DIRS`: `bin`, `obj`, `.vs`, `.idea`, `target`, `.dart_tool`.
3. Added fast hex pre-filter (`if cols and "#" in line:`) to avoid regex execution on lines without color codes.
4. Added `--compact-json` (single-line JSON) and `--summary` (concise human-readable text) CLI options.

#### Benchmark Results (Synthetic repo with 100 files, 50,000 lines, 2,600 hits):
- **Baseline Runtime:** 1,076.34 ms
- **Optimized Runtime:** 761.20 ms (**29.3% faster**)
- **Memory:** 796.4 KB (down from 865.6 KB)
- **Detection Accuracy:** Exactly 2,600 matches identified (100% precision and recall match).

---

### Phase 6: `contrast.py` sRGB Lookup Table

**File:** `.agents/skills/replica-design/contrast.py`

#### Changes:
1. Precomputed a 256-entry sRGB gamma curve lookup table `_SRGB_LUT` for channel values 0 through 255, eliminating repeated `pow(c / 255.0, 2.4)` calls.
2. Added `--compact-json` and `--summary` output modes.
3. Verified bitwise mathematical equivalence for all 256 color channels against reference calculations.

#### Benchmark Results (32,000 WCAG contrast calculations):
- **Baseline Runtime:** 764.59 ms
- **Optimized Runtime:** 531.36 ms (**30.5% faster**)
- **Peak Memory:** 126.4 KB
- **Accuracy:** 100% compliant with WCAG 2.2 contrast formulas.

---

### Phase 7: `reviews.py` Fast ISO Date Parser

**File:** `.agents/skills/replica-entrepreneur/reviews.py`

#### Changes:
1. Replaced `datetime.strptime` with fast ISO string slicing and `datetime.date.fromisoformat` validation.
2. Preserved strict format validation so invalid dates (e.g. `2024-04-31`) are rejected cleanly without silent corruption.
3. Added `--compact-json` and `--summary` modes.

#### Benchmark Results (5,000 review dates):
- **Baseline Runtime:** 245.59 ms
- **Optimized Runtime:** 6.00 ms (**40.9x speedup**)
- **Peak Memory:** 0.2 KB (down from 337.4 KB, **99.9% reduction**)
- **Accuracy:** 100% match on all date fixtures and edge cases.

---

### Phase 8: `imgdiff.py` Peak Memory and Layout Speedup

**File:** `.agents/skills/replica-diff/imgdiff.py`

#### Changes:
1. Replaced per-pixel `(r, g, b)` 3-tuple heap allocations with `_GREY_LUT` tuple indexing for monochrome pixels, eliminating hundreds of thousands of redundant heap objects.
2. Precomputed a 52-entry `_DIM_LUT` for grayscale dimming calculations.
3. Converted row edge-detection buffers in `edges()` to flat `bytearray(w)` instead of Python lists of integers.
4. Added `--compact-json` and `--summary` modes.

#### Benchmark Results (Comparison of two 480x800 RGB screenshots):
- **Baseline Runtime:** 9,011.08 ms
- **Optimized Runtime:** 7,163.34 ms (**20.5% faster**)
- **Baseline Peak Memory:** 94,998.0 KB (~92.8 MB)
- **Optimized Peak Memory:** 23,644.9 KB (~23.1 MB) (**4.0x reduction in RAM**)
- **Score:** Exactly 78.7 (100% metric preservation).

---

### Phase 9: Compact Utility Outputs

All six Python CLI tools now support two standardized output reduction flags:

1. `--compact-json`: Outputs unindented JSON on a single line (`separators=(",", ":")`), stripping whitespace to save 40% to 65% of output tokens when an agent executes tools via bash or powershell.
2. `--summary`: Outputs a single concise line with key status and counts, ideal for agent decision-making when full detail is not required.

| Tool | Default Output Sample | `--summary` Output Sample | Token Savings |
|---|---|---|---|
| `parity.py` | Full multi-table ASCII report | `Parity score: 85.0/100 (shippable: False, missing must-haves: 2)` | ~85% |
| `sweep.py` | Multi-line hit table with lines | `Clean sweep: 0 brand hits found.` / `Sweep: 3 brand hits in 2 files.` | ~90% |
| `contrast.py` | Full multi-pair rating table | `Contrast: 12 pairs tested, 12 passed, 0 failed.` | ~80% |
| `reviews.py` | Complete feedback breakdown | `Reviews: 145 reviews analyzed across 4 themes.` | ~88% |
| `listing.py` | Store limit breakdown | `Listing: 0 errors, 1 warnings across 2 stores.` | ~75% |
| `imgdiff.py` | Multi-field JSON or report | `Layout match score: 78.7% (2 changed regions)` | ~70% |

---

### Phase 10: Regression Verification and Test Suite Expansion

The test suite was expanded from 58 to 72 automated unit tests across 7 test modules:

```pwsh
python -m unittest discover -s tests -v
```

**Results:** Ran 72 tests in 1.113s. All 72 passed.

Key tests added:
- `test_frontmatter_name_and_description`: Validates YAML frontmatter presence, valid structure, and length bounds (150 to 350 chars) on parsed descriptions.
- `test_local_reference_links`: Validates that all local Markdown reference links resolve to existing files.
- `test_no_em_dashes_anywhere`: Verifies zero em-dashes (`\u2014`) across all repository files.
- `test_compact_json_and_summary_flags`: Validates `--compact-json` and `--summary` functionality across all 6 tools.
- `test_lut_matches_exact_srgb_channels`: Validates that `_SRGB_LUT` is identical to floating-point exponent calculations for all channel values [0..255].
- `test_parse_date_formats_and_edge_cases`: Validates strict rejection of invalid dates (e.g. `2024-04-31`).
- `test_generated_directories_skipped`: Validates that `bin`, `obj`, `.vs`, and `.idea` are skipped by `sweep.py`.

---

### Summary of Measured Improvements

| Metric | Baseline | Optimized | Improvement |
|---|---|---|---|
| **System Prompt Discovery Metadata** | 5,700 chars (927 words) | 2,916 chars (377 words) | **-48.8% (~700 tokens saved / turn)** |
| **`replica-workflow` Body Context** | 819 words (7,489 chars) | 410 words (3,181 chars) | **-50.0% words (-57.5% chars)** |
| **Total Instruction Body Words** | 7,646 words | 6,895 words | **-751 words (-9.8%) via progressive disclosure** |
| **`reviews.py` Date Parsing Runtime** | 245.59 ms | 6.00 ms | **40.9x speedup** |
| **`reviews.py` Date Parsing RAM** | 337.4 KB | 0.2 KB | **99.9% reduction** |
| **`imgdiff.py` Peak RAM** | 94,998 KB (~92.8 MB) | 23,645 KB (~23.1 MB) | **4.0x memory reduction** |
| **`imgdiff.py` Runtime** | 9,011.08 ms | 7,163.34 ms | **20.5% speedup** |
| **`sweep.py` Runtime** | 1,076.34 ms | 761.20 ms | **29.3% speedup** |
| **`contrast.py` Runtime** | 764.59 ms | 531.36 ms | **30.5% speedup** |
| **Tool CLI Output Tokens** | Multi-line ASCII / indented JSON | `--compact-json` / `--summary` | **70% to 90% fewer output tokens** |
| **Unit Test Coverage** | 58 tests | 72 tests | **+14 tests (100% pass rate)** |
