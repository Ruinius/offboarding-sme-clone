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

- [x] Antigravity skill definition (`.gemini/` custom instructions)
- [x] Claude Code skill definition (`CLAUDE.md`)
- [x] Cursor skill definition (`.cursorrules`)
- [ ] End-to-end testing with each coding agent

## Milestone 5: CI / Release

- [ ] GitHub Actions CI pipeline
- [ ] Unit test coverage
- [x] README with quickstart guide
- [ ] First tagged release
