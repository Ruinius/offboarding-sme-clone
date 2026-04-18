"""
tone_extractor.py — Extract the SME's communication style into tone_profile.md.

Analyzes writing across all parsed documents to capture:
  - Vocabulary patterns and go-to phrases
  - Level of directness vs. hedging
  - Use of analogies and metaphors
  - Humor and personality markers
  - Explanation style (top-down vs. bottom-up, examples-first vs. theory-first)
"""

from pathlib import Path


def extract_tone(parsed_dir: Path, output_path: Path) -> Path:
    """Analyze parsed documents and generate tone_profile.md template.

    Args:
        parsed_dir: Path to the parsed/ directory containing markdown files.
        output_path: Path where tone_profile.md will be written.

    Returns:
        Path to the generated tone_profile.md file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# SME Tone Profile",
        "",
        "This document captures the communication style and cognitive patterns of the departing SME.",
        "It should be used by the replacement agent to preserve the SME's 'voice' in decision-making.",
        "",
        "## 1. Communication Style",
        "[PENDING: Describe directness, vocabulary, and go-to phrases]",
        "",
        "## 2. Cognitive Patterns",
        "[PENDING: Describe explanation style - top-down vs bottom-up, etc]",
        "",
        "## 3. Personality Markers",
        "[PENDING: Describe use of humor, analogies, and metaphors]",
        "",
        "---",
        "*(Note: This profile was left as [PENDING]. Ask your AI agent to 'Analyze tone across parsed files' to populate this analysis.)*",
        "",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
