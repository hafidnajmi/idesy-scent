# Google Ads — Indoeasy Scent

Lembar siap copy-paste ke Google Ads Console.

> **Dokumen ini di-generate oleh `deploy/gen-ads-copysheet.py` dari data di
> `deploy/validate-ads-copy.py`.** Jangan edit file ini secara manual — ubah
> datanya, lalu jalankan ulang generator. Validator menolak field yang
> melewati batas karakter Google, jadi semua angka di bawah sudah lolos.

Validasi ulang kapan pun:

```bash
python3 deploy/validate-ads-copy.py    # panjang, URL, klaim
bash deploy/gen-ads-assets.sh           # gambar & logo
```

## 1. Yang perlu Anda siapkan sebelum akun dibuat

| # | Kebutuhan | Status |
|---|---|---|
| 1 | Akun Google Ads + metode pembayaran | Anda buat sendiri |
| 2 | **Verifikasi advertiser** (wajib di Indonesia) | **Belum** |
| 3 | Google Business Profile | Belum |
| 4 | Tag konversi (WhatsApp click) | Belum |

### Verifikasi advertiser — ini yang paling sering memblokir

Google mewajibkan advertiser di Indonesia menyelesaikan verifikasi identitas.
Menu: **Admin > Kebijakan > Akun > Mulai tugas**.

Profil pembayaran harus berstatus **Organisasi**, dan detail pada dokumen
harus **sama persis** dengan nama di profil pembayaran. Dokumen yang
diterima: akta perusahaan / NIB / izin usaha / NPWP, **plus** KTP atau
paspor milik：admin akun yang membayar iklan.

Foto dokumen harus berwarna, jelas, pencahayaan baik, seluruh sudut
terlihat, dan **bukan fotokopi**. Ketidakcocokan nama = verifikasi gagal,
dan akun bisa dijeda.

> Catatan: kata "nama bisnis" pada aset iklan harus cocok dengan nama
> domain atau nama legal hasil verifikasi, kalau tidak asetnya ditolak.

## 2. Pengaturan akun

| Pengaturan | Nilai |
|---|---|
| Nama akun | `Indoeasy Scent` |
| Zona waktu | `(GMT+07:00) Jakarta` |
| Mata uang | IDR |
| Bahasa | Indonesia |
| Nama kampanye | `Sewa Diffuser Aroma - Bekasi` |
| Tipe | Search (cari) |
| Lokasi | Target: Bekasi, Jakarta, Jawa Barat |
| excluding | Presence: **Hanya orang yang ada di lokasi target** |
| Bahasa | Indonesia, English |
| Jadwal | Setiap hari, 08.00–20.00 (WIB) |
| Strategi bidding | **Mulai dengan Manual CPC** lalu naik ke Target CPA |
| Anggaran harian | Mulai Rp 150.000, naik 20%/minggu |

**Kenapa "hanya orang yang ada di lokasi":** bisnis Anda installing
difuser secara on-site. Iklan yang menjangkau orang yang tidak ada di
Bekasi/Jakarta hanya membayar klik yang tidak bisa jadi pelanggan.

## 3. Kampanye — Sewa Diffuser Aroma

Nama: `Sewa Diffuser Aroma - Bekasi`

**URL akhir:** `https://indoeasyscent.com/`

**Display path:** `sewa-diffuser` / `bekasi`

#### Headline (15, maks 15 — minimal 3)

| # | Headline | 15/30 | |
|---|---|---|---|
| 1 | Sewa Diffuser Aroma | **19**/30 | OK |
| 2 | Jasa Scenting Diffuser | **22**/30 | OK |
| 3 | Commercial Scenting | **19**/30 | OK |
| 4 | Diffuser Aroma Hotel | **20**/30 | OK |
| 5 | 30 m3 - 4.000 m3 | **16**/30 | OK |
| 6 | Trial & Sampel Gratis | **21**/30 | OK |
| 7 | Pemasangan Gratis | **17**/30 | OK |
| 8 | Bekasi, Jakarta, Jawa Barat | **27**/30 | OK |
| 9 | IFRA & Kemenkes RI | **18**/30 | OK |
| 10 | 11 Model Diffuser ISX | **21**/30 | OK |
| 11 | Refill & Maintenance | **20**/30 | OK |
| 12 | Garansi Unit 1x24 Jam | **21**/30 | OK |
| 13 | Konsultasi Aroma Gratis | **23**/30 | OK |
| 14 | Hubungi via WhatsApp | **20**/30 | OK |
| 15 | Hotel, Kantor & Retail | **22**/30 | OK |

#### Description (4, maks 4 — minimal 2)

| # | Description | 4/90 | |
|---|---|---|---|
| 1 | Sewa & instalasi diffuser aroma cold-air untuk hotel, kantor, retail | **68**/90 | OK |
| 2 | Cakupan 30 m3 sampai 4.000 m3. Trial unit dan sampel wewangian gratis | **69**/90 | OK |
| 3 | Pemasangan gratis teknisi. Refill & maintenance berkala | **55**/90 | OK |
| 4 | Konsultasi kurasi aroma B2B tanpa biaya. Area Bekasi & Jawa Barat | **65**/90 | OK |

#### Kata kunci

- `sewa diffuser aroma`
- `jasa scenting diffuser`
- `sewa pengharum ruangan`
- `diffuser aroma hotel`
- `diffuser aroma kantor`
- `jasa aroma diffuser bekasi`
- `sewa diffuser jakarta`
- `cold air diffuser indonesia`
- `sistem scenting hotel`
- `[sewa diffuser aroma bekasi]`
- `[jasa scenting diffuser jakarta]`
- `"sewa diffuser aroma"`
- `"jasa scenting diffuser"`

#### Kata kunci negatif

```
murah
termurah
gratis
second hand
bekas
manual
homemade
resep
youtube
tutorial
cara buat
lowongan
karang tarum
shopee
tokopedia
```

> **Jangan pakai URL berparameter `?area=` di final URL.** Google
> menolaknya kalau parameter tidak ada di akun.

## 4. Grup Iklan 2 — Fragrance Oil & Reed Diffuser

Nama: `Fragrance Oil & Reed Diffuser`

**URL akhir:** `https://indoeasyscent.com/collection.html`

**Display path:** `fragrance-oil` / `reed-diffuser`

#### Headline (9, maks 15 — minimal 3)

| # | Headline | 9/30 | |
|---|---|---|---|
| 1 | Fragrance Oil Premium | **21**/30 | OK |
| 2 | Reed Diffuser Premium | **21**/30 | OK |
| 3 | Wewangian Eksklusif | **19**/30 | OK |
| 4 | Minyak Wewangian Hotel | **22**/30 | OK |
| 5 | Aroma Signature | **15**/30 | OK |
| 6 | Empat Aroma Eksklusif | **21**/30 | OK |
| 7 | Bekasi, Jakarta, Jawa Barat | **27**/30 | OK |
| 8 | Konsultasi Gratis | **17**/30 | OK |
| 9 | Siap Dicoba | **11**/30 | OK |

#### Description (3, maks 4 — minimal 2)

| # | Description | 3/90 | |
|---|---|---|---|
| 1 | Empat aroma eksklusif siap dicoba lebih dulu sebelum Anda memesan | **65**/90 | OK |
| 2 | Fragrance oil premium & reed diffuser untuk hotel, kantor, butik | **64**/90 | OK |
| 3 | Konsultasi karakter aroma gratis. Sampel dikirim ke lokasi bisnis | **65**/90 | OK |

#### Kata kunci

- `fragrance oil premium`
- `minyak wewangian hotel`
- `reed diffuser premium`
- `wewangian eksklusif`
- `reed diffuser hotel`
- `fragrance oil jakarta`
- `room spray signature`
- `"fragrance oil premium"`
- `"reed diffuser premium"`

## 5. Grup Iklan 3 — Katalog Diffuser ISX

Nama: `Katalog Diffuser ISX`

**URL akhir:** `https://indoeasyscent.com/products.html`

**Display path:** `diffuser-isx` / `katalog`

#### Headline (9, maks 15 — minimal 3)

| # | Headline | 9/30 | |
|---|---|---|---|
| 1 | Scenting Diffuser ISX | **21**/30 | OK |
| 2 | 11 Model Diffuser | **17**/30 | OK |
| 3 | Cold-Air Micro-Diffusion | **24**/30 | OK |
| 4 | Cakupan 30 - 4.000 m3 | **21**/30 | OK |
| 5 | Spesifikasi Lengkap | **19**/30 | OK |
| 6 | Bekasi & Jabodetabek | **20**/30 | OK |
| 7 | Konsultasi Gratis | **17**/30 | OK |
| 8 | Trial Unit Gratis | **17**/30 | OK |
| 9 | Pemasangan Gratis | **17**/30 | OK |

#### Description (2, maks 4 — minimal 2)

| # | Description | 2/90 | |
|---|---|---|---|
| 1 | Katalog resmi ISX Series: spesifikasi, daya, kebisingan, dan kapasitas | **70**/90 | OK |
| 2 | Satuan dari 30 m3 sampai 4.000 m3. Lihat spesifikasi tiap model | **63**/90 | OK |

#### Kata kunci

- `scenting diffuser hotel`
- `mesin diffuser aroma`
- `diffuser aroma profesional`
- `cold air diffuser`
- `diffuser aroma 4000m3`
- `commercial scent diffuser`

**Pisahkan jadi 3 grup, jangan 1 grup besar.** Satu halaman tidak bisa
menang untuk "sewa diffuser aroma" dan "fragrance oil premium"
sekaligus. Mencampur keduanya membuat Google's learning lebih lama dan
Quality Score turun di keduanya.

## 6. Aset Iklan (level akun)

### Sitelink (6)

| Link text | Baris 1 | Baris 2 | URL |
|---|---|---|---|
| Sewa Diffuser Aroma | Cold-air presisi, 30 m3 - 4.000 m3 | Pemasangan gratis oleh teknisi | `https://indoeasyscent.com/` |
| Katalog Diffuser ISX | 11 model, spesifikasi lengkap | Cakupan 30 m3 sampai 4.000 m3 | `https://indoeasyscent.com/products.html` |
| Koleksi Wewangian | Fragrance oil premium | Reed diffuser untuk bisnis | `https://indoeasyscent.com/collection.html` |
| Layanan & Proses | Sewa, refill, maintenance | Trial dan sampel aroma gratis | `https://indoeasyscent.com/about.html` |
| Konsultasi Gratis | Trial unit dan sampel aroma | Hubungi tim kami hari ini | `https://indoeasyscent.com/contact.html` |
| Cerita Kami | Standar produksi | Konsultasi karakter aroma | `https://indoeasyscent.com/about.html#cerita-kami` |

### Callout (8, maks 25 karakter)

```
Trial & Sampel Gratis
Pemasangan Gratis
Bekasi, Jakarta
IFRA & Kemenkes RI
Garansi 1x24 Jam
Refill Berkala
Konsultasi Gratis
Coverage 4.000 m3
```

### Structured snippet

**Header: Layanan**

```
Sewa Diffuser
Instalasi
Refill Berkala
Maintenance
Trial & Sampel
Konsultasi Aroma
```

**Header: Model Diffuser**

```
ISX-I-0  30 m3
ISX-H2  300 m3
ISX-H5  1000 m3
ISXPR-OV-5/5  800 m3
ISX-U-5  3.000 m3
ISX-U10  4.000 m3
```

## 7. Gambar & logo

Semua sudah di-generate ke `img/ads/` oleh `bash deploy/gen-ads-assets.sh`.
Ukuran di bawah dibaca langsung dari disk, jadi tidak bisa basi.

| File | Piksel | Ukuran | Untuk |
|---|---|---|---|
| `ads-hotel-landscape.jpg` | 1200x628 | 162KB | Gambar 1.91:1 |
| `ads-restoran-landscape.jpg` | 1200x628 | 147KB | Gambar 1.91:1 |
| `ads-retail-landscape.jpg` | 1200x628 | 116KB | Gambar 1.91:1 |
| `ads-diffuser-landscape.jpg` | 1200x628 | 20KB | Gambar 1.91:1 |
| `ads-wewangian-landscape.jpg` | 1200x628 | 27KB | Gambar 1.91:1 |
| `ads-hotel-square.jpg` | 1200x1200 | 259KB | Gambar 1:1 |
| `ads-restoran-square.jpg` | 1200x1200 | 262KB | Gambar 1:1 |
| `ads-retail-square.jpg` | 1200x1200 | 158KB | Gambar 1:1 |
| `ads-diffuser-square.jpg` | 1200x1200 | 33KB | Gambar 1:1 |
| `ads-wewangian-square.jpg` | 1200x1200 | 61KB | Gambar 1:1 |
| `ads-logo-square.png` | 1200x1200 | 41KB | Logo 1:1 |
| `ads-logo-wide.png` | 1200x300 | 13KB | Logo 4:1 |

Batas Google: gambar maks **5120KB**, logo maks **150KB**.

**Muat minimal 5 gambar per rasio** agar Google punya variasi untuk diuji.
Upload 5 landscape + 5 square + 2 logo (Responsive Display Ad), atau
pakai Display & Performance Max yang mengambil aset level akun.

### Foto yang TIDAK dipakai, dan alasannya

| File | Alasan |
|---|---|
| `professional_diffuser.png` | Foto hotel lobby pihak ketiga; produk di
dalamnya bertuliskan **"AURA"** — merek orang lain. Memamerkan
merek pihak lain dalam iklan itu pelanggaran kebijakan, bukan sekadar
soal rasa. |
| `kantor.jpg` | Foto kantor pihak ketiga; monitor ada logo **"acer"**
dan wajah karyawan terlihat. |
| `img/og/*.jpg` | Rasio 1200x630 (1.90:1), **bukan** rasio yang
Google Ads terima. Bukan OG cover yang gagal, memang format berbeda. |
| `img/logo-shopee.svg`, `tokopedia.webp` | Badge marketplace bukan milik
Anda untuk ditampilkan sebagai aset iklan. |

Kalau Anda **memiliki** foto hotel/kantor yang memang milik klien dan
sudah ada izin kontribusi, ganti file sumbernya di `gen-ads-assets.sh`
lalu jalankan ulang — hasilnya tetap validasi otomatis.

## 8. Pelacakan konversi — belum ada, ini prasyarat

Situs sekarang hanya punya Umami (`analytics.indoeasyscent.com`). Umami
**bukan** sumber konversi untuk Google Ads — Google hanya menerima
konversi dari Google Tag, Analytics 4, atau Ads.

Tanpa tag konversi, Google optimizes towards traffic, bukan towards
WhatsApp. Efeknya: budget habis di klik yang tidak konversi, dan Smart
Bidding belajar dari sinyal yang salah.

### Yang perlu ditambahkan

```html
<!-- Ganti AW-XXXXXXXXXX dengan ID konversi Google Ads Anda -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXXXX');
</script>
```

Lalu daftarkan konversi **Klik WhatsApp** (primary) dan **Kirim form
inquiry** (secondary).

> **Penting:** CSP di `deploy/nginx/indoeasyscent.conf` saat ini
> mengizinkan `script-src` hanya untuk host sendiri, Tailwind CDN,
> Google Maps, dan subdomain analytics. `googletagmanager.com` **belum**
> ada di sana — tanpa itu tag diblokir diam-diam, tanpa error di
> console, persis seperti kasus Umami. CSP harus diperbarui saat tag
> dipasang.

## 9. Kalender ICD yang perlu disiapkan

| Kalender | Dimensi | Nilai |
|---|---|---|
| Bulan | 202610 | Oktober 2026 |
| Bahasa | en | Indonesia |
| Negara | ID | Indonesia |
| Biaya | 11401000 | IDR |

MDK (Bulan, Bahasa, Negara, Biaya) harus cocok atau konversi tidak
tercatat.

## 10. Checklist sebelum iklan dipublikasikan

- [ ] Verifikasi advertiser selesai (Organisasi, dokumen cocok nama)
- [ ] `checkout.html` **tidak** dipakai sebagai tujuan iklan (noindex)
- [ ] Tag konversi terpasang dan **teruji** satu klik WhatsApp sungguhan
- [ ] CSP mengizinkan `googletagmanager.com` (dan `google-analytics.com`)
- [ ] 5 gambar landscape + 5 square + 2 logo terupload
- [ ] Lokasi disetel *presence*, bukan *interest*
- [ ] Semua field teks sudah within limit (tidak ada yang perlu dipotong)
- [ ] Kontrol: cek Ad Preview dengan beberapa kata kunci pengicu

---

Sumber batas karakter: Google Ads Help 7684791, 17092074, 17090561, 9872280.
Diverifikasi 2026-10-05.
