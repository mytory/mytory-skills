---
name: setup-matt-pocock-skills
description: AGENTS.md/CLAUDE.md와 `docs/agents/`에 `## Agent skills` 블록을 설정하여 엔지니어링 스킬들이 이 저장소의 이슈 트래커(GitHub 또는 로컬 마크다운), 분류 라벨 어휘, 도메인 문서 레이아웃을 알 수 있게 합니다. `to-issues`, `to-prd`, `triage`, `diagnose`, `tdd`, `improve-codebase-architecture`, `zoom-out`을 처음 사용하기 전이나, 이 스킬들이 이슈 트래커, 분류 라벨, 도메인 문서에 대한 컨텍스트가 부족해 보일 때 실행하세요.
disable-model-invocation: true
---

# Matt Pocock 스킬 설정

엔지니어링 스킬들이 가정하는 저장소별 설정을 스캐폴딩:

- **이슈 트래커** — 이슈가 어디에 있는지 (기본값 GitHub; 로컬 마크다운도 기본 지원)
- **분류 라벨** — 다섯 가지 공식 분류 역할에 사용되는 문자열
- **도메인 문서** — `CONTEXT.md`와 ADR의 위치, 그리고 그것들을 읽는 소비자 규칙

이것은 결정론적 스크립트가 아닌 프롬프트 기반 스킬입니다. 탐색하고, 찾은 것을 제시하고, 사용자와 확인한 후 작성하세요.

## 절차

### 1. 탐색

현재 저장소를 보고 시작 상태를 이해하세요. 있는 것을 읽고, 가정하지 마세요:

- `git remote -v`와 `.git/config` — GitHub 저장소인가? 어느 것?
- 저장소 루트의 `AGENTS.md`와 `CLAUDE.md` — 둘 중 하나가 존재하는가? 이미 `## Agent skills` 섹션이 있는가?
- 저장소 루트의 `CONTEXT.md`와 `CONTEXT-MAP.md`
- `docs/adr/`와 모든 `src/*/docs/adr/` 디렉터리
- `docs/agents/` — 이 스킬의 이전 출력이 이미 존재하는가?
- `.scratch/` — 로컬 마크다운 이슈 트래커 관례가 이미 사용 중이라는 신호

### 2. 발견사항 제시 및 질문

존재하는 것과 누락된 것을 요약하세요. 그런 다음 세 가지 결정을 **한 번에 하나씩** 사용자에게 안내하세요 — 섹션을 제시하고, 사용자 답변을 받은 후 다음으로 이동. 한 번에 세 가지를 모두 던지지 마세요.

사용자가 이 용어들의 의미를 모른다고 가정하세요. 각 섹션은 짧은 설명(무엇인지, 왜 이 스킬들이 필요한지, 다르게 선택하면 무엇이 바뀌는지)으로 시작합니다. 그런 다음 선택지와 기본값을 보여주세요.

**섹션 A — 이슈 트래커.**

> 설명: "이슈 트래커"는 이 저장소의 이슈가 존재하는 곳입니다. `to-issues`, `triage`, `to-prd`, `qa` 같은 스킬들이 여기에서 읽고 씁니다 — `gh issue create`를 호출할지, `.scratch/` 아래에 마크다운 파일을 쓸지, 아니면 당신이 설명하는 다른 워크플로우를 따를지 알아야 합니다. 이 저장소에서 실제로 작업을 추적하는 곳을 선택하세요.

기본 자세: 이 스킬들은 GitHub용으로 설계되었습니다. `git remote`가 GitHub를 가리키면 그렇게 제안하세요. `git remote`가 GitLab(`gitlab.com` 또는 자체 호스팅 호스트)을 가리키면 GitLab을 제안하세요. 그 외의 경우(또는 사용자가 선호하는 경우) 다음을 제안:

- **GitHub** — 이슈가 저장소의 GitHub Issues에 있음 (`gh` CLI 사용)
- **GitLab** — 이슈가 저장소의 GitLab Issues에 있음 ([`glab`](https://gitlab.com/gitlab-org/cli) CLI 사용)
- **로컬 마크다운** — 이슈가 이 저장소의 `.scratch/<feature>/` 아래에 파일로 존재 (단독 프로젝트나 원격 없는 저장소에 적합)
- **기타** (Jira, Linear 등) — 사용자에게 워크플로우를 한 문단으로 설명해 달라고 요청; 스킬은 이를 자유 형식 산문으로 기록

**섹션 B — 분류 라벨 어휘.**

> 설명: `triage` 스킬이 들어오는 이슈를 처리할 때, 상태 머신을 통해 이동시킵니다 — 평가 필요, 보고자 대기 중, AFK 에이전트가 가져갈 준비 완료, 사람 필요, 또는 수정 안 함. 이를 위해 *당신이 실제로 구성한* 문자열과 일치하는 라벨(또는 이슈 트래커의 동등물)을 적용해야 합니다. 저장소가 이미 다른 라벨명(예: `needs-triage` 대신 `bug:triage`)을 사용 중이면 여기서 매핑하여 스킬이 중복을 생성하는 대신 올바른 것을 적용하게 하세요.

다섯 가지 공식 역할:

- `needs-triage` — 메인테이너가 평가 필요
- `needs-info` — 보고자 대기 중
- `ready-for-agent` — 완전히 명세화됨, AFK 대응 가능 (에이전트가 사람 컨텍스트 없이 가져갈 수 있음)
- `ready-for-human` — 사람 구현 필요
- `wontfix` — 조치되지 않을 것

기본값: 각 역할의 문자열은 그 이름과 동일. 사용자에게 재정의할 것이 있는지 물어보세요. 이슈 트래커에 기존 라벨이 없으면 기본값이 괜찮습니다.

**섹션 C — 도메인 문서.**

> 설명: 일부 스킬(`improve-codebase-architecture`, `diagnose`, `tdd`)은 프로젝트의 도메인 언어를 배우기 위해 `CONTEXT.md` 파일을, 과거 아키텍처 결정을 위해 `docs/adr/`을 읽습니다. 저장소에 하나의 전역 컨텍스트가 있는지 여러 개가 있는지(예: 별도의 frontend/backend 컨텍스트가 있는 모노레포) 알아야 올바른 위치를 찾습니다.

레이아웃 확인:

- **단일 컨텍스트** — 저장소 루트에 하나의 `CONTEXT.md` + `docs/adr/`. 대부분의 저장소가 이에 해당.
- **다중 컨텍스트** — 루트의 `CONTEXT-MAP.md`가 컨텍스트별 `CONTEXT.md` 파일을 가리킴 (일반적으로 모노레포).

### 3. 확인 및 편집

사용자에게 초안 보여주기:

- 편집 중인 `CLAUDE.md` / `AGENTS.md`에 추가할 `## Agent skills` 블록 (4단계에서 선택 규칙 참조)
- `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`의 내용

작성 전에 편집할 수 있게 하세요.

### 4. 작성

**편집할 파일 선택:**

- `CLAUDE.md`가 있으면 편집.
- 없으면 `AGENTS.md`가 있으면 편집.
- 둘 다 없으면 사용자에게 어느 것을 생성할지 물어보기 — 대신 선택하지 마세요.

`CLAUDE.md`가 이미 있을 때 `AGENTS.md`를 생성하지 마세요 (또는 그 반대) — 항상 이미 있는 것을 편집하세요.

선택한 파일에 `## Agent skills` 블록이 이미 존재하면 중복 추가 대신 내용을 제자리에서 업데이트하세요. 주변 섹션의 사용자 편집을 덮어쓰지 마세요.

블록:

```markdown
## Agent skills

### Issue tracker

[이슈가 추적되는 위치에 대한 한 줄 요약]. `docs/agents/issue-tracker.md` 참조.

### Triage labels

[라벨 어휘에 대한 한 줄 요약]. `docs/agents/triage-labels.md` 참조.

### Domain docs

[레이아웃에 대한 한 줄 요약 — "단일 컨텍스트" 또는 "다중 컨텍스트"]. `docs/agents/domain.md` 참조.
```

그런 다음 이 스킬 폴더의 시드 템플릿을 시작점으로 세 문서 파일 작성:

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub 이슈 트래커
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab 이슈 트래커
- [issue-tracker-local.md](./issue-tracker-local.md) — 로컬 마크다운 이슈 트래커
- [triage-labels.md](./triage-labels.md) — 라벨 매핑
- [domain.md](./domain.md) — 도메인 문서 소비자 규칙 + 레이아웃

"기타" 이슈 트래커의 경우, 사용자 설명을 사용해 `docs/agents/issue-tracker.md`를 처음부터 작성.

### 5. 완료

사용자에게 설정이 완료되었으며 어떤 엔지니어링 스킬들이 이제 이 파일들에서 읽을 것인지 알리세요. 나중에 `docs/agents/*.md`를 직접 편집할 수 있다고 언급 — 이 스킬을 다시 실행하는 것은 이슈 트래커를 전환하거나 처음부터 다시 시작하려는 경우에만 필요합니다.
