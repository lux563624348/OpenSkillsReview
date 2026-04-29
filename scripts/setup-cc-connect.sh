#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${HOME}/.cc-connect"
CONFIG_FILE="${CONFIG_DIR}/config.toml"

TOKEN="${1:-}"
TELEGRAM_USER_ID="${2:-}"
ALLOW_FROM="${CC_CONNECT_ALLOW_FROM:-${TELEGRAM_USER_ID}}"
ADMIN_FROM="${CC_CONNECT_ADMIN_FROM:-${ALLOW_FROM}}"
WORK_DIR="${CC_CONNECT_WORK_DIR:-${HOME}/github}"
PROJECT_NAME="${CC_CONNECT_PROJECT_NAME:-github-workspace}"

if [[ -z "${TOKEN}" || -z "${TELEGRAM_USER_ID}" ]]; then
  echo "Usage: $0 <TELEGRAM_BOT_TOKEN> <TELEGRAM_USER_ID>" >&2
  exit 1
fi

if [[ -z "${ALLOW_FROM}" ]]; then
  echo "Missing TELEGRAM_USER_ID or CC_CONNECT_ALLOW_FROM" >&2
  exit 1
fi

mkdir -p "${CONFIG_DIR}"

cat > "${CONFIG_FILE}" <<EOF
language = "en"

[log]
level = "info"

[display]
thinking_messages = true
tool_messages = false

[[projects]]
name = "${PROJECT_NAME}"

[projects.agent]
type = "codex"

[projects.agent.options]
work_dir = "${WORK_DIR}"
mode = "suggest"

[[projects.platforms]]
type = "telegram"

[projects.platforms.options]
token = "${TOKEN}"
allow_from = "${ALLOW_FROM}"
admin_from = "${ADMIN_FROM}"
EOF

if cc-connect daemon status 2>/dev/null | rg -q 'Status:\s+Running'; then
  cc-connect daemon restart
else
  cc-connect daemon install
fi
