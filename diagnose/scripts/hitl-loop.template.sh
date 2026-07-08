#!/usr/bin/env bash
# 사람이 포함된 재현 루프.
# 이 파일을 복사하고 아래 단계를 편집한 후 실행.
# 에이전트가 스크립트 실행; 사용자는 터미널의 프롬프트를 따름.
#
# 사용법:
#   bash hitl-loop.template.sh
#
# 두 가지 헬퍼:
#   step "<지시사항>"             → 지시사항 표시, Enter 대기
#   capture VAR "<질문>"          → 질문 표시, 응답을 VAR로 읽기
#
# 마지막에 캡처된 값이 KEY=VALUE로 출력되어 에이전트가 파싱.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- 아래 편집 ---------------------------------------------------------

step "http://localhost:3000에서 앱을 열고 로그인하세요."

capture ERRORED "'내보내기' 버튼을 클릭하세요. 오류가 발생했나요? (y/n)"

capture ERROR_MSG "오류 메시지를 붙여넣으세요 (또는 'none'):"

# --- 위 편집 ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
