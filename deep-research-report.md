# Deep Research on AI Agent Skills Marketplaces, Directories, and Repos

## Scope and research method

This research verifies (or updates) the **current “skills published” counts** and the **primary search/list interfaces or commands** for the marketplaces/directories you listed, using each site’s own UI/Docs/README where possible. All figures below reflect what the sites themselves display **as of March 8, 2026 (America/New_York)** and should be treated as *living metrics* that can change daily.

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

## What these “skill counts” actually mean

A key reason marketplace counts can look wildly different (even when they all reference the same SKILL.md-style ecosystem) is that the platforms often count **different units**:

SkillsMP exposes a **global “Total Skills”** metric (400,856) on its timeline page, and frames the dataset as skills “pushed to GitHub over time,” implying a GitHub-indexed corpus with time-series aggregation.

Agent Skills Directory distinguishes **“unique AI agent skills”** from **“indexed skill files”** (309,322 unique skills vs. 878,423 indexed files), signaling deduplication and/or normalization logic across repos/forks/paths.

skills.sh’s “All Time (86,630)” appears to reflect the count of skills in **its own directory/leaderboard registry**, which is then paired with CLI flows (`npx skills ...`) for install/search/list.

prompts.chat uses the word “Skills” for a much smaller, curated/created set inside prompts.chat itself (“35 found”), and counts “Prompts” separately at “1402 found.”

The practical implication: for product/market analysis or due diligence, you typically want to record the count *and* the platform’s definition (unique skills vs. skill files vs. curated entries), otherwise comparisons can be misleading.

## How search and installation flows differ across platforms

Across your list, there are three dominant “interfaces” for discovery and adoption:

Web-first directories: SkillsMP, Agent Skills Directory, MCP Market, AwesomeSkill.ai, and AgentSkills.to all emphasize browsing/searching in the browser (often with categories/tags). SkillsMP’s interface is explicitly built around a search/filter UX and even frames “AI search” as an interaction mode (enter to search).

CLI-first ecosystems: skills.sh is tightly linked to the `npx skills` CLI, which supports both **search** (`npx skills find [query]`) and **listing** (`npx skills list`), plus repo-level listing without install (`npx skills add owner/repo --list`). This is a more “package-manager-like” model than web-only directories.

Slash-command / agent-integrated install: agentskill.sh’s core pitch is “Install any skill with `/learn @owner/skill-name`,” and their docs show how to add their marketplace JSON and install the learn plugin so that `/learn` becomes available inside supported agents (not just the website).

prompts.chat sits somewhat between categories: it’s web-first for browsing prompts/skills, but it also supports agent integration pathways (e.g., it maintains a Claude Code plugin described in its repo docs).

## Caveats and reliability notes

Counts are volatile by design. Many of these sites are indexing Git repos or continuously ingesting community contributions, so “approximate # skills” should be timestamped and periodically re-verified (especially SkillsMP, Agent Skills Directory, agentskill.sh, skills.sh, MCP Market).

Curated vs. indexed matters for trust and risk. Curated directories like awesomeskills.dev and awesome-skills.com inherently have smaller counts, but often provide clearer install instructions and implied human review/selection, whereas large-scale indexes maximize coverage but can include duplicates or low-signal entries. The awesome-skills.com page explicitly frames itself as “a curated list” and includes structured tags + install commands per entry.

Finally, “skills” are not necessarily safe to run blindly. Some ecosystems explicitly caution users to review skills before installing/using (the skills.sh docs include a safety disclaimer about not guaranteeing quality/security of every listed skill).

## Automating the refresh

To lower the manual effort of revisiting each marketplace, run the refresh helper:

```
python scripts/refresh_marketplace_counts.py
```

It will pull the primary landing pages, try to extract the headline counters with simple regex patterns, and write the last-two-digit counts plus the fetch timestamp into `data/marketplace_counts.json`. After running it, inspect the array entry that corresponds to the marketplace you care about, verify the scraped value makes sense, and copy the updated number back into this report (along with any new context or updated URL). The script is deliberately conservative: the regex patterns can be tuned further, and missing matches are logged so you can capture new phrasing before publishing the next snapshot.
