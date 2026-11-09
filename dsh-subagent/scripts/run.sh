#!/usr/bin/env bash
# dsh headless를 실행하고 메인 컨텍스트에 넣을 요약만 출력한다.
# 사용: run.sh <작업폴더> <명세.md> <출력.jsonl> [세션ID]
set -uo pipefail

if [ "$#" -lt 3 ]; then
  echo "사용: run.sh <작업폴더> <명세.md> <출력.jsonl> [세션ID]" >&2
  exit 2
fi

abs() { printf '%s/%s' "$(cd "$(dirname "$1")" && pwd)" "$(basename "$1")"; }

dir=$1
spec=$(abs "$2")
out=$(abs "$3")
session=${4:-}
here=$(cd "$(dirname "$0")/.." && pwd)

args=(--profile headless --patch "$here/assets/deepseek-flash-high.yml" --json)
[ -n "$session" ] && args+=(--session-id "$session")

cd "$dir" || exit 2
dsh "${args[@]}" - < "$spec" > "$out" 2> "${out%.jsonl}.err"
code=$?
python3 "$here/scripts/summarize.py" "$out" "${out%.jsonl}.err" "$code"
exit "$code"
