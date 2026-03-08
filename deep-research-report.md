# Deep Research on AI Agent Skills Marketplaces, Directories, and Repos

## Scope and research method

This research verifies (or updates) the **current “skills published” counts** and the **primary search/list interfaces or commands** for the marketplaces/directories you listed, using each site’s own UI/Docs/README where possible. All figures below reflect what the sites themselves display **as of March 8, 2026 (America/New_York)** and should be treated as *living metrics* that can change daily. citeturn17view0turn17view3turn3view0turn3view2turn12view0turn14view0

## Filled and verified table

| Name | URL | Approx. # Skills | Skill Search / List Command or Interface |
| --- | --- | --- | --- |
| SkillsMP (Agent Skills Marketplace) | [https://skillsmp.com](https://skillsmp.com) | **400,856+** (site shows “Total Skills 400856”). citeturn17view0 | **Web “terminal-style” search UI** at `/search` with sort options (e.g., *stars/recent*) and a type-to-filter UX, plus an “AI search” prompt flow. citeturn17view1 |
| Agent Skills Directory | [https://www.skillsdirectory.org](https://www.skillsdirectory.org) | **309,322+ unique** (sourced from **878,423 indexed skill files** per the directory landing content retrieved via crawl). citeturn2search0 | **Web browsing + sections like Trending** (site navigation includes “Browse” and “Trending”; Trending page is accessible and lists skills). citeturn2search0turn2search10 |
| agentskill.sh | [https://agentskill.sh](https://agentskill.sh) | **107,000+** (homepage currently states “Find and install 107,000+ skills”). citeturn17view3 | **`/learn @owner/skill-name`** is the primary “install/search entry point” (homepage callout). The install docs show adding their marketplace JSON and installing the **`/learn`** plugin into supported agents. citeturn17view3turn0search2 |
| skills.sh | [https://skills.sh](https://skills.sh) | **86,630+** (site leaderboard shows “All Time (86,630)”). citeturn3view0 | **CLI + web leaderboard**: the canonical CLI (vercel-labs/skills) documents `npx skills find [query]` (search) and `npx skills list` (list installed), plus `npx skills add <owner/repo> --list` to list skills inside a repo without installing. citeturn21view0turn3view0 |
| MCP Market – Skills | [https://mcpmarket.com/tools/skills](https://mcpmarket.com/tools/skills) | **59,272+** (page shows “59,272 Skills”). citeturn3view2 | **Web directory with search + category filters**, plus an ecosystem-related CLI mention (`$npm i skillfish`) on the page. citeturn3view2 |
| AwesomeSkill.ai | [https://awesomeskill.ai](https://awesomeskill.ai) | **50,000+** (homepage text explicitly claims “50,000+ skills”). citeturn7search0 | **Web search + category/tag navigation** (top nav includes Search/Category/Tag; search page supports filtering/sorting). citeturn3view3turn4view0 |
| AgentSkills Directory | [https://agentskills.to/skills](https://agentskills.to/skills) | **24K+** (page headline: “Discover 24K++ … skills”; also shows “24K+ Skills”). citeturn3view4 | **Web directory browsing** with category counts (e.g., Backend/Frontend/DevOps) and an installs metric. citeturn3view4 |
| prompts.chat | [https://prompts.chat](https://prompts.chat) | **35+** skills (prompts.chat Skills page says “35 found”; prompts page separately lists **1,402+** prompts). citeturn11view1turn12view0 | **Web prompt/skill search UI** with dedicated sections for Prompts and Skills, and “Create Prompt / Create Skill” entry points. citeturn11view1turn12view0 |
| awesomeskills.dev (curated) | [https://awesomeskills.dev](https://awesomeskills.dev) | **2,287+** (homepage has a “View all 2287 skills →” link). citeturn14view0 | **Curated category browsing + one-line install commands** shown inline (examples use `npx add-skill owner/repo`). citeturn14view0 |
| Awesome Claude Skills | [https://awesome-skills.com](https://awesome-skills.com) | **122+** curated skills/plugins (site snippet/metadata claims “Discover 122+ curated skills and plugins”). citeturn13search2 | **Curated web directory** with tag filtering and category sections; entries include installation instructions (e.g., `/plugin install …`, `git clone …`). The page also explicitly states it’s curated and shows it was updated on March 6, 2026. citeturn16view2 |

## What these “skill counts” actually mean

A key reason marketplace counts can look wildly different (even when they all reference the same SKILL.md-style ecosystem) is that the platforms often count **different units**:

SkillsMP exposes a **global “Total Skills”** metric (400,856) on its timeline page, and frames the dataset as skills “pushed to GitHub over time,” implying a GitHub-indexed corpus with time-series aggregation. citeturn17view0

Agent Skills Directory distinguishes **“unique AI agent skills”** from **“indexed skill files”** (309,322 unique skills vs. 878,423 indexed files), signaling deduplication and/or normalization logic across repos/forks/paths. citeturn2search0

skills.sh’s “All Time (86,630)” appears to reflect the count of skills in **its own directory/leaderboard registry**, which is then paired with CLI flows (`npx skills ...`) for install/search/list. citeturn3view0turn21view0

prompts.chat uses the word “Skills” for a much smaller, curated/created set inside prompts.chat itself (“35 found”), and counts “Prompts” separately at “1402 found.” citeturn11view1turn12view0

The practical implication: for product/market analysis or due diligence, you typically want to record the count *and* the platform’s definition (unique skills vs. skill files vs. curated entries), otherwise comparisons can be misleading. citeturn2search0turn17view0turn3view0turn12view0

## How search and installation flows differ across platforms

Across your list, there are three dominant “interfaces” for discovery and adoption:

Web-first directories: SkillsMP, Agent Skills Directory, MCP Market, AwesomeSkill.ai, and AgentSkills.to all emphasize browsing/searching in the browser (often with categories/tags). SkillsMP’s interface is explicitly built around a search/filter UX and even frames “AI search” as an interaction mode (enter to search). citeturn17view1turn3view2turn4view0turn3view4

CLI-first ecosystems: skills.sh is tightly linked to the `npx skills` CLI, which supports both **search** (`npx skills find [query]`) and **listing** (`npx skills list`), plus repo-level listing without install (`npx skills add owner/repo --list`). This is a more “package-manager-like” model than web-only directories. citeturn21view0turn3view0

Slash-command / agent-integrated install: agentskill.sh’s core pitch is “Install any skill with `/learn @owner/skill-name`,” and their docs show how to add their marketplace JSON and install the learn plugin so that `/learn` becomes available inside supported agents (not just the website). citeturn17view3turn0search2

prompts.chat sits somewhat between categories: it’s web-first for browsing prompts/skills, but it also supports agent integration pathways (e.g., it maintains a Claude Code plugin described in its repo docs). citeturn12view0turn11view1turn8search1

## Caveats and reliability notes

Counts are volatile by design. Many of these sites are indexing Git repos or continuously ingesting community contributions, so “approximate # skills” should be timestamped and periodically re-verified (especially SkillsMP, Agent Skills Directory, agentskill.sh, skills.sh, MCP Market). citeturn17view0turn2search0turn17view3turn3view0turn3view2

Curated vs. indexed matters for trust and risk. Curated directories like awesomeskills.dev and awesome-skills.com inherently have smaller counts, but often provide clearer install instructions and implied human review/selection, whereas large-scale indexes maximize coverage but can include duplicates or low-signal entries. The awesome-skills.com page explicitly frames itself as “a curated list” and includes structured tags + install commands per entry. citeturn14view0turn16view2

Finally, “skills” are not necessarily safe to run blindly. Some ecosystems explicitly caution users to review skills before installing/using (the skills.sh docs include a safety disclaimer about not guaranteeing quality/security of every listed skill). citeturn0search11

## Automating the refresh

To lower the manual effort of revisiting each marketplace, run the refresh helper:

```
python scripts/refresh_marketplace_counts.py
```

It will pull the primary landing pages, try to extract the headline counters with simple regex patterns, and write the last-two-digit counts plus the fetch timestamp into `data/marketplace_counts.json`. After running it, inspect the array entry that corresponds to the marketplace you care about, verify the scraped value makes sense, and copy the updated number back into this report (along with any new context or updated URL). The script is deliberately conservative: the regex patterns can be tuned further, and missing matches are logged so you can capture new phrasing before publishing the next snapshot.
