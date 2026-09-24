#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

COMPOSE=(docker compose -f docker-compose.yml)
STATE_FILE="deploy/active_color"
NGINX_CONF="deploy/nginx/default.conf"
RETRIES="${DEPLOY_RETRIES:-30}"
SLEEP_SECS="${DEPLOY_SLEEP:-2}"
EXPECTED_SHA="${EXPECTED_SHA:-${GIT_SHA:-${GITHUB_SHA:-}}}"

log() {
  printf '[deploy] %s\n' "$*"
}

fail() {
  printf '[deploy] ERROR: %s\n' "$*" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

write_nginx_upstream() {
  local color="$1"
  cat > "$NGINX_CONF" <<EOF
upstream app {
    server app-${color}:5000;
}

server {
    listen 80;

    location / {
        proxy_pass http://app;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
}

check_endpoint() {
  local color="$1"
  local path="$2"
  "${COMPOSE[@]}" exec -T nginx \
    wget -qO- "http://app-${color}:5000${path}"
}

wait_healthy() {
  local color="$1"
  local i
  for i in $(seq 1 "$RETRIES"); do
    if check_endpoint "$color" /health 2>/dev/null | grep -q '"status":"ok"'; then
      log "healthcheck OK on app-${color}"
      return 0
    fi
    log "waiting for app-${color} health (${i}/${RETRIES})"
    sleep "$SLEEP_SECS"
  done
  return 1
}

smoke_test() {
  local color="$1"
  local status_json
  status_json="$(check_endpoint "$color" /status)"
  if ! printf '%s\n' "$status_json" | grep -q "\"deploy_color\":\"${color}\""; then
    log "smoke test failed: expected deploy_color=${color}, got: ${status_json}"
    return 1
  fi

  if [[ -n "$EXPECTED_SHA" ]]; then
    if ! printf '%s\n' "$status_json" | grep -q "\"git_sha\":\"${EXPECTED_SHA}\""; then
      log "smoke test failed: expected git_sha=${EXPECTED_SHA}, got: ${status_json}"
      return 1
    fi
    log "git_sha OK (${EXPECTED_SHA})"
  fi

  log "smoke test OK on app-${color}"
}

rollback_inactive() {
  local color="$1"
  log "rolling back inactive color: ${color}"
  "${COMPOSE[@]}" stop "app-${color}" >/dev/null 2>&1 || true
}

main() {
  require_file "$STATE_FILE"
  require_file "$NGINX_CONF"

  local active inactive
  active="$(tr -d '[:space:]' < "$STATE_FILE")"
  [[ "$active" == "blue" || "$active" == "green" ]] \
    || fail "invalid active color in ${STATE_FILE}: ${active}"

  if [[ "$active" == "blue" ]]; then
    inactive="green"
  else
    inactive="blue"
  fi

  local up_args=(--profile "$inactive" up -d --no-deps "app-${inactive}")
  if [[ "${DEPLOY_NO_BUILD:-0}" != "1" ]]; then
    up_args=(--profile "$inactive" up -d --build --no-deps "app-${inactive}")
  fi

  log "active=${active} inactive=${inactive}"
  log "starting app-${inactive}"
  "${COMPOSE[@]}" "${up_args[@]}"

  if ! wait_healthy "$inactive"; then
    rollback_inactive "$inactive"
    fail "healthcheck failed for app-${inactive}; active color unchanged (${active})"
  fi

  if ! smoke_test "$inactive"; then
    rollback_inactive "$inactive"
    fail "smoke test failed for app-${inactive}; active color unchanged (${active})"
  fi

  log "switching nginx traffic to app-${inactive}"
  write_nginx_upstream "$inactive"
  "${COMPOSE[@]}" exec -T nginx nginx -s reload
  printf '%s\n' "$inactive" > "$STATE_FILE"

  log "stopping previous color app-${active}"
  "${COMPOSE[@]}" stop "app-${active}" >/dev/null 2>&1 || true

  log "deploy succeeded — active color is now ${inactive}"
}

main "$@"
