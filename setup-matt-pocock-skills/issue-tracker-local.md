# 이슈 트래커: 로컬 마크다운

이 저장소의 이슈와 PRD는 `.scratch/`에 마크다운 파일로 존재합니다.

## 관례

- 기능당 하나의 디렉터리: `.scratch/<feature-slug>/`
- PRD는 `.scratch/<feature-slug>/PRD.md`
- 구현 이슈는 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, `01`부터 번호 매기기
- 분류 상태는 각 이슈 파일 상단 근처의 `Status:` 줄로 기록 (역할 문자열은 `triage-labels.md` 참조)
- 코멘트와 대화 이력은 `## Comments` 헤딩 아래 파일 하단에 추가

## 스킬이 "이슈 트래커에 게시"라고 말할 때

`.scratch/<feature-slug>/` 아래에 새 파일 생성 (필요시 디렉터리 생성).

## 스킬이 "관련 티켓 가져오기"라고 말할 때

참조된 경로의 파일 읽기. 사용자가 보통 경로나 이슈 번호를 직접 전달.
