# Jadwal Pemantauan SEO — indoeasyscent.com

Semua groundwork teknis selesai dan terverifikasi 2026-10-04. Yang tersisa
adalah menunggu dan bereaksi atas data. Tanggal di bawah adalah titik cek,
bukan promise akan ada perubahan.

## Timeline

| Kapan | Cek di | Yang dicari |
|---|---|---|
| 2026-10-07 (3 hari) | GSC → Performance | Data mulai masuk. Yang penting bukan impression, tapi query dengan impression tinggi + CTR rendah. Itu masalah judul/deskripsi. |
| 2026-10-11 (7 hari) | GSC → Coverage | Halaman penting muncul di "Excluded"? `checkout.html` & `terms-of-service.html` sebagai "Disallowed" itu benar dan diharapkan. |
| 2026-10-18 (14 hari) | GSC + Umami | Baseline traffic. Umami mulai mencatat sejak 2026-10-04, jadi ini ~2 minggu data pertama. |
| 2026-11-04 (30 hari) | Umami → Pages | Halaman mana yang membawa traffic tapi tidak konversi ke WhatsApp. Itu halaman berikutnya untuk dikerjakan. |

## Prosedur Request Indexing

1. GSC → bilah pencarian atas → ketik URL lengkap, misalnya
   `https://indoeasyscent.com/products.html`
2. Google menampilkan "URL is on Google" atau "URL is not on Google"
3. Klik **Request Indexing** → tunggu "Request received"
4. Ulangi untuk halaman berikutnya

Lakukan untuk: `/`, `products.html`, `collection.html`. Jangan untuk
`contact.html` dan `about.html` — nilainya rendah, biarkan Google datang
saat memang relevan.

## Yang sudah otomatis dan tidak perlu dikerjakan ulang

- Sitemap: 6 URL, XML valid, `lastmod` per halaman, tidak ada URL terlarang
- robots.txt: `Disallow` 2 halaman + arahkan ke sitemap
- `checkout.html`, `terms-of-service.html`: `noindex, follow` di meta
- Canonical self-referential di 8 halaman, `www` → apex 301, HTTP → HTTPS 301
- 404 branded dengan `noindex, follow`
- `analytics.` + `panelhosting.`: `X-Robots-Tag: noindex`
- 46 JSON-LD node valid terhadap schema.org vocabulary
- Heading: tiap halaman punya tepat 1 `<h1>`, semua berisi teks
- Umami merekam traffic via `js/analytics.js` (semua 9 halaman)

## Kalau ada masalah

**Halaman penting tidak ter-index.** Cek URL Inspection untuk URL-nya.
Kalau muncul "Crawled - currently not indexed", itu biasanya masalah kualitas
konten, bukan markup. Periksa apakah halaman punya inbound link.

**CTR rendah padahal impression tinggi.** Ubah `<title>` dan
`<meta name="description">`. Setelah diubah, jalankan `npm run seo:inject`
lalu Request Indexing ulang.

**Sitemap gagal di GSC.** Jalankan dari mesin ini:
`curl -sI https://indoeasyscent.com/sitemap.xml` — harus balas 200 dengan
`content-type: text/xml`.

**Umami tidak merekam apa pun.** Cek dua hal: `js/analytics.js` harus
balas 200, dan CSP di `deploy/nginx/indoeasyscent.conf` harus memuat
`https://analytics.indoeasyscent.com` di `script-src`. Gejalanya tracker
tidak error tapi `window.umami` undefined — terlihat seperti URL salah,
padahal CSP yang memblokir.