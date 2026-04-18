"""
slack_parser.py — Parse Slack export ZIPs into per-channel markdown files.

Slack exports are ZIP archives containing:
  - channels.json       (channel metadata)
  - users.json          (user metadata)
  - <channel_name>/     (directory per channel)
      - YYYY-MM-DD.json (array of message objects per day)

This parser:
  1. Unzips the archive.
  2. Resolves user IDs to display names via users.json.
  3. Filters messages to only those from the target SME (by email or user ID).
  4. Groups messages by channel, preserving thread structure.
  5. Strips system messages (join/leave, channel topic changes).
  6. Outputs one .md file per channel into parsed/slack/.
"""

from pathlib import Path


def parse_slack_export(
    zip_path: Path,
    output_dir: Path,
    sme_email: str,
) -> list[Path]:
    """Parse a Slack export ZIP and write per-channel markdown files.

    Args:
        zip_path: Path to the Slack export .zip file.
        output_dir: Directory to write parsed markdown files (e.g., parsed/slack/).
        sme_email: Email of the departing SME to filter messages.

    Returns:
        List of paths to the generated markdown files.
    """
    # TODO: Implement
    raise NotImplementedError("Slack parser not yet implemented")
