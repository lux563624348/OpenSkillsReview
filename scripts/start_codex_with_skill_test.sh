#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_SOURCE_DIR="${SKILL_SOURCE_DIR:-$REPO_ROOT/skill_test}"
LAUNCH_CODEX_HOME="${LAUNCH_CODEX_HOME:-$REPO_ROOT/.codex-skill-test-home}"
BASE_CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <skill_path> [codex args...]" >&2
  exit 1
fi

INPUT_SKILL_PATH="$1"
shift

if [[ -f "$INPUT_SKILL_PATH" && "$(basename "$INPUT_SKILL_PATH")" == "SKILL.md" ]]; then
  INPUT_SKILL_PATH="$(cd "$(dirname "$INPUT_SKILL_PATH")" && pwd)"
fi

if [[ ! -d "$INPUT_SKILL_PATH" ]]; then
  echo "Error: skill path must be a directory (or SKILL.md): $INPUT_SKILL_PATH" >&2
  exit 1
fi

mkdir -p "$LAUNCH_CODEX_HOME"
mkdir -p "$SKILL_SOURCE_DIR"

if [[ ! -f "$INPUT_SKILL_PATH/SKILL.md" ]]; then
  echo "Error: SKILL.md not found in: $INPUT_SKILL_PATH" >&2
  exit 1
fi

# Replace previous test skills with the selected one.
find "$SKILL_SOURCE_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
cp -a "$INPUT_SKILL_PATH" "$SKILL_SOURCE_DIR/"

# Reuse existing Codex settings and auth when available.
for filename in config.toml auth.json; do
  if [[ -f "$BASE_CODEX_HOME/$filename" ]]; then
    cp -f "$BASE_CODEX_HOME/$filename" "$LAUNCH_CODEX_HOME/$filename"
  fi
done

rm -rf "$LAUNCH_CODEX_HOME/skills"
ln -s "$SKILL_SOURCE_DIR" "$LAUNCH_CODEX_HOME/skills"

if ! find "$SKILL_SOURCE_DIR" -name "SKILL.md" -type f | grep -q .; then
  echo "Warning: no SKILL.md files found under $SKILL_SOURCE_DIR" >&2
fi

exec env CODEX_HOME="$LAUNCH_CODEX_HOME" codex "$@"
