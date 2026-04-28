# offboarding-sme-clone

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: v0.1.0 Validated](https://img.shields.io/badge/status-v0.1.0%20validated-brightgreen.svg)]()
[![uv](https://img.shields.io/badge/uv-package%20manager-blueviolet.svg)](https://docs.astral.sh/uv/)
[![Agent: Antigravity](https://img.shields.io/badge/agent-Antigravity-4285F4.svg)]()
[![Agent: Claude Code](https://img.shields.io/badge/agent-Claude%20Code-D97706.svg)]()
[![Agent: Cursor](https://img.shields.io/badge/agent-Cursor-00D1B2.svg)]()

> _"Export your decision-making logic before you leave your next job."_

**offboarding-sme-clone** turns a departing engineer's documents into structured knowledge artifacts that any coding agent can query — in the engineer's own voice.

No server. No database. No deployment. Just markdown files and the coding agent you already use.

---

## The Problem

A senior engineer leaves. Months of tribal knowledge — the _why_ behind architectural decisions, the unwritten rules, the debugging intuition — vanishes overnight. What remains are stale wikis, scattered Slack threads, and teammates left guessing.

## The Solution

The departing engineer drops their key files into a shared Google Drive folder. A teammate clones this repo, runs a single command, and the tool generates structured knowledge artifacts back into that same folder. Any coding agent (Antigravity, Claude Code, Cursor) can then answer questions _as_ the departed expert.

## Quick Start

### Prerequisites

- [Python 3.11+](https://python.org)
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- A coding agent (Google Antigravity, Claude Code, Cursor, or similar)

### 1. Clone the repo

```bash
git clone https://github.com/Ruinius/offboarding-sme-clone.git
cd offboarding-sme-clone
uv sync
```

### 2. Point it at a shared folder

The departing engineer should have already placed their files (Slack exports, emails, PDFs, presentations, etc.) into a shared folder.

```bash
uv run sme-clone \
    --source "G:/My Drive/offboarding/jane-doe" \
    --sme-email jane@company.com
```

### 3. Ask questions through your coding agent

Open your coding agent, point it at the shared folder, and ask away. The agent reads the generated artifacts and responds with facts — in the departing engineer's voice.

## What It Produces

The tool runs a two-stage pipeline and writes everything into a `.sme-clone/` subfolder inside the shared folder:

```
shared-folder/
├── slack_export.zip              ← Raw: what the SME dropped in
├── design_doc.pdf
├── gmail_takeout.mbox
└── .sme-clone/                   ← Generated: what the tool creates
    ├── parsed/                   # Stage 1: format conversion
    │   ├── slack/general.md
    │   ├── email/thread_api_redesign.md
    │   └── docs/design_doc.md
    ├── _INDEX.md                 # Stage 2: document catalog
    ├── tone_profile.md           # Stage 2: voice & style
    └── skills/                   # Stage 2: decision logic
        └── api_design_patterns.md
```

| Artifact              | What It Is                                                                                                                                          |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`parsed/`**         | Every raw file converted to clean, readable markdown. Slack JSON → channel conversations. mbox → email threads. PDF/DOCX/PPTX/XLSX → plain text.    |
| **`_INDEX.md`**       | A document catalog with a one-paragraph summary of each file, key topics, and cross-references. The agent reads this first.                         |
| **`tone_profile.md`** | The SME's communication style — vocabulary patterns, explanation structure, humor, directness level.                                                |
| **`skills/*.md`**     | One file per domain of expertise. Contains triggers ("when to consult this skill"), decision trees, and evidence pointers back to source documents. |

## Supported File Formats

| Format                          | What It Does                                    |
| :------------------------------ | :---------------------------------------------- |
| Slack export (`.zip`)           | Unpacks JSON, filters by SME, groups by channel |
| Email archive (`.mbox`, `.eml`) | Parses threads, strips MIME noise               |
| PDF                             | Text extraction with layout preservation        |
| Word (`.docx`)                  | Paragraph and heading extraction                |
| PowerPoint (`.pptx`)            | Slide text + speaker notes                      |
| Excel (`.xlsx`)                 | Sheet-by-sheet table extraction                 |
| MHTML (`.mhtml`)                | Text extraction from HTML components            |
| Markdown / text / code          | Pass-through                                    |

## Coding Agent Support

The repo includes ready-to-use skill definitions:

| Agent                  | File                                   | Setup                                  |
| :--------------------- | :------------------------------------- | :------------------------------------- |
| **Google Antigravity** | `skill_definitions/antigravity/`       | Copy to your `.gemini/` directory      |
| **Claude Code**        | `skill_definitions/claude_code.md`     | Copy to your project as `CLAUDE.md`    |
| **Cursor**             | `skill_definitions/cursor.cursorrules` | Copy to your project as `.cursorrules` |

Each skill definition teaches the agent **two skills**: how to answer questions in the SME's voice, and how to autonomously run the full clone-generation pipeline (Stage 1 parse + Stage 2 analysis).

## Test Examples

### `test-example-2/` — Warren Buffett Letters (Real-World Validated)

The [`test-example-2/`](test-example-2/) folder contains Warren Buffett's Berkshire Hathaway Chairman's Letters from 1977–2024 (48 files: MHTML + PDF). This is the primary showcase — a complete, validated run of the full pipeline on real data.

The generated artifacts in [`test-example-2/.sme-clone/`](test-example-2/.sme-clone/) include:
- **`_INDEX.md`** — Full catalog of all 48 letters with per-document summaries and topic cross-references
- **`tone_profile.md`** — Deep analysis of Buffett's plain-spoken style, bottom-up reasoning, dry humor, and error-acknowledgment patterns
- **`skills/investment_philosophy.md`** — His 4-criterion stock selection framework and hold/sell logic
- **`skills/business_evaluation.md`** — The 6 acquisition criteria, franchise vs. commodity distinction, founder-seller dynamics
- **`skills/insurance_and_float.md`** — Float concept, combined ratio interpretation, fortress capital philosophy
- **`skills/capital_allocation.md`** — The 5-way capital hierarchy, share buyback criteria, owner earnings vs. EBITDA
- **`skills/management_philosophy.md`** — Decentralized operating model, how to identify great managers, succession

To generate your own clone from this data, ask your agent:

> _"Generate an SME clone for `./test-example-2`"_

### `test-example-1/` — Synthetic Sample Data

The [`test-example-1/`](test-example-1/) folder contains synthetic sample data with pre-generated output — useful for understanding the output format without running the full pipeline.

## Live Demo

Here is the clone answering a real question, grounded strictly in the source letters:

**Q: What is Warren Buffett's perspective on his American Express investment?**

> American Express is the investment that taught me what "durable competitive advantage" actually means in practice — not as a theory, but as something you can feel when you own a piece of a business for thirty years and watch it keep compounding while you do precisely nothing.
>
> Berkshire essentially completed its purchases of American Express shares by 1995. The total cost: approximately $1.3 billion. The annual dividend in 1995 was $41 million. By 2022 — without buying a single additional share — that dividend had grown to $302 million. Our ownership percentage rose from 12.6% to 17.9% entirely because the company was repurchasing its own shares; we did nothing. In 2018, our share of Amex's earnings was $1.2 billion — approximately 96% of the entire $1.3 billion we originally paid.
>
> The lesson: **the weeds wither away in significance as the flowers bloom.** When you find a truly wonderful business, stick with it. Patience pays, and one wonderful business can offset many mediocre decisions.
>
> _— Warren Buffett (synthesized from 1997, 2004, 2018, 2022, 2023 letters)_

**Q: What does Warren Buffett think about General Mills?**

> I have to be straight with you: General Mills does not appear in my thinking as a company I have studied, owned, or written about in any meaningful way. In 48 years of Chairman's letters, the name comes up exactly once — a passing illustration in 1988 about the breakfast cereal industry's return on capital versus auto insurance. An honest "I don't know" is worth considerably more than a confident answer built on thin foundations.
>
> _— Warren Buffett (synthesized from 1988 letter; no position held across 1977–2024)_

The clone correctly refused to fabricate a view Buffett never expressed — a critical property for knowledge artifacts intended for real use.

## Project Structure

```
offboarding-sme-clone/
├── sme_clone/                    # Main package
│   ├── setup.py                  # Main entry point & file dispatcher
│   ├── parsers/                  # Format-specific parsers
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   ├── pptx_parser.py
│   │   ├── xlsx_parser.py
│   │   ├── mhtml_parser.py
│   │   ├── email_parser.py
│   │   └── slack_parser.py
│   ├── indexer.py                # Generates _INDEX.md
│   ├── tone_extractor.py         # Generates tone_profile.md
│   └── skill_generator.py        # Generates SKILL.md files
├── skill_definitions/            # Agent skill templates
│   ├── antigravity/skill.md      # Skill 1: answer as SME
│   ├── antigravity/generate_clone.md  # Skill 2: run the pipeline
│   ├── claude_code.md            # Both skills for Claude Code
│   └── cursor.cursorrules        # Both skills for Cursor
├── test-example-1/               # Synthetic sample data + expected output
├── test-example-2/               # Warren Buffett letters (real-world test)
├── docs/
│   ├── PRODUCT_SPEC.md           # Full product specification
│   └── ROADMAP.md                # Development roadmap
├── pyproject.toml
└── README.md
```

## Status

✅ **v0.1.0 — End-to-End Validated.** All core format parsers (including MHTML), index generation, tone extraction, and skill generation are fully implemented and validated on real-world data. The full pipeline was run on 48 Warren Buffett Chairman's Letters (1977–2024), producing a complete knowledge base that was then queried live — including a case where the clone correctly refused to fabricate a view the SME never expressed. Each supported agent has two agentic skills: answering questions in the SME's voice, and autonomously running the full clone pipeline. See the [roadmap](docs/ROADMAP.md) for full details on completed milestones.

## Forking

This is a personal project. You're welcome to **fork it** and build on it — that's encouraged! However, I'm not accepting pull requests or external contributions at this time.

## Other Projects

Explore more of my work:

- [**tiger-cafe**](https://github.com/Ruinius/tiger-cafe) — A high-performance, modern web application showcase.
- [**tiger-transformer**](https://github.com/Ruinius/tiger-transformer) — Advanced model transformation utilities for AI engineers.
- [**financial-analyst-skills**](https://github.com/Ruinius/financial-analyst-skills) — A comprehensive suite of agentic skills for financial modeling.

## License

[MIT](LICENSE) — do whatever you want with it.

## Further Reading

- [Product Specification](docs/PRODUCT_SPEC.md) — Full vision, architecture, and design decisions.
- [Roadmap](docs/ROADMAP.md) — What's built, what's next.
