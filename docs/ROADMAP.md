# Roadmap — offboarding-sme-clone

## Milestone 1: Parser Prototypes (Current)

- [x] Slack export parser (ZIP/JSON → per-channel markdown)
- [x] Email archive parser (mbox/eml → per-thread markdown)
- [x] PDF parser (text extraction with layout preservation)
- [x] Word parser (docx → markdown)
- [x] PowerPoint parser (pptx → markdown with speaker notes)
- [x] Excel parser (xlsx → markdown tables)
- [x] Parser dispatch logic in `setup.py`
- [x] Markdown/text pass-through parser
- [x] Code file pass-through parser (with language tagging)
- [x] Synthetic test fixtures (`test-example/`)
- [x] Unit tests for each parser using `test-example/` fixtures

## Milestone 2: Index & Tone Engine

- [x] `_INDEX.md` generator (recursive file crawler with category mapping)
- [x] `tone_profile.md` extractor (analysis framework template)
- [x] LLM integration for summarization and tone analysis (via host agent — Antigravity, Claude Code, or Cursor)

## Milestone 3: Skill Generator

- [x] Identify domains/topic clusters from `_INDEX.md` (via AI agent)
- [x] Generate `SKILL.md` files with triggers, decision trees, evidence pointers (via AI agent)
- [x] YAML frontmatter schema for skill manifests

## Milestone 4: Agent Skill Definitions

- [x] Antigravity skill definition (`.gemini/` custom instructions)
- [x] Claude Code skill definition (`CLAUDE.md`)
- [x] Cursor skill definition (`.cursorrules`)
- [x] End-to-end testing with each coding agent (Antigravity validation)

## Milestone 5: CI / Release

- [x] GitHub Actions CI pipeline
- [x] Unit test coverage (pytest suite for all parsers)
- [x] README with quickstart guide
- [x] First tagged release (v0.1.0)
