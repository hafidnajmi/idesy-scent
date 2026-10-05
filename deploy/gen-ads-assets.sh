#!/usr/bin/env bash
# Generate Google Ads image + logo assets for indoeasyscent.com.
#
# WHY A SEPARATE GENERATOR: img/og/*.jpg are 1200x630 OpenGraph covers. That
# ratio (1.90:1) is NOT one of the ratios Google Ads accepts, so the OG covers
# cannot be uploaded to a responsive display ad. The site photos are mostly
# 4:3 / 1:1 / 1536x1024, which also do not match. Google Ads wants:
#
#   landscape image  1.91:1   1200x628   (min 600x314)   max 5120 KB
#   square image     1:1      1200x1200 (min 300x300)   max 5120 KB
#   logo             1:1      1200x1200 (min 128x128)   max 150 KB
#   logo             4:1      1200x300   (min 512x128)   max 150 KB
#
# IDEMPOTENT: re-running overwrites the same files with the same bytes.
# No text is burned into the lifestyle crops on purpose -- Google re-crops
# images to many placements and baked-in text gets clipped. Only the product
# shots carry a caption, and only in the empty bottom band.
#
# Brand palette (read from the site CSS, not guessed):
#   forest #0D2A1D   gold #C9A24B   ivory #F7F3EC   stone #EDE6D8
set -euo pipefail

cd "$(dirname "$0")/.."
OUT="img/ads"
SERIF="/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"
SANS="/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
SANSB="/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

[ -f "$SERIF" ] || { echo "FATAL: font not found $SERIF" >&2; exit 1; }
command -v magick >/dev/null || { echo "FATAL: magick not found" >&2; exit 1; }
command -v rsvg-convert >/dev/null || { echo "FATAL: rsvg-convert not found" >&2; exit 1; }
mkdir -p "$OUT"

FOREST="#0D2A1D"
GOLD="#C9A24B"
IVORY="#F7F3EC"
STONE="#EDE6D8"

# Photos deliberately EXCLUDED from ad assets:
#   professional_diffuser.png -- third-party hotel lobby, product on it is
#     branded "AURA", plus identifiable staff. Advertising someone else's
#     trademark is a policy violation, not just a taste problem.
#   kantor.jpg -- third-party office, visible "acer" monitor branding and
#     identifiable employee faces.
#   *_harga / marketplace badges -- marketplace marks are not ours to show.
USED_PHOTOS=()

# photo_cover <src> <slug> <WxH> <gravity>
# Centre-weighted crop to the target ratio, then a soft brand scrim in the
# bottom band so the shot reads as ours without covering the photo.
photo_cover() {
  local src="$1" slug="$2" size="$3" grav="${4:-center}"
  [ -f "img/$src" ] || { echo "  skip $slug (missing img/$src)"; return 0; }
  USED_PHOTOS+=("$src")
  local dst="$OUT/$slug.jpg" acc="$OUT/.tmp-$slug.png"
  magick "img/$src" \
    -auto-orient -colorspace sRGB \
    -resize "$size^" -gravity "$grav" -extent "$size" \
    -gravity south -fill "$FOREST" -undercolor '#0D2A1DAA' \
    -extent "$size" \
    "$acc"
  magick "$acc" -strip -interlace Plane -sampling-factor 4:2:0 -quality 82 "$dst"
  rm -f "$acc"
  printf '  %-26s %-10s %sKB\n' "$slug.jpg" "$size" "$(( $(stat -c%s "$dst") / 1024 ))"
}

# product_shot <src> <slug> <WxH> <caption>
# Product centred on a white plate inside a dark brand frame, with the
# caption in the dark band at the bottom. The caption must NOT sit on the
# white plate: gold-on-white measured as weak contrast in review, and Google
# renders these small on mobile.
product_shot() {
  local src="$1" slug="$2" size="$3" caption="$4"
  [ -f "img/$src" ] || { echo "  skip $slug (missing img/$src)"; return 0; }
  USED_PHOTOS+=("$src")
  local dst="$OUT/$slug.jpg" acc="$OUT/.tmp-$slug.png"
  local w="${size%x*}" h="${size#*x}"

  # White plate leaves a margin so the product never touches the edge.
  local pw=$(( w * 72 / 100 ))
  local ph=$(( h * 62 / 100 ))
  magick -size "${pw}x${ph}" "xc:#F7F3EC" \
    \( "img/$src" -auto-orient -colorspace sRGB -resize "${pw}x${ph}" \
       -background '#F7F3EC' -gravity center -extent "${pw}x${ph}" \) \
    -composite \
    -background "$FOREST" -gravity center -extent "$size" \
    -font "$SANSB" -pointsize 24 -fill "$IVORY" \
    -gravity south -annotate "+0+$(( h * 4 / 100 ))" "$caption" \
    "$acc"
  magick "$acc" -strip -interlace Plane -sampling-factor 4:2:0 -quality 85 "$dst"
  rm -f "$acc"
  printf '  %-26s %-10s %sKB\n' "$slug.jpg" "$size" "$(( $(stat -c%s "$dst") / 1024 ))"
}

echo "Generating Google Ads assets -> $OUT/"

echo " -- landscape 1.91:1 (1200x628) --"
photo_cover  resort.jpg    ads-hotel-landscape    1200x628 center
photo_cover  restoran.jpg  ads-restoran-landscape  1200x628 center
photo_cover  retail.jpg    ads-retail-landscape    1200x628 center
product_shot ISX-H5.jpg   ads-diffuser-landscape 1200x628 "ISX-H5  -  500-1000 m3"
product_shot exclusive-fragrance.jpg ads-wewangian-landscape 1200x628 "Fragrance Oil Premium"

echo " -- square 1:1 (1200x1200) --"
photo_cover  resort.jpg    ads-hotel-square       1200x1200 center
photo_cover  restoran.jpg  ads-restoran-square     1200x1200 center
photo_cover  retail.jpg    ads-retail-square       1200x1200 center
product_shot ISX-H5.jpg   ads-diffuser-square    1200x1200 "ISX-H5  -  500-1000 m3"
product_shot exclusive-fragrance.jpg ads-wewangian-square 1200x1200 "Fragrance Oil Premium"

echo " -- logo 1:1 (1200x1200) + logo 4:1 (1200x300) --"
# Built from img/logo.svg (the real brand mark) with rsvg-convert, never
# redrawn by hand. Transparent background so it sits on any placement.
LOGO_RAW="$OUT/.tmp-logo.png"
rsvg-convert -w 900 img/logo.svg -o "$LOGO_RAW"
# -colors 256 + png8-style output: the mark is a smooth gold gradient, so a
# 256-colour palette is visually identical here but cuts the file roughly in
# half. Google rejects a logo above 150 KB, and the full-depth version landed
# at 139 KB -- too little headroom to survive a future logo tweak.
magick "$LOGO_RAW" -trim +repage -resize 700x900 \
  -background none -gravity center -extent 1200x1200 \
  -strip -colors 256 -define png:color-type=3 \
  "$OUT/ads-logo-square.png"
# 4:1 wants a horizontal lockup; the stacked emblem+wordmark would render
# too small, so this one is a wordmark plate with the emblem beside it.
# Built in flat sequential steps -- deeply nested \( ... \) groups spanning
# line continuations are not worth the parse risk.
magick "$LOGO_RAW" -trim +repage -resize 190x230 "$OUT/.tmp-mark.png"
magick -size 1200x300 "xc:$FOREST" \
  -font "$SERIF" -pointsize 54 -fill "$IVORY" \
  -annotate +330+116 "INDOEASY" \
  -font "$SANS" -pointsize 20 -fill "$GOLD" \
  -annotate +333+176 "SCENT  -  Signature Scent Indonesia" \
  "$OUT/.tmp-plate.png"
magick "$OUT/.tmp-plate.png" "$OUT/.tmp-mark.png" \
  -geometry +60+35 -composite \
  -strip -colors 256 -define png:color-type=3 \
  "$OUT/ads-logo-wide.png"
rm -f "$LOGO_RAW" "$OUT/.tmp-mark.png" "$OUT/.tmp-plate.png"

for l in "$OUT/ads-logo-square.png" "$OUT/ads-logo-wide.png"; do
  printf '  %-26s %-10s %sKB\n' "$(basename "$l")" \
    "$(identify -format '%wx%h' "$l")" "$(( $(stat -c%s "$l") / 1024 ))"
done

echo
echo "Verify before upload:"
echo "  * landscape/square images  <= 5120 KB   (Google limit)"
echo "  * logos                    <= 150 KB    (Google limit)"
big=0
for f in "$OUT"/*.jpg; do
  kb=$(( $(stat -c%s "$f") / 1024 )); [ "$kb" -le 5120 ] || { echo "  FAIL $f = ${kb}KB"; big=1; }
done
for f in "$OUT"/ads-logo-*.png; do
  kb=$(( $(stat -c%s "$f") / 1024 )); [ "$kb" -le 150 ] || { echo "  FAIL $f = ${kb}KB (max 150)"; big=1; }
done
[ "$big" -eq 0 ] || { echo "FATAL: file over the Google Ads limit" >&2; exit 1; }
echo "  all files within Google Ads limits"
echo
printf 'Photos used: %s\n' "${USED_PHOTOS[*]}"
echo "Done: $(ls "$OUT"/ads-* | wc -l) assets"