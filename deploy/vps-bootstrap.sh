#!/usr/bin/env bash
# =============================================================================
#  Indoeasy Scent — VPS Bootstrap  (Ubuntu 24.04 / Debian 12)
#  Jalankan di VPS lewat console provider (root shell).
#  Skrip ini idempotent: aman dijalankan ulang.
#
#  Pakai:  bash <(curl -fsSL https://paste-url-anda/bootstrap.sh)   ← JANGAN, lihat catatan
#  Pakai:  salin blok di bawah ini ke console provider, lalu jalankan.
#
#  Isi:
#    1. Hardening SSH + firewall
#    2. Nginx + certbot
#    3. Swapfile (kalau RAM kecil)
#    4. Cockpit (system panel + file manager + terminal web)
#    5. Umami (SEO/analytics monitoring)
#    6. Firewall rule untuk panel
# =============================================================================

set -euo pipefail

SITE="indoeasyscent.com"
SITEALT="www.${SITE}"
DEPLOY_USER="deploy"
EMAIL_LE="CHANGE-ME@example.com"     # ← GANTI dengan email Anda
SERVER_IP="34.50.118.52"
COCKPIT_PORT="9090"
UMAMI_PORT="3001"

log()  { printf '\n\033[1;32m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m[!] %s\033[0m\n' "$*"; }
die()  { printf '\033[1;31m[x] %s\033[0m\n' "$*" >&2; exit 1; }

[ "$(id -u)" -eq 0 ] || die "jalankan sebagai root"
. /etc/os-release
echo "OS: $PRETTY_NAME"
echo "IP : $SERVER_IP"

# ---------------------------------------------------------------- 0. update
log "0/7 Update paket"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -yqq
apt-get install -yqq curl git rsync unzip nginx certbot python3-certbot-nginx \
  ufw fail2ban unattended-upgrades chrony ca-certificates

# ------------------------------------------------------- 1. swapfile (jika perlu)
log "1/7 Swapfile"
TOTAL_MB=$(free -m | awk '/^Mem:/{print $2}')
if [ "$TOTAL_MB" -lt 2048 ] && [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
  chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
  echo "swapfile 2G dibuat (RAM ${TOTAL_MB}MB)"
else
  echo "swap dilewati (RAM ${TOTAL_MB}MB, atau swap sudah ada)"
fi
swapon --show || true

# ---------------------------------------------------------- 2. time & timezone
log "2/7 Timezone → Asia/Jakarta + automatic security update"
timedatectl set-timezone Asia/Jakarta
timedatectl set-ntp true
dpkg-reconfigure -plow unattended-upgrades </dev/null || true
systemctl enable --now unattended-upgrades || true

# ------------------------------------------------------------- 3. hardening SSH
log "3/7 Hardening SSH"
cat > /etc/ssh/sshd_config.d/99-hardening.conf <<'EOF'
PermitRootLogin prohibit-password
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
X11Forwarding no
MaxAuthTries 3
ClientAliveInterval 300
EOF

# user non-root untuk deploy
if ! id "$DEPLOY_USER" >/dev/null 2>&1; then
  useradd -m -s /bin/bash "$DEPLOY_USER"
  usermod -aG www-data "$DEPLOY_USER"
  echo "user $DEPLOY_USER dibuat"
else
  echo "user $DEPLOY_USER sudah ada"
fi
echo ">>> JANGAN logout dulu. Paste public key Anda di prompt di bawah."
echo ">>> (public key dibuat dari laptop Anda; belum ada di server ini)"
mkdir -p "/home/$DEPLOY_USER/.ssh"
chmod 700 "/home/$DEPLOY_USER/.ssh"
touch "/home/$DEPLOY_USER/.ssh/authorized_keys"
chmod 600 "/home/$DEPLOY_USER/.ssh/authorized_keys"

# --------------------------------------------------------- 4. firewall (ufw)
log "4/7 Firewall ufw"
ufw --force reset >/dev/null
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 80/tcp  comment 'HTTP (acme + redirect)'
ufw allow 443/tcp comment 'HTTPS'
ufw allow "${COCKPIT_PORT}/tcp" comment 'Cockpit panel'
ufw allow "${UMAMI_PORT}/tcp" comment 'Umami analytics'
ufw --force enable
ufw status verbose

# ----------------------------------------------------------- 5. fail2ban + logrotate
log "5/7 fail2ban + logrotate"
cat > /etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
bantime  = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true
EOF
systemctl enable --now fail2ban
systemctl restart fail2ban
fail2ban-client status || true

cat > /etc/logrotate.d/nginx <<'EOF'
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
EOF

# ---------------------------------------------------------------- 6. nginx
log "6/7 Nginx — HTTP_ACME_CHALLENGE dulu (belum redirect, SSL belum ada)"
cat > /etc/nginx/sites-available/${SITE}.conf <<EOF
limit_req_zone \$binary_remote_addr zone=idesy_rl:10m rate=20r/s;

server {
    listen 80;
    listen [::]:80;
    server_name ${SITE} ${SITEALT};

    # Biarkan file statis dilayani dulu supaya Let's Encrypt bisa validasi
    root /var/www/html;
    index index.html;

    location /.well-known/acme-challenge/ { root /var/www/html; }
    location / { try_files \$uri \$uri/ =404; }
}
EOF
ln -sf /etc/nginx/sites-available/${SITE}.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
mkdir -p /var/www/html
nginx -t
systemctl enable --now nginx
systemctl reload nginx
echo "nginx aktif; /etc/nginx/sites-available/${SITE}.conf dibuat"

# ---------------------------------------------------------------- 7. Cockpit
log "7/7 Cockpit — system panel + file manager + terminal web"
apt-get install -yqq cockpit cockpit-storaged
cat > /etc/cockpit/cockpit.conf <<EOF
[Service]
WebSocketEndpoint=${COCKPIT_PORT}
EOF
systemctl enable --now cockpit.socket
echo "Cockpit aktif di port ${COCKPIT_PORT}"

# ------------------------------------------------------------------ 8. Umami
log "8/8 Umami — SEO/analytics monitoring"
command -v docker >/dev/null 2>&1 || {
  curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
  sh /tmp/get-docker.sh
  systemctl enable --now docker
}
docker pull ghcr.io/louislam/umami:postgresql-latest >/dev/null 2>&1 || true   # pre-warm
mkdir -p /opt/umami
cat > /opt/umami/docker-compose.yml <<'EOF'
services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: CHANGE_ME_DB
      POSTGRES_DB: umami
    volumes:
      - umami-db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U umami"]
      interval: 10s
      retries: 5

  umami:
    image: ghcr.io/louislam/umami:postgresql-latest
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_TYPE: postgresql
      DATABASE_URL: postgresql://umami:CHANGE_ME_DB@db:5432/umami
      DATABASE_PASSWORD: CHANGE_ME_DB
      APP_SECRET: CHANGE_ME_SECRET
    ports:
      - "3001:3000"
volumes:
  umami-db:
EOF
docker compose -f /opt/umami/docker-compose.yml up -d
docker compose -f /opt/umami/docker-compose.yml ps

# ============================================================ RINGKASAN
cat <<SUMMARY

============================================================
 BOOTSTRAP SELESAI
============================================================
 Cockpit  : https://${SERVER_IP}:${COCKPIT_PORT}/
            login = user Linux Anda (root atau ${DEPLOY_USER})
 Umami    : http://${SERVER_IP}:${UMAMI_PORT}/
            login default: admin / admin  → GANTI SEGERA
 Nginx    : /etc/nginx/sites-available/${SITE}.conf
 Site     : /var/www/html  (deploy dengan rsync)
 User     : ${DEPLOY_USER} (grup www-data)

 YANG MASIH HARUS DIJALINKAN:
 1. Paste public key ke ${HOME}/.ssh/authorized_keys
 2. certbot --nginx -d ${SITE} -d ${SITEALT} --redirect \\
      --agree-tos -m ${EMAIL_LE} --no-eff-email
 3. Copy config repo → /etc/nginx/sites-available/${SITE}.conf
    lalu: nginx -t && systemctl reload nginx
 4. rsync -avz --delete ./ ${DEPLOY_USER}@${SERVER_IP}:/var/www/html/

 CATATAN: certbot butuh A record -> ${SERVER_IP} dulu (DNS belum siap)
============================================================
SUMMARY