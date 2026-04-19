# offboarding-sme-clone

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: v0.1.0 Release](https://img.shields.io/badge/status-v0.1.0%20release-brightgreen.svg)]()
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

| Artifact | What It Is |
| :--- | :--- |
| **`parsed/`** | Every raw file converted to clean, readable markdown. Slack JSON → channel conversations. mbox → email threads. PDF/DOCX/PPTX/XLSX → plain text. |
| **`_INDEX.md`** | A document catalog with a one-paragraph summary of each file, key topics, and cross-references. The agent reads this first. |
| **`tone_profile.md`** | The SME's communication style — vocabulary patterns, explanation structure, humor, directness level. |
| **`skills/*.md`** | One file per domain of expertise. Contains triggers ("when to consult this skill"), decision trees, and evidence pointers back to source documents. |

## Supported File Formats

| Format | What It Does |
| :--- | :--- |
| Slack export (`.zip`) | Unpacks JSON, filters by SME, groups by channel |
| Email archive (`.mbox`, `.eml`) | Parses threads, strips MIME noise |
| PDF | Text extraction with layout preservation |
| Word (`.docx`) | Paragraph and heading extraction |
| PowerPoint (`.pptx`) | Slide text + speaker notes |
| Excel (`.xlsx`) | Sheet-by-sheet table extraction |
| Markdown / text / code | Pass-through |

## Coding Agent Support

The repo includes ready-to-use skill definitions:

| Agent | File | Setup |
| :--- | :--- | :--- |
| **Google Antigravity** | `skill_definitions/antigravity/` | Copy to your `.gemini/` directory |
| **Claude Code** | `skill_definitions/claude_code.md` | Copy to your project as `CLAUDE.md` |
| **Cursor** | `skill_definitions/cursor.cursorrules` | Copy to your project as `.cursorrules` |

Each skill definition teaches the agent how to navigate the knowledge base and respond in the SME's voice.

## Test Example

The [`test-example/`](test-example/) folder contains synthetic sample data and pre-generated output so you can see exactly what the tool produces without running it on real data.

```bash
# Run the pipeline against the test data
uv run sme-clone --source ./test-example --sme-email jane@example.com
```

Browse the output at [`test-example/.sme-clone/`](test-example/.sme-clone/) — it includes a sample `_INDEX.md`, `tone_profile.md`, and a `SKILL.md` for API design patterns.

## Project Structure

```
offboarding-sme-clone/
├── sme_clone/                    # Main package (formerly scripts/)
│   ├── setup.py                  # Main entry point
│   ├── parsers/                  # Format-specific parsers
│   ├── indexer.py                # Generates _INDEX.md
│   ├── tone_extractor.py         # Generates tone_profile.md
│   └── skill_generator.py        # Generates SKILL.md files
├── skill_definitions/            # Agent skill templates
├── test-example/                 # Sample data + expected output
├── docs/
│   ├── PRODUCT_SPEC.md           # Full product specification
│   └── ROADMAP.md                # Development roadmap
├── pyproject.toml
└── README.md
```

## Status

🚀 **v0.1.0 Release.** All core format parsers, index generation, tone extraction, and skill generation features are fully implemented. The pipeline works end-to-end to parse Slack, emails, PDFs, Word docs, PowerPoints, and Excel sheets into structured markdown artifacts. See the [roadmap](docs/ROADMAP.md) for full details on completed milestones.

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
