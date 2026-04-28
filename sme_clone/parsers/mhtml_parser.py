"""
mhtml_parser.py — Extract text from MHTML files into markdown.

This parser:
  1. Reads the MHTML file.
  2. Extracts text using email parser and BeautifulSoup.
  3. Outputs one .md file per document into parsed/docs/.
"""

import email
from email import policy
from pathlib import Path
from bs4 import BeautifulSoup

def parse_mhtml(
    mhtml_path: Path,
    output_dir: Path,
) -> Path:
    """Parse an MHTML document and write a markdown file.

    Args:
        mhtml_path: Path to the .mhtml file.
        output_dir: Directory to write the parsed markdown (e.g., parsed/docs/).

    Returns:
        Path to the generated markdown file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{mhtml_path.stem}.md"

    lines: list[str] = []
    lines.append(f"# {mhtml_path.stem.replace('_', ' ').replace('-', ' ').title()}")
    lines.append("")
    lines.append(f"> Parsed from `{mhtml_path.name}`")
    lines.append("")
    lines.append("---")
    lines.append("")

    try:
        with open(mhtml_path, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=policy.default)
        
        html_content = ""
        # MHTML can be multipart or single part
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/html':
                    try:
                        html_content += part.get_content()
                    except Exception:
                        pass
                elif content_type == 'text/plain' and not html_content:
                    try:
                        html_content += part.get_content()
                    except Exception:
                        pass
        else:
            content_type = msg.get_content_type()
            if content_type in ('text/html', 'text/plain'):
                try:
                    html_content = msg.get_content()
                except Exception:
                    pass
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            if text:
                lines.append(text)
                lines.append("")
    except Exception as e:
        print(f"Error reading MHTML {mhtml_path}: {e}")

    if len(lines) <= 6:
        # Only header was written, no content extracted
        lines.append("*No text content could be extracted from this MHTML file.*")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
