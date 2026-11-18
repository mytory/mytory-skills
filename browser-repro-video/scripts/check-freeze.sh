#!/bin/bash
# 정지 화면 검사. 사용: check-freeze.sh <영상.mp4> [최대초=5] [noise=0.0005]
# 정지 구간이 최대초를 넘으면 시작·길이를 출력하고 종료 코드 1. 통과하면 0. 읽기 실패는 2.
#
# 동작: ffmpeg freezedetect로 1초 이상 정지한 조각을 모두 뽑고, 틈이 0.3초 이하이면서 틈 앞뒤 화면이 같은(차이 ≤ noise) 조각은
#   이어 붙여 하나의 정지로 본다. 틈 앞뒤 화면이 다르면(장면 전환·캡션 변경) 틈이 짧아도 따로 센다.
#   (webm을 mp4로 바꾼 영상은 약 5.1초마다 한 프레임이 미세하게 바뀌어, 그냥 쓰면 긴 정지가 5.1초 조각으로 쪼개져 보인다.)
# noise: 프레임 전체의 평균 변화 허용치(0~1). 기본 0.0005.
#   - 커서 이동, 체크박스 클릭, 타이핑처럼 화면의 극히 일부만 바뀌는 변화는 0.001 이상에서 "정지"로 판정될 수 있다.
#     너무 낮추면(0.0002 이하) 인코딩 잡음이 움직임으로 잡혀 정지를 놓친다. 결과가 애매하면 0.0003과 0.001 두 값으로 돌려 본다.
#   - 스피너·깜빡이는 커서는 반대로 정지를 움직임으로 판정하게 만들 수 있다.
#   - 의심 구간은 extract-frames.sh로 시작·중간·끝 프레임을 뽑아 눈으로 확인한다.
set -u
video=${1:?"사용: check-freeze.sh <영상.mp4> [최대초] [noise]"}
max=${2:-5}
noise=${3:-0.0005}
[ -f "$video" ] || { echo "파일 없음: $video" >&2; exit 2; }
total=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$video") || exit 2
log=$(ffmpeg -hide_banner -nostats -i "$video" -an \
  -vf "freezedetect=n=${noise}:d=1" -f null - 2>&1) || { echo "ffmpeg 실패" >&2; exit 2; }
pieces=$(echo "$log" | awk -v total="$total" '
  /freeze_start/ { s=$NF; open=1 }
  /freeze_end/   { print s, $NF; open=0 }
  END { if (open) print s, total }')   # 끝나지 않은 조각은 영상 끝까지 정지

# 두 시각의 프레임 밝기 차이(평균 절대차, 0~1)
diff_at() {
  ffmpeg -nostdin -hide_banner -nostats -ss "$1" -i "$video" -ss "$2" -i "$video" \
    -lavfi "[0:v]trim=end_frame=1,setpts=0[a];[1:v]trim=end_frame=1,setpts=0[b];[a][b]blend=all_mode=difference,format=gray,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" \
    -f null - 2>/dev/null | awk -F= '/YAVG/ { print $2/255 }'
}

# 틈이 0.3초 이하이고 틈 앞뒤 조각의 화면이 같을 때만 잇는다. 장면 전환·캡션 변경은 틈이 짧아도 실제 변화라 잇지 않는다.
merged=() ps= pe= pmid=
while read -r a b; do
  [ -n "$a" ] || continue
  mid=$(awk -v a="$a" -v b="$b" 'BEGIN { print (a+b)/2 }')
  if [ -n "$pe" ] && awk -v a="$a" -v e="$pe" 'BEGIN { exit !(a - e <= 0.3) }' \
     && awk -v d="$(diff_at "$pmid" "$mid")" -v n="$noise" 'BEGIN { exit !(d != "" && d <= n) }'; then
    pe=$b
  else
    [ -n "$pe" ] && merged+=("$ps $pe")
    ps=$a pe=$b
  fi
  pmid=$mid
done <<< "$pieces"
[ -n "$pe" ] && merged+=("$ps $pe")

printf '%s\n' "${merged[@]}" | awk -v total="$total" -v max="$max" '
  NF == 2 { d=$2-$1; if (d>longest) longest=d
            if (d>max) { printf "정지 %.1f초 시작, %.1f초 동안\n", $1, d; bad++ } }
  END {
    printf "영상 %.1f초 / 기준 %s초 초과 구간 %d개 / 가장 긴 정지 %.1f초\n", total, max, bad, longest
    exit (bad>0 ? 1 : 0)
  }'
