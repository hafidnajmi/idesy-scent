# Google Search Console — langkah verifikasi (Domain property)

Status per 2026-10-04: apex + www sudah di VPS, 8 halaman 200, 46 JSON-LD valid,
sitemap valid, www/HTTP/panel semua 301 atau noindex dengan benar. Yang kurang
hanya pendaftaran properti di Search Console — itu tidak bisa diotomasi.

## 1. Buka Verification di Search Console

Buka https://search.google.com/search-console, login dengan akun Google yang
mengelola email @indoeasyscent.com (Google Workspace), lalu:

- menu **Settings** → **Search Console** → **Add property**
- pilih tipe **Domain**
- isi `indoeasyscent.com` (tanpa `https://`, tanpa `www.`, tanpa slash)

Penting: pakai email @indoeasyscent.com, bukan indoeasyscent@gmail.com. Akun
mana pun yang verify akan menjadi owner, dan akun lain diorganisasi yang sama
perlu di-*subscribe* sebagai user. Kalau Ingin gmail yang tetap, harus login
dengan gmail itu lalu *add user* ke properti ini nanti.

## 2. Ambil token TXT

Google menampilkan string sepanjang 64 karakter, misalnya:

    google-site-verification=A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6A7b8C9d0E1f

Salin **persis**, termasuk awalan `google-site-verification=`.

## 3. Tempel di DNS (langkah yang perlu kamu lakukan di panel hosting)

Zona DNS indoeasyscent.com dipegang nameserver `hermes.dns-parking.com` /
`artemis.dns-parking.com`. Buka panel tempat zona itu dikelola, tambah:

    Tipe   : TXT
    Nama   : @            (atau biarkan kosong = root)
    TTL    : 3600
    Nilai  : google-site-verification=<TOKEN>

Satu TXT baru aman ditambahkan tanpa menghapus yang ada. Yang sekarang ada:

    "v=spf1 include:_spf.google.com ~all"
    "google-site-verification=cipPn4o6f0SVkLlCkb0ZA6_wcejrPGVgljNRSsmgmUs"

Yang kedua itu milik properti lain yang sudah diverifikasi sebelumnya — jangan
dihapus kecuali kamu tahu itu properti lama yang memang sudah tidak dipakai.

## 4. Verifikasi di Search Console

Klik **Verify**. Biasanya selesai dalam beberapa menit karena TXT dibaca
langsung dari NS otoritatif. Kalau gagal:

- pastikan **tipe TXT**, bukan CNAME atau A
- jangan ada `https://` di nilai
- cek propagasi dari mesinmu:

      dig +short TXT indoeasyscent.com

Ia harus menampilkan baris `google-site-verification=<token>`. Kalau belum, tunggu
TTL (3600 = 1 jam, tapi nameserver parking biasanya lebih cepat).

## 5. Submit sitemap

Setelah verifikasi lolos:

- menu **Sitemaps** → **Add a sitemap**
- tempel URL penuh: `https://indoeasyscent.com/sitemap.xml`
- status yang diharapkan: **Success**

## Yang sudah otomatis (tidak perlu kamu lakukan)

- 6 URL di sitemap.xml + `lastmod` per halaman (2 halaman noindex sengaja dikeluarkan)
- `robots.txt` mengarahkan ke sitemap
- canonical self-referential di 8 halaman
- `www` → apex 301, HTTP → HTTPS 301 (tidak ada duplicate content)
- 404 branded dengan `noindex, follow`
- `analytics.` dan `panelhosting.` punya header `X-Robots-Tag: noindex`
- Umami sudah merekam visitor (tracker di js/analytics.js, semua 9 halaman)

## Catatan

- Privasi: tracker dimatikan kalau `navigator.doNotTrack === '1'`.
  Itu keputusan privasi, bukan bug.
- Untuk GA4 nanti, pola yang sama: buat file `js/analytics-ga4.js` terpisah, jangan
  taruh di `cart.js`.