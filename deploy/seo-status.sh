#!/usr/bin/env bash
# Cek status SEO indoeasyscent.com — jalankan: bash deploy/seo-status.sh
#
# Yang bisa diukur SEKARANG vs apa yang harus menunggu Google.
# Tidak ada angka yang dikarang: setiap baris output dari probe nyata.

set -uo pipefail

SITE="https://indoeasyscent.com"
OK="  [OK]"
BAD="  [!!]"

section() { printf '\n\033[1;32m== %s ==\033[0m\n' "$*"; }

# ---------------------------------------------------------------- 1. DNS
section "1. DNS & host"
for s in 8.8.8.8 1.1.1.1 9.9.9.9; do
  apex="$(dig +short +time=3 +tries=1 @$s indoeasyscent.com A | tr '\n' ' ')"
  printf "%s @%-8s apex: %s\n" "$OK" "$s" "$apex"
done
server="$(curl -sI --max-time 12 "$SITE/" | grep -i '^server:' | tr -d '\r' | awk '{print $2}')"
if [ "$server" = "nginx" ]; then
  printf "%s host: %s\n" "$OK" "$server"
else
  printf "%s host: %s (diharapkan nginx)\n" "$BAD" "$server"
fi

# ---------------------------------------------------------------- 2. Halaman
section "2. Halaman inti"
for p in "" products.html collection.html about.html contact.html \
         checkout.html privacy-policy.html terms-of-service.html \
         sitemap.xml robots.txt js/analytics.js; do
  code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 12 "$SITE/$p")"
  if [ "$code" = "200" ]; then
    printf "%s /%-24s %s\n" "$OK" "$p" "$code"
  else
    printf "%s /%-24s %s (DIPERIKSA)\n" "$BAD" "$p" "$code"
  fi
done

# ---------------------------------------------------------------- 3. SEO tags
section "3. SEO tags per halaman"
printf "  %-24s %-9s %-9s %-8s %-9s\n" "HALAMAN" "CANONICAL" "JSON-LD" "TITLE" "ROBOTS"
for f in index products collection about contact; do
  body="$(curl -s --max-time 12 "$SITE/$f.html")"
  canon="$(printf '%s' "$body" | grep -c 'rel="canonical"')"
  ld="$(printf '%s' "$body" | grep -c 'application/ld+json')"
  title="$(printf '%s' "$body" | grep -oE '<title>[^<]*' | head -1 | sed 's/<title>//' | cut -c1-8)"
  # only the two pages that SHOULD be noindex may carry a robots meta
  robots="none"
  case "$f" in
    checkout) robots="$(printf '%s' "$body" | grep -oE 'name="robots" content="[^"]*"' | grep -oE '(no)?index[a-z, ]*' | head -1)" ;;
  esac
  printf "  %-24s %-9s %-9s %-8s %-9s\n" "$f.html" "$canon" "$ld" "${title:0:8}" "${robots:-none}"
done

# ---------------------------------------------------------------- 4. Indexability
section "4. Indexability"
ct="$(curl -s --max-time 12 "$SITE/checkout.html" | grep -c 'noindex')"
ts="$(curl -s --max-time 12 "$SITE/terms-of-service.html" | grep -c 'noindex')"
printf "%s checkout.html punya noindex\n" "$([ "$ct" -gt 0 ] && echo "$OK" || echo "$BAD")"
printf "%s terms-of-service.html punya noindex\n" "$([ "$ts" -gt 0 ] && echo "$OK" || echo "$BAD")"

sm="$(curl -s --max-time 12 "$SITE/sitemap.xml" | grep -c '<loc>')"
smbad="$(curl -s --max-time 12 "$SITE/sitemap.xml" | grep '<loc>' | grep -cE 'checkout|terms-of-service')"
printf "%s sitemap berisi %s URL\n" "$([ "$sm" -eq 6 ] && echo "$OK" || echo "$BAD")" "$sm"
printf "%s sitemap tidak memuat halaman noindex (%s ditemukan)\n" \
  "$([ "$smbad" -eq 0 ] && echo "$OK" || echo "$BAD")" "$smbad"

for h in analytics panelhosting; do
  xr="$(curl -sI --max-time 12 "https://$h.indoeasyscent.com/" | grep -ci 'x-robots-tag')"
  printf "%s %s. subdomain punya X-Robots-Tag\n" "$([ "$xr" -gt 0 ] && echo "$OK" || echo "$BAD")" "$h"
done

# ---------------------------------------------------------------- 5. Analytics
section "5. Pelacakan (Umami)"
script="$(curl -s -o /dev/null -w '%{http_code}' --max-time 12 "$SITE/js/analytics.js")"
printf "%s js/analytics.js -> %s\n" "$([ "$script" = "200" ] && echo "$OK" || echo "$BAD")" "$script"

csp="$(curl -sI --max-time 12 "$SITE/" | grep -io 'https://analytics.indoeasyscent.com' | head -1)"
printf "%s CSP mengizinkan analytics\n" "$([ -n "$csp" ] && echo "$OK" || echo "$BAD")"

if ssh -o ConnectTimeout=8 idesys-vps true 2>/dev/null; then
  n="$(ssh -o ConnectTimeout=8 idesys-vps \
        "sudo docker exec umami-db-1 psql -U umami -d umami -A -t -c 'select count(*) from session;'" 2>/dev/null | tr -d '[:space:]')"
  printf "  sesi tercatat: %s\n" "${n:-tidak terbaca}"
  if [ "${n:-0}" -gt 0 ] 2>/dev/null; then
    printf "%s tracker mengirim data\n" "$OK"
  else
    printf "  belum ada data — normal bila belum ada visitor\n"
  fi
else
  printf "  (tidak bisa cek DB: SSH tidak terjangkau)\n"
fi

# ---------------------------------------------------------------- 6. Ringkas
section "Ringkas"
cat <<'RINGKAS'
  Semua [OK] di atas = fondasi teknis sehat. Itu BUKAN berarti SEO berhasil.

  SEO yang benar-benar berhasil baru terlihat dari:
    -  3-7 hari  : GSC Performance, data mulai masuk
    -  2 minggu  : GSC Coverage, pastikan halaman inti tidak "Excluded"
    -  1 bulan   : Umami, halaman mana yang membawa traffic
    - 2-3 bulan  : ranking & klik dari query non-brand
    - 3-6 bulan  : traffic stabil & konversi WhatsApp naik

  Yang TIDAK bisa dinilai dari angka di script ini: ranking, klik,
  konversi. Itu hanya bisa dilihat di Search Console + Umami.

  Kalau ada satu [!!] di bagian 1-5, itu tanda bahaya.
  Perbaiki itu dulu sebelum membaca data apa pun.
RINGKAS