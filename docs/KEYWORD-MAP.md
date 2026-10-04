# Pemetaan Keyword — indoeasyscent.com

Disusun 2026-10-04 dari isi markup yang benar-benar ada, bukan dari tebakan.
Setiap keyword di bawah harus bisa dibuktikan oleh teks di halaman yang
ditujukan. Kalau someday ada layanan yang berubah, dokumen ini ikut berubah.

## 1. Yang sudah terkonfirmasi ada (dari `about.html`)

Layanan nyata yang boleh dipakai sebagai target keyword:

| Layanan | Sumber di markup |
|---|---|
| Commercial scenting terpadu, cold-air diffuser presisi | "Our Services" + "Commercial Use" |
| Wewangian & Reed Diffuser (fragrance oil premium) | "Wewangian & Reed Diffuser" |
| Sewa & instalasi diffuser presisi, pasang gratis | "Sewa & Instalasi Diffuser Presisi" |
| Refill & maintenance berkala (per bulan) | "Refill & Maintenance Berkala" |
| Trial & sampel aroma gratis | "Trial & Sampel Aroma Gratis" |
| Solusi personal use | "Personal Use" |
| Konsultasi & curation aroma | "Cara Kami Bekerja" |

Alamat: Griya Mulya Indah, Jayamulya, Kec. Serang Baru, Kab. Bekasi, Jawa Barat 17330.

## 2. `areaServed` — sudah diperbaiki 2026-10-04

`index.html` awalnya hanya mendeklarasikan `{"@type":"Country","name":"Indonesia"}`,
yang menyatakan Anda melayani seluruh Indonesia. Karena `seo-inject.py`
meng-generate ulang JSON-LD setiap kali dijalankan, perbaikannya harus di
`deploy/seo-inject.py` — mengedit `index.html` langsung akan hilang lagi.

Sekarang: `Jawa Barat` (AdministrativeArea), `Bekasi` (City), dan
`Jakarta` (City) — cakupan yang jujur untuk bisnis yang beroperasi dari Bekasi
dengan layanan on-site di Jabodetabek.

Kalau nanti layanan berkembang ke luar Jawa Barat, ubah di `seo-inject.py`
lalu jalankan `npm run seo:inject`.

## 3. Peta keyword per halaman

Format: `keyword utama` · `keyword pendukung` · intent

### `index.html` — brand + kategori umum
- utama: `jasa commercial scenting Indonesia`
- pendukung: `solusi aromaterapi bisnis`, `scenting diffuser profesional`,
  `fragrance company Indonesia`
- intent: riset
- aksi: rewrite `<title>` dan `<meta description>` untuk memuat
  `jasa commercial scenting` + `Bekasi` secara natural. Saat ini title
  berbahasa Inggris ("Atmospheric Branding & Signature Scent") — buruk untuk
  query lokal.

### `products.html` — katalog produk (beli)
- utama: `scenting diffuser hotel` · `diffuser aroma kantor`
- pendukung: `cold air diffuser`, `mesin pengharum ruangan profesional`,
  `diffuser aroma 200m3`, `reed diffuser premium`
- intent: beli / riset teknis
- catatan: `products.html` sekarang jadi satu katalog untuk semua kategori —
  satu halaman tidak akan menang untuk semua keyword ini. Idealnya dipecah,
  tapi itu perubahan besar; lihat bagian 6.

### `collection.html` — wewangian & fragrance oil (beli)
- utama: `fragrance oil premium` · `minyak wewangian hotel`
- pendukung: `reed diffuser premium`, `room spray signature`,
  `fragrance oil hotel`
- intent: beli
- **status 2026-10-04 — koreksi.** Catatan versi sebelumnya mengklaim halaman ini
  "hampir tidak ada copy tekstual — hanya gallery". Itu SALAH: halaman ini
  sudah punya 4 deskripsi scent (Musk White, Soda High, Lemongrass, Royal Tulip)
  beserta notes dan harga, plus paragraf pembuka. Yang hilang bukan deskripsi
  per scent, melainkan KATEGORI: kata "fragrance oil", "reed diffuser", dan
  "Signature Scent" tidak pernah muncul, padahal itu istilah pencarian utama
  kategori wewangian.
- **sudah dikerjakan:** satu paragraf kategori ditambahkan di atas daftar scent
  (fragrance oil premium, cold-air micro-diffusion, Reed Diffuser, hotel/
  kantor/butik/retail) dan `meta description` ditulis ulang agar memuat
  "Fragrance oil premium & Reed Diffuser". Sumber: deskripsi "Wewangian &
  Reed Diffuser" di `about.html` — bukan teks karangan.
- kata kunci `minyak wewangian hotel` tetap **tidak** ditargeting: tidak ada
  klaim layanan hotel khusus di markup. Jangan tambahkan tanpa konfirmasi klien.

### `about.html` — kredibilitas + layanan (jasa)
- utama: `jasa sewa diffuser aroma` · `sewa pengharum ruangan hotel`
- pendukung: `instalasi diffuser hotel`, `maintenance diffuser bulanan`
- pending: `jasa scenting kantor Jakarta`
- intent: jasa
- **Ini gap terbesar Anda.** Pesaing seperti `arkescent.com` punya halaman
  khusus "Sewa & Jual Mesin Scenting Diffuser". Anda punya layanan yang sama
  tetapi tidak punya halaman yang bisa diranking untuk itu. Peluang ini besar.

### `contact.html` — konversi
- utama: `konsultasi scenting diffuser gratis`
- pending: `trial aroma diffuser`, `sample wewangian`
- intent: transaksi
- action: satu-satunya CTA utama adalah WhatsApp. Pastikan `contact.html`
  menyebut trial/sample gratis di title + description — layanan ini unik dan
  tidak dimiliki kompetitor.

## 4. Kata kunci yang TIDAK boleh dipakai

| Jangan pakai | Alasan |
|---|---|
| `sewa diffuser jakarta` tanpa batas area | Kalau tidak ada on-site service di Jakarta, traffic tidak konversi |
| `diffuser termurah` / `murah` | Posisi harga Anda bukan market — jangan tarik traffic yang salah |
| `toko diffuser online` | intent orang beli e-commerce, bukan B2B jasa |
| `review` / `testimonial` | Belum ada review publik. Bahasa yang menipu |
| Apa pun yang tidak ada di markup | Risikonya: Google mengabaikan halaman sebagai konten tidak kredibel, dan canonical jadi tidak bermakna |

## 5. Peluang geo yang belum dipakai

Alamat Anda di Bekasi. Untuk bisnis yang berbasis lokasi, kata kunci
`+ kota` punya konversi jauh di atas keyword nasional:

    scenting diffuser Bekasi
    jasa aroma diffuser Bekasi
    pengharum ruangan Bekasi

Kompetitor besar (scenting.co.id, dr-scent.com) tidak mengoptimasi ini —
mereka nasional atau menyasar pasar asing. Ini celah yang murah dan tinggi konversi.

Setelah Anda daftar di **Google Business Profile**, Local Pack akan menangani
bagian ini secara otomatis. Itu alasan GBP adalah prioritas #1.

## 6. Yang perlu diputuskan

**Pecah `products.html` atau tidak.** Satu halaman untuk 6+ kategori produk
tidak akan menang untuk `scenting diffuser hotel` DAN `reed diffuser premium`
sekaligus — Google memilih satu query utama per halaman. Memecahnya jadi
sub-halaman per kategori akan memberi 3-4 jalur rank tambahan.

Belum saya kerjakan: itu perubahan struktur besar dan butuh konfirmasi Anda
karena berdampak ke sitemap, navigasi, dan JSON-LD.

**Halaman layanan terpisah.** Website layanan saat ini tersembunyi di anchor
`about.html#layanan-kami`. Untuk keyword `jasa sewa diffuser`, halaman
dedicated akan jauh lebih kuat daripada anchor di halaman profil.

## 7. Cara mengukur (dan kenapa ini belum bisa dinilai)

Pemetaan ini tidak akan menunjukkan hasil selama belum ada data. Urutan:

1. Request Indexing untuk halaman yang diubah setelah edit metadata
2. 3-7 hari: GSC Performance — cari query dengan impression tinggi + CTR rendah
3. 2 minggu: GSC Coverage — halaman baru apakah "Discovered" atau sudah "Indexed"
4. 1 bulan: Umami — halaman mana yang membawa traffic

Jangan menebak keyword mana yang berhasil dari penghitung. Angka GSC yang
satu-satunya yang bisa menjawab pertanyaan ini.

## 8. Rekomendasi urutan kerja

**Sudah selesai 2026-10-04:**
1. ~~Perbaiki `areaServed` di JSON-LD~~ — Jabodetabek + Jawa Barat, termasuk
   Service nodes. (`deploy/seo-inject.py`, konstanta `AREA_SERVED`.)
2. ~~Rewrite title + description `index.html`~~ — "Sewa Diffuser Aroma &
   Commercial Scenting", plus title/description semua halaman dalam batas
   60/160 karakter.
3. ~~Teks deskriptif di `collection.html`~~ — paragraf kategori ditambahkan
   (fragrance oil / Reed Diffuser / cold-air), 172 → 217 kata.
4. Anchor katalog diperbaiki: 45 link `products.html#diffuser|#fragrance|#all`
   sebelumnya menunjuk id yang tidak ada (`#section-diffuser`,
   `#section-fragrance`). `collection.html` kini punya inbound link dari 8 halaman.
5. FAQPage + konten FAQ terlihat di `products.html` (5 pertanyaan).
6. Favicon dibuat dari `img/logo.svg` (sebelumnya `/favicon.ico` 404).

**Sisa — urutannya penting:**
1. **Verifikasi Search Console + Request Indexing** — sitemap sudah disubmit
   2026-10-04 dan Googlebot sudah meng-fetch sitemap + robots.txt, tapi belum
   satu pun halaman konten. Request Indexing memicu crawl langsung.
2. **Google Business Profile** — dampak paling besar untuk Local Pack.
3. **Halaman layanan terpisah** (`jasa sewa diffuser aroma`) — gap terbesar,
   butuh persetujuan karena mengubah sitemap + navigasi.
4. **Pecah `products.html`** — satu katalog untuk 6+ kategori tidak bisa menang
   untuk dua query utama sekaligus. Butuh persetujuan.