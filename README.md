# OpenSkillsReview

OpenSkillsReview is an open-source initiative to review the most popular AI Agent Skills, document their behavior, and surface the reliable, testable implementations that agents can trust. We keep an ongoing catalog of knowledge that agents can inspect before invoking third-party Skills so that every action has a verified safety and performance profile.

## Filled and verified table

| Name | URL | Approx. # Skills | Skill Discovery Access (Web/API/CLI) |
| --- | --- | --- | --- |
| SkillsMP (Agent Skills Marketplace) | [https://skillsmp.com](https://skillsmp.com) | **400,856+** | **Web search**: [https://skillsmp.com/search](https://skillsmp.com/search) (terminal-style query UI + AI search flow). |
| Agent Skills Directory | [https://www.skillsdirectory.org](https://www.skillsdirectory.org) | **309,322+ unique** | **Web browse/search**: [https://www.skillsdirectory.org](https://www.skillsdirectory.org) and Trending list pages. |
| agentskill.sh | [https://agentskill.sh](https://agentskill.sh) | **107,000+** | **CLI-like slash command + web/docs**: `/learn @owner/skill-name`, marketplace [https://agentskill.sh](https://agentskill.sh), install docs [https://www.agentskill.sh/docs](https://www.agentskill.sh/docs). |
| skills.sh | [https://skills.sh](https://skills.sh) | **86,630+** | **CLI + Web**: `npx skills find [query]`, `npx skills list`, `npx skills add <owner/repo> --list`; leaderboard [https://skills.sh](https://skills.sh). |
| MCP Market – Skills | [https://mcpmarket.com/tools/skills](https://mcpmarket.com/tools/skills) | **59,272+** | **Web search/filter**: [https://mcpmarket.com/tools/skills](https://mcpmarket.com/tools/skills); ecosystem CLI mention (`npm i skillfish`) appears on page. |
| AwesomeSkill.ai | [https://awesomeskill.ai](https://awesomeskill.ai) | **50,000+** | **Web search**: [https://awesomeskill.ai](https://awesomeskill.ai) with Search/Category/Tag navigation. |
| AgentSkills Directory | [https://agentskills.to/skills](https://agentskills.to/skills) | **24K+**  | **Web browse/search**: [https://agentskills.to/skills](https://agentskills.to/skills) with category-driven listing. |
| prompts.chat | [https://prompts.chat](https://prompts.chat) | **35+** **1,402+** prompts | **Web search**: [https://prompts.chat/skills](https://prompts.chat/skills) and [https://prompts.chat/prompts](https://prompts.chat/prompts). |
| awesomeskills.dev (curated) | [https://awesomeskills.dev](https://awesomeskills.dev) | **2,287+** | **Web browse + install command hints**: [https://awesomeskills.dev](https://awesomeskills.dev), examples include `npx add-skill owner/repo`. |
| Awesome Claude Skills | [https://awesome-skills.com](https://awesome-skills.com) | **122+** | **Web curated listing + install snippets**: [https://awesome-skills.com](https://awesome-skills.com) (tag/category filtering; command snippets in entries). |

## Skill for Skill-Search

| Skill | Path | Used Platform (from skill README) | Related URL (from skill README) |
| --- | --- | --- | --- |
| `find-skills` | `skills/Search_Skills/find-skills` | `vercel-labs` | [https://github.com/vercel-labs/skills/tree/main#](https://github.com/vercel-labs/skills/tree/main#) |
| `skill-lookup` | `skills/Search_Skills/skill-lookup` | `prompts.chat` (registry plugin path in repo) | [https://github.com/f/prompts.chat/tree/main/plugins/claude/prompts.chat/skills/skill-lookup](https://github.com/f/prompts.chat/tree/main/plugins/claude/prompts.chat/skills/skill-lookup) |
| `skills-search` | `skills/Search_Skills/skills-search` | `skills.sh` | N/A |


## Goals
- Review widely used Skills in the AI agent ecosystem, evaluating clarity, security, and reproducibility.
- Provide runnable, testable Skill implementations along with precise requirements so agents can execute them confidently.
- Maintain transparent, up-to-date documentation that makes it easy for contributors to submit new Skills or improvements.
- Equip agents with the information they need to choose the right Skill for the situation, avoiding brittle or unverified shortcuts.

## How It Works
1. Identify a popular Skill (via telemetry, community request, or noted absence in the catalogue).
2. Assess the existing implementation for testability, documentation, and reliability.
3. Publish a verified version of the Skill, complete with automated checks, sandbox instructions, and usage notes.
4. Keep the catalogue fresh by reviewing pull requests, monitoring regressions, and signaling when a Skill needs re-validation.

## Contribution
- Fork this repo, add or improve Skill reviews under `skills/`, and open a PR with your rationale plus reproducible tests.
- Update the verification artifacts (tests, data files, fixtures) so future agents can re-run validation quickly.
- When reviewing an existing Skill, document both strengths and potential failure modes so the agent community can make informed choices.

## Reliability Practices
- Every Skill entry must include a reproducible test suite or invocation script.
- Clearly document required inputs, assumptions, and any external dependencies.
- Track known limitations and alert maintainers when upstream changes impact behavior.

## Marketplace data refresh
- To keep the research report counts current, run `python scripts/refresh_marketplace_counts.py` from the repo root; it scrapes each marketplace home page for the latest counters and writes the results to `data/marketplace_counts.json`. Review the extracted entries, verify the matches, and copy any confirmed updates back into the report along with the new timestamp.
