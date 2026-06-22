#!/usr/bin/env bash
# Despliega Formación Pública a la Raspberry Pi:
#   build local -> rsync (app + public/ + requirements) -> pip install -> restart.
# El túnel Cloudflare y el DNS ya apuntan al servicio; no se tocan.
#
# Uso:   web/deploy.sh
#   SKIP_BUILD=1 web/deploy.sh        # no reconstruir, solo sincronizar
#   REMOTE_HOST=raspi REMOTE_DIR=... web/deploy.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_HOST="${REMOTE_HOST:-raspi}"
REMOTE_DIR="${REMOTE_DIR:-/home/server-f1/projects/formacion-publica}"
SERVICE="${SERVICE:-formacion-publica}"
PORT="${PORT:-5001}"

if [ "${SKIP_BUILD:-0}" != "1" ]; then
  "$HERE/build.sh"
fi

[ -d "$HERE/public" ] && [ -n "$(ls -A "$HERE/public" 2>/dev/null)" ] || {
  echo "ERROR: web/public/ vacío. Ejecuta build.sh primero."; exit 1; }

echo "==> Sincronizando a $REMOTE_HOST:$REMOTE_DIR"
# Estático: --delete para limpiar artefactos viejos del sitio.
rsync -az --delete "$HERE/public/" "$REMOTE_HOST:$REMOTE_DIR/public/"
# App y deps: SIN --delete (no tocar venv/ ni otros archivos del proyecto).
rsync -az "$HERE/app/" "$REMOTE_HOST:$REMOTE_DIR/app/"
rsync -az "$HERE/requirements.txt" "$REMOTE_HOST:$REMOTE_DIR/requirements.txt"

echo "==> Instalando deps y reiniciando '$SERVICE'"
ssh "$REMOTE_HOST" "cd '$REMOTE_DIR' && venv/bin/pip install -q -r requirements.txt && sudo systemctl restart '$SERVICE'"

echo "==> Verificación (local en la Pi)"
sleep 2
ssh "$REMOTE_HOST" "curl -fsS http://127.0.0.1:$PORT/health && echo && curl -fsS -o /dev/null -w 'GET / -> %{http_code}\n' http://127.0.0.1:$PORT/ && curl -fsS -o /dev/null -w 'GET /lite/ -> %{http_code}\n' http://127.0.0.1:$PORT/lite/"
echo "Deploy OK."
