"""
xlsx_parser.py — Extract data from Excel spreadsheets (.xlsx) into markdown.

This parser:
  1. Reads the .xlsx file.
  2. Extracts data sheet-by-sheet as markdown tables.
  3. Outputs one .md file per workbook into parsed/docs/.
"""

from pathlib import Path


def parse_xlsx(
    xlsx_path: Path,
    output_dir: Path,
) -> Path:
    """Parse an Excel spreadsheet and write a markdown file.

    Args:
        xlsx_path: Path to the .xlsx file.
        output_dir: Directory to write the parsed markdown (e.g., parsed/docs/).

    Returns:
        Path to the generated markdown file.
    """
    # TODO: Implement (consider openpyxl)
    raise NotImplementedError("XLSX parser not yet implemented")
