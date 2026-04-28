# Antigravity Skill Definitions — offboarding-sme-clone

## Skill 2: Generate SME Clone

You can generate a complete Subject-Matter Expert (SME) knowledge clone from a directory of raw files. This skill automates the two-stage pipeline: parsing the raw files into markdown, and then iteratively analyzing those files to generate high-quality, agent-readable knowledge artifacts.

### How to Generate a Clone

When a user asks to generate a clone for a specific folder and email, follow these exact steps:

1. **Run the Parsing Pipeline (Stage 1 & Draft Stage 2)**
   Execute the `sme-clone` command to convert the raw files and generate the initial draft artifacts.
   ```bash
   # On Windows, use `cmd /c uv run ...` to prevent hanging
   cmd /c uv run sme-clone --source <folder_path> --sme-email <sme_email>
   ```

2. **Iterative Analysis (Complete Stage 2)**
   The pipeline will create draft files in `<folder_path>/.sme-clone/`. Your job is to actually perform the deep analysis by reading the parsed markdown files in `<folder_path>/.sme-clone/parsed/` and updating the drafts.
   
   - **Refine `_INDEX.md`**: Read the parsed files and update `_INDEX.md` with accurate one-paragraph summaries for each file, extract key topics, and establish cross-references.
   - **Refine `tone_profile.md`**: Analyze the SME's communication style (vocabulary patterns, explanation structure, humor, directness level) across the parsed files (especially emails and Slack messages) and comprehensively document it.
   - **Generate `skills/*.md`**: Identify the core domains of expertise from the parsed files. For each domain, create or update a `SKILL.md` file in the `skills/` directory. Each skill file must contain clear triggers ("when to consult this skill"), detailed decision trees, and evidence pointers back to the specific source documents.

3. **Finalize and Report**
   Once you have finished iterating over the parsed files and have fully fleshed out the knowledge artifacts, provide the user with a summary of the expertise domains you successfully cloned and the artifacts you finalized.
