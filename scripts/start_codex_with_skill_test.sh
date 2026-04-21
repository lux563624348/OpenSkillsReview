#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_SOURCE_DIR="${SKILL_SOURCE_DIR:-$REPO_ROOT/skill_test}"
LAUNCH_CODEX_HOME="${LAUNCH_CODEX_HOME:-$REPO_ROOT/.codex-skill-test-home}"
BASE_CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <work_dir> [skill_root_or_skill_path] [codex args...]" >&2
  exit 1
fi

WORK_DIR="$1"
shift

if [[ ! -d "$WORK_DIR" ]]; then
  echo "Error: work dir must be an existing directory: $WORK_DIR" >&2
  exit 1
fi
WORK_DIR="$(cd "$WORK_DIR" && pwd)"

INPUT_SKILL_PATH=""
if [[ $# -gt 0 ]]; then
  if [[ "$1" != -* && ( -d "$1" || ( -f "$1" && "$(basename "$1")" == "SKILL.md" ) ) ]]; then
    INPUT_SKILL_PATH="$1"
    shift
  fi
fi

mkdir -p "$LAUNCH_CODEX_HOME"

if [[ -n "$INPUT_SKILL_PATH" ]]; then
  if [[ -f "$INPUT_SKILL_PATH" && "$(basename "$INPUT_SKILL_PATH")" == "SKILL.md" ]]; then
    INPUT_SKILL_PATH="$(cd "$(dirname "$INPUT_SKILL_PATH")" && pwd)"
  fi

  if [[ ! -d "$INPUT_SKILL_PATH" ]]; then
    echo "Error: skill path must be a directory (or SKILL.md): $INPUT_SKILL_PATH" >&2
    exit 1
  fi

  mkdir -p "$SKILL_SOURCE_DIR"

  if ! find "$INPUT_SKILL_PATH" -type f -name "SKILL.md" -print -quit | grep -q .; then
    echo "Error: no SKILL.md files found under: $INPUT_SKILL_PATH" >&2
    exit 1
  fi

  # Replace previous test skills with the selected skill tree.
  find "$SKILL_SOURCE_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  cp -a "$INPUT_SKILL_PATH"/. "$SKILL_SOURCE_DIR/"
fi

# Reuse existing Codex settings and auth when available.
for filename in config.toml auth.json; do
  if [[ -f "$BASE_CODEX_HOME/$filename" ]]; then
    cp -f "$BASE_CODEX_HOME/$filename" "$LAUNCH_CODEX_HOME/$filename"
  fi
done

# Force the skill-test launcher to use the requested default model.
cat > "$LAUNCH_CODEX_HOME/config.toml" <<'EOF'
model = "gpt-5.4-mini"
model_reasoning_effort = "medium"
personality = "pragmatic"

[projects."/home/xli/github/LLC/deep_agent"]
trust_level = "trusted"

[projects."/home/xli/github/LLC/yubihana.github.io"]
trust_level = "trusted"

[projects."/home/xli/github/LLC"]
trust_level = "trusted"

[projects."/home/xli"]
trust_level = "trusted"

[projects."/home/xli/github/PSC/OpenSkillsReview"]
trust_level = "trusted"

[projects."/home/xli/github/PSC/OpenSkillsReview/Skills_Hub/Skill-Finance/polymarket-agent-skills"]
trust_level = "trusted"

[notice.model_migrations]
"gpt-5.2-codex" = "gpt-5.4"
"gpt-5.3-codex" = "gpt-5.4"

[features]
multi_agent = true
EOF

rm -rf "$LAUNCH_CODEX_HOME/skills"
ln -s "$SKILL_SOURCE_DIR" "$LAUNCH_CODEX_HOME/skills"

if ! find "$SKILL_SOURCE_DIR" -name "SKILL.md" -type f | grep -q .; then
  echo "Warning: no SKILL.md files found under $SKILL_SOURCE_DIR" >&2
fi

if [[ -f "$REPO_ROOT/.env" ]]; then
  set -a
  # Load repo-local environment variables into the Codex launch environment.
  # shellcheck disable=SC1090
  source "$REPO_ROOT/.env"
  set +a
fi

cd "$WORK_DIR"
exec env CODEX_HOME="$LAUNCH_CODEX_HOME" codex "$@"
