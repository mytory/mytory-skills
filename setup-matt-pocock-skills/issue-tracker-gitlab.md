# 이슈 트래커: GitLab

이 저장소의 이슈와 명세는 GitLab 이슈로 저장합니다. 모든 작업에 [`glab`](https://gitlab.com/gitlab-org/cli) CLI를 사용하세요.

## 관례

- **이슈 생성**: `glab issue create --title "..." --description "..."`. 여러 줄의 설명은 heredoc을 사용하세요. `--description -`를 전달하면 편집기가 열립니다.
- **이슈 읽기**: `glab issue view <number> --comments`. 기계가 읽을 출력은 `-F json`을 사용하세요.
- **이슈 목록**: 필요에 따라 `--label` 필터를 지정해 `glab issue list -O json`을 실행하세요.
- **이슈에 댓글 작성**: `glab issue note <number> --message "..."`. GitLab에서는 댓글을 "note"라고 부릅니다.
- **라벨 추가 / 제거**: `glab issue update <number> --label "..."` / `--unlabel "..."`. 라벨 여러 개는 쉼표로 구분하거나 플래그를 반복하세요.
- **닫기**: `glab issue close <number>`. 이 명령은 닫기 댓글을 받지 않으므로 먼저 `glab issue note <number> --message "..."`로 설명을 올린 뒤 닫으세요.
- **머지 리퀘스트**: GitLab에서는 PR을 "merge request"라고 부릅니다. `glab mr create`, `glab mr view`, `glab mr note` 등을 사용하세요. `gh pr ...`와 비슷하지만 `pr` 대신 `mr`, `comment`/`--body` 대신 `note`/`--message`를 사용합니다.

`git remote -v`로 저장소를 파악하세요. 복제본 안에서 실행한 `glab`는 저장소를 자동으로 알아냅니다.

## 머지 리퀘스트를 분류 대상으로 사용

**MRs as a request surface: no.** _(외부 머지 리퀘스트를 기능 요청으로 취급하는 저장소라면 `yes`로 설정하세요. `/triage`가 이 플래그를 읽습니다.)_

`yes`이면 MR에도 이슈와 같은 라벨과 상태를 적용하고, 이에 대응하는 `glab mr` 명령을 사용합니다.

- **MR 읽기**: `glab mr view <number> --comments`, 차이는 `glab mr diff <number>`.
- **분류할 외부 MR 목록**: `glab mr list -F json`을 실행한 뒤 프로젝트 멤버나 소유자가 작성하지 않은 MR만 남기세요. 관리자가 진행 중인 작업을 제외하고 외부 기여자의 MR을 대상으로 합니다.
- **댓글 / 라벨 / 닫기**: `glab mr note`, `glab mr update --label`/`--unlabel`, `glab mr close`.

GitLab은 이슈와 MR 번호를 별도로 매깁니다. 관리자가 어느 유형을 말하는지 알면 `#42`를 식별할 수 있습니다.

## 스킬이 "이슈 트래커에 게시"하라고 할 때

GitLab 이슈를 만드세요.

## 스킬이 "관련 티켓 가져오기"라고 할 때

`glab issue view <number> --comments`를 실행하세요.

## 길찾기 작업

`/wayfinder`에서 사용합니다. **지도**는 이슈 하나이며 **하위** 이슈가 티켓입니다.

- **지도**: `wayfinder:map` 라벨이 달린 단일 이슈. Notes / Decisions-so-far / Fog 본문을 담습니다. `glab issue create --label wayfinder:map`. (기본 epic 기능이 있는 GitLab 요금제에서는 epic을 지도로 사용할 수도 있습니다. 라벨이 달린 이슈는 어디서나 사용할 수 있습니다.)
- **하위 티켓**: 설명 맨 위에 `Part of #<map>`를 적고 `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`) 라벨을 단 이슈입니다. 작업을 선점하면 담당 개발자에게 할당합니다.
- **차단 관계**: UI에 표시되는 GitLab의 **기본 차단 링크**를 기준으로 삼습니다. `/blocked_by #<n>` 빠른 작업을 댓글로 게시하세요 (`glab issue note <child> --message "/blocked_by #<blocker>"`). 기본 차단 링크는 Premium/Ultimate 기능입니다. 무료 요금제 등에서 사용할 수 없으면 설명 맨 위에 `Blocked by: #<n>, #<n>`을 적으세요. 모든 차단 이슈가 닫히면 티켓의 차단이 해제됩니다.
- **다음 작업 조회**: 지도의 하위 이슈에 범위를 맞춰 `glab issue list -O json`을 실행하세요. 열린 차단 이슈(열린 이슈를 가리키는 기본 `blocked_by` 링크: `glab api projects/:id/issues/<child-iid>/links`, 또는 `Blocked by` 행의 열린 이슈)가 있거나 담당자가 있는 이슈는 제외합니다. 지도에 먼저 나온 이슈를 선택합니다.
- **작업 선점**: 세션의 첫 쓰기 작업으로 `glab issue update <n> --assignee @me`를 실행합니다.
- **해결**: `glab issue note <n> --message "<answer>"`, `glab issue close <n>` 순으로 실행한 뒤 지도의 Decisions-so-far에 맥락 요약과 링크를 덧붙입니다.
