# 이슈 트래커: GitHub

이 저장소의 이슈와 명세는 GitHub 이슈로 저장합니다. 모든 작업에 `gh` CLI를 사용하세요.

## 관례

- **이슈 생성**: `gh issue create --title "..." --body "..."`. 여러 줄의 본문은 heredoc을 사용하세요.
- **이슈 읽기**: `gh issue view <number> --json number,title,body,labels,comments`.
- **이슈 목록**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`. 필요에 따라 `--label`과 `--state` 필터를 지정하세요.
- **하위 이슈 연결**: `gh issue create --parent <parent> ...` 또는 생성 후 `gh issue edit <parent> --add-sub-issue <child>` (`gh` 2.94 이상). 이전 버전에서는 `gh api --method POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-db-id>`를 사용하세요 (아래 **차단 관계**와 같은 데이터베이스 ID). 하위 이슈 기능이 없으면 하위 이슈 본문 맨 위에 `Part of #<parent>`를 적으세요.
- **이슈에 댓글 작성**: `gh issue comment <number> --body "..."`
- **라벨 추가 / 제거**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **닫기**: `gh issue close <number> --comment "..."`

`git remote -v`로 저장소를 파악하세요. 복제본 안에서 실행한 `gh`는 저장소를 자동으로 알아냅니다.

## 풀 리퀘스트를 분류 대상으로 사용

**PRs as a request surface: no.** _(외부 PR을 기능 요청으로 취급하는 저장소라면 `yes`로 설정하세요. `/triage`가 이 플래그를 읽습니다.)_

`yes`이면 PR에도 이슈와 같은 라벨과 상태를 적용하고, 이에 대응하는 `gh pr` 명령을 사용합니다.

- **PR 읽기**: `gh pr view <number> --comments`, 차이는 `gh pr diff <number>`.
- **분류할 외부 PR 목록**: `gh api --paginate 'repos/{owner}/{repo}/pulls?state=open' --jq '.[] | select(.author_association | IN("OWNER","MEMBER","COLLABORATOR") | not) | {number, title, author: .user.login, author_association, labels: [.labels[].name]}'`.
- **댓글 / 라벨 / 닫기**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub에서는 이슈와 PR이 같은 번호 체계를 사용하므로 `#42`만으로는 구분할 수 없습니다. `gh pr view 42`로 확인하고 없으면 `gh issue view 42`를 사용하세요.

## 스킬이 "이슈 트래커에 게시"하라고 할 때

GitHub 이슈를 만드세요.

## 스킬이 "관련 티켓 가져오기"라고 할 때

위의 **이슈 읽기** 절차를 따르세요.

## 길찾기 작업

`/wayfinder`에서 사용합니다. **지도**는 이슈 하나이며 **하위** 이슈가 티켓입니다.

- **지도**: `wayfinder:map` 라벨이 달린 단일 이슈. Notes / Decisions-so-far / Fog 본문을 담습니다. `gh issue create --label wayfinder:map`.
- **하위 티켓**: 지도에 GitHub 하위 이슈로 연결한 이슈 (**하위 이슈 연결** 참고). 하위 이슈 기능이 없으면 지도 본문의 작업 목록에 추가하고 하위 이슈 본문 맨 위에 `Part of #<map>`를 적으세요. 라벨은 `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`)입니다. 작업을 선점하면 담당 개발자에게 할당합니다.
- **차단 관계**: UI에 표시되는 GitHub의 **기본 이슈 종속성**을 기준으로 삼습니다. `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`로 연결하세요. `<blocker-db-id>`는 차단 이슈의 숫자 **데이터베이스 ID**이며 (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`), `#number`나 `node_id`가 아닙니다. GitHub의 `issue_dependencies_summary.blocked_by`에는 열려 있는 차단 이슈만 포함됩니다. 종속성 기능을 사용할 수 없으면 하위 이슈 본문 맨 위에 `Blocked by: #<n>, #<n>`을 적으세요. 모든 차단 이슈가 닫히면 티켓의 차단이 해제됩니다.
- **다음 작업 조회**: 지도에 속한 열린 하위 이슈를 나열합니다 (`gh issue list --state open`, 지도의 하위 이슈나 작업 목록으로 범위 지정). 열린 차단 이슈가 있거나 (`issue_dependencies_summary.blocked_by > 0` 또는 `Blocked by` 행의 열린 이슈) 담당자가 있는 이슈를 제외합니다. 지도에 먼저 나온 이슈를 선택합니다.
- **작업 선점**: 세션의 첫 쓰기 작업으로 `gh issue edit <n> --add-assignee @me`를 실행합니다.
- **해결**: `gh issue comment <n> --body "<answer>"`, `gh issue close <n>` 순으로 실행한 뒤 지도의 Decisions-so-far에 맥락 요약과 링크를 덧붙입니다.
