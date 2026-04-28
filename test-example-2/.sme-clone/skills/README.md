# SME Expert Skills

This directory contains structured skill manifests (`SKILL.md`) derived from the SME's documents.

## How to Generate Skills
Since skill synthesis requires deep reasoning, this tool relies on your AI agent to populate the manifests.

1. Open `_INDEX.md` and identify key domains (e.g., 'Deployment Logic', 'Auth Architecture').
2. For each domain, ask your AI agent:
   > 'Read all relevant files in `.sme-clone/parsed/` for the [Domain] topic and generate a `SKILL.md` manifest.'

## Manifest Schema
Each `SKILL.md` should follow this structure:
- **Triggers**: When the agent should activate this skill.
- **Context**: Background knowledge and entities.
- **Decision Logic**: IF/THEN flows and decision trees.
- **Evidence**: Links back to parsed markdown files for auditability.
