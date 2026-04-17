# Product Vision: offboarding-sme-clone

## The Problem

Every organization has experienced it: a senior engineer or domain expert leaves, and months of tribal knowledge — the _why_ behind architectural decisions, the unwritten rules about legacy systems, the intuition for debugging production — vanishes overnight. What remains are stale wikis, scattered Slack threads, and teammates left guessing.

This is the **knowledge vacuum** problem, and it's one of the most expensive, invisible costs of employee turnover in software engineering.

## The Vision

**offboarding-sme-clone** is an open-source developer toolkit for **opt-in, curated knowledge offboarding**. It enables departing subject-matter experts (SMEs) to export their decision-making logic, institutional memory, and personal reasoning style into a portable, queryable artifact — before they walk out the door.

> _"Export your decision-making logic before you leave your next job."_

The end result is not a chatbot. It is a **structured agent skill** — a machine-readable, human-auditable knowledge package that any agentic framework can consume.

## Who Is This For?

| Persona                      | Use Case                                                                         |
| :--------------------------- | :------------------------------------------------------------------------------- |
| **Departing Engineers**      | Capture and preserve your expertise as a professional contribution to your team. |
| **Engineering Managers**     | Reduce onboarding friction and knowledge-loss risk during team transitions.      |
| **AI/Agent Developers**      | Consume structured SME skills as plug-in modules for agentic workflows.          |
| **Open-Source Contributors** | Build and share reusable "SME persona templates" for the community.              |

## Deployment Model: Upload → Process → Query

**offboarding-sme-clone** is a **thin, VPC-hosted web application**. There is nothing to install locally — the departing engineer interacts with the app through a browser.

| Phase | Actor | What Happens |
| :---- | :---- | :----------- |
| **1. Upload** | Departing SME | Uploads curated files (Slack exports, emails, PDFs, code, docs) to a workspace via the web UI. |
| **2. Process** | App (automated) | Ingests documents into LanceDB, extracts tone & style, generates `SKILL.md` manifests. |
| **3. Query** | Any teammate | Searches the knowledge base or asks questions through the web UI or API. |

The SME curates what to upload; the app handles everything else. A teammate or manager can also upload files on the SME's behalf if preferred.

> **Key Assumption:** The app is deployed on the organization's **internal VPC or private cloud** and has access to an **enterprise LLM API key** (e.g., Azure OpenAI, AWS Bedrock, Google Vertex). No data leaves the organization's infrastructure boundary.

## Core Principles

### 1. Privacy-First & Org-Controlled

All data stays within the organization's **VPC or private cloud**. The app never phones home, never sends data to external services (except the configured enterprise LLM endpoint), and never exposes data outside the network boundary. Privacy is enforced at two levels: the **SME decides what to upload**, and the **organization controls the infrastructure** where it lives.

### 2. Structured Over Conversational

The primary output is the **`SKILL.md` manifest** — a standardized, machine-readable document with YAML frontmatter that captures triggers, decision trees, and evidence pointers. Conversation is a means to an end, not the product itself.

### 3. Agent-Native, Not Agent-Dependent

Skills produced by this tool are designed to be consumed by agentic frameworks (LangGraph, AutoGPT, etc.), but the tool itself is self-contained. No external agent platform is required to create or query a skill.

### 4. Graceful Degradation

The app provides value at three layers, each requiring progressively more configuration:

| Layer | What You Get | What You Need |
| :---- | :----------- | :------------ |
| **Layer 1: SKILL.md Files** | Decision trees, triggers, logic flows — readable by any human or AI assistant. | Just the app. Export files to any repo. |
| **Layer 2: Structured Search** | Semantic search over ingested docs with source citations. | The app. No LLM needed for retrieval. |
| **Layer 3: Agent Query** | Full conversational access in the SME's voice with evidence linking. | The app + enterprise LLM key. |

### 5. Developer-Grade UX

The interface is a clean, minimal web UI — fast, purposeful, and distraction-free. This is a tool built _by_ developers, _for_ developers. A CLI is available for scripted or headless workflows.

## Key Capabilities

### Knowledge Ingestion

Ingest local documentation, codebases, and written artifacts (Markdown, PDF, code files) into a local **LanceDB** vector store. This is the raw evidence base.

### Tone & Style Extraction

Analyze an SME's writing across documents to capture their unique voice — how they explain things, what analogies they reach for, their level of directness. The resulting agent doesn't just know _what_ the SME knew; it communicates _how_ they communicated.

### Skill Manifest Generation

Synthesize ingested knowledge into a `SKILL.md` file — a portable, versioned artifact containing:

- **Triggers** — When to consult this skill (e.g., "debugging Redis latency spikes").
- **Decision Trees** — Concrete logic flows with branch conditions.
- **Evidence** — Pointers back to source chunks in the vector store.

### Export

Any persona's knowledge artifacts can be exported as a portable archive for backup, migration, or integration with external systems:

```
exported_package/
├── skill_manifests/       # SKILL.md files (plain markdown)
├── vector_store/          # LanceDB data (file-based, self-contained)
├── tone_profile/          # Extracted voice/style metadata
└── manifest.json          # Package index and version info
```

Export is optional — the primary consumption path is through the app itself.

### Web UI & API

The app is a lightweight **FastAPI** server with a minimal web frontend:

- **Upload UI** — Drag-and-drop file upload into a persona workspace.
- **Query UI** — Search and converse with any persona.
- **REST API** — Programmatic access for integrations and agentic workflows.

It runs as a single Python process with minimal resource requirements — deployable on the smallest internal VM.

### Agentic Search (Layered Reasoning)

A multi-layer retrieval pipeline:

- **Layer 1:** Local codebase and documentation (LanceDB vectors).
- **Layer 2:** External context and archives (Slack exports, Jira dumps, etc.).
- **Synthesis:** The agent combines evidence across layers and responds in the SME's extracted tone, powered by the enterprise LLM.

## What Success Looks Like

1. A departing engineer spends a focused afternoon curating their key documents and uploading them to the app.
2. The app ingests everything, extracts their communication style, and generates a set of `SKILL.md` files — one per domain of expertise.
3. The laptop goes back to IT. **The knowledge survives on the VPC.**
4. Months later, a new teammate hits an obscure production issue. They open the app, query the departing engineer's persona, and the agent walks them through the exact debugging logic — in their voice, citing specific code and docs.
5. The knowledge didn't leave with the person. It's still there, structured, queryable, and useful.

## Differentiation

| Approach                        | Limitation                                       | How We Differ                                        |
| :------------------------------ | :----------------------------------------------- | :--------------------------------------------------- |
| Internal wikis / Confluence     | Stale within weeks; no structured reasoning.     | `SKILL.md` encodes _decision logic_, not just facts. |
| Generic RAG chatbots            | No personality, no curation, no structure.       | Tone extraction + layered search + manifest format.  |
| Exit interviews / handoff docs  | One-shot, unstructured, rarely referenced again. | Living, queryable artifacts with evidence linking.   |
| Proprietary knowledge platforms | Vendor lock-in, cloud-dependent, expensive.      | Self-hosted on your VPC, open-source, agent-framework agnostic. |

## Long-Term Direction

1. **Community SME Templates** — A library of shareable persona archetypes (e.g., "The Legacy Code Whisperer", "The Infrastructure Firefighter") that teams can fork and customize.
2. **Framework Integrations** — First-class skill adapters for major agentic platforms (AutoGPT, CrewAI, LangGraph).
3. **Team-Scale Deployment** — Support for merging multiple SME skills into a unified team knowledge agent.
4. **Guided Interview Mode** — An interactive session that systematically draws out decision-making logic from the SME through targeted questions.
