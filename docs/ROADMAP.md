# Roadmap — offboarding-sme-clone

## Milestone 1: Parser Prototypes (Current)

- [ ] Slack export parser (ZIP/JSON → per-channel markdown)
- [ ] Email archive parser (mbox/eml → per-thread markdown)
- [ ] PDF parser (text extraction with layout preservation)
- [ ] Word parser (docx → markdown)
- [ ] PowerPoint parser (pptx → markdown with speaker notes)
- [ ] Excel parser (xlsx → markdown tables)
- [ ] Parser dispatch logic in `setup.py`
- [ ] Unit tests for each parser using `test-example/` fixtures

## Milestone 2: Index & Tone Engine

- [ ] `_INDEX.md` generator (summarize each parsed file, extract topics/entities)
- [ ] `tone_profile.md` extractor (analyze writing style across documents)
- [ ] LLM integration for summarization and tone analysis
- [ ] Configuration for LLM provider (API key, model selection)

## Milestone 3: Skill Generator

- [ ] Identify domains/topic clusters from `_INDEX.md`
- [ ] Generate `SKILL.md` files with triggers, decision trees, evidence pointers
- [ ] YAML frontmatter schema for skill manifests

## Milestone 4: Agent Skill Definitions

- [ ] Antigravity skill definition (`.gemini/` custom instructions)
- [ ] Claude Code skill definition (`CLAUDE.md`)
- [ ] Cursor skill definition (`.cursorrules`)
- [ ] End-to-end testing with each coding agent

## Milestone 5: CI / Release

- [ ] GitHub Actions CI pipeline
- [ ] Unit test coverage
- [ ] README with quickstart guide
- [ ] First tagged release
