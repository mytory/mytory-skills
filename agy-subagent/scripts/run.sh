#!/usr/bin/env bash
# agy를 명세 파일 하나로 비대화 실행하고 요약을 출력한다.
# 사용: run.sh <작업폴더> <명세.md> <결과.json> [모델] [모드=auto] [대화ID]
# 모델을 비우면 AGY_MODEL, 그것도 없으면 agy 기본값을 쓴다.
set -uo pipefail

if [ $# -lt 3 ]; then
	echo "사용: $0 <작업폴더> <명세.md> <결과.json> [모델] [모드=auto] [대화ID]" >&2
	exit 2
fi
dir=$1
spec=$2
out=$3
model=${4:-${AGY_MODEL:-}}
mode=${5:-auto}
conv=${6:-}

command -v agy >/dev/null || { echo "agy를 찾을 수 없습니다(PATH 확인)." >&2; exit 2; }
[ -d "$dir" ] || { echo "작업 폴더 없음: $dir" >&2; exit 2; }
[ -s "$spec" ] || { echo "명세 파일 없음 또는 비어 있음: $spec" >&2; exit 2; }

spec_dir=$(cd "$(dirname "$spec")" && pwd)
out_dir=$(mkdir -p "$(dirname "$out")" && cd "$(dirname "$out")" && pwd)
base="$out_dir/$(basename "${out%.json}")"
out="$base.json"

args=(-p "$(cat "$spec")" --mode "$mode" --output-format json --add-dir "$spec_dir" --log-file "$base.log")
[ -n "$model" ] && args+=(--model "$model")
[ -n "$conv" ] && args+=(--conversation "$conv")

start=$(date +%s)
(cd "$dir" && agy "${args[@]}") >"$out" 2>"$base.stderr"
code=$?
echo "agy 종료 코드 $code, $(( $(date +%s) - start ))초. 결과: $out"

python3 - "$out" <<'PY'
import json, sys
path = sys.argv[1]
try:
    data = json.load(open(path, encoding="utf-8"))
except Exception as exc:
    print(f"결과 JSON을 읽지 못함: {exc}. {path}와 같은 이름의 .stderr·.log를 확인하세요.")
    sys.exit(1)
usage = data.get("usage") or {}
print(f"conversation_id: {data.get('conversation_id')}")
print(f"status: {data.get('status')}  turns: {data.get('num_turns')}  seconds: {data.get('duration_seconds')}")
print(f"tokens: total {usage.get('total_tokens')} (input {usage.get('input_tokens')}, output {usage.get('output_tokens')}, cache_read {usage.get('cache_read_tokens')})")
print("--- 최종 보고 ---")
print(data.get("response", ""))
PY
exit $code
