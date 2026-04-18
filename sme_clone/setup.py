"""
setup.py — Main entry point for the offboarding-sme-clone pipeline.

Usage:
    uv run python scripts/setup.py --source <path-to-folder> --sme-email <email>

This script orchestrates the two-stage pipeline:
    Stage 1 (Parse):   Detect file formats and convert to clean markdown.
    Stage 2 (Analyze): Generate _INDEX.md, tone_profile.md, and SKILL.md files.

All output is written to a .sme-clone/ subfolder within the source folder.
"""

import argparse
import sys
from pathlib import Path

# Ensure the repo root is on sys.path so imports work whether the script
# is invoked as `python scripts/setup.py` or `python -m scripts.setup`.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from sme_clone.parsers.docx_parser import parse_docx
from sme_clone.parsers.email_parser import parse_email_archive
from sme_clone.parsers.pdf_parser import parse_pdf
from sme_clone.parsers.pptx_parser import parse_pptx
from sme_clone.parsers.slack_parser import parse_slack_export
from sme_clone.parsers.xlsx_parser import parse_xlsx
from sme_clone.indexer import build_index
from sme_clone.tone_extractor import extract_tone
from sme_clone.skill_generator import generate_skills

# ---------------------------------------------------------------------------
# File-type routing table
# ---------------------------------------------------------------------------
# Maps file extensions to (parser_function, output_subdirectory).
# The parser function signature varies slightly between formats, so
# dispatch_file() handles the differences.
EXTENSION_MAP: dict[str, tuple[str, str]] = {
    ".pdf": ("pdf", "docs"),
    ".docx": ("docx", "docs"),
    ".pptx": ("pptx", "docs"),
    ".xlsx": ("xlsx", "docs"),
    ".xls": ("xlsx", "docs"),
    ".mbox": ("email", "email"),
    ".eml": ("email", "email"),
    ".zip": ("slack", "slack"),
    # Pass-through formats — copy as-is or wrap in markdown
    ".md": ("passthrough", "docs"),
    ".txt": ("passthrough", "docs"),
    ".py": ("code", "docs"),
    ".js": ("code", "docs"),
    ".ts": ("code", "docs"),
    ".java": ("code", "docs"),
    ".go": ("code", "docs"),
    ".rs": ("code", "docs"),
    ".rb": ("code", "docs"),
    ".sh": ("code", "docs"),
    ".yaml": ("code", "docs"),
    ".yml": ("code", "docs"),
    ".json": ("code", "docs"),
    ".toml": ("code", "docs"),
    ".css": ("code", "docs"),
    ".html": ("code", "docs"),
    ".sql": ("code", "docs"),
    ".c": ("code", "docs"),
    ".cpp": ("code", "docs"),
    ".h": ("code", "docs"),
}

# Map extensions to language identifiers for code fences
LANG_MAP: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".sh": "bash",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
    ".css": "css",
    ".html": "html",
    ".sql": "sql",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
}


def _parse_passthrough(file_path: Path, output_dir: Path) -> Path:
    """Copy a markdown or plain text file as-is (or with a header)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{file_path.stem}.md"

    content = file_path.read_text(encoding="utf-8", errors="replace")

    if file_path.suffix.lower() == ".md":
        # Markdown files pass through directly
        output_path.write_text(content, encoding="utf-8")
    else:
        # Plain text gets a header
        lines = [
            f"# {file_path.stem.replace('_', ' ').replace('-', ' ').title()}",
            "",
            f"> Parsed from `{file_path.name}`",
            "",
            "---",
            "",
            content,
        ]
        output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def _parse_code(file_path: Path, output_dir: Path) -> Path:
    """Wrap a code file in a markdown code fence with language tagging."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{file_path.stem}.md"

    content = file_path.read_text(encoding="utf-8", errors="replace")
    lang = LANG_MAP.get(file_path.suffix.lower(), "")

    lines = [
        f"# {file_path.name}",
        "",
        f"> Parsed from `{file_path.name}`",
        "",
        "---",
        "",
        f"```{lang}",
        content,
        "```",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def dispatch_file(
    file_path: Path,
    parsed_dir: Path,
    sme_email: str,
) -> list[Path]:
    """Route a single file to the appropriate parser.

    Args:
        file_path: Path to the raw input file.
        parsed_dir: Base parsed/ directory.
        sme_email: SME email for filtering Slack/email.

    Returns:
        List of output markdown file paths generated.
    """
    ext = file_path.suffix.lower()
    if ext not in EXTENSION_MAP:
        return []

    parser_type, subdir = EXTENSION_MAP[ext]
    output_dir = parsed_dir / subdir

    try:
        if parser_type == "pdf":
            return [parse_pdf(file_path, output_dir)]
        elif parser_type == "docx":
            return [parse_docx(file_path, output_dir)]
        elif parser_type == "pptx":
            return [parse_pptx(file_path, output_dir)]
        elif parser_type == "xlsx":
            return [parse_xlsx(file_path, output_dir)]
        elif parser_type == "email":
            return parse_email_archive(file_path, output_dir, sme_email)
        elif parser_type == "slack":
            return parse_slack_export(file_path, output_dir, sme_email)
        elif parser_type == "passthrough":
            return [_parse_passthrough(file_path, output_dir)]
        elif parser_type == "code":
            return [_parse_code(file_path, output_dir)]
    except Exception as e:
        print(f"  ERROR parsing {file_path.name}: {e}")
        return []

    return []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process SME documents into structured knowledge artifacts.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the shared folder containing raw SME documents.",
    )
    parser.add_argument(
        "--sme-email",
        type=str,
        required=True,
        help="Email address of the departing SME (used to filter Slack/email exports).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    source: Path = args.source.resolve()
    if not source.is_dir():
        print(f"Error: source folder not found: {source}", file=sys.stderr)
        sys.exit(1)

    sme_clone_dir = source / ".sme-clone"
    parsed_dir = sme_clone_dir / "parsed"
    skills_dir = sme_clone_dir / "skills"

    # Ensure output directories exist
    for d in [parsed_dir / "slack", parsed_dir / "email", parsed_dir / "docs", skills_dir]:
        d.mkdir(parents=True, exist_ok=True)

    print()
    print("+--- offboarding-sme-clone ---+")
    print(f"  Source folder : {source}")
    print(f"  SME email     : {args.sme_email}")
    print(f"  Output folder : {sme_clone_dir}")
    print()

    # ------------------------------------------------------------------
    # Stage 1: Parse -- convert raw files to markdown
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Stage 1: Parse -- converting raw files to markdown")
    print("=" * 60)
    print()

    # Collect all files in the source directory (non-recursive top-level only,
    # excluding the .sme-clone output directory itself)
    raw_files = sorted(
        f for f in source.iterdir()
        if f.is_file() and not f.name.startswith(".")
    )

    if not raw_files:
        print("  No files found in source folder.")
    else:
        parsed_count = 0
        skipped_count = 0

        for raw_file in raw_files:
            ext = raw_file.suffix.lower()
            if ext not in EXTENSION_MAP:
                print(f"  - Skipping unsupported format: {raw_file.name}")
                skipped_count += 1
                continue

            print(f"  Parsing {raw_file.name}...", end=" ")
            output_paths = dispatch_file(raw_file, parsed_dir, args.sme_email)

            if output_paths:
                for i, p in enumerate(output_paths):
                    rel = p.relative_to(sme_clone_dir)
                    if i == 0:
                        print(f"OK -> {rel}")
                    else:
                        print(f"    {'':>{len(raw_file.name)}}   -> {rel}")
                parsed_count += len(output_paths)
            else:
                print("no output generated")
                skipped_count += 1

        print()
        print(f"  Parsed: {parsed_count} files  |  Skipped: {skipped_count} files")

    print()

    # ------------------------------------------------------------------
    # Stage 2: Analyze -- generate knowledge artifacts
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Stage 2: Analyze -- generating knowledge artifacts")
    print("=" * 60)
    print()

    # Step 2a: Build _INDEX.md
    print("  2a. Generating _INDEX.md...", end=" ")
    index_path = sme_clone_dir / "_INDEX.md"
    build_index(parsed_dir, index_path)
    print(f"OK -> {index_path.relative_to(sme_clone_dir)}")

    # Step 2b: Extract tone profile
    print("  2b. Generating tone_profile.md...", end=" ")
    tone_path = sme_clone_dir / "tone_profile.md"
    extract_tone(parsed_dir, tone_path)
    print(f"OK -> {tone_path.relative_to(sme_clone_dir)}")

    # Step 2c: Generate SKILL.md templates
    print("  2c. Generating SKILL.md files...", end=" ")
    generated_skills = generate_skills(parsed_dir, index_path, skills_dir)
    if generated_skills:
        print(f"OK -> {len(generated_skills)} tasks created in {skills_dir.relative_to(sme_clone_dir)}")

    print()
    print("+" + "-" * 58 + "+")
    print(f"  Stage 1 (Parse) complete. Parsed files: {parsed_dir.relative_to(source)}")
    print(f"  Stage 2 (Analyze) ready. AI-readable drafts created.")
    print()
    print("  NEXT STEPS:")
    print(f"  1. Open {index_path.relative_to(source)}")
    print("  2. Ask your AI agent (Antigravity, Claude Code, Cursor) to:")
    print("     'Complete the Stage 2 analysis using the parsed documents.'")
    print("+" + "-" * 58 + "+")


if __name__ == "__main__":
    main()

