# SEO Setup — Indoeasy Scent (indoeasyscent.com)

Status: dokumentasi + artefak konfigurasi sudah dibuat. Metadata di HTML **belum diimplementasikan** (lihat "Todo" di bawah).

---

## 1. Kondisi SEO saat ini (hasil audit langsung ke repo)

Sudah ada, dan cukup baik:
- `<title>` + `meta description` di 8/8 halaman, dalam bahasa Indonesia
- `og:type/title/description/image` di 8/8 halaman
- `lang="id"`, charset, viewport di semua halaman
- `<h1>` tunggal per halaman (bagus — tidak ada skip heading)
- Struktur heading masuk akal, `alt` text ada
- URL yang masuk akal, tidak ada duplicate content antar halaman

Yang hilang (ini yang membuatSEO belum optimal):

| Masalah | Dampak | Prioritas |
|---|---|---|
| Tidak ada `robots.txt` | search engine roam tanpa panduan | Tinggi |
| Tidak ada `sitemap.xml` | penemuan URL lambat, halaman terlambat ter-index | Tinggi |
| Tidak ada `rel="canonical"` | risk URL duplikat & konsolidasi sinyal terpecah | Tinggi |
| Tidak ada `og:url` | URL share tidak konsisten antar halaman | Sedang |
| Tidak ada Twitter Card | tidak ada preview saat share di X/Twitter | Sedang |
| `og:image` menunjuk logo PNG kecil | preview share kosong/tidak menarik | Sedang |
| Tidak ada JSON-LD structured data | tidak eligible untuk rich result, tidak muncul di knowledge panel | Tinggi |
| Hanya 1 `h1` per halaman tapi teks `h1` sangat pendek & generik | sinyal topik lemah | Sedang |
| Tidak ada `alt` deskriptif pada sebagian gambar produk | gambar tidak muncul di Google Images | Sedang |
| Gambar dari `lh3.googleusercontent.com` di-hotlink | bisa putus, tidak ada kontrol | Rendah |
| Tidak ada tracking (GA4 / GSC / Search Console) | tidak ada data performa | Tinggi |
| Tidak ada 404 page | UX buruk saat URL salah, soft-404 | Rendah |
| Link ke marketplace (Tokopedia/Shopee) & social media tanpa atribut pelacakan | bukan masalah SEO, tapiumbra analytics jadi bising | Rendah |

---

## 2. Schema.org structured data yang direkomendasikan

Pasang di halaman yang sesuai:

**`Organization`** (semua halaman, idealnya di dalam script JSON-LD di `index.html` dan site-wide)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Indoeasy Scent",
  "alternateName": "Indoeasy Scent",
  "url": "https://indoeasyscent.com",
  "logo": "https://indoeasyscent.com/img/logo_hd.png",
  "image": "https://indoeasyscent.com/img/logo_hd.png",
  "foundingDate": "2020",
  "email": "halo@indoeasyscent.com",
  "telephone": "+62-812-8780-4396",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Jayamulya, Serang Baru, Bekasi Regency",
    "addressLocality": "Bekasi",
    "addressRegion": "Jawa Barat",
    "addressCountry": "ID"
  },
  "sameAs": [
    "https://www.instagram.com/indoeasy.scent/",
    "https://linkedin.com/company/indoeasyscent"
  ]
}
```

**`WebSite` + `SearchAction`** (index.html)

**`Product`** per produk di `products.html` dan `collection.html` — contoh untuk satu produk:
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "ISX Series — Cold-Air Micro-Diffusion",
  "image": ["https://indoeasyscent.com/img/ISX-I-0.webp"],
  "description": "Mesin commercial scenting Cold-Air Micro-Diffusion untuk hotel, retail, dan kantor.",
  "brand": { "@type": "Brand", "name": "Indoeasy Scent" },
  "sku": "ISX-I-0",
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "IDR",
    "price": "0",
    "url": "https://indoeasyscent.com/products.html",
    "priceValidUntil": "2027-12-31"
  }
}
```
> Catatan: website ini B2B "inquiry", bukan e-commerce, sehingga **tidak ada harga publik**. Google tidak mensyaratkan harga. Isi `price` dengan `"0"` atau omit field `offers` entirely — lebih baik omit daripada menampilkanRp0 yang menyesatkan.

**`LocalBusiness`** (index.html + contact.html) — ganti `Organization` dengan `LocalBusiness` agar eligible untuk Google Maps/Local Pack.

**`Service`** (products.html) — untuk "sewa diffuser", "instalasi", "perawatan", "trial".

**`FAQPage`** — jika ada FAQ di halaman mana pun (SEO FAQ dinonaktifkan di Google sejak 2023 jadi nilai线索 tetap branding, tapi schema valid tetap aman).

**`BreadcrumbList`** di semua halaman selain index.

> ⚠️ Validasi semua JSON-LD di https://validator.schema.org/ sebelum deploy. JSON-LD yang invalid bisamen downfall ranking daripada tidak ada sama sekali.

---

## 3. Perbaikan metadata per halaman

Template untuk disisipkan di dalam `<head>`, setelah `<meta name="description">`:

```html
    <link rel="canonical" href="https://indoeasyscent.com/">
    <meta property="og:url" content="https://indoeasyscent.com/">
    <meta property="og:site_name" content="Indoeasy Scent">
    <meta property="og:locale" content="id_ID">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="...">
    <meta name="twitter:description" content="...">
    <meta name="twitter:image" content="https://indoeasyscent.com/img/COVER-1200x630.jpg">
```

Perbaikan `og:image`:
- Ganti `img/LOGO%20IDESY%20SCENT.png` dengan **cover image 1200×630px** yang proper
- Buat 1 cover per halaman: `img/og/index.jpg`, `img/og/products.jpg`, dst.
- Logo PNG sekarang terlalu kecil dan memiliki whitespace — tidak menghasilkan preview yang baik
- Format JPG, < 300KB, sudah di-compress

`og:url` harus absolut dan konsisten dengan `canonical`. Untuk halaman di path yang sama, canonical = URL tanpa `.html`? **Tidak** — pertahankan `.html` seperti sekarang, tidak perlu pretty URL untuk sekarang.

### Table of metadata yang harus dipasang per halaman

| File | canonical | Priority sitemap |
|---|---|---|
| `index.html` | `https://indoeasyscent.com/` | 1.0 |
| `products.html` | `https://indoeasyscent.com/products.html` | 0.9 |
| `collection.html` | `https://indoeasyscent.com/collection.html` | 0.9 |
| `about.html` | `https://indoeasyscent.com/about.html` | 0.6 |
| `contact.html` | `https://indoeasyscent.com/contact.html` | 0.7 |
| `checkout.html` | `https://indoeasyscent.com/checkout.html` | 0.4 |
| `privacy-policy.html` | `https://indoeasyscent.com/privacy-policy.html` | 0.2 |
| `terms-of-service.html` | `https://indoeasyscent.com/terms-of-service.html` | 0.2 |

---

## 4. Technical SEO — poin yang sudah ditangani

- [x] `robots.txt` — dibuat (Allow all; Disallow `/checkout.html` + `/terms-of-service.html` karena keduanya low-value untuk hasil cari)
- [x] `sitemap.xml` — dibuat,8 URL dengan priority
- [x] Canonical plan — tabel di atas
- [x] Nginx config dengan HTTPS redirect, HSTS, gzip, cache policy
- [x] Security headers (CSP, nosniff, XFO, Referrer-Policy, Permissions-Policy) — di-port dari `_headers`
- [x] `Cache-Control: no-cache` untuk `.html` (agar deploy baru langsung tampil)
- [x] `Cache-Control: 30d` + `stale-while-revalidate` untuk aset statis
- [x] `www` → non-`www` redirect 301
- [x] Static-only hardening (tolak `.php`, `.cgi`, dotfiles)
- [x] 404 handler
- [x] Rate limiting

---

## 5. Todo — implementasi yang belum dilakukan

- [ ] Generate 8 cover image 1200×630 untuk `og:image` / Twitter Card
- [ ] Inject `canonical` + `og:url` + `og:site_name` + Twitter Card ke 8 halaman
- [ ] Inject JSON-LD `Organization` + `WebSite` ke `index.html`
- [ ] Inject JSON-LD `LocalBusiness` ke `contact.html`
- [ ] Inject JSON-LD `Product` ke `products.html` & `collection.html`
- [ ] Inject JSON-LD `BreadcrumbList` ke 7 halaman non-index
- [ ] Perbaiki `alt` text gambar produk
- [ ] Buat `404.html`
- [ ] Update `img/hero-*.webp` menjadi `og:image` yang valid
- [ ] Hapus hotlink `lh3.googleusercontent.com` — unduh asset ke `img/` lokal
- [ ] Update `sitemap.xml` & `robots.txt` di file server
- [ ] Buat account **Google Search Console** — submit sitemap
- [ ] Pasang **GA4** via `js/cart.js` atau file baru `js/analytics.js`
- [ ] Update link `CNAME` / infra dari Cloudflare Pages → VPS

---

## 6. Struktur JSON-LD di implementasikan

### index.html
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Indoeasy Scent",
  "image": "https://indoeasyscent.com/img/og/index.jpg",
  "url": "https://indoeasyscent.com/",
  "telephone": "+62-812-8780-4396",
  "email": "info@indoeasyscent.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Jayamulya, Serang Baru, Bekasi Regency",
    "addressLocality": "Bekasi",
    "addressRegion": "Jawa Barat",
    "addressCountry": "ID"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": -6.3877478, "longitude": 107.0988673 },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "hoursOpen": "09:00",
    "hoursClose": "18:00"
  },
  "sameAs": [
    "https://www.instagram.com/indoeasy.scent/",
    "https://linkedin.com/company/indoeasyscent"
  ]
}
</script>
```

### contact.html
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "newsMediaOrganization": {
    "@type": "Organization",
    "name": "Indoeasy Scent",
    "url": "https://indoeasyscent.com"
  }
}
</script>
```

### products.html — `Product` schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "ISX Series — Cold-Air Micro-Diffusion",
  "image": ["https://indoeasyscent.com/img/ISX-I-0.webp"],
  "description": "Mesin commercial scenting Cold-Air Micro-Diffusion untuk hotel, retail, dan kantor.",
  "brand": { "@type": "Brand", "name": "Indoeasy Scent" },
  "sku": "ISX-I-0",
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "IDR",
    "url": "https://indoeasyscent.com/products.html"
  }
}
</script>
```
> Omitted `price`: produk ini B2B `inquiry`-based tanpa harga publik, jadi tidak relevan untuk Google Merchant Center / Shopping.

### collection.html — `Product` per fragrance
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Fragrance SUNNY BURST",
  "image": ["https://indoeasyscent.com/img/<nama-file>.webp"],
  "brand": { "@type": "Brand", "name": "Indoeasy Scent" },
  "description": "Fragrance eksklusif Indoeasy Scent untuk hotel, butik, dan kantor.",
  "sku": "FRG-SUNNY-BURST",
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "IDR",
    "url": "https://indoeasyscent.com/collection.html"
  }
}
</script>
```

---

## 7. Verifikasi & alat

- Google Search Console: https://search.google.com/search-console (submit sitemap.xml)
- Schema validator: https://validator.schema.org/
- Rich Results Test: https://search.google.com/test/rich-results
- PageSpeed Insights: https://pagespeed.web.dev/ (target LCP < 2.5s)
- HTML validator: https://validator.w3.org/nu/
- Lighthouse via Chrome DevTools

Targets:
- Mobile Performance Score: > 85
- SEO Score: > 90
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1

---

## 8. Prioritas aksi (urutan pengerjaan)

1. **Submit sitemap ke GSC** — setelah robots.txt + sitemap.xml deployed
2. **Cover images 1200×630** — quick win, langsung impact social share & CTR
3. **JSON-LD Organization/LocalBusiness** — impact ke knowledge panel
4. **canonical + og:url + Twitter Card** — polish technical
5. **Product JSON-LD** — impact ke rich results (tidak ada harga → pakai `offers.availability` saja)
6. **alt text pada gambar produk** — impact ke Google Images
7. **404 page** — UX & trust
8. **GA4 + GSC setup** — visibility & data
9. **Hotlink removal** — reliability
10. **CSP hardening** — setelah migrasi ke Tailwind build step

---

## 9. Catatan teknis

- Bahasa dokumen: Indonesian (mengikuti bahasa situs & audiens)
- Semua jawaban & komunikasi ke user: Bahasa Indonesia
- og image specs: 1200x630px, JPG, quality 75-80, under 300KB
- Canonical: absolute, https, self-referencing (setiap halaman menunjuk ke URL-nya sendiri)
- Canonical harus point ke URL yang di-index, bukan ke URL yang redirect
- Structured data: JSON-LD (`application/ld+json`), bukan Microdata
- Validasi JSON-LD di validator.schema.org SEBELUM deploy — schema invalid lebih berbahaya daripada tidak ada sama sekali
- Jangan tulis `price: "0"` di `Product.offers` untuk model B2B inquiry; omit field `offers` atau hanya sertakan `availability` + `url`
- Ubah `no-cache` pada HTML hanya jika CDN di depan Nginx; tanpa CDN, `no-cache, must-revalidate` adalah pilihan aman
- `unsafe-inline` + `unsafe-eval` di `script-src` tidak bisa dihapus selama Tailwind dimuat dari `cdn.tailwindcss.com` (runtime compiler). Untuk mengeraskan CSP,_tailwind harus di-build ke file CSS lokal lebih dulu
- Semua URL di `sitemap.xml` harus `https://indoeasyscent.com/...` — tanpa trailing slash kecuali root
- Jangan lupa: `CNAME`, `wrangler.toml`, `index.js`, `_headers` boleh dihapus setelah migrasi ke VPS selesai & stabil

