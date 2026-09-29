#!/usr/bin/env bash
set -euo pipefail

GLOBAL_SETTINGS="$HOME/.config/claude/settings.json"

MONOREPO_SETTINGS="$HOME/repositories/symbolith-exogram/exogram/settings.json"

global_allow=$(jq -r '.permissions.allow // [] | .[]' "$GLOBAL_SETTINGS" "$MONOREPO_SETTINGS" 2>/dev/null)
global_deny=$(jq -r '.permissions.deny // [] | .[]' "$GLOBAL_SETTINGS" 2>/dev/null)

global_all=$(printf '%s\n%s' "$global_allow" "$global_deny" | sort -u)

fd 'settings\.local\.json' "$HOME/repositories/" --hidden --no-ignore --type f \
  | while read -r file; do
    project=$(echo "$file" | sed "s|$HOME/repositories/||;s|/\.claude/settings\.local\.json||")
    jq -r '.permissions.allow // [] | .[]' "$file" 2>/dev/null \
      | while read -r perm; do
        printf '%s\t%s\n' "$perm" "$project"
      done
  done \
  | sort -t$'\t' -k1,1 \
  | while IFS=$'\t' read -r perm project; do
    if ! echo "$global_all" | grep -qxF "$perm"; then
      printf '%s\t%s\n' "$perm" "$project"
    fi
  done \
  | awk -F'\t' '{
    if ($1 != prev) {
      if (prev != "") printf "%s\t%s\n", prev, sources
      prev = $1; sources = $2
    } else {
      sources = sources ", " $2
    }
  }
  END { if (prev != "") printf "%s\t%s\n", prev, sources }'
