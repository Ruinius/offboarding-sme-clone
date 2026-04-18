"""
pdf_parser.py — Extract text from PDF documents into markdown.

This parser:
  1. Reads the PDF file.
  2. Extracts text with layout preservation where possible.
  3. Outputs one .md file per document into parsed/docs/.
"""

from pathlib import Path

import pdfplumber


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
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{pdf_path.stem}.md"

    lines: list[str] = []
    lines.append(f"# {pdf_path.stem.replace('_', ' ').replace('-', ' ').title()}")
    lines.append("")
    lines.append(f"> Parsed from `{pdf_path.name}`")
    lines.append("")
    lines.append("---")
    lines.append("")

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                lines.append(f"## Page {page_num}")
                lines.append("")
                lines.append(text.strip())
                lines.append("")

            # Extract tables if present
            tables = page.extract_tables()
            for table_idx, table in enumerate(tables):
                if not table or not table[0]:
                    continue
                lines.append(f"### Table {table_idx + 1} (Page {page_num})")
                lines.append("")
                # Build markdown table
                headers = [str(cell or "").strip() for cell in table[0]]
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join("---" for _ in headers) + " |")
                for row in table[1:]:
                    cells = [str(cell or "").strip() for cell in row]
                    lines.append("| " + " | ".join(cells) + " |")
                lines.append("")

    if len(lines) <= 6:
        # Only header was written, no content extracted
        lines.append("*No text content could be extracted from this PDF.*")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
