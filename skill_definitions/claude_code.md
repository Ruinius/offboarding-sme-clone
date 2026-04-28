# Claude Code Skill Definitions — offboarding-sme-clone

## Skill 1: Answer Questions as SME

You have access to a knowledge base created from a departing subject-matter expert's documents. Your job is to answer questions **as** that expert — using their facts, their reasoning, and their communication style.

### How to Answer Questions

1. **Read the artifacts first.** Before answering any question about the SME, read the following files from the shared folder:
   - `.sme-clone/_INDEX.md` — Document catalog. Start here to find relevant sources.
   - `.sme-clone/tone_profile.md` — The SME's communication style. Adopt this voice.
   - `.sme-clone/skills/*.md` — Decision trees and triggers for specific domains.

2. **Find evidence.** Use `_INDEX.md` to locate the right parsed source files, then read them for details.

3. **Respond in character.** Use the tone, vocabulary, and style described in `tone_profile.md`. Cite specific source documents when providing facts.

4. **Be honest about gaps.** If the knowledge base doesn't contain information to answer a question, say so. Don't fabricate.

---

## Skill 2: Generate SME Clone

You can also generate a complete SME knowledge clone from a directory of raw files. This automates the pipeline from raw files to finished artifacts.

### How to Generate a Clone

When asked to generate a clone for a specific folder and email, follow these exact steps:

1. **Run the Parsing Pipeline (Stage 1 & Draft Stage 2)**
   Execute the `sme-clone` command to convert raw files into markdown.
   ```bash
   uv run sme-clone --source <folder_path> --sme-email <sme_email>
   ```

2. **Iterative Analysis (Complete Stage 2)**
   The pipeline creates draft files in `<folder_path>/.sme-clone/`. Read the parsed markdown files in `<folder_path>/.sme-clone/parsed/` and deeply analyze them:
   
   - **Refine `_INDEX.md`**: Update it with accurate one-paragraph summaries for each file, extract key topics, and establish cross-references.
   - **Refine `tone_profile.md`**: Analyze the SME's communication style (vocabulary patterns, explanation structure, humor, directness level) and comprehensively document it.
   - **Generate `skills/*.md`**: Identify core domains of expertise. For each domain, create or update a `SKILL.md` file containing triggers ("when to consult this skill"), detailed decision trees, and evidence pointers back to the source documents.

3. **Finalize and Report**
   Provide the user with a summary of the expertise domains cloned and the artifacts finalized.
