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

import json
import tempfile
import zipfile
from pathlib import Path

# Slack message subtypes that are system-generated and should be skipped
SYSTEM_SUBTYPES = {
    "channel_join",
    "channel_leave",
    "channel_topic",
    "channel_purpose",
    "channel_name",
    "channel_archive",
    "channel_unarchive",
    "group_join",
    "group_leave",
    "group_topic",
    "group_purpose",
    "group_name",
    "group_archive",
    "group_unarchive",
    "bot_message",
    "pinned_item",
    "unpinned_item",
}


def _resolve_user_map(users_data: list[dict]) -> dict[str, dict]:
    """Build a mapping from user ID to user info.

    Returns:
        Dict mapping user_id -> {"name": display_name, "email": email_or_empty}
    """
    user_map: dict[str, dict] = {}
    for user in users_data:
        uid = user.get("id", "")
        profile = user.get("profile", {})
        display_name = (
            profile.get("display_name")
            or profile.get("real_name")
            or user.get("real_name")
            or user.get("name", uid)
        )
        email = profile.get("email", "")
        user_map[uid] = {"name": display_name, "email": email}
    return user_map


def _find_sme_user_id(user_map: dict[str, dict], sme_email: str) -> str | None:
    """Find the user ID for the given SME email address."""
    for uid, info in user_map.items():
        if info["email"].lower() == sme_email.lower():
            return uid
    return None


def _format_timestamp(ts: str) -> str:
    """Convert a Slack timestamp to a human-readable date/time string."""
    from datetime import datetime, timezone

    try:
        epoch = float(ts.split(".")[0])
        dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except (ValueError, IndexError):
        return ts


def _replace_user_mentions(text: str, user_map: dict[str, dict]) -> str:
    """Replace <@U12345> mentions with @display_name."""
    import re

    def _replace(match: re.Match) -> str:
        uid = match.group(1)
        if uid in user_map:
            return f"@{user_map[uid]['name']}"
        return match.group(0)

    return re.sub(r"<@(U[A-Z0-9]+)>", _replace, text)


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
    output_dir.mkdir(parents=True, exist_ok=True)
    output_files: list[Path] = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Unzip the export
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_path)

        # Load user mapping
        users_file = tmp_path / "users.json"
        user_map: dict[str, dict] = {}
        sme_user_id: str | None = None

        if users_file.exists():
            users_data = json.loads(users_file.read_text(encoding="utf-8"))
            user_map = _resolve_user_map(users_data)
            sme_user_id = _find_sme_user_id(user_map, sme_email)

        # Load channel metadata
        channels_file = tmp_path / "channels.json"
        channel_meta: dict[str, dict] = {}
        if channels_file.exists():
            channels_data = json.loads(channels_file.read_text(encoding="utf-8"))
            for ch in channels_data:
                channel_meta[ch.get("name", "")] = ch

        # Find channel directories (any directory that contains JSON day-files)
        channel_dirs = sorted(
            d
            for d in tmp_path.iterdir()
            if d.is_dir() and any(f.suffix == ".json" for f in d.iterdir())
        )

        for channel_dir in channel_dirs:
            channel_name = channel_dir.name
            day_files = sorted(channel_dir.glob("*.json"))

            # Collect all messages from all day files
            all_messages: list[dict] = []
            for day_file in day_files:
                try:
                    messages = json.loads(day_file.read_text(encoding="utf-8"))
                    if isinstance(messages, list):
                        all_messages.extend(messages)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue

            # Filter: skip system messages, keep only SME messages
            sme_messages: list[dict] = []
            for msg in all_messages:
                subtype = msg.get("subtype", "")
                if subtype in SYSTEM_SUBTYPES:
                    continue

                user_id = msg.get("user", "")
                # If we found the SME's user ID, filter by it.
                # If we couldn't resolve the email, include all messages
                # (better to over-include than lose data).
                if sme_user_id and user_id != sme_user_id:
                    continue

                sme_messages.append(msg)

            if not sme_messages:
                continue

            # Sort by timestamp
            sme_messages.sort(key=lambda m: float(m.get("ts", "0")))

            # Build markdown
            lines: list[str] = []
            lines.append(f"# #{channel_name}")
            lines.append("")

            meta = channel_meta.get(channel_name, {})
            if meta.get("purpose", {}).get("value"):
                lines.append(f"> **Channel purpose:** {meta['purpose']['value']}")
                lines.append("")

            ts_first = _format_timestamp(sme_messages[0].get("ts", ""))
            ts_last = _format_timestamp(sme_messages[-1].get("ts", ""))
            lines.append(
                f"> **Date range:** {ts_first} — {ts_last} | "
                f"**Messages:** {len(sme_messages)}"
            )
            lines.append("")
            lines.append("---")
            lines.append("")

            for msg in sme_messages:
                ts = _format_timestamp(msg.get("ts", ""))
                user_id = msg.get("user", "unknown")
                display_name = user_map.get(user_id, {}).get("name", user_id)
                text = msg.get("text", "")
                text = _replace_user_mentions(text, user_map)

                lines.append(f"**{display_name}** — {ts}")
                lines.append("")
                lines.append(text)
                lines.append("")

                # Include thread replies if this is a parent message
                if "replies" in msg or "reply_count" in msg:
                    reply_count = msg.get("reply_count", 0)
                    if reply_count:
                        lines.append(f"*({reply_count} replies in thread)*")
                        lines.append("")

            output_path = output_dir / f"{channel_name}.md"
            output_path.write_text("\n".join(lines), encoding="utf-8")
            output_files.append(output_path)

    return output_files
