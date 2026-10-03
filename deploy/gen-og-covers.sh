#!/usr/bin/env bash
# Generate OG/Twitter cover images 1200x630 JPG (<300KB) for Indoeasy Scent.
# Brand: forest #0D2A1D, gold #C9A24B, ivory #F7F3EC, stone #EDE6D8
set -euo pipefail

cd "$(dirname "$0")/.."
OUT="img/og"
SERIF="/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"
SANS="/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
SANSB="/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

[ -f "$SERIF" ] || { echo "FATAL: font not found $SERIF" >&2; exit 1; }
mkdir -p "$OUT"

# gen <slug> <eyebrow> <headline1> <headline2> [logo]
gen() {
  local slug="$1" eyebrow="$2" h1="$3" h2="$4" logo="${5:-}"
  local dst="$OUT/$slug.jpg"
  local acc="$OUT/.tmp-$slug.png"

  local args=(
    -size 1200x630 "gradient:#123524-#081b13"
    -font "$SANSB" -pointsize 20 -fill "#C9A24B"
    -gravity northwest -annotate +80+74 "I N D O E A S Y   S C E N T"
    -stroke "#C9A24B" -strokewidth 2 -fill none
    -draw "line 80,120 240,120"
    -stroke none
    -font "$SERIF" -pointsize 62 -fill "#F7F3EC"
    -gravity northwest -annotate +80+176 "$h1"
  )
  [ -n "$h2" ] && args+=(-pointsize 34 -fill "#EDE6D8" -annotate +80+258 "$h2")
  args+=(
    -font "$SANS" -pointsize 21 -fill "#C9A24B"
    -gravity southwest -annotate +80+74 "$eyebrow"
    -font "$SANS" -pointsize 18 -fill "#EDE6D8"
    -annotate +80+104 "indoeasyscent.com"
  )
  [ -n "$logo" ] && args+=(
    -font "$SANSB" -pointsize 22 -fill "#C9A24B"
    -gravity southeast -annotate +80+80 "IFRA  ·  KEMENKES RI"
  )

  magick "${args[@]}" "$acc"
  magick "$acc" -strip -interlace Plane -sampling-factor 4:2:0 \
    -quality 80 "$dst"
  rm -f "$acc"

  local kb; kb=$(( $(stat -c%s "$dst") / 1024 ))
  printf '  %-22s %s\n' "$slug.jpg" "$(( 1200 ))x630  ${kb}KB"
  [ "$kb" -lt 300 ] || { echo "FATAL: $slug.jpg is ${kb}KB (>300KB)" >&2; exit 1; }
}

echo "Generating OG covers -> $OUT/"
gen index      "Commercial Scenting · Indonesia" "Branding Atmosferik" "Signature Scent"                        1
gen products   "11 Model Diffuser · Cold-Air"   "Professional"        "Scenting Diffuser"                     1
gen collection "Fragrance & Reed Diffuser"       "Eksklusif"           "Koleksi Wewangian"                     1
gen about      "Bekasi · Jawa Barat"            "Tentang"             "Indoeasy Scent"                       1
gen contact    "Konsultasi Gratis"              "Hubungi"             "Tim Indoeasy Scent"                   1
gen checkout    "B2B Inquiry · Tanpa Komitmen"   "Penawaran"           "Form Inquiry"                         1
gen privacy    "Kebijakan Privasi"              "Legal"               "Privasi Pengguna"                     ""
gen terms      "Ketentuan Layanan"              "Legal"               "Syarat & Ketentuan"                   ""
gen 404        "Halaman Tidak Ditemukan"         "Error 404"           "Kembali ke Beranda"                   ""
echo "Done: $(ls "$OUT"/*.jpg | wc -l) covers"