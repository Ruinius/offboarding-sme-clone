"""
email_parser.py — Parse email archives (.mbox, .eml) into per-thread markdown files.

Supported formats:
  - .mbox (Gmail Takeout, Thunderbird export)
  - .eml  (individual email files)

This parser:
  1. Reads the email archive.
  2. Filters for messages sent by the target SME.
  3. Groups messages into conversation threads.
  4. Strips signatures, MIME encoding, and header noise.
  5. Outputs one .md file per thread into parsed/email/.
"""

from pathlib import Path


def parse_email_archive(
    archive_path: Path,
    output_dir: Path,
    sme_email: str,
) -> list[Path]:
    """Parse an email archive and write per-thread markdown files.

    Args:
        archive_path: Path to the .mbox or .eml file.
        output_dir: Directory to write parsed markdown files (e.g., parsed/email/).
        sme_email: Email of the departing SME to filter messages.

    Returns:
        List of paths to the generated markdown files.
    """
    # TODO: Implement
    raise NotImplementedError("Email parser not yet implemented")
