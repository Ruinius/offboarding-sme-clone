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
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Collect all markdown files recursively
    md_files = sorted(parsed_dir.rglob("*.md"))

    lines = [
        "# Knowledge Index",
        "",
        "This index provides a catalog of all documents parsed from the SME's shared folder. ",
        "It is designed to help an AI agent quickly locate relevant information and decision-making logic.",
        "",
        "| Document | Category | Summary (Auto-generated) |",
        "| :--- | :--- | :--- |",
    ]

    for md_file in md_files:
        # Determine category based on parent directory
        category = md_file.parent.name.title()
        # Relative path for linking inside the .sme-clone folder
        rel_path = md_file.relative_to(output_path.parent)
        
        # In a real Agent-First tool, we might use placeholders or prompts here.
        # For now, we'll use a placeholder that the host agent is expected to fill.
        summary = "[PENDING SUMMARY]"
        
        lines.append(f"| [{md_file.name}]({rel_path}) | {category} | {summary} |")

    lines.append("")
    lines.append("---")
    lines.append("*(Note: Summaries above were left as [PENDING]. Ask your AI agent to 'Complete the Index' to populate them.)*")
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
