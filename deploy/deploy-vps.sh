#!/usr/bin/env bash
# Deploy Indoeasy Scent -> VPS (34.101.66.215)
# Static site only. Nginx already configured by vps-bootstrap.sh.
#
# Usage:
#   bash deploy/deploy-vps.sh          # dry-run (tidak ada yang berubah)
#   bash deploy/deploy-vps.sh --live   # eksekusi sungguhan

set -euo pipefail

HOST="idesys-vps"   # alias -> 34.101.66.215 (Debian 13)
ROOT="/var/www/html"
SRC="$(cd "$(dirname "$0")/.." && pwd)"

LIVE=0
[ "${1:-}" = "--live" ] && LIVE=1

RSYNC_OPTS=(
  --delete
  --exclude '.git'
  --exclude 'node_modules'
  --exclude '.wrangler'
  --exclude '__pycache__'
  --exclude '*.pyc'
  --exclude 'docs'
  --exclude 'deploy'
  --exclude '.env'
)

if [ "$LIVE" -eq 1 ]; then
  echo "==> DEPLOY LIVE ke $HOST:$ROOT"
  # backup dulu, supaya ada rollback
  ssh "$HOST" "sudo tar czf /root/idesy-backup-\$(date +%Y%m%d-%H%M%S).tar.gz -C $ROOT . 2>/dev/null || true"
  rsync -avz "${RSYNC_OPTS[@]}" "$SRC/" "$HOST:$ROOT/"
else
  echo "==> DRY-RUN ke $HOST:$ROOT (tidak ada yang berubah)"
  rsync -avzn "${RSYNC_OPTS[@]}" "$SRC/" "$HOST:$ROOT/"
  exit 0
fi

echo "==> permission"
ssh "$HOST" "sudo chown -R www-data:www-data $ROOT && sudo chmod -R 755 $ROOT && sudo find $ROOT -type f -exec chmod 644 {} \;"

echo "==> verifikasi nginx"
ssh "$HOST" "sudo nginx -t"

echo
echo "=== DEPLOY SELESAI ==="
echo "File count : $(ssh "$HOST" "find $ROOT -type f | wc -l")"
echo "Size       : $(ssh "$HOST" "du -sh $ROOT | cut -f1")"
echo
echo "Uji:"
echo "  ssh $HOST 'sudo nginx -s reload'"
echo "  curl -sI --resolve indoeasyscent.com:80:34.101.66.215 http://indoeasyscent.com/ | head -3"