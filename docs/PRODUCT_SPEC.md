# Product Vision: offboarding-sme-clone

## The Problem

Every organization has experienced it: a senior engineer or domain expert leaves, and months of tribal knowledge — the _why_ behind architectural decisions, the unwritten rules about legacy systems, the intuition for debugging production — vanishes overnight. What remains are stale wikis, scattered Slack threads, and teammates left guessing.

This is the **knowledge vacuum** problem, and it's one of the most expensive, invisible costs of employee turnover in software engineering.

## The Vision

**offboarding-sme-clone** is an open-source developer toolkit for **opt-in, curated knowledge offboarding**. It enables departing subject-matter experts (SMEs) to export their decision-making logic, institutional memory, and personal reasoning style into a portable, queryable artifact — before they walk out the door.

> _"Export your decision-making logic before you leave your next job."_

The end result is not a chatbot. It is a **structured agent skill** — a set of plain markdown files that any coding agent (Antigravity, Claude Code, Cursor, etc.) can consume to answer questions _as_ the departed expert.

## Who Is This For?

| Persona                      | Use Case                                                                         |
| :--------------------------- | :------------------------------------------------------------------------------- |
| **Departing Engineers**      | Capture and preserve your expertise as a professional contribution to your team. |
| **Engineering Managers**     | Reduce onboarding friction and knowledge-loss risk during team transitions.      |
| **AI/Agent Developers**      | Consume structured SME skills as plug-in modules for agentic workflows.          |
| **Open-Source Contributors** | Build and share reusable "SME persona templates" for the community.              |

## How It Works

### Prerequisites

The user has a coding agent — **Google Antigravity** (default), **Claude Code**, **Cursor**, or similar — already set up in their development environment.

### User Journey

1. **Departing engineer curates their knowledge.** They place key files — Slack exports, email exports, presentations, spreadsheets, PDFs, design docs — into a **Google Drive folder** (or another corporate-controlled shared storage like SharePoint or OneDrive).

2. **Any teammate clones this repo** to their local machine.

3. **The teammate points the tool at the shared folder.** A single setup command processes the raw documents and generates structured artifacts back into the same folder:

   ```bash
   uv run python scripts/setup.py --source "G:/My Drive/offboarding/jane-doe" --sme-email jane@company.com
   ```

4. **The tool runs a two-stage pipeline:**

   **Stage 1 — Parse:** The tool detects each file's format and converts it into clean, readable markdown. Slack export ZIPs are unpacked and filtered for the SME's messages (grouped by channel). Email archives (`.mbox`, `.eml`) are parsed into threaded conversations. PDFs, Word docs, PowerPoint decks, and spreadsheets are extracted to plain text. The parsed output is stored in `.sme-clone/parsed/`.

   **Stage 2 — Analyze:** The tool reads the parsed markdown and generates three categories of knowledge artifacts:
   - **`_INDEX.md`** — A document catalog with a one-paragraph summary of every parsed file, its path, key topics, and entities. This is the agent's table of contents.
   - **`tone_profile.md`** — The SME's extracted communication style: how they explain things, what analogies they reach for, their level of directness, their humor, their go-to phrases.
   - **`skills/*.md`** — One `SKILL.md` file per domain of expertise, containing triggers, decision trees, and evidence pointers back to parsed source documents.

5. **The teammate opens their coding agent and asks questions.** The agent reads the generated artifacts, navigates to the parsed source documents when needed, and responds with facts — in the departing engineer's voice and style.

### Folder Structures

There are two separate folder structures: the **repo** (the tool) and the **Google Drive folder** (the data). The repo runs locally on the teammate's machine; the Drive folder is shared corporate storage where the SME's knowledge lives.

#### The Repo (what the teammate clones)

```
offboarding-sme-clone/                # This repository
├── scripts/
│   ├── setup.py                      # Main entry point: parse → analyze pipeline
│   ├── parsers/
│   │   ├── slack_parser.py           # Slack export ZIP/JSON → markdown
│   │   ├── email_parser.py           # mbox/eml → markdown
│   │   ├── pdf_parser.py             # PDF → markdown
│   │   ├── docx_parser.py            # Word → markdown
│   │   ├── pptx_parser.py            # PowerPoint → markdown
│   │   └── xlsx_parser.py            # Excel → markdown
│   ├── indexer.py                    # Generates _INDEX.md from parsed files
│   ├── tone_extractor.py             # Generates tone_profile.md
│   └── skill_generator.py            # Generates SKILL.md files
├── skill_definitions/
│   ├── antigravity/                  # .gemini/ custom instructions template
│   ├── claude_code.md                # CLAUDE.md template
│   └── cursor.cursorrules            # .cursorrules template
├── test-example/                     # Sample data + expected output
│   ├── sample_slack_export.zip       # Synthetic Slack export for testing
│   ├── sample_design_doc.pdf         # Sample PDF input
│   ├── sample_emails.mbox            # Synthetic email archive
│   └── .sme-clone/                   # Pre-generated output (committed to repo)
│       ├── parsed/
│       │   ├── slack/
│       │   │   └── general.md
│       │   ├── email/
│       │   │   └── thread_api_redesign.md
│       │   └── docs/
│       │       └── sample_design_doc.md
│       ├── _INDEX.md
│       ├── tone_profile.md
│       └── skills/
│           └── api_design_patterns.md
├── docs/
│   ├── PRODUCT_SPEC.md               # This document
│   └── ROADMAP.md
├── pyproject.toml
└── README.md
```

The `test-example/` folder serves two purposes: it is a **test fixture** for validating the scripts during development, and a **demo** that shows new users exactly what the tool produces — before they run it on real data. The `.sme-clone/` subfolder inside it is **committed to the repo** so the expected output is always visible.

This repo contains **no real user data** — only scripts, configuration, and synthetic test examples.

#### The Google Drive Folder (where the knowledge lives)

```
Google Drive (or SharePoint, OneDrive, etc.)
└── offboarding/jane-doe/
    │
    │  ── Raw: what the SME drops in ──────────────────
    ├── slack_export.zip
    ├── architecture_decisions.pdf
    ├── incident_runbooks.docx
    ├── quarterly_planning.pptx
    ├── budget_model.xlsx
    ├── gmail_takeout.mbox
    │
    │  ── Generated: what the tool creates ────────────
    └── .sme-clone/
        ├── parsed/                   # Stage 1: format conversion
        │   ├── slack/
        │   │   ├── incident-response.md
        │   │   └── architecture-decisions.md
        │   ├── email/
        │   │   ├── thread_redis_migration.md
        │   │   └── thread_deploy_incident.md
        │   └── docs/
        │       ├── architecture_decisions.md
        │       ├── incident_runbooks.md
        │       ├── quarterly_planning.md
        │       └── budget_model.md
        ├── _INDEX.md                 # Stage 2: document catalog & summaries
        ├── tone_profile.md           # Stage 2: voice, style, personality
        └── skills/                   # Stage 2: decision logic
            ├── debugging_redis.md
            ├── deploy_pipeline.md
            └── capacity_planning.md
```

The SME populates the root of this folder with raw files. The tool writes everything under `.sme-clone/`. **Nothing flows back into the repo.**

#### How they connect

```
┌─────────────────────────┐         ┌──────────────────────────────────┐
│  Teammate's Machine     │         │  Google Drive (shared)            │
│                         │         │                                  │
│  offboarding-sme-clone/ │──runs──▶│  offboarding/jane-doe/           │
│  (cloned repo)          │  setup  │    ├── raw files (SME uploads)   │
│                         │  script │    └── .sme-clone/ (generated)   │
└─────────────────────────┘         └──────────────────────────────────┘
                                                    │
                                                    │ reads
                                                    ▼
                                    ┌──────────────────────────────────┐
                                    │  Coding Agent                    │
                                    │  (Antigravity / Claude / Cursor) │
                                    │  answers questions using         │
                                    │  _INDEX.md + tone_profile.md     │
                                    │  + skills/*.md                   │
                                    └──────────────────────────────────┘
```

One share link gives a teammate access to the raw source material, the parsed readable versions, and the generated knowledge artifacts. Access control is handled entirely by the corporate storage platform.

## Core Principles

### 1. Zero Infrastructure

There is no server to deploy, no database to run, no API to host. The tool generates **plain markdown files** into a shared folder. The coding agent the team already uses is the query interface. If you can clone a repo and run a Python script, you can use this tool.

### 2. Privacy via Curation

Privacy is enforced at two boundaries: the **SME decides what files to share**, and the **organization controls access** to the shared folder. No data passes through third-party infrastructure. The only external call is from the teammate's coding agent to its own LLM provider — which is already configured and approved by the organization.

### 3. Structured Over Conversational

The primary output is the **`SKILL.md` manifest** — a standardized, machine-readable document that captures triggers, decision trees, and evidence pointers. Conversation is a means to an end, not the product itself.

### 4. Agent-Native, Agent-Agnostic

The generated artifacts are plain markdown — readable by any coding agent, any LLM, or any human. The repo ships with skill definitions for Antigravity (`.gemini/`), Claude Code (`CLAUDE.md`), and Cursor (`.cursorrules`), but the artifacts themselves are format-agnostic.

### 5. Graceful Degradation

The tool provides value at three layers, each requiring progressively less tooling:

| Layer                       | What You Get                                                                   | What You Need                             |
| :-------------------------- | :----------------------------------------------------------------------------- | :---------------------------------------- |
| **Layer 1: SKILL.md Files** | Decision trees, triggers, logic flows — readable by any human or AI assistant. | Nothing. Just open the markdown files.    |
| **Layer 2: Indexed Search** | Document catalog with summaries, topics, and cross-references.                 | The generated `_INDEX.md` file.           |
| **Layer 3: Persona Query**  | Full conversational access in the SME's voice with evidence linking.           | A coding agent + the generated artifacts. |

## Key Capabilities

### Format Parsing

Detect and convert heterogeneous file formats into clean, readable markdown:

| Input Format                    | Parser                                                                | Output                                            |
| :------------------------------ | :-------------------------------------------------------------------- | :------------------------------------------------ |
| Slack export (`.zip` of JSON)   | Unzip, filter by SME user ID, group by channel, strip system messages | One `.md` per channel with threaded conversations |
| Email archive (`.mbox`, `.eml`) | Parse headers/body, group by thread, strip signatures/MIME noise      | One `.md` per conversation thread                 |
| PDF                             | Text extraction with layout preservation                              | One `.md` per document                            |
| Word (`.docx`)                  | Paragraph and heading extraction                                      | One `.md` per document                            |
| PowerPoint (`.pptx`)            | Slide-by-slide text extraction with speaker notes                     | One `.md` per presentation                        |
| Excel (`.xlsx`)                 | Sheet-by-sheet tabular extraction                                     | One `.md` per workbook                            |
| Markdown / plain text           | Pass-through (copy as-is)                                             | One `.md` per file                                |
| Code files                      | Pass-through with language tagging                                    | One `.md` per file                                |

All parsed output is written to `.sme-clone/parsed/` and becomes the input for the analysis stage.

### Knowledge Indexing

Process the parsed markdown files into a structured document catalog (`_INDEX.md`) containing a one-paragraph summary of every file, its path, key topics, entities, and cross-references. This is the agent's primary entry point for navigating the knowledge base.

### Tone & Style Extraction

Analyze a SME's writing across documents to capture their unique voice — how they explain things, what analogies they reach for, their level of directness. The resulting `tone_profile.md` enables the coding agent to respond not just with _what_ the SME knew, but _how_ they communicated.

### Skill Manifest Generation

Synthesize ingested knowledge into `SKILL.md` files — portable, versioned artifacts containing:

- **Triggers** — When to consult this skill (e.g., "debugging Redis latency spikes").
- **Decision Trees** — Concrete logic flows with branch conditions.
- **Evidence** — Pointers back to specific source documents and sections.

### Multi-Agent Skill Definitions

The repo includes ready-to-use skill definitions for major coding agents:

| Agent                  | Skill File                     | How It Works                                                            |
| :--------------------- | :----------------------------- | :---------------------------------------------------------------------- |
| **Google Antigravity** | `.gemini/` custom instructions | Agent reads artifacts from the shared folder and responds in character. |
| **Claude Code**        | `CLAUDE.md` at repo root       | Same artifacts, Claude-native instruction format.                       |
| **Cursor**             | `.cursorrules`                 | Same artifacts, Cursor-native instruction format.                       |

Each skill definition teaches the agent the folder structure, how to read the index and SKILL files, and how to apply the tone profile when responding.

## What Success Looks Like

1. A departing engineer spends a focused afternoon dragging their key documents into a shared Google Drive folder.
2. A teammate clones this repo and runs a single setup command pointed at the folder.
3. The tool processes everything and generates `_INDEX.md`, `tone_profile.md`, and a set of `SKILL.md` files — all written back into the same folder.
4. The laptop goes back to IT. **The knowledge survives in the shared folder.**
5. Months later, a new teammate hits an obscure production issue. They open Antigravity (or Claude Code, or Cursor), ask a question, and the agent walks them through the exact debugging logic the original engineer would have used — in their voice, citing specific documents.
6. The knowledge didn't leave with the person. It's still there, structured, queryable, and useful.

## Differentiation

| Approach                        | Limitation                                        | How We Differ                                         |
| :------------------------------ | :------------------------------------------------ | :---------------------------------------------------- |
| Internal wikis / Confluence     | Stale within weeks; no structured reasoning.      | `SKILL.md` encodes _decision logic_, not just facts.  |
| Generic RAG chatbots            | No personality, no curation, no structure.        | Tone extraction + structured index + manifest format. |
| Exit interviews / handoff docs  | One-shot, unstructured, rarely referenced again.  | Living, queryable artifacts with evidence linking.    |
| Proprietary knowledge platforms | Vendor lock-in, server infrastructure, expensive. | Zero infrastructure, open-source, agent-agnostic.     |

## Long-Term Direction

1. **Community SME Templates** — A library of shareable persona archetypes (e.g., "The Legacy Code Whisperer", "The Infrastructure Firefighter") that teams can fork and customize.
2. **Incremental Re-indexing** — Detect new files added to the shared folder and update artifacts without re-processing the entire corpus.
3. **Team-Scale Personas** — Support for merging multiple SME knowledge bases into a unified team knowledge agent.
4. **Guided Interview Mode** — An interactive session (run through the coding agent) that systematically draws out decision-making logic from the SME through targeted questions.
5. **Cross-Agent Compatibility Testing** — Automated validation that skill definitions work correctly across Antigravity, Claude Code, and Cursor.
