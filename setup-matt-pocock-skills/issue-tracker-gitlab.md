# 이슈 트래커: GitLab

이 저장소의 이슈와 PRD는 GitLab 이슈로 존재합니다. 모든 작업에 [`glab`](https://gitlab.com/gitlab-org/cli) CLI 사용.

## 관례

- **이슈 생성**: `glab issue create --title "..." --description "..."`. 여러 줄 설명에는 heredoc 사용. 에디터를 열려면 `--description -` 전달.
- **이슈 읽기**: `glab issue view <number> --comments`. 기계 판독 가능 출력에는 `-F json` 사용.
- **이슈 목록**: `glab issue list -F json`, 적절한 `--label` 필터 사용.
- **이슈에 코멘트**: `glab issue note <number> --message "..."`. GitLab은 코멘트를 "notes"라고 부름.
- **라벨 적용 / 제거**: `glab issue update <number> --label "..."` / `--unlabel "..."`. 여러 라벨은 쉼표 구분 또는 플래그 반복 가능.
- **닫기**: `glab issue close <number>`. `glab issue close`는 종료 코멘트를 허용하지 않으므로, 먼저 `glab issue note <number> --message "..."`로 설명을 게시한 후 닫기.
- **머지 리퀘스트**: GitLab은 PR을 "merge requests"라고 부름. `glab mr create`, `glab mr view`, `glab mr note` 등 사용 — `gh pr ...`와 동일한 형태, `pr` 대신 `mr`, `comment`/`--body` 대신 `note`/`--message`.

클론 내에서 실행 시 `git remote -v`에서 저장소 추론 — `glab`이 자동으로 수행.

## 스킬이 "이슈 트래커에 게시"라고 말할 때

GitLab 이슈 생성.

## 스킬이 "관련 티켓 가져오기"라고 말할 때

`glab issue view <number> --comments` 실행.
