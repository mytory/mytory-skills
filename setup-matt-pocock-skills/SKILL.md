---
name: setup-matt-pocock-skills
description: "이 저장소에서 Matt Pocock의 엔지니어링 스킬을 처음 사용하기 전에 이슈 트래커, 분류 라벨 용어, 도메인 문서 구조를 설정합니다. 'Matt Pocock 스킬 설정', '엔지니어링 스킬 초기 설정'을 요청할 때 사용합니다."
disable-model-invocation: true
---

# Matt Pocock 스킬 설정

엔지니어링 스킬이 기대하는 저장소별 설정을 만듭니다.

- **이슈 트래커**: 이슈가 저장되는 곳 (기본값 GitHub, 로컬 마크다운도 지원)
- **분류 라벨**: 다섯 가지 표준 분류 역할에 사용하는 문자열
- **도메인 문서**: `GLOSSARY.md`와 ADR의 위치 및 이를 읽는 규칙

이 스킬은 결정적 스크립트가 아니라 대화형 절차입니다. 조사하고, 발견한 내용을 제시하고, 사용자에게 확인받은 뒤 작성하세요.

## 절차

### 1. 조사

현재 저장소를 살펴보고 출발 상태를 파악하세요. 존재하는 자료를 읽고 추측하지 마세요.

- `git remote -v`와 `.git/config`: GitHub 저장소인가요? 어느 저장소인가요?
- 저장소 루트의 `AGENTS.md`와 `CLAUDE.md`: 어느 파일이 있나요? 이미 `## Agent skills` 섹션이 있나요?
- 저장소 루트의 `GLOSSARY.md`와 `GLOSSARY-MAP.md`
- `docs/adr/` 및 `src/*/docs/adr/` 디렉터리
- `docs/agents/`: 이 스킬이 이전에 만든 파일이 있나요?
- `.scratch/`: 로컬 마크다운 이슈 트래커 관례를 이미 사용한다는 신호입니다.
- `triage` 스킬이 설치되어 있나요? 이 스킬 옆의 `triage` 폴더나 사용 가능한 스킬 목록을 확인하세요. 이에 따라 B절 실행 여부가 결정됩니다.
- 모노레포 신호: `pnpm-workspace.yaml`, `package.json`의 `workspaces` 필드, 자체 `src/`가 있는 `packages/*`. 실제로 규모가 큰 여러 패키지 저장소에만 해당합니다. 없으면 대부분의 저장소처럼 단일 컨텍스트로 간주합니다.

### 2. 조사 결과를 제시하고 질문

있는 항목과 없는 항목을 요약하세요. 각 절을 순서대로 진행하고, 한 절의 답을 받은 뒤 다음 절로 넘어가세요.

각 절에서는 권장 답을 먼저 제시해 사용자가 한마디로 수락할 수 있게 하세요. 선택에 따라 경로가 달라질 때만 한 줄 설명을 덧붙이세요. 조사 결과로 이미 결정된 절은 건너뛰세요 (`triage`가 없으면 B절, 모노레포가 아니면 C절 질문).

**A절: 이슈 트래커.**

> 설명: 이슈 트래커는 이 저장소의 이슈가 저장되는 곳입니다. `to-tickets`, `triage`, `to-spec` 같은 스킬은 여기에서 읽고 여기에 씁니다. `gh issue create`를 호출할지, `.scratch/` 아래에 마크다운 파일을 쓸지, 사용자가 설명한 다른 절차를 따를지 알아야 합니다. 실제로 이 저장소의 작업을 관리하는 곳을 선택하세요.

기본 방향: 이 스킬들은 GitHub용으로 설계되었습니다. `git remote`가 GitHub를 가리키면 GitHub를 권장하고, GitLab(`gitlab.com` 또는 자체 호스팅)을 가리키면 GitLab을 권장하세요. 그 외의 경우나 사용자가 원하면 다음을 제시하세요.

- **GitHub**: 해당 저장소의 GitHub Issues (`gh` CLI 사용)
- **GitLab**: 해당 저장소의 GitLab Issues ([`glab`](https://gitlab.com/gitlab-org/cli) CLI 사용)
- **로컬 마크다운**: 이 저장소의 `.scratch/<feature>/`에 파일로 저장. 개인 프로젝트나 원격 저장소가 없는 경우에 적합합니다.
- **기타** (Jira, Linear 등): 사용자에게 작업 절차를 한 문단으로 설명받고 자유 형식의 글로 기록합니다.

선택을 `docs/agents/issue-tracker.md`에 기록하세요. GitHub와 GitLab 템플릿에는 "요청 접수 경로로 PR 사용" 플래그가 있으며 기본값은 **꺼짐**입니다. 그대로 두고 별도로 질문하지 마세요. 외부 PR을 분류 대기열에 포함하려는 사용자는 나중에 파일에서 직접 켤 수 있습니다.

**B절: 분류 라벨 용어.** 조사 결과 `triage` 스킬이 설치되어 있지 않다면 이 절 전체를 건너뛰세요. 설치하지 않은 스킬에 라벨은 필요하지 않습니다.

설치되어 있다면 질문은 하나만 하세요.

> 기본 분류 라벨을 그대로 사용하시겠습니까? (권장: **예**)

기본값은 다섯 가지 표준 역할이며, 각 라벨 문자열은 역할 이름과 같습니다: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. **예**라면 그대로 작성하세요. **아니요**인 경우에만, 보통 트래커에서 이미 다른 이름을 사용한다면 (예: `needs-triage` 대신 `bug:triage`), 기존 라벨과 중복되지 않도록 바꿀 문자열을 수집하세요.

**C절: 도메인 문서.** 기본값은 **단일 컨텍스트**입니다 (저장소 루트의 `GLOSSARY.md` 하나와 `docs/adr/`). 대부분의 저장소에 적합하므로 묻지 말고 작성하세요.

조사에서 모노레포 신호가 발견된 경우에만 **다중 컨텍스트** (루트의 `GLOSSARY-MAP.md`가 컨텍스트별 `GLOSSARY.md`를 가리킴)를 제시하고 어느 구조를 사용할지 확인하세요.

### 3. 확인하고 편집

다음 초안을 사용자에게 보여주세요.

- `CLAUDE.md`나 `AGENTS.md` 중 편집할 파일에 추가할 `## Agent skills` 블록 (선택 규칙은 4단계 참고)
- `docs/agents/issue-tracker.md`, `docs/agents/domain.md` 및 `docs/agents/triage-labels.md`의 내용 (마지막 파일은 `triage`가 설치된 경우에만)

작성 전에 사용자가 초안을 수정할 수 있게 하세요.

### 4. 작성

**편집할 파일 선택:**

- `CLAUDE.md`가 있으면 그 파일을 편집합니다.
- 그렇지 않고 `AGENTS.md`가 있으면 그 파일을 편집합니다.
- 둘 다 없으면 어느 파일을 만들지 사용자에게 묻고 임의로 선택하지 마세요.

`CLAUDE.md`가 있는데 `AGENTS.md`를 새로 만들거나, 반대 상황에서 `CLAUDE.md`를 새로 만들지 마세요. 항상 기존 파일을 편집하세요.

선택한 파일에 이미 `## Agent skills` 블록이 있다면 중복해서 덧붙이지 말고 기존 내용을 수정하세요. 주변 섹션에 사용자가 작성한 내용은 덮어쓰지 마세요.

블록 형식:

```markdown
## Agent skills

### Issue tracker

[이슈가 저장되는 곳 한 줄 요약]. See `docs/agents/issue-tracker.md`.

### Triage labels

[라벨 용어 한 줄 요약]. See `docs/agents/triage-labels.md`.

### Domain docs

["single-context" 또는 "multi-context" 구조 한 줄 요약]. See `docs/agents/domain.md`.
```

`### Triage labels` 하위 블록과 `docs/agents/triage-labels.md`는 `triage`가 설치되어 B절을 진행한 경우에만 포함하세요. 그렇지 않으면 둘 다 생략하세요.

B절을 GitHub나 GitLab에서 진행했다면, 설정한 라벨 중 트래커에 없는 것을 각각 만드세요 (`gh label create` / `glab label create`).

이 스킬 폴더의 템플릿을 시작점으로 삼아 문서 파일을 작성하세요.

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub 이슈 트래커
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab 이슈 트래커
- [issue-tracker-local.md](./issue-tracker-local.md): 로컬 마크다운 이슈 트래커
- [triage-labels.md](./triage-labels.md): 라벨 매핑 (`triage`가 설치된 경우에만)
- [domain.md](./domain.md): 도메인 문서를 읽는 규칙 및 구조

"기타" 이슈 트래커라면 사용자의 설명을 바탕으로 `docs/agents/issue-tracker.md`를 처음부터 작성하세요.

### 5. 완료

설정이 끝났다고 알리고, 이제 어느 엔지니어링 스킬이 이 파일들을 읽는지 설명하세요. 사용자는 나중에 `docs/agents/*.md`를 직접 편집할 수 있습니다. 이슈 트래커를 바꾸거나 처음부터 다시 설정하려는 경우에만 이 스킬을 다시 실행하면 됩니다.
