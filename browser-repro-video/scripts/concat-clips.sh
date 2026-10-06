#!/bin/bash
# 클립 이어 붙이기. 사용: concat-clips.sh <출력.mp4> <클립1.mp4> <클립2.mp4> ...
# 코덱·해상도·fps가 다르면 중단한다. 구간 시작 시각을 출력한다(보고서에 넣을 용도).
# 클립 옆에 같은 이름의 .srt가 있으면 클립 길이만큼 밀어 합친 <출력>.srt, <출력>.vtt도 만든다.
set -eu
out=${1:?}; shift
[ $# -ge 1 ] || { echo "클립이 없음" >&2; exit 2; }
sig() { ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate -of csv=p=0 "$1"; }
first=$(sig "$1"); args=(); filt=""; i=0; t=0
for f in "$@"; do
  [ "$(sig "$f")" = "$first" ] || { echo "형식이 다름: $f ($(sig "$f")) != $first" >&2; exit 1; }
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  printf "구간 %d 시작 %.1f초  %s\n" "$((i+1))" "$t" "$f"
  t=$(awk -v a="$t" -v b="$d" 'BEGIN{print a+b}')
  args+=(-i "$f"); filt+="[$i:v]"; i=$((i+1))
done
ffmpeg -y -loglevel error "${args[@]}" -filter_complex "${filt}concat=n=$i:v=1:a=0[v]" \
  -map "[v]" -pix_fmt yuv420p -movflags +faststart "$out"
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of default=nw=1 "$out"
node "$(dirname "$0")/merge-captions.mjs" "$out" "$@"
