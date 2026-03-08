#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_REPO_PATHS=(
  "Skills_Hub/claude-scientific-skills"
  "Skills_Hub/Awesome-finance-skills"
  "Skills_Hub/OpenFinTech"
  "Skills_Hub/binance-skills-hub"
)

for rel_repo_path in "${SKILL_REPO_PATHS[@]}"; do
  upstream_repo_dir="$REPO_ROOT/$rel_repo_path"
  repo_name="$(basename "$upstream_repo_dir")"

  if [[ ! -d "$upstream_repo_dir/.git" ]]; then
    echo "Error: source repo not found at $upstream_repo_dir"
    exit 1
  fi

  # Source auto-detection:
  # 1) scientific-skills folder
  # 2) skills folder
  # 3) repo root
  if [[ -d "$upstream_repo_dir/scientific-skills" ]]; then
    source_dir="$upstream_repo_dir/scientific-skills"
  elif [[ -d "$upstream_repo_dir/skills" ]]; then
    source_dir="$upstream_repo_dir/skills"
  else
    source_dir="$upstream_repo_dir"
  fi

  # Category auto-routing:
  # - repos containing "scientific" go to Skill-Science
  # - everything else defaults to Skill-Finance
  repo_name_lc="$(printf '%s' "$repo_name" | tr '[:upper:]' '[:lower:]')"
  if [[ "$repo_name_lc" == *scientific* ]]; then
    skill_category="Skill-Science"
  else
    skill_category="Skill-Finance"
  fi

  dest_dir="$REPO_ROOT/skills/$skill_category/$repo_name"

  echo "Running git pull in: $upstream_repo_dir"
  git -C "$upstream_repo_dir" pull

  echo "Syncing $source_dir -> $dest_dir"
  mkdir -p "$dest_dir"
  find "$dest_dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  find "$source_dir" -mindepth 1 -maxdepth 1 ! -name ".git" -exec cp -a {} "$dest_dir"/ \;
done

echo "Sync completed for all configured folders."
