#!/bin/bash
# 검수용 프레임 추출. 사용: extract-frames.sh <영상.mp4> <출력폴더> <초> [<초> ...]
# 예: extract-frames.sh out.mp4 frames 1 5 12.5   → frames/t-1.png ...
# 추출한 PNG는 Read 도구로 직접 열어 확인한다.
set -eu
video=${1:?}; dir=${2:?}; shift 2
mkdir -p "$dir"
for t in "$@"; do
  ffmpeg -y -loglevel error -ss "$t" -i "$video" -frames:v 1 "$dir/t-$t.png"
  echo "$dir/t-$t.png"
done
