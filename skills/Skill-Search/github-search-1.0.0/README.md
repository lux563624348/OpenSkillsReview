# GitHub Research 🐙

GitHub repository deep search and analysis tool for technology research across domains.

# Author: lux563624348 & Claude

## Quick start

```bash
# Basic search
node scripts/github-search.mjs "agent memory"

# Python projects, minimum 1000 stars
node scripts/github-search.mjs "rag" --language python --min-stars 1000

# Recently updated projects (last 30 days)
node scripts/github-search.mjs "vector database" --updated-within 30 --limit 15

# Get repository details
node scripts/repo-detail.mjs "microsoft/autogen"

# Batch fetch details from search results
node scripts/github-search.mjs "agent" --output json | node scripts/batch-detail.mjs
```

## Features

- 🔍 **Precise search** — Find repos by keywords, language, stars, activity
- 📊 **Multi-dimensional filtering** — Stars, language, forks, update frequency
- 📈 **Trend analysis** — Identify active projects and emerging trends
- 🏷️ **Auto-extraction** — Tags and topics from repository metadata
- 📋 **Structured output** — Markdown tables, JSON, CSV
- 🚀 **Batch processing** — Fetch details for multiple repos at once

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `query` | Search keywords | **required** |
| `--language` | Programming language filter | none |
| `--min-stars` | Minimum stars | 100 |
| `--max-stars` | Maximum stars | unlimited |
| `--updated-within` | Updated within N days | 365 |
| `--created-after` | Created after date (ISO 8601) | none |
| `--sort` | Sort by: stars, updated, forks | stars |
| `--order` | Order: asc, desc | desc |
| `--limit` | Results limit | 10 |
| `--output` | Format: table, json, csv | table |

## Usage examples

### Search across domains

```bash
# AI agents and multi-agent systems
node scripts/github-search.mjs "agent" --language python --min-stars 500 --limit 15

# Vector databases and embeddings
node scripts/github-search.mjs "vector database" --min-stars 1000 --limit 10

# RAG (Retrieval-Augmented Generation)
node scripts/github-search.mjs "rag" --language typescript --updated-within 90
```

### Repository details

```bash
# Single repository
node scripts/repo-detail.mjs "microsoft/autogen"

# Batch from search results (pipe JSON output)
node scripts/github-search.mjs "multi-agent" --output json | node scripts/batch-detail.mjs

# Batch from command-line arguments
node scripts/batch-detail.mjs "langchain-ai/langchain" "openai/openai-python"
```

### Output formats

```bash
# Default: Markdown table
node scripts/github-search.mjs "llm" --limit 5

# JSON (good for downstream processing)
node scripts/github-search.mjs "llm" --limit 5 --output json > results.json

# CSV (for Excel/data analysis)
node scripts/github-search.mjs "llm" --limit 5 --output csv > results.csv
```

### Batch workflow

```bash
#!/bin/bash
# Research multiple topics and generate unified report

echo "# Research Report" > report.md
echo "" >> report.md

TOPICS=("agent memory" "rag" "vector database" "llm orchestration")

for topic in "${TOPICS[@]}"; do
  echo "## $topic" >> report.md
  node scripts/github-search.mjs "$topic" \
    --min-stars 500 \
    --limit 10 \
    --output json | \
    node scripts/batch-detail.mjs >> report.md
  echo "" >> report.md
done

echo "✅ Report generated: report.md"
```

## Output examples

### Search results (table format)

```markdown
## 🔥 GitHub 热门项目: agent memory

| 排名 | 项目 | ⭐ Stars | 🍴 Forks | 💻 语言 | 📅 更新 | 🔗 链接 |
|-----|------|---------|---------|--------|--------|--------|
| 1 | microsoft/autogen | 32.5k | 4.8k | Python | 2天前 | [查看](https://github.com/microsoft/autogen) |
| 2 | langchain-ai/langchain | 89.2k | 14.1k | Python | 1天前 | [查看](https://github.com/langchain-ai/langchain) |

### 📊 统计摘要
- **总项目数**: 15
- **平均 Stars**: 5,230
- **主要语言**: Python (80%), TypeScript (13%)
- **活跃度**: 73% 最近30天有更新
```

### Repository details

```markdown
## 📋 项目详情: microsoft/autogen

**名称**: AutoGen
**描述**: A programming framework for building AI agents
**🏷️ 标签**: ai-agents, multi-agent, llm, python

### 📈 数据统计
- ⭐ **Stars**: 32,547
- 🍴 **Forks**: 4,823
- 👁️ **Watchers**: 1,250

### 💻 代码信息
- **主要语言**: Python
- **许可证**: MIT
- **默认分支**: main
- **仓库大小**: 15,234 kB

### 📅 活跃度
- **最后提交**: 2天前 (🟢 非常活跃)
- **创建时间**: 2023年8月15日
- **更新时间**: 2024年3月13日

### 🔗 链接
- **仓库**: https://github.com/microsoft/autogen
- **Issues**: https://github.com/microsoft/autogen/issues
- **Pull Requests**: https://github.com/microsoft/autogen/pulls
```

## API rate limits

- **Unauthenticated**: 60 requests/hour
- **Authenticated** (with GITHUB_TOKEN): 5000 requests/hour

### Configure GitHub Token (optional)

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Get a token: https://github.com/settings/tokens (create personal access token with `public_repo` scope)

## Implementation notes

- Uses native `fetch()` (Node.js 18+) — no external dependencies
- Secure headers handling (no shell injection vulnerabilities)
- Typed error handling (RateLimitError, NotFoundError, NetworkError)
- Rate limit awareness in batch operations (200ms delay between requests)
- Supports multiple input formats for batch processing

---

*GitHub Research v1.0 | Open-source research tool*
