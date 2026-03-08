#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
UPSTREAM_REPO_DIR="$REPO_ROOT/Skills_Hub/claude-scientific-skills"
SOURCE_DIR="$UPSTREAM_REPO_DIR/scientific-skills"
DEST_PARENT="$REPO_ROOT/skills/Skill-Science/claude-scientific-skills"
DEST_DIR="$DEST_PARENT"

if [[ ! -d "$UPSTREAM_REPO_DIR/.git" ]]; then
  echo "Error: source repo not found at $UPSTREAM_REPO_DIR"
  exit 1
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Error: source folder not found at $SOURCE_DIR"
  exit 1
fi

echo "Running git pull in: $UPSTREAM_REPO_DIR"
git -C "$UPSTREAM_REPO_DIR" pull

echo "Syncing folder to: $DEST_DIR"
mkdir -p "$DEST_PARENT"
find "$DEST_PARENT" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -exec cp -a {} "$DEST_DIR"/ \;

echo "Sync completed."
