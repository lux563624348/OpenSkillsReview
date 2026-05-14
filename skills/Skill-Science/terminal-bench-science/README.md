# Terminal Bench Science

This skill reviews benchmark task PRs end to end. It downloads PR artifacts, checks the task against the rubric, triages `/run` and `/cheat` trials, launches `harbor view`, and writes a structured review summary.

## When to Use

Use this skill when you need to:

- Review a benchmark task PR against the repo rubric
- Compare normal trials with cheating trials
- Inspect generated artifacts and failure modes before merging

## What It Does

1. Parses the PR URL and detects the target repository.
2. Creates a worktree for the PR and downloads PR metadata.
3. Copies the implementation and trial rubrics into the review workspace.
4. Extracts sticky CI bot comments plus `/run` and `/cheat` result comments.
5. Downloads workflow artifacts and triages the trial outputs.
6. Launches `harbor view` on a free port for interactive inspection.
7. Writes a structured `review-summary.md` with findings and a recommendation.

## Entry Point

The workflow is defined in [`SKILL.md`](SKILL.md). The skill name inside that file is `review-task`, while the folder name is `terminal-bench-science`.

## Notes

- Run this from inside a local clone of the benchmark repo.
- Required tools include `gh`, `harbor`, and `jq`.
- The review workspace is created as a sibling worktree named `review-<task-name>`.
