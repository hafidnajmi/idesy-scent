# TODO — Indoeasy Scent: SEO Setup & Migrasi VPS

Status legenda: `[x]` selesai & terverifikasi · `[ ]` belum dikerjakan
Target: `indoeasyscent.com` di VPS pribadi (Ubuntu/Debian + Nginx, static only)

---

## FASE 0 — Fondasi repo (WAJIB PERTAMA)

- [x] `git init` di `/home/pandeandhika/Documents/idesy-scent-main`
- [x] `git add -A && git commit -m "Initial: static site Indoeasy Scent (pre-migrasi VPS)"`
- [x] Pastikan `.gitignore` sudah cover `.wrangler/` (sudah ada — verify)
- [x] Tambahkan `__pycache__/` + `*.pyc` ke `.gitignore`
- [x] Pastikan `docs/` & `deploy/` ikut ter-commit (sebagai referensi tim)
- [x] Branch `feat/seo-metadata` dibuat untuk semua perubahan HTML

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

## FASE 2 — Metadata HTML (Selesai)

- [x] 9 cover image 1200×630 JPG, semua <300KB (16–26KB) → `img/og/` via `deploy/gen-og-covers.sh`
- [x] Inject ke 8 halaman + `404.html`:
  - [x] `<link rel="canonical">` self-referencing, absolute https
  - [x] `og:url`, `og:site_name`, `og:locale`, `og:image` + `og:image:alt`
  - [x] Twitter Card `summary_large_image` + title/desc/image
  - [x] `og:image` logo PNG diganti cover per halaman
- [x] Semua tag di-escape dengan benar (`&amp;`)
- [x] Terverifikasi di browser: 8/8 halaman punya canonical + og:url + og:image + twitter:card
- [ ] Verifikasi setelah deploy: `curl -s https://indoeasyscent.com/ | grep canonical`

> Injector: `npm run seo:inject` (idempotent, aman di-run ulang).
> Script: `deploy/seo-inject.py`

---

## FASE 3 — Structured Data (Selesai)

- [x] `index.html` → `LocalBusiness` (dengan `geo` dari koordinat Google Maps di `contact.html`) + `WebSite`
- [x] `contact.html` → `ContactPage`
- [x] `products.html` → 24 `Product` (11 diffuser ISX + 12 fragrance + 1 reed diffuser)
- [x] `products.html` → 4 `Service` (sewa, instalasi, perawatan, trial)
- [x] `collection.html` → 4 `Product` fragrance (Musk White, Soda High, Lemongrass, Royal Tulip)
- [x] `BreadcrumbList` di 7 halaman non-index
- [x] **46 node JSON-LD lolos validasi offline terhadap vocabulary schema.org** (`npm run seo:validate`)
- [x] `@id` unik di seluruh situs (tidak ada duplikat entitas)
- [x] `Product` B2B tanpa `offers.price`; `collection.html` yang ADA harga publik → price ikut ditulis
- [ ] Test di https://search.google.com/test/rich-results (setelah deploy)

> Catatan: `foundingDate` SENGAJA tidak ditulis — tidak ada tahun berdiri di markup mana pun.
> Jangan tambahkan tanpa konfirmasi dari klien.

> PENTING: jangan tulis `price` di `offers` — model B2B inquiry, tidak ada harga publik. Omit field tersebut.

---

## FASE 4 — On-Page Technical (Sebagian selesai)

- [x] `alt` text deskriptif untuk 23 gambar katalog di `products.html` (model, jenis, kegunaan)
- [x] Logo marketplace/sertifikasi TIDAK tersentuh oleh script alt
- [x] `404.html` dibuat — branded, `noindex, follow`, cocok dengan `error_page` Nginx
- [x] 5 aset hotlink `lh3.googleusercontent.com` diunduh ke `img/` (`scent-*.webp`), HTML ditulis ulang
- [x] `sitemap.xml` + `lastmod` di 8 URL
- [ ] Link ke `/404.html` dari navbar (opsional — error_page Nginx sudah otomatis)
- [ ] Periksa heading hierarchy per halaman (h1 terlihat sudah deskriptif & unik)
- [ ] ~~`alt` di `collection.html`~~ — tidak ada `<img>` katalog di sana (pakai `data-image-url`), sudah otomatis ikut ter-localize

> CATATAN PENTING — bug latent di `collection.html`: file ini punya markup duplikat
> (2× `<footer>`, 2× CTA section, blok "Scent 4: Royal Tulip" muncul 2×, 5 scent-row
> untuk 4 scent). Schema sudah di-dedup, tapi duplikasi markup-nya belum dibersihkan.
> Perlu diputuskan: hapus blok kembar, atau memang disengaja untuk animasi JS?
> Selector JS (`#scent-list-container`, `.scent-row`) mungkin bergantung pada duplikasi ini.
> src: img/collection.html baris ~56251 vs ~77133

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

> **Penting (-impact langsung):**
1. ~~FASE 0 — git init~~ **SELESAI**
2. ~~FASE 2 — canonical + og:image + Twitter Card~~ **SELESAI**
3. **FASE 7 — DNS A record** ← ini yang memblokir semua
4. FASE 8 — SSL + Nginx
5. FASE 9 — deploy

**High value (impact jangka menengah):**
6. ~~FASE 3 — JSON-LD~~ **SELESAI** (46 node, tervalidasi)
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

# SEO — jalankan ulang setelah edit HTML
npm run seo:all        # covers + localize images + inject + validate
npm run seo:check      # idempotency check, tidak mengubah file
npm run seo:validate   # validasi JSON-LD vs vocabulary schema.org

# Upload ke VPS (dry-run dulu)
npm run deploy:dry
npm run deploy:live

# Di VPS
nginx -t && systemctl reload nginx
certbot renew --dry-run
systemctl status nginx
tail -50 /var/log/nginx/indoeasyscent.error.log

# Dari lokal — verifikasi
curl -sI https://indoeasyscent.com/ | grep -iE 'location|cache-control'
curl -s https://indoeasyscent.com/sitemap.xml | head -10
```
