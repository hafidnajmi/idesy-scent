# Migrasi: Cloudflare Pages → VPS Pribadi

Domain: `indoeasyscent.com`
Stack target: Ubuntu/Debian + Nginx, static files only (tanpa PHP/Node)
Repo sumber: `/home/pandeandhika/Documents/idesy-scent-main`

---

## 0. Ringkasan

Sekitar 30–45 menit aktif, tergantung upload bandwidth. Yang berubah: hosting. Yang tidak berubah: seluruh kode situs.

```
Sebelum:  DNS → Cloudflare Pages (indoeasyscent.pages.dev) + CNAME indoeasyscent.com
Sesudah: DNS → VPS (A record ke IP VPS) + Nginx serve /var/www/html
```

> Penting: ini **bukan** memindahkan DNS ke Cloudflare proxy. Sesuai keputusan, DNS dipindah penuh ke registrar — Cloudflare Pages dinonaktifkan.

---

## 1. Persiapan VPS

### 1.1 Install Nginx +Certbot

```bash
ssh root@IP_VPS_ANDA

apt update && apt upgrade -y
apt install -y nginx certbot python3-certbot-nginx rsync ufw fail2ban

# Firewall: hanya SSH + HTTP/HTTPS
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
```

### 1.2 Buat user non-root untuk deploy (opsional tapi disarankan)

```bash
adduser --disabled-password --gecos "" deploy
usermod -aG www-data deploy
mkdir -p /var/www/html
chown -R deploy:www-data /var/www/html
```

### 1.3 Arahkan domain ke VPS (SEBELUM SSL)

Di registrar tempat `indoeasyscent.com` terdaftar (bukan di Cloudflare):

```
A     @     IP_VPS_ANDA
A     www   IP_VPS_ANDA
```
Hapus record lama yang mengarah ke Cloudflare Pages.

Verifikasi propagasi (bisa butuh 1–24 jam):
```bash
dig +short indoeasyscent.com
# harus mengembalikan IP VPS Anda
```

> Timeout SSL: sementara tidak bisa HTTPS di direktori /var/www/html — biarkan dulu, SSL di langkah 3.

---

## 2. Upload site

Dari mesin lokal:

```bash
# Dry-run dulu: berapa yang akan terkirim
rsync -avzn --delete \
  --exclude '.wrangler' \
  --exclude 'node_modules' \
  --exclude '.git' \
  --exclude 'docs' \
  --exclude 'deploy' \
  /home/pandeandhika/Documents/idesy-scent-main/ \
  deploy@IP_VPS_ANDA:/var/www/html/
```

Kalau approve, jalankan tanpa `-n` (`-a` sudah termasuk delete). **Hapus `--delete`** untuk run pertama supaya tidak ada yang hilang.

Atur permission di server:
```bash
chown -R deploy:www-data /var/www/html
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;
```

### 2.1 Verifikasi upload
```bash
curl -sI http://indoeasyscent.com/ | head -5
curl -s http://indoeasyscent.com/robots.txt
curl -s http://indoeasyscent.com/sitemap.xml | head -5
```

---

## 3. SSL dengan Let's Encrypt

```bash
certbot --nginx -d indoeasyscent.com -d www.indoeasyscent.com \
  --redirect --agree-tos -m EMAIL_ANDA@example.com --no-eff-email
```

Certbot otomatis:
- Memasang sertifikat
- Mengubah config Nginx untuk redirect HTTP→HTTPS
- Menjalankan timer renewal (`certbot.timer`, cek dengan `systemctl list-timers | grep certbot`)

---

## 4. Pasang config Nginx

Di server:
```bash
cp deploy/nginx/indoeasyscent.conf /etc/nginx/sites-available/indoeasyscent.com
ln -s /etc/nginx/sites-available/indoeasyscent.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
```

> Config di repo sudah mencakup blok HTTP→HTTPS dan www→non-www. Karena Certbot sudah memodifikasi `sites-available`, **periksa hasilnya** — duplikasi blok `server` akan membuat `nginx -t` gagal. Kalau gagal, pakai config repo sebagai ganti total ( Certbot sebelumnya tidak perlu dihapus manual, cukup reload).

---

## 5. Checklist verifikasi

```bash
# HTTPS & redirect
curl -sI http://indoeasyscent.com/ | grep -i location
# harus: 301 ke https

curl -sI https://www.indoeasyscent.com/ | grep -i location
# harus: 301 ke https://indoeasyscent.com

# Security headers
curl -sI https://indoeasyscent.com/ | grep -iE 'content-security|x-frame|x-content|referrer|strict-transport'

# Konten
curl -s https://indoeasyscent.com/ | grep -o '<title>[^<]*'

# SEO files
curl -s https://indoeasyscent.com/robots.txt
curl -s https://indoeasyscent.com/sitemap.xml | head

# Kompresi
curl -sI -H 'Accept-Encoding: gzip' https://indoeasyscent.com/ | grep -i content-encoding

# 404
curl -sI https://indoeasyscent.com/halaman-tidak-ada.html | head -1
```

Test di browser: buka semua 8 halaman, cek navbar, cart drawer, dan form inquiry masih berfungsi (semua JS lokal, harusnya tidak ada perubahan).

---

## 6. Backup Cloudflare Pages (sebelum dimatikan)

Di dashboard Cloudflare → Pages → project `idesy-scent`, unduh build/latest sebagai zip. Simpan offline. Jangan hapus project sampai 1–2 minggu setelah migrasi stabil.

---

## 7. Matikan Cloudflare Pages

Setelah semua verifikasi lulus dan 1–2 minggu stabil:
1. Cloudflare dashboard → Pages → `idesy-scent` → hapus project
2. Hapus DNS record lama di Cloudflare (kalau masih ada)
3. Bersihkan repo: `CNAME`, `wrangler.toml`, `index.js`, `_headers` — atau simpan di `deploy/cloudflare-legacy/` sebagai arsip

`npm run deploy` (script `wrangler pages deploy`) **tidak akan berfungsi lagi** setelah ini — ganti dengan rsync, atau tulis ulang script jadi:

```json
"deploy": "rsync -avz --delete --exclude '.wrangler' --exclude 'node_modules' --exclude '.git' --exclude 'docs' --exclude 'deploy' ./ deploy@IP_VPS_ANDA:/var/www/html/ && ssh deploy@IP_VPS_ANDA 'chown -R deploy:www-data /var/www/html'"
```

---

## 8. Credential & akses

Simpan somewhere yang aman:
- IP VPS
- SSH key / password
- Email Let's Encrypt (untuk expiry notice)
- Cloudflare account (untuk Pages lama, sampai dihapus)

---

## 9. Maintenance

Update Nginx:
```bash
vim /etc/nginx/sites-available/indoeasyscent.com
nginx -t && systemctl reload nginx
```

Renew SSL (otomatis, tapi cek):
```bash
certbot renew --dry-run
```

Backup:
```bash
# Cron harian, tar ke /var/backups
0 3 * * * rsync -a --delete /var/www/html/ /var/backups/idesy-html/
```

Update keamanan:
```bash
apt upgrade -y && needrestart
```

---

## 10. Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `502 Bad Gateway` | Nginx jalan, tapi tidak ada file | `ls -la /var/www/html/index.html`, cek permission |
| SSL error di browser | Sertifikat belum terbit / expired | `certbot certificates`, `certbot renew` |
| `nginx -t` gagal "duplicate server" | Config repo + Certbot duplikat | `rm sites-enabled/default`, reload single config |
| Halaman lama masih tampil | Cache browser | Hard reload (Ctrl+Shift+R) |
| 404 di semua halaman | `root` salah di config | `grep root /etc/nginx/sites-enabled/indoeasyscent.com` → harus `/var/www/html` |
| Gambar tidak load | Permission | `chown -R deploy:www-data /var/www/html && find ... -type f -exec chmod 644` |
| Host mismatch | Propagation DNS belum selesai | tunggu TTL, `dig indoeasyscent.com` |
| Gaya hilang (Tailwind) | CSP memblokir `cdn.tailwindcss.com` | Cek header CSP vs config, jangan ubah CSP acak |

---

## 11. Alur rollback

Kalau migrasi gagal dan mau kembali ke Cloudflare Pages:
1. Restore DNS A record → IP Cloudflare (atau restore CNAME ke `indoeasyscent.pages.dev`)
2. Restore project Pages dari backup zip
3. Tunggu propagasi DNS (24–48 jam)
4. Update docs/SEO.md untuk menandai hosting kembali Cloudflare
