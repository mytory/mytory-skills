#!/bin/bash
# 보고서 폴더의 PNG 스크린샷을 WebP로 바꾸고 HTML의 참조도 고친다.
# 사용: to-webp.sh <보고서폴더> [품질=82]
#   - <폴더> 아래 모든 .png → 같은 이름의 .webp (cwebp). 변환에 성공한 PNG는 지운다.
#   - <폴더>/*.html 안의 그 파일 경로(.png)를 .webp로 바꾼다.
#   - 화면 캡처는 손실 82면 글자가 뭉개지지 않는다. 뭉개지면 품질을 올리거나 -lossless.
set -euo pipefail
dir=${1:?"사용: to-webp.sh <보고서폴더> [품질]"}
q=${2:-82}
command -v cwebp >/dev/null || { echo "cwebp가 없다: brew install webp" >&2; exit 2; }
before=0; after=0; n=0
while IFS= read -r -d '' png; do
    webp="${png%.png}.webp"
    cwebp -quiet -q "$q" "$png" -o "$webp"
    before=$((before + $(stat -f%z "$png" 2>/dev/null || stat -c%s "$png")))
    after=$((after + $(stat -f%z "$webp" 2>/dev/null || stat -c%s "$webp")))
    rm "$png"; n=$((n + 1))
done < <(find "$dir" -name '*.png' -print0)
for html in "$dir"/*.html; do
    [ -f "$html" ] || continue
    perl -pi -e 's/(\b(?:src|href|poster)="[^"]*?)\.png"/$1.webp"/g' "$html"
done
echo "PNG ${n}개 → WebP. $((before / 1024))KB → $((after / 1024))KB"
