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
    """Analyze parsed documents and generate tone_profile.md.

    Args:
        parsed_dir: Path to the parsed/ directory containing markdown files.
        output_path: Path where tone_profile.md will be written.

    Returns:
        Path to the generated tone_profile.md file.
    """
    # TODO: Implement
    #   - Read a sample of parsed files
    #   - Send to LLM with a tone-extraction prompt
    #   - Write structured tone profile to output_path
    raise NotImplementedError("Tone extractor not yet implemented")
