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

    print(f"Source folder : {source}")
    print(f"SME email     : {args.sme_email}")
    print(f"Output folder : {sme_clone_dir}")
    print()

    # ------------------------------------------------------------------
    # Stage 1: Parse — convert raw files to markdown
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Stage 1: Parse — converting raw files to markdown")
    print("=" * 60)
    # TODO: Implement parser dispatch logic
    #   - Detect file types in source folder
    #   - Route each file to the appropriate parser
    #   - Write parsed markdown to parsed_dir
    print("  [not yet implemented]\n")

    # ------------------------------------------------------------------
    # Stage 2: Analyze — generate knowledge artifacts
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Stage 2: Analyze — generating knowledge artifacts")
    print("=" * 60)

    # Step 2a: Build _INDEX.md
    # TODO: from scripts.indexer import build_index
    print("  2a. Generating _INDEX.md ... [not yet implemented]")

    # Step 2b: Extract tone profile
    # TODO: from scripts.tone_extractor import extract_tone
    print("  2b. Generating tone_profile.md ... [not yet implemented]")

    # Step 2c: Generate SKILL.md files
    # TODO: from scripts.skill_generator import generate_skills
    print("  2c. Generating SKILL.md files ... [not yet implemented]")

    print()
    print("Done. Artifacts written to:", sme_clone_dir)


if __name__ == "__main__":
    main()
