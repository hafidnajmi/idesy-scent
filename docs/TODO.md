# TODO — Indoeasy Scent: SEO Setup & Migrasi VPS

Status legenda: `[x]` selesai & terverifikasi · `[ ]` belum dikerjakan
Target: `indoeasyscent.com` di VPS pribadi (Ubuntu/Debian + Nginx, static only)

---

## FASE 0 — Fondasi repo (WAJIB PERTAMA)

- [ ] `git init` di `/home/pandeandhika/Documents/idesy-scent-main`
- [ ] `git add -A && git commit -m "Initial: static site Indoeasy Scent (pre-migrasi VPS)"`
- [ ] Pastikan `.gitignore` sudah cover `.wrangler/` (sudah ada — verify)
- [ ] Pastikan `docs/` & `deploy/` ikut ter-commit (sebagai referensi tim)
- [ ] Buat branch `feat/seo-metadata` untuk semua perubahan HTML

> Alasan: repo tidak punya `.git` sama sekali. Tanpa ini, salah ubah 8 file HTML = tidak ada rollback.

---

## FASE 1 — Sudah Selesai (dari sesi ini)

- [x] Audit SEO awal — 8 halaman, temuan & prioritas ada di `docs/SEO.md`
- [x] `robots.txt` — Allow all, Disallow `/checkout.html` + `/terms-of-service.html`, pointer sitemap
- [x] `sitemap.xml` — 8 URL dengan `changefreq` + `priority` (valid XML, terverifikasi)
- [x] `deploy/nginx/indoeasyscent.conf` — HTTPS redirect, HSTS, CSP, gzip, cache policy, www→non-www, static-only hardening, rate limit, 404 handler
- [x] `docs/SEO.md` — rencana structured data & metadata per halaman
- [x] `docs/MIGRATION-VPS.md` — runbook migrasi lengkap + troubleshooting + rollback
- [x] Hermes skill `idesy-scent-seo-vps` — agar sesi berikutnya load konteks project ini
- [x] `npm run build` masih jalan (verified: "Static Site Ready")

---

## FASE 2 — Metadata HTML (seo Dasar, Impact Tinggi)

- [ ] Generate 8 cover image 1200×630 JPG, < 300KB → `img/og/{index,products,collection,about,contact,checkout,privacy,terms}.jpg`
- [ ] Inject ke `index.html`:
  - [ ] `<link rel="canonical" href="https://indoeasyscent.com/">`
  - [ ] `og:url`, `og:site_name`, `og:locale`
  - [ ] Twitter Card (`summary_large_image` + title/desc/image)
  - [ ] Ganti `og:image` dari logo PNG → `img/og/index.jpg`
- [ ] Inject `canonical` + `og:url` + Twitter Card ke 7 halaman lainnya
- [ ] Ganti `og:image` di semua halaman ke cover yang sesuai
- [ ] Verifikasi: `curl -s https://indoeasyscent.com/ | grep canonical`

---

## FASE 3 — Structured Data (JSON-LD)

- [ ] `index.html` → JSON-LD `LocalBusiness` (+ `geo` dari koordinat Google Maps yang sudah ada di `contact.html`)
- [ ] `contact.html` → JSON-LD `ContactPage`
- [ ] `products.html` → JSON-LD `Product` per produk ISX Series (SKU dari nama file, mis. `ISX-I-0`)
- [ ] `collection.html` → JSON-LD `Product` per fragrance
- [ ] `products.html` → JSON-LD `Service` (sewa diffuser, instalasi, perawatan, trial)
- [ ] `BreadcrumbList` di 7 halaman non-index
- [ ] Validasi SEMUA JSON-LD di https://validator.schema.org/ → harus 0 error
- [ ] Test di https://search.google.com/test/rich-results

> PENTING: jangan tulis `price` di `offers` — model B2B inquiry, tidak ada harga publik. Omit field tersebut.

---

## FASE 4 — On-Page Technical

- [ ] Perbaiki `alt` text gambar produk di `products.html` & `collection.html` (deskriptif,mengandung keyword utama)
- [ ] Buat `404.html` (Nginx sudah mereferensikannya — sekarang akan 404 error)
- [ ] Link ke `/404.html` yang estetis, matching brand
- [ ] Download asset yang di-hotlink `lh3.googleusercontent.com` ke `img/` lokal
- [ ] Ganti URL hotlink di `contact.html` (Maps iframe boleh tetap — `frame-src` sudah diizinkan)
- [ ] Periksa heading hierarchy di tiap halaman (H1 → H2 → H3, tidak ada lompatan)
- [ ] Pastikan `h1` tiap halaman lebih deskriptif & berisi keyword utama

---

## FASE 5 — SEO Eksternal & Tracking

- [ ] Buat account **Google Search Console** — verifikasi domain via DNS TXT
- [ ] Submit `https://indoeasyscent.com/sitemap.xml`
- [ ] Pasang **GA4** — buat file baru `js/analytics.js` (JANGAN taruh di `js/cart.js`, pisahkan)
- [ ] Verifikasi GA4 realtime & GSC property terbentuk
- [ ] Daftar **Google Business Profile** (penting untuk Local Pack — bisnis lokal dengan alamat fisik di Bekasi)
- [ ] Daftar di Bing Webmaster Tools
- [ ] Backlink: daftarkan ke direktori bisnis Indonesia, Chamber of Commerce, dll

---

## FASE 6 — Setup VPS

- [ ] Siapkan VPS Ubuntu/Debian — catat IP
- [ ] `apt install nginx certbot python3-certbot-nginx rsync ufw fail2ban`
- [ ] Setup firewall: `ufw allow OpenSSH && ufw allow 'Nginx Full' && ufw enable`
- [ ] Buat user `deploy` non-root, group `www-data`
- [ ] Buat SSH key untuk `deploy`, salin `~/.ssh/authorized_keys`
- [ ] Hardening SSH: disable password login, disable root login (`sshd_config`)
- [ ] `swapfile` jika RAM < 1GB
- [ ] Timezone server → Asia/Jakarta (`timedatectl`)
- [ ] `apt install unattended-upgrades` → auto security patch
- [ ] Setup logrotate untuk log Nginx

---

## FASE 7 — Migrasi Domain & DNS

- [ ] Backup lokal repo dulu (zip/tar ke tempat aman)
- [ ] Di registrar: A record `@` → IP VPS, A record `www` → IP VPS
- [ ] Hapus record lama yang mengarah ke Cloudflare Pages
- [ ] Verifikasi propagasi: `dig +short indoeasyscent.com` (bisa 1–24 jam)
- [ ] JANGAN hapus project Cloudflare Pages dulu — tunggu stabil

---

## FASE 8 — SSL & Nginx

- [ ] `certbot --nginx -d indoeasyscent.com -d www.indoeasyscent.com --redirect --agree-tos -m EMAIL --no-eff-email`
- [ ] Copy config repo → `/etc/nginx/sites-available/indoeasyscent.com`
- [ ] Symlink ke `sites-enabled`, hapus `default`
- [ ] **`nginx -t`** ← WAJIB, kemungkinan konflik dengan Certbot (lihat troubleshooting)
- [ ] `systemctl reload nginx`
- [ ] Verifikasi renewal: `certbot renew --dry-run` + `systemctl list-timers | grep certbot`

---

## FASE 9 — Deploy Konten

- [ ] `rsync -avzn --delete --exclude '.wrangler' --exclude 'node_modules' --exclude '.git' ./ deploy@IP:/var/www/html/` (dry-run dulu)
- [ ] Jalankan tanpa `-n` (hapus `--delete` untuk run pertama)
- [ ] Fix permission: `chown -R deploy:www-data /var/www/html` + `chmod 755/644`
- [ ] Update script `package.json`: ganti `deploy` dari wrangler → rsync
- [ ] Manual test di browser: 8 halaman, navbar, cart drawer, form inquiry, smooth transition

---

## FASE 10 — Verifikasi End-to-End

- [ ] `curl -sI http://indoeasyscent.com/ | grep location` → 301 ke https
- [ ] `curl -sI https://www.indoeasyscent.com/ | grep location` → 301 ke non-www
- [ ] `curl -sI https://indoeasyscent.com/ | grep -iE 'content-security|strict-transport|x-frame|x-content|referrer'`
- [ ] `curl -s https://indoeasyscent.com/robots.txt`
- [ ] `curl -s https://indoeasyscent.com/sitemap.xml | head`
- [ ] `curl -sI -H 'Accept-Encoding: gzip' https://indoeasyscent.com/ | grep content-encoding`
- [ ] `curl -sI https://indoeasyscent.com/tidak-ada.html` → 404 dengan halaman custom
- [ ] PageSpeed Insights: target Performance > 85, SEO > 90, LCP < 2.5s, CLS < 0.1
- [ ] SSL Labs test: target A atau A+
- [ ] Test semua 8 halaman di validator.w3.org/nu/

---

## FASE 11 — Decommission Cloudflare Pages

- [ ] Tunggu 1–2 minggu stabil, cek Search Console tidak ada traffic drop
- [ ] Download backup build dari Cloudflare Pages dashboard (simpan offline)
- [ ] Hapus project Pages `idesy-scent`
- [ ] Hapus DNS record lama di Cloudflare
- [ ] Bersihkan repo: pindahkan `CNAME`, `wrangler.toml`, `index.js`, `_headers` ke `deploy/cloudflare-legacy/` sebagai arsip
- [ ] Commit final

---

## FASE 12 — Maintenance (Setup Sekali)

- [ ] Cron backup harian: `0 3 * * * rsync -a --delete /var/www/html/ /var/backups/idesy-html/`
- [ ] Cron monitoring uptime: setiap 5 menit `curl -sf https://indoeasyscent.com/`
- [ ] Alert email kalau SSL tinggal < 14 hari
- [ ] Dokumentasi credentials di password manager (IP VPS, SSH key, email Let's Encrypt)
- [ ] Update `docs/MIGRATION-VPS.md` bagian maintenance dengan command aktual
- [ ] Review keamanan berkala: `fail2ban-client status`, `journalctl -u nginx`

---

## PRIORITAS JIKA WAKTU TERBATAS

**Penting (-impact langsung):**
1. FASE 0 — git init (15 menit, protects semua kerjaan berikutnya)
2. FASE 2 — canonical + og:image + Twitter Card (quick win, langsung CTR)
3. FASE 7 — DNS A record
4. FASE 8 — SSL + Nginx
5. FASE 9 — deploy

**High value (impact jangka menengah):**
6. FASE 3 — JSON-LD (knowledge panel + rich results)
7. FASE 5 — GSC + GA4 (tanpa ini, optimasi done but you're flying blind)
8. FASE 10 — verifikasi end-to-end

**Nice to have:**
9. FASE 4 — on-page polish, 404 page
10. FASE 12 — monitoring & backup
11. FASE 11 — decommission Cloudflare

---

## CATATAN PENTING

- **Jangan pernah** taruh `price` di JSON-LD `Product` — model bisnis B2B inquiry, tidak ada harga publik
- **Jangan** ubah cache policy HTML jadi `immutable` — deploy baru harus langsung tampil
- **Jangan** hapus `unsafe-inline`/`unsafe-eval` dari CSP sebelum Tailwind dipindah ke build step (runtime compiler butuh keduanya)
- **Selalu** `nginx -t` sebelum `reload`
- **Selalu** test JSON-LD di validator.schema.org sebelum deploy
- **Backup sebelum** setiap `rsync --delete` (pertama kali, jangan pakai `--delete`)
- **Jangan lupa** hapus project Cloudflare Pages sebelum hapus DNS-nya

---

## QUICK REFERENCE — Command Penting

```bash
# Cek status lokal
cd /home/pandeandhika/Documents/idesy-scent-main
npm run build

# Upload ke VPS
rsync -avz --delete \
  --exclude '.wrangler' --exclude 'node_modules' \
  --exclude '.git' --exclude 'docs' --exclude 'deploy' \
  ./ deploy@IP_VPS:/var/www/html/

# Di VPS
nginx -t && systemctl reload nginx
certbot renew --dry-run
systemctl status nginx
tail -50 /var/log/nginx/indoeasyscent.error.log

# Dari lokal — verifikasi
curl -sI https://indoeasyscent.com/ | grep -iE 'location|cache-control'
curl -s https://indoeasyscent.com/sitemap.xml | head -10
```
