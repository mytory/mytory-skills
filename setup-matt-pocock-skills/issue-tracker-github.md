# 이슈 트래커: GitHub

이 저장소의 이슈와 PRD는 GitHub 이슈로 존재합니다. 모든 작업에 `gh` CLI 사용.

## 관례

- **이슈 생성**: `gh issue create --title "..." --body "..."`. 여러 줄 본문에는 heredoc 사용.
- **이슈 읽기**: `gh issue view <number> --comments`, `jq`로 코멘트 필터링 및 라벨도 가져오기.
- **이슈 목록**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`, 적절한 `--label` 및 `--state` 필터 사용.
- **이슈에 코멘트**: `gh issue comment <number> --body "..."`
- **라벨 적용 / 제거**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **닫기**: `gh issue close <number> --comment "..."`

`git remote -v`에서 저장소 추론 — 클론 내에서 실행 시 `gh`가 자동으로 수행.

## 스킬이 "이슈 트래커에 게시"라고 말할 때

GitHub 이슈 생성.

## 스킬이 "관련 티켓 가져오기"라고 말할 때

`gh issue view <number> --comments` 실행.
