---
name: github-research
description: GitHub repository deep search & analysis. Multi-dimensional filtering by keywords, language, stars, update time. Identifies emerging trends and popular projects in specific domains.
metadata: {"openclaw":{"emoji":"🐙","category":"research","tags":["github","opensource","research","repository"]}, "author": {xiang & Claude}}
---

# GitHub Research 🐙

GitHub repository deep search and analysis tool for technology research across domains.

## Intent routing

| Intent | Command | Example |
|--------|---------|---------|
| Search repositories | `{baseDir}/scripts/github-search.mjs` | `node scripts/github-search.mjs "agent memory"` |
| Repository details (single) | `{baseDir}/scripts/repo-detail.mjs` | `node scripts/repo-detail.mjs "microsoft/autogen"` |
| Repository details (batch) | `{baseDir}/scripts/batch-detail.mjs` | `cat results.json \| node scripts/batch-detail.mjs` |

## API reference

### GitHub Search API qualifiers

| Qualifier | Example | Description |
|-----------|---------|-------------|
| `language:` | `language:python` | Filter by programming language |
| `stars:>=N` | `stars:>=1000` | Filter by star count (use `>`, `>=`, `<`, `<=`) |
| `pushed:>=DATE` | `pushed:>=2024-01-01` | Filter by last commit date (ISO 8601) |
| `created:>=DATE` | `created:>=2024-01-01` | Filter by creation date |
| `is:archived` | `is:archived:false` | Exclude archived repos |
| `is:fork` | `is:fork:false` | Exclude forks (default behavior) |

### github-search.mjs

```bash
node scripts/github-search.mjs <query> [options]
```

**Options:**
- `--language, -l <lang>` — Programming language filter (python, javascript, go, rust, etc.)
- `--min-stars <N>` — Minimum stars (default: 100)
- `--max-stars <N>` — Maximum stars
- `--updated-within <days>` — Updated within N days (default: 365)
- `--created-after <date>` — Created after date (ISO 8601, e.g., 2024-01-01)
- `--sort <field>` — Sort by: stars (default), updated, forks
- `--order <direction>` — Order: desc (default), asc
- `--limit, -n <N>` — Results limit (default: 10)
- `--output, -o <fmt>` — Output format: table (default), json, csv

**Environment:**
- `GITHUB_TOKEN` — GitHub API token (optional; increases rate limit from 60/hr to 5000/hr)

### repo-detail.mjs

```bash
node scripts/repo-detail.mjs <owner/repo>
```

Fetches comprehensive details: stats, code info, activity, contributors, links.

### batch-detail.mjs

```bash
# From stdin (JSON array or search result):
node scripts/github-search.mjs "agent" --output json | node scripts/batch-detail.mjs

# From command-line arguments:
node scripts/batch-detail.mjs "microsoft/autogen" "langchain-ai/langchain"

# From JSON file:
cat repos.json | node scripts/batch-detail.mjs
```

**Supported input formats:**
- JSON array of strings: `["owner/repo", "owner/repo"]`
- JSON array of objects: `[{full_name: "owner/repo"}, ...]`
- Search result object: `{repositories: [{full_name: "owner/repo"}, ...]}`

## Anti-hallucination

### Concept mapping

- **Repository** = exact GitHub repository (owner/repo format required)
- **Stars** = stargazers_count (never "views", "watchers", or "followers")
- **Forks** = forks_count (exact count, not "branches")
- **Language** = primary language detected by GitHub (from `language` field)
- **Size** = repository size in kilobytes (from GitHub API `size` field, not calculated)
- **Pull requests** = GitHub REST API does NOT provide a `pull_requests_count` field; use `open_issues_count` (includes both issues and PRs)
- **Activity level** = derived from `pushed_at` timestamp:
  - 🟢 Very active: ≤7 days since last push
  - 🟡 Active: 8-30 days
  - 🟠 Moderate: 31-90 days
  - 🔴 Inactive: >90 days

### Blacklist (things we don't do)

- ❌ Use `execSync` / shell execution — use native fetch()
- ❌ Report `pull_requests_count` field (doesn't exist in API)
- ❌ Calculate repository size in MB by dividing kB by 1024 — API returns kB, label as such
- ❌ Report hardcoded `rank: 0` in JSON output — use array index + 1
- ❌ Parse curl output with regex — use native JSON parsing after fetch()
- ❌ Unauthenticated API calls for bulk requests — always check GITHUB_TOKEN; warn if missing

### Error handling

- **404 Not Found** → "Repository not found: owner/repo"
- **403 Rate Limited** → "Set GITHUB_TOKEN for 5000 req/hr (unauthenticated: 60 req/hr)"
- **Network timeout** → "Cannot reach GitHub API, check connection"

## Features

- 🔍 **Precise search** — Find repos by keywords, language, stars, update frequency
- 📊 **Multi-dimensional filtering** — Stars, language, forks, recent updates
- 📈 **Trend analysis** — Identify active projects and emerging trends
- 🏷️ **Auto-extraction** — Tags and topics from repository metadata
- 📋 **Structured output** — Markdown tables, JSON, CSV for report integration
- 🚀 **Batch processing** — Fetch details for 10+ repos in one command

## Examples

### Basic search
```bash
node scripts/github-search.mjs "agent memory"
node scripts/github-search.mjs "rag" --language python
```

### Advanced filtering
```bash
# High-star Python projects updated recently
node scripts/github-search.mjs "vector database" \
  --language python \
  --min-stars 1000 \
  --updated-within 30 \
  --limit 15

# Output as JSON for downstream processing
node scripts/github-search.mjs "llm" \
  --limit 20 \
  --output json > results.json
```

### Repository details
```bash
# Single repo
node scripts/repo-detail.mjs "microsoft/autogen"

# Batch from search results
node scripts/github-search.mjs "agent" --output json | node scripts/batch-detail.mjs

# Batch from list
node scripts/batch-detail.mjs "langchain-ai/langchain" "openai/openai-python"
```

### Integration in workflows
```bash
#!/bin/bash
# Research multiple topics
TOPICS=("agent memory" "rag" "vector database")
for topic in "${TOPICS[@]}"; do
  echo "=== $topic ===" >> report.md
  node scripts/github-search.mjs "$topic" \
    --min-stars 500 \
    --limit 10 \
    --output json | \
    node scripts/batch-detail.mjs >> report.md
done
```

## Rate limits

- **Unauthenticated**: 60 requests/hour
- **Authenticated** (with GITHUB_TOKEN): 5000 requests/hour

Set token:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

---

*GitHub Research v1.0 | Skills Hub*
