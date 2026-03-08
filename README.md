# OpenSkillsReview

OpenSkillsReview is an open-source initiative to review the most popular AI Agent Skills, document their behavior, and surface the reliable, testable implementations that agents can trust. We keep an ongoing catalog of knowledge that agents can inspect before invoking third-party Skills so that every action has a verified safety and performance profile.

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
