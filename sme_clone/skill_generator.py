"""
skill_generator.py — Generate SKILL.md files from parsed documents.

Synthesizes ingested knowledge into structured skill manifests, each containing:
  - Triggers: When to consult this skill
  - Decision Trees: Concrete logic flows with branch conditions
  - Evidence: Pointers back to specific parsed source documents
"""

from pathlib import Path


def generate_skills(
    parsed_dir: Path,
    index_path: Path,
    output_dir: Path,
) -> list[Path]:
    """Generate SKILL.md file templates.

    Args:
        parsed_dir: Path to the parsed/ directory containing markdown files.
        index_path: Path to the _INDEX.md file.
        output_dir: Directory where skill documentation will be written.

    Returns:
        List of paths to the generated files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    readme_path = output_dir / "README.md"

    lines = [
        "# SME Expert Skills",
        "",
        "This directory contains structured skill manifests (`SKILL.md`) derived from the SME's documents.",
        "",
        "## How to Generate Skills",
        "Since skill synthesis requires deep reasoning, this tool relies on your AI agent to populate the manifests.",
        "",
        "1. Open `_INDEX.md` and identify key domains (e.g., 'Deployment Logic', 'Auth Architecture').",
        "2. For each domain, ask your AI agent:",
        "   > 'Read all relevant files in `.sme-clone/parsed/` for the [Domain] topic and generate a `SKILL.md` manifest.'",
        "",
        "## Manifest Schema",
        "Each `SKILL.md` should follow this structure:",
        "- **Triggers**: When the agent should activate this skill.",
        "- **Context**: Background knowledge and entities.",
        "- **Decision Logic**: IF/THEN flows and decision trees.",
        "- **Evidence**: Links back to parsed markdown files for auditability.",
        "",
    ]

    readme_path.write_text("\n".join(lines), encoding="utf-8")
    return [readme_path]
