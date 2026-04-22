---
name: github-release-maintainer
description: Maintain a GitHub repo by producing a markdown summary of the latest release plus brief bullet points for a LinkedIn post. Use when a user asks for release updates, changelog condensation, or social-ready release highlights.
---

# GitHub Release Maintainer

Workflow for turning the most recent GitHub release into:
- A clean Markdown release update
- A short LinkedIn bullet draft

## Use this skill when
- A user asks for the latest release summary for a GitHub repository.
- A user wants release notes rewritten into concise Markdown.
- A user asks for short LinkedIn bullets based on the latest release.

## Inputs
- `repo`: `owner/repo`
- Optional: target audience, tone, hashtag preference, max bullet count

## Workflow
1. Collect latest release facts (title, tag, publish date, URL, notes).
2. Collect supporting details from compare view / merged PR titles when needed.
3. Extract user-facing changes:
- New features
- Fixes
- Performance/security changes
- Breaking changes and migration notes
4. Write two outputs:
- Markdown release summary (structured, factual, link-backed)
- LinkedIn bullets (brief, skimmable, non-hype)
5. Validate:
- Every claim must map to release notes, PRs, or commits.
- Mark inferred points explicitly when release notes are sparse.
- Include concrete dates (`YYYY-MM-DD`) and links.

## Suggested commands
```bash
gh release view --repo <owner/repo> --json name,tagName,publishedAt,url,isPrerelease,isDraft,body
gh api repos/<owner>/<repo>/releases/latest
gh api repos/<owner>/<repo>/compare/<previous_tag>...<latest_tag>
```

## Output format

### 1) Markdown release summary
```md
# <repo> Release Update: <tag>

- Release: <name>
- Tag: <tag>
- Published: <YYYY-MM-DD>
- Link: <url>

## Highlights
- ...
- ...

## Fixes and Improvements
- ...

## Breaking Changes (if any)
- ...

## Upgrade Notes
- ...

## Sources
- <release url>
- <compare/pr links>
```

### 2) LinkedIn bullet draft
```md
Release update for <repo> (<tag>, <YYYY-MM-DD>):
- ...
- ...
- ...

Read more: <release url>
#opensource #github #release
```

## Style guardrails
- Prefer plain language over marketing language.
- Keep LinkedIn bullets short (around 8-18 words each).
- Do not invent metrics, timelines, or impact claims.
- If no GitHub release exists, state that clearly and fall back to latest tag/changelog.
