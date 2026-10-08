# 이슈 트래커: 로컬 마크다운

이 저장소의 이슈와 명세는 `.scratch/` 아래의 마크다운 파일로 저장합니다.

## 관례

- 기능마다 디렉터리 하나를 사용합니다: `.scratch/<feature-slug>/`
- 명세 파일은 `.scratch/<feature-slug>/spec.md`입니다.
- 구현 이슈는 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`에 티켓별 파일로 작성하고 `01`부터 번호를 붙입니다. 티켓을 하나의 파일로 합치지 마세요.
- 분류 상태는 각 이슈 파일 상단 근처의 `Status:` 행에 기록합니다 (역할 문자열은 `triage-labels.md` 참고).
- 댓글과 대화 기록은 파일 끝의 `## Comments` 제목 아래에 덧붙입니다.

## 스킬이 "이슈 트래커에 게시"하라고 할 때

필요하면 디렉터리를 만든 뒤 `.scratch/<feature-slug>/` 아래에 새 파일을 작성하세요.

## 스킬이 "관련 티켓 가져오기"라고 할 때

참조된 경로의 파일을 읽으세요. 보통 사용자가 경로나 이슈 번호를 직접 알려줍니다.

## 길찾기 작업

`/wayfinder`에서 사용합니다. **지도**는 파일 하나이며 티켓마다 **하위** 파일이 하나씩 있습니다.

- **지도**: `.scratch/<effort>/map.md` (Notes / Decisions-so-far / Fog 본문).
- **하위 티켓**: `.scratch/<effort>/issues/NN-<slug>.md`. `01`부터 번호를 붙이고 본문에 질문을 적습니다. `Type:` 행에는 티켓 유형(`research`/`prototype`/`grilling`/`task`), `Status:` 행에는 `claimed`/`resolved`를 기록합니다.
- **차단 관계**: 상단 근처의 `Blocked by: NN, NN` 행. 나열된 파일이 모두 `resolved`가 되면 차단이 해제됩니다.
- **다음 작업**: `.scratch/<effort>/issues/`에서 열려 있고 차단되지 않았으며 담당자가 없는 파일을 찾습니다. 번호가 가장 빠른 파일부터 진행합니다.
- **작업 선점**: 다른 작업 전에 `Status: claimed`로 설정하고 저장합니다.
- **해결**: `## Answer` 제목 아래에 답을 덧붙이고 `Status: resolved`로 설정합니다. 그다음 `map.md`의 Decisions-so-far에 맥락 요약과 링크를 덧붙입니다.
