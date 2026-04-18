"""
docx_parser.py — Extract text from Word documents (.docx) into markdown.

This parser:
  1. Reads the .docx file.
  2. Extracts paragraphs, headings, and basic formatting.
  3. Outputs one .md file per document into parsed/docs/.
"""

from pathlib import Path


def parse_docx(
    docx_path: Path,
    output_dir: Path,
) -> Path:
    """Parse a Word document and write a markdown file.

    Args:
        docx_path: Path to the .docx file.
        output_dir: Directory to write the parsed markdown (e.g., parsed/docs/).

    Returns:
        Path to the generated markdown file.
    """
    # TODO: Implement (consider python-docx)
    raise NotImplementedError("DOCX parser not yet implemented")
