"""
pdf_parser.py — Extract text from PDF documents into markdown.

This parser:
  1. Reads the PDF file.
  2. Extracts text with layout preservation where possible.
  3. Outputs one .md file per document into parsed/docs/.
"""

from pathlib import Path


def parse_pdf(
    pdf_path: Path,
    output_dir: Path,
) -> Path:
    """Parse a PDF document and write a markdown file.

    Args:
        pdf_path: Path to the .pdf file.
        output_dir: Directory to write the parsed markdown (e.g., parsed/docs/).

    Returns:
        Path to the generated markdown file.
    """
    # TODO: Implement (consider pdfplumber or pymupdf)
    raise NotImplementedError("PDF parser not yet implemented")
