"""
pptx_parser.py — Extract text from PowerPoint presentations (.pptx) into markdown.

This parser:
  1. Reads the .pptx file.
  2. Extracts slide-by-slide text content including speaker notes.
  3. Outputs one .md file per presentation into parsed/docs/.
"""

from pathlib import Path


def parse_pptx(
    pptx_path: Path,
    output_dir: Path,
) -> Path:
    """Parse a PowerPoint presentation and write a markdown file.

    Args:
        pptx_path: Path to the .pptx file.
        output_dir: Directory to write the parsed markdown (e.g., parsed/docs/).

    Returns:
        Path to the generated markdown file.
    """
    # TODO: Implement (consider python-pptx)
    raise NotImplementedError("PPTX parser not yet implemented")
