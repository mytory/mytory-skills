#!/usr/bin/env bash
# 명령을 실행하고 출력을 증거 로그로 남긴다. 보고서가 실제로 돌린 결과를 인용하게 한다.
# 사용: run-evidence.sh <출력.log> <명령> [인자...]
#   - 로그: 1행 `# 실행 시각 · 커밋 해시(미커밋 변경 있으면 표시)`, 2행 `$ 명령`, 이어서 stdout+stderr, 마지막 행 `# 종료 코드 N`.
#   - 출력은 터미널에도 그대로 나오고, 이 스크립트의 종료 코드는 명령의 종료 코드와 같다.
#   - 미커밋 변경은 추적 중인 파일만 본다(보고서 폴더 같은 추적 안 된 파일은 무시).
#   - 파이프·환경 변수·cd가 필요하면 bash -c '...'로 감싼다.
set -u
[ $# -ge 2 ] || { echo "사용: run-evidence.sh <출력.log> <명령> [인자...]" >&2; exit 2; }
log=$1
shift
if hash=$(git rev-parse --short HEAD 2>/dev/null); then
    [ -n "$(git status --porcelain --untracked-files=no)" ] && hash="$hash (미커밋 변경 있음)"
else
    hash="없음"
fi
mkdir -p "$(dirname "$log")"
# 명령 줄은 읽기용으로 인자를 공백으로 잇는다(macOS bash 3.2의 printf %q는 한글을 8진수로 바꾼다).
printf '# 실행 %s · 커밋 %s\n$ %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$hash" "$*" > "$log"
"$@" 2>&1 | tee -a "$log"
code=${PIPESTATUS[0]}
echo "# 종료 코드 $code" | tee -a "$log"
exit "$code"
