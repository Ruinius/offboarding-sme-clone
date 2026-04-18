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
    """Generate SKILL.md files from parsed documents and index.

    Args:
        parsed_dir: Path to the parsed/ directory containing markdown files.
        index_path: Path to the _INDEX.md file.
        output_dir: Directory where SKILL.md files will be written (e.g., skills/).

    Returns:
        List of paths to the generated SKILL.md files.
    """
    # TODO: Implement
    #   - Read _INDEX.md to identify domains / topic clusters
    #   - For each cluster, read relevant parsed files
    #   - Send to LLM with skill-generation prompt
    #   - Write structured SKILL.md to output_dir
    raise NotImplementedError("Skill generator not yet implemented")
