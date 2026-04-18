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

import email
import email.policy
import mailbox
import re
from pathlib import Path


def _extract_body(msg: email.message.EmailMessage) -> str:
    """Extract the plain text body from an email message, stripping signatures."""
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode(charset, errors="replace")
                        break
                except Exception:
                    continue
    else:
        charset = msg.get_content_charset() or "utf-8"
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode(charset, errors="replace")
        except Exception:
            body = str(msg.get_payload())

    # Strip common email signatures
    # Cut at "-- \n" (standard signature delimiter) or common patterns
    sig_patterns = [
        r"\n-- \n.*",           # Standard sig delimiter
        r"\nSent from my .*",   # Mobile signatures
        r"\n_{3,}\n.*",         # Underscore separators
    ]
    for pattern in sig_patterns:
        body = re.split(pattern, body, maxsplit=1, flags=re.DOTALL)[0]

    return body.strip()


def _get_thread_key(msg: email.message.EmailMessage) -> str:
    """Derive a thread grouping key from the email headers.

    Uses In-Reply-To, References, or falls back to normalized Subject.
    """
    # References header lists all ancestor message IDs; the first entry
    # is always the root of the thread — use it as the canonical key so
    # all replies at any depth group together.
    references = msg.get("References", "").strip()
    in_reply_to = msg.get("In-Reply-To", "").strip()

    if references:
        return references.split()[0]  # Root message ID
    if in_reply_to:
        return in_reply_to.split()[0]  # Direct parent (single-level reply)

    # Fall back to normalized subject
    subject = msg.get("Subject", "No Subject")
    # Strip Re: Fwd: prefixes for grouping
    normalized = re.sub(r"^(Re|Fwd|Fw)\s*:\s*", "", subject, flags=re.IGNORECASE).strip()
    return f"subject:{normalized}"


def _slugify(text: str) -> str:
    """Convert text to a safe filename slug."""
    text = text.lower()
    text = re.sub(r"^(re|fwd|fw)\s*:\s*", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "_", text)
    text = text.strip("_")
    return text[:80] or "untitled"


def _parse_single_message(raw_msg) -> email.message.EmailMessage | None:
    """Parse a raw message from mbox or eml into an EmailMessage."""
    try:
        if isinstance(raw_msg, mailbox.mboxMessage):
            return email.message_from_bytes(
                raw_msg.as_bytes(), policy=email.policy.default
            )
        return raw_msg
    except Exception:
        return None


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
    output_dir.mkdir(parents=True, exist_ok=True)
    output_files: list[Path] = []
    sme_email_lower = sme_email.lower()

    # Collect all messages
    all_messages: list[email.message.EmailMessage] = []

    if archive_path.suffix.lower() == ".mbox":
        mbox = mailbox.mbox(str(archive_path))
        for raw_msg in mbox:
            parsed = _parse_single_message(raw_msg)
            if parsed:
                all_messages.append(parsed)
        mbox.close()
    elif archive_path.suffix.lower() == ".eml":
        raw_bytes = archive_path.read_bytes()
        parsed = email.message_from_bytes(raw_bytes, policy=email.policy.default)
        if parsed:
            all_messages.append(parsed)
    else:
        return output_files

    # Filter for SME messages (sent by or sent to the SME — we include
    # thread context where the SME participated)
    sme_messages: list[email.message.EmailMessage] = []
    for msg in all_messages:
        from_addr = msg.get("From", "").lower()
        to_addr = msg.get("To", "").lower()
        cc_addr = msg.get("Cc", "").lower()

        if sme_email_lower in from_addr or sme_email_lower in to_addr or sme_email_lower in cc_addr:
            sme_messages.append(msg)

    if not sme_messages:
        # If no SME filter match, include all (user may have used a different email format)
        sme_messages = all_messages

    # Group into threads using a two-pass approach:
    #   Pass 1: Assign each message a thread key based on References/In-Reply-To/Message-ID
    #   Pass 2: Merge subject-only keys with their Message-ID based key
    threads: dict[str, list[email.message.EmailMessage]] = {}

    # Build a set of all Message-IDs so we can recognize root messages
    msg_ids: set[str] = set()
    for msg in sme_messages:
        mid = msg.get("Message-ID", "").strip()
        if mid:
            msg_ids.add(mid)

    for msg in sme_messages:
        references = msg.get("References", "").strip()
        in_reply_to = msg.get("In-Reply-To", "").strip()
        mid = msg.get("Message-ID", "").strip()

        if references:
            # Use the first (root) message ID from References
            key = references.split()[0]
        elif in_reply_to:
            # Direct reply to a root message
            key = in_reply_to.split()[0]
        elif mid:
            # Root message — use its own Message-ID as the key so replies
            # referencing this ID will group with it
            key = mid
        else:
            # Last resort: normalized subject
            subject = msg.get("Subject", "No Subject")
            normalized = re.sub(r"^(Re|Fwd|Fw)\s*:\s*", "", subject, flags=re.IGNORECASE).strip()
            key = f"subject:{normalized}"

        threads.setdefault(key, []).append(msg)

    # Sort messages within each thread by Date
    for key in threads:
        threads[key].sort(
            key=lambda m: email.utils.parsedate_to_datetime(
                m.get("Date", "Thu, 01 Jan 1970 00:00:00 +0000")
            )
        )

    # Write each thread as a markdown file
    for thread_key, messages in threads.items():
        first_msg = messages[0]
        subject = first_msg.get("Subject", "No Subject")
        slug = _slugify(subject)
        output_path = output_dir / f"thread_{slug}.md"

        # Collect participants
        participants: set[str] = set()
        for msg in messages:
            for header in ("From", "To", "Cc"):
                addr = msg.get(header, "")
                if addr:
                    # Extract just the name/email parts
                    for name, email_addr in email.utils.getaddresses([addr]):
                        display = name if name else email_addr
                        participants.add(display)

        first_date = first_msg.get("Date", "Unknown")
        last_date = messages[-1].get("Date", "Unknown") if len(messages) > 1 else first_date

        lines: list[str] = []
        lines.append(f"# {subject}")
        lines.append("")
        lines.append(f"> **Thread:** {subject}")
        lines.append(f"> **Participants:** {', '.join(sorted(participants))}")
        lines.append(f"> **Date range:** {first_date} — {last_date}")
        lines.append(f"> **Messages:** {len(messages)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for msg in messages:
            from_addr = msg.get("From", "Unknown")
            date = msg.get("Date", "Unknown")
            body = _extract_body(msg)

            lines.append(f"**{from_addr}** — {date}")
            lines.append("")
            if body:
                lines.append(body)
            else:
                lines.append("*[No text content]*")
            lines.append("")
            lines.append("---")
            lines.append("")

        output_path.write_text("\n".join(lines), encoding="utf-8")
        output_files.append(output_path)

    return output_files
