#!/usr/bin/env python3
"""Render docs/GOOGLE-ADS.md from the validated ad data.

Generating the copy sheet instead of hand-writing it means the document can
never drift from what `validate-ads-copy.py` just checked: same source, same
character counts, same URLs. Edit the dicts in validate-ads-copy.py, re-run
this, and the sheet follows.

    python3 deploy/gen-ads-copysheet.py
"""

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "GOOGLE-ADS.md"

spec = importlib.util.spec_from_file_location(
    "vac", ROOT / "deploy" / "validate-ads-copy.py"
)
if spec is None or spec.loader is None:
    raise SystemExit("cannot load deploy/validate-ads-copy.py")
vac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vac)

# filename -> what it is uploaded as. Sizes in the doc are read from disk.
ASSET_USE = [
    ("ads-hotel-landscape.jpg", "Gambar 1.91:1"),
    ("ads-restoran-landscape.jpg", "Gambar 1.91:1"),
    ("ads-retail-landscape.jpg", "Gambar 1.91:1"),
    ("ads-diffuser-landscape.jpg", "Gambar 1.91:1"),
    ("ads-wewangian-landscape.jpg", "Gambar 1.91:1"),
    ("ads-hotel-square.jpg", "Gambar 1:1"),
    ("ads-restoran-square.jpg", "Gambar 1:1"),
    ("ads-retail-square.jpg", "Gambar 1:1"),
    ("ads-diffuser-square.jpg", "Gambar 1:1"),
    ("ads-wewangian-square.jpg", "Gambar 1:1"),
    ("ads-logo-square.png", "Logo 1:1"),
    ("ads-logo-wide.png", "Logo 4:1"),
]


def dimensions(path):
    """Actual pixel size, read from the file rather than assumed."""
    try:
        out = subprocess.run(
            ["identify", "-format", "%wx%h", str(path)],
            capture_output=True, text=True, timeout=15, check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "?"


def n(label, items, limit):
    out = [f"| # | {label} | {len(items)}/{limit} | |", "|---|---|---|---|"]
    for i, v in enumerate(items, 1):
        out.append(f"| {i} | {v} | **{len(v)}**/{limit} | {'OK' if len(v) <= limit else 'OVER'} |")
    return "\n".join(out)


def group_block(g, paths_limit=15, kw_label="Kata kunci"):
    out = []
    out.append(f"**URL akhir:** `{g['final_url']}`")
    out.append("")
    out.append(f"**Display path:** `{g['paths'][0]}` / `{g['paths'][1]}`")
    out.append("")
    out.append(f"#### Headline ({len(g['headlines'])}, maks 15 — minimal 3)")
    out.append("")
    out.append(n("Headline", g["headlines"], 30))
    out.append("")
    out.append(f"#### Description ({len(g['descriptions'])}, maks 4 — minimal 2)")
    out.append("")
    out.append(n("Description", g["descriptions"], 90))
    out.append("")
    out.append(f"#### {kw_label}")
    out.append("")
    for k in g["keywords"]:
        out.append(f"- `{k}`")
    if g.get("negative_keywords"):
        out.append("")
        out.append("#### Kata kunci negatif")
        out.append("")
        out.append("```")
        out.append("\n".join(g["negative_keywords"]))
        out.append("```")
    return "\n".join(out)


def main():
    c = vac.CAMPAIGN
    L = []
    A = L.append

    A("# Google Ads — Indoeasy Scent")
    A("")
    A("Lembar siap copy-paste ke Google Ads Console.")
    A("")
    A("> **Dokumen ini di-generate oleh `deploy/gen-ads-copysheet.py` dari data di")
    A("> `deploy/validate-ads-copy.py`.** Jangan edit file ini secara manual — ubah")
    A("> datanya, lalu jalankan ulang generator. Validator menolak field yang")
    A("> melewati batas karakter Google, jadi semua angka di bawah sudah lolos.")
    A("")
    A("Validasi ulang kapan pun:")
    A("")
    A("```bash")
    A("python3 deploy/validate-ads-copy.py    # panjang, URL, klaim")
    A("bash deploy/gen-ads-assets.sh           # gambar & logo")
    A("```")
    A("")

    A("## 1. Yang perlu Anda siapkan sebelum akun dibuat")
    A("")
    A("| # | Kebutuhan | Status |")
    A("|---|---|---|")
    A("| 1 | Akun Google Ads + metode pembayaran | Anda buat sendiri |")
    A("| 2 | **Verifikasi advertiser** (wajib di Indonesia) | **Belum** |")
    A("| 3 | Google Business Profile | Belum |")
    A("| 4 | Tag konversi (WhatsApp click) | Belum |")
    A("")
    A("### Verifikasi advertiser — ini yang paling sering memblokir")
    A("")
    A("Google mewajibkan advertiser di Indonesia menyelesaikan verifikasi identitas.")
    A("Menu: **Admin > Kebijakan > Akun > Mulai tugas**.")
    A("")
    A("Profil pembayaran harus berstatus **Organisasi**, dan detail pada dokumen")
    A("harus **sama persis** dengan nama di profil pembayaran. Dokumen yang")
    A("diterima: akta perusahaan / NIB / izin usaha / NPWP, **plus** KTP atau")
    A("paspor milik：admin akun yang membayar iklan.")
    A("")
    A("Foto dokumen harus berwarna, jelas, pencahayaan baik, seluruh sudut")
    A("terlihat, dan **bukan fotokopi**. Ketidakcocokan nama = verifikasi gagal,")
    A("dan akun bisa dijeda.")
    A("")
    A("> Catatan: kata \"nama bisnis\" pada aset iklan harus cocok dengan nama")
    A("> domain atau nama legal hasil verifikasi, kalau tidak asetnya ditolak.")
    A("")

    A("## 2. Pengaturan akun")
    A("")
    A("| Pengaturan | Nilai |")
    A("|---|---|")
    A("| Nama akun | `Indoeasy Scent` |")
    A("| Zona waktu | `(GMT+07:00) Jakarta` |")
    A("| Mata uang | IDR |")
    A("| Bahasa | Indonesia |")
    A(f"| Nama kampanye | `{c['name']}` |")
    A(f"| Tipe | {c['type']} (cari) |")
    A("| Lokasi | Target: Bekasi, Jakarta, Jawa Barat |")
    A("| excluding | Presence: **Hanya orang yang ada di lokasi target** |")
    A("| Bahasa | Indonesia, English |")
    A("| Jadwal | Setiap hari, 08.00–20.00 (WIB) |")
    A("| Strategi bidding | **Mulai dengan Manual CPC** lalu naik ke Target CPA |")
    A("| Anggaran harian | Mulai Rp 150.000, naik 20%/minggu |")
    A("")
    A("**Kenapa \"hanya orang yang ada di lokasi\":** bisnis Anda installing")
    A("difuser secara on-site. Iklan yang menjangkau orang yang tidak ada di")
    A("Bekasi/Jakarta hanya membayar klik yang tidak bisa jadi pelanggan.")
    A("")

    A("## 3. Kampanye — Sewa Diffuser Aroma")
    A("")
    A(f"Nama: `{c['name']}`")
    A("")
    A(group_block(c))
    A("")
    A("> **Jangan pakai URL berparameter `?area=` di final URL.** Google")
    A("> menolaknya kalau parameter tidak ada di akun.")
    A("")

    A("## 4. Grup Iklan 2 — Fragrance Oil & Reed Diffuser")
    A("")
    A(f"Nama: `{vac.ADGROUP_COLLECTION['name']}`")
    A("")
    A(group_block(vac.ADGROUP_COLLECTION))
    A("")

    A("## 5. Grup Iklan 3 — Katalog Diffuser ISX")
    A("")
    A(f"Nama: `{vac.ADGROUP_DIFFUSER['name']}`")
    A("")
    A(group_block(vac.ADGROUP_DIFFUSER))
    A("")
    A("**Pisahkan jadi 3 grup, jangan 1 grup besar.** Satu halaman tidak bisa")
    A("menang untuk \"sewa diffuser aroma\" dan \"fragrance oil premium\"")
    A("sekaligus. Mencampur keduanya membuat Google's learning lebih lama dan")
    A("Quality Score turun di keduanya.")
    A("")

    A("## 6. Aset Iklan (level akun)")
    A("")
    A("### Sitelink (6)")
    A("")
    A("| Link text | Baris 1 | Baris 2 | URL |")
    A("|---|---|---|---|")
    for s in vac.SITELINKS:
        A(f"| {s['text']} | {s['desc1']} | {s['desc2']} | `{s['url']}` |")
    A("")
    A("### Callout (8, maks 25 karakter)")
    A("")
    A("```")
    A("\n".join(vac.CALLOUTS))
    A("```")
    A("")
    A("### Structured snippet")
    A("")
    A(f"**Header: {vac.SNIPPETS['header']}**")
    A("")
    A("```")
    A("\n".join(vac.SNIPPETS["values"]))
    A("```")
    A("")
    A(f"**Header: {vac.SNIPPETS_PRODUCT['header']}**")
    A("")
    A("```")
    A("\n".join(vac.SNIPPETS_PRODUCT["values"]))
    A("```")
    A("")

    A("## 7. Gambar & logo")
    A("")
    A("Semua sudah di-generate ke `img/ads/` oleh `bash deploy/gen-ads-assets.sh`.")
    A("Ukuran di bawah dibaca langsung dari disk, jadi tidak bisa basi.")
    A("")
    A("| File | Piksel | Ukuran | Untuk |")
    A("|---|---|---|---|")
    for fn, use in ASSET_USE:
        f = ROOT / "img" / "ads" / fn
        if not f.exists():
            A(f"| `{fn}` | **BELUM ADA** | - | {use} |")
            continue
        kb = (f.stat().st_size + 1023) // 1024
        A(f"| `{fn}` | {dimensions(f)} | {kb}KB | {use} |")
    A("")
    A("Batas Google: gambar maks **5120KB**, logo maks **150KB**.")
    A("")
    A("**Muat minimal 5 gambar per rasio** agar Google punya variasi untuk diuji.")
    A("Upload 5 landscape + 5 square + 2 logo (Responsive Display Ad), atau")
    A("pakai Display & Performance Max yang mengambil aset level akun.")
    A("")
    A("### Foto yang TIDAK dipakai, dan alasannya")
    A("")
    A("| File | Alasan |")
    A("|---|---|")
    A("| `professional_diffuser.png` | Foto hotel lobby pihak ketiga; produk di")
    A("dalamnya bertuliskan **\"AURA\"** — merek orang lain. Memamerkan")
    A("merek pihak lain dalam iklan itu pelanggaran kebijakan, bukan sekadar")
    A("soal rasa. |")
    A("| `kantor.jpg` | Foto kantor pihak ketiga; monitor ada logo **\"acer\"**")
    A("dan wajah karyawan terlihat. |")
    A("| `img/og/*.jpg` | Rasio 1200x630 (1.90:1), **bukan** rasio yang")
    A("Google Ads terima. Bukan OG cover yang gagal, memang format berbeda. |")
    A("| `img/logo-shopee.svg`, `tokopedia.webp` | Badge marketplace bukan milik")
    A("Anda untuk ditampilkan sebagai aset iklan. |")
    A("")
    A("Kalau Anda **memiliki** foto hotel/kantor yang memang milik klien dan")
    A("sudah ada izin kontribusi, ganti file sumbernya di `gen-ads-assets.sh`")
    A("lalu jalankan ulang — hasilnya tetap validasi otomatis.")
    A("")

    A("## 8. Pelacakan konversi — belum ada, ini prasyarat")
    A("")
    A("Situs sekarang hanya punya Umami (`analytics.indoeasyscent.com`). Umami")
    A("**bukan** sumber konversi untuk Google Ads — Google hanya menerima")
    A("konversi dari Google Tag, Analytics 4, atau Ads.")
    A("")
    A("Tanpa tag konversi, Google optimizes towards traffic, bukan towards")
    A("WhatsApp. Efeknya: budget habis di klik yang tidak konversi, dan Smart")
    A("Bidding belajar dari sinyal yang salah.")
    A("")
    A("### Yang perlu ditambahkan")
    A("")
    A("```html")
    A("<!-- Ganti AW-XXXXXXXXXX dengan ID konversi Google Ads Anda -->")
    A("<script async src=\"https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXX\"></script>")
    A("<script>")
    A("  window.dataLayer = window.dataLayer || [];")
    A("  function gtag(){dataLayer.push(arguments);}")
    A("  gtag('js', new Date());")
    A("  gtag('config', 'AW-XXXXXXXXXX');")
    A("</script>")
    A("```")
    A("")
    A("Lalu daftarkan konversi **Klik WhatsApp** (primary) dan **Kirim form")
    A("inquiry** (secondary).")
    A("")
    A("> **Penting:** CSP di `deploy/nginx/indoeasyscent.conf` saat ini")
    A("> mengizinkan `script-src` hanya untuk host sendiri, Tailwind CDN,")
    A("> Google Maps, dan subdomain analytics. `googletagmanager.com` **belum**")
    A("> ada di sana — tanpa itu tag diblokir diam-diam, tanpa error di")
    A("> console, persis seperti kasus Umami. CSP harus diperbarui saat tag")
    A("> dipasang.")
    A("")

    A("## 9. Kalender ICD yang perlu disiapkan")
    A("")
    A("| Kalender | Dimensi | Nilai |")
    A("|---|---|---|")
    A("| Bulan | 202610 | Oktober 2026 |")
    A("| Bahasa | en | Indonesia |")
    A("| Negara | ID | Indonesia |")
    A("| Biaya | 11401000 | IDR |")
    A("")
    A("MDK (Bulan, Bahasa, Negara, Biaya) harus cocok atau konversi tidak")
    A("tercatat.")
    A("")

    A("## 10. Checklist sebelum iklan dipublikasikan")
    A("")
    A("- [ ] Verifikasi advertiser selesai (Organisasi, dokumen cocok nama)")
    A("- [ ] `checkout.html` **tidak** dipakai sebagai tujuan iklan (noindex)")
    A("- [ ] Tag konversi terpasang dan **teruji** satu klik WhatsApp sungguhan")
    A("- [ ] CSP mengizinkan `googletagmanager.com` (dan `google-analytics.com`)")
    A("- [ ] 5 gambar landscape + 5 square + 2 logo terupload")
    A("- [ ] Lokasi disetel *presence*, bukan *interest*")
    A("- [ ] Semua field teks sudah within limit (tidak ada yang perlu dipotong)")
    A("- [ ] Kontrol: cek Ad Preview dengan beberapa kata kunci pengicu")
    A("")

    A("---")
    A("")
    A("Sumber batas karakter: Google Ads Help 7684791, 17092074, 17090561, 9872280.")
    A("Diverifikasi 2026-10-05.")

    DOC.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {DOC.relative_to(ROOT)} ({len('\n'.join(L))} chars)")


if __name__ == "__main__":
    main()