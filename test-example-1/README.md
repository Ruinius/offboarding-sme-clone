# Test Example

This folder contains **synthetic sample data** and **pre-generated output** to demonstrate what `offboarding-sme-clone` produces.

## What's here

- `sample_slack_export.zip` — A small synthetic Slack export (fake channels, fake messages).
- `sample_design_doc.pdf` — A sample PDF design document.
- `sample_emails.mbox` — A synthetic email archive with a few threaded conversations.
- `.sme-clone/` — The output the setup script generates from the above inputs.

## How to use this for testing

```bash
# Run the setup script against this folder
uv run python scripts/setup.py --source ./test-example --sme-email jane@example.com
```

The script will overwrite the contents of `.sme-clone/`. You can compare the new output against the committed version to validate changes.
