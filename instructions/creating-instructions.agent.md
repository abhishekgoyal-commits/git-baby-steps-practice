# Creating Instructions

- Add new project instructions under `./instructions/` with a verb-first, hyphen-separated `[name].agent.md` filename.
- Keep each instruction focused on one workflow and write short, actionable bullet points.
- Add every new instruction to `./instructions/main.agent.md` with a one-line description and matching Keywords.
- Keep instruction content platform-agnostic; put IDE-specific loading behavior in thin wrappers.
- Use `./instructions/main.agent.md` as the catalog and route requests to the smallest relevant instruction.
- Reference shared instructions with relative paths such as `./instructions/[name].agent.md`.
- Use a skill under `./instructions/[name]/SKILL.md` when the workflow needs scripts, reference documents, or reusable assets.
- Give skills YAML frontmatter with `name`, `description`, and `version`, then document executable steps with relative paths.
- For VS Code and GitHub Copilot, add task wrappers under `./.github/prompts/` using `to-[name].prompt.md`.
- Keep `./.github/copilot-instructions.md` pointed at the complete `./instructions/main.agent.md` catalog.
- Preserve existing instruction content when updating files; make targeted additions instead of broad rewrites.
- Validate new files, links, frontmatter, and practical examples before considering an instruction complete.