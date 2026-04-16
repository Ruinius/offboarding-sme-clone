# Project Plan: offboarding-sme-clone

## 1. Vision & Strategy

**The Hook:** "The open-source toolkit for opt-in curated offboarding. Export your decision-making logic before you leave your next job."

Positioning the project as a **Developer Tool** for "Agent Skills" (2026 Trend) rather than a simple chatbot. The goal is to reach 1k+ GitHub stars by solving the "knowledge vacuum" problem when senior developers leave.

## 2. Core Technical Artifacts

### The "Skill Manifest" (`SKILL.md`)

A standardized, machine-readable format for decision-making logic.

- **Format:** Markdown with YAML frontmatter.
- **Fields:**
  - `Triggers`: When to consult this SME.
  - `Decision Tree`: Logic flows (e.g., "If latency > 200ms, check Redis").
  - `Evidence`: Pointers to LanceDB vector chunks.

### Agentic Search (Layered Reasoning)

- **Layer 1:** Local codebase and documentation (LanceDB).
- **Layer 2:** External context/archives (Slack, Jira, etc.).
- **Result:** Agent synthesizes evidence and summarizes in the user's specific tone.

## 3. Technical Stack

| Component         | Technology              | Rationale                                                     |
| :---------------- | :---------------------- | :------------------------------------------------------------ |
| **Vector DB**     | LanceDB                 | "The vector DB for local SMEs"—high performance, local-first. |
| **Orchestration** | LangGraph / Pydantic AI | Robust handling of search loops and agentic logic.            |
| **Inference**     | Ollama                  | Privacy-centric, local-first execution.                       |
| **Interface**     | TUI (Rich / Textual)    | High "star appeal" for developers; fast and keyboard-driven.  |

## 4. Implementation Roadmap

### Phase 1: Foundation & Ingestion

- [ ] Initialize Python environment and project structure.
- [ ] Implement local document ingestion pipeline (Markdown, PDF, Code).
- [ ] Integrate **LanceDB** for vector storage.
- [ ] Build basic RAG (Retrieval Augmented Generation) logic using local LLM via Ollama.

### Phase 2: The Skill Manifest Engine

- [ ] Define the `SKILL.md` specification.
- [ ] Create a "Tone Extractor" script to analyze personal writing styles.
- [ ] Develop logic to generate `SKILL.md` manifests from ingested data/interviews.
- [ ] Build visual "Decision Tree" generation (Mermaid support in Markdown).

### Phase 3: Agentic Reasoning Loop

- [ ] Implement **LangGraph** workflows for multi-layer search.
- [ ] Add support for "Evidence Linking" (verbatim quotes + source paths).
- [ ] Refine "Agent Personality" prompt injection based on SME profiles.

### Phase 4: Developer Experience (TUI)

- [ ] Build a sleek terminal dashboard using **Textual**.
- [ ] Implement `sme-mirror chat` and `sme-mirror ingest` commands.
- [ ] Add an animated "Agent Thinking" indicator for CLI appeal.

## 5. GitHub Launch Strategy

### README Structure

1. **The "Why":** A relatable story of a project collapse after a key dev leaves.
2. **Quick Start:** The 3-command installer (`pip install`, `ingest`, `chat`).
3. **Demo Gif:** High-quality TUI recording showing layered search.
4. **Tone Extractor Demo:** Converting dry docs into a personality-driven agent.
5. **Call to Contribution:** "SME Templates" (e.g., "The Legacy Code Whisperer", "Sassy Project Manager").

### Initial SME Persona Demos

- **Primary Demo:** _The Legacy Code Whisperer_ — Explains 10-year-old "spaghetti" logic with historical context.
- **Secondary Demo:** _The Sassy Project Manager_ — Answers "When will this be done?" with realistic, data-backed skepticism.

## 6. Success Metrics

- [ ] GitHub Stars: 1,000+
- [ ] Community SME Templates: 10+
- [ ] Integration with at least one major Agentic Framework (e.g., AutoGPT skills).
