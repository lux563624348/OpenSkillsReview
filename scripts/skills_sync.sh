#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_REPO_PATHS=(
  "Skills_Hub/Skill-Science/claude-scientific-skills"
  "Skills_Hub/Skill-Science/ClawBio"
  "Skills_Hub/Skill-Finance/Awesome-finance-skills"
  "Skills_Hub/Skill-Finance/OpenFinTech"
  "Skills_Hub/Skill-Finance/binance-skills-hub"
)

for rel_repo_path in "${SKILL_REPO_PATHS[@]}"; do
  upstream_repo_dir="$REPO_ROOT/$rel_repo_path"
  source_dir="$upstream_repo_dir"
  rel_dest_path="${rel_repo_path#Skills_Hub/}"
  dest_dir="$REPO_ROOT/skills/$rel_dest_path"

  if [[ ! -d "$upstream_repo_dir/.git" ]]; then
    echo "Error: source repo not found at $upstream_repo_dir"
    exit 1
  fi

  if [[ "$rel_dest_path" == "$rel_repo_path" ]]; then
    echo "Error: expected path under Skills_Hub/, got: $rel_repo_path"
    exit 1
  fi

  echo "Running git pull in: $upstream_repo_dir"
  git -C "$upstream_repo_dir" pull

  echo "Syncing $source_dir -> $dest_dir"
  mkdir -p "$dest_dir"
  find "$dest_dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  find "$source_dir" -mindepth 1 -maxdepth 1 ! -name ".git" -exec cp -a {} "$dest_dir"/ \;
done

echo "Sync completed for all configured folders."
