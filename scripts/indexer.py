"""
indexer.py — Generate _INDEX.md from parsed markdown files.

Reads all files in .sme-clone/parsed/ and produces a document catalog
containing a one-paragraph summary of each file, its path, key topics,
and entities. This is the coding agent's primary entry point for
navigating the knowledge base.
"""

from pathlib import Path


def build_index(parsed_dir: Path, output_path: Path) -> Path:
    """Generate _INDEX.md from all parsed markdown files.

    Args:
        parsed_dir: Path to the parsed/ directory containing markdown files.
        output_path: Path where _INDEX.md will be written.

    Returns:
        Path to the generated _INDEX.md file.
    """
    # TODO: Implement
    #   - Walk parsed_dir recursively
    #   - For each .md file, generate a summary (via LLM or extractive)
    #   - Write structured catalog to output_path
    raise NotImplementedError("Indexer not yet implemented")
