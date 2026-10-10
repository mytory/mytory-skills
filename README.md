# mytory-skills

> 개인적으로 모은 AI 코딩 에이전트용 스킬 모음입니다.
>
> 원본 스킬들을 한국어로 번역하여 개인 용도로 사용하고 있습니다.

## 설치

Node.js와 npm(`npx`), Git이 필요합니다. [skills CLI](https://github.com/vercel-labs/skills)를 실행하면 설치할 스킬과 사용할 에이전트를 대화형으로 선택할 수 있습니다.

```bash
npx skills add mytory/mytory-skills
```

설치하지 않고 사용 가능한 스킬 목록만 확인하려면:

```bash
npx skills add mytory/mytory-skills --list
```

특정 스킬만 설치하려면 `--skill`을 지정합니다.

```bash
npx skills add mytory/mytory-skills --skill diagnose
```

기본 설치 범위는 현재 프로젝트입니다. 모든 프로젝트에서 사용할 수 있도록 사용자 홈에 설치하려면 `-g`를 추가합니다. 다음은 `diagnose`를 Codex용으로 전역 설치하는 예시입니다.

```bash
npx skills add mytory/mytory-skills --skill diagnose -a codex -g
```

스킬 폴더의 스크립트와 참고 자료도 함께 설치됩니다. 스킬에서 사용하는 외부 도구와 API 인증은 각 `SKILL.md`의 안내에 따라 별도로 준비해야 합니다.

## 📂 스킬 목록 (총 37개)

<details>
<summary><strong>🛠️ 개발 워크플로우</strong></summary>

| 스킬 | 설명 |
|------|------|
| [open-code-review](open-code-review/) | `ocr` CLI로 Git 변경사항 AI 기반 코드 리뷰 수행 |
| [open-code-review-delegate](open-code-review-delegate/) | OCR은 파일 선택·규칙 해석만, 리뷰는 호스트 에이전트가 직접 수행 |
| [code-review](code-review/) | 코드 변경을 단계별로 검토 |
| [diagnosing-bugs](diagnosing-bugs/) | 버그와 성능 저하를 위한 재현 중심 진단 루프 |
| [tdd](tdd/) | Red-Green-Refactor 루프를 통한 테스트 주도 개발 |
| [prototype](prototype/) | 디자인 커밋 전 구체화를 위한 일회용 프로토타입 |
| [full-output-enforcement](full-output-enforcement/) | LLM 출력 잘림 방지, 완전한 코드 생성 강제 |

</details>

<details>
<summary><strong>🎨 디자인 / UI</strong></summary>

| 스킬 | 설명 |
|------|------|
| [design-taste-frontend](design-taste-frontend/) | 반-슬롭 프론트엔드 랜딩페이지/포트폴리오/리디자인 |
| [frontend-design](frontend-design/) | 새 UI 구축/재구성 시 독특한 시각 디자인 가이드 |
| [image-to-code](image-to-code/) | 이미지 → 코드 변환 |
| [codebase-design](codebase-design/) | 코드베이스의 설계 선택지를 비교하고 구체화 |

</details>

<details>
<summary><strong>📝 문서 / 글쓰기</strong></summary>

| 스킬 | 설명 |
|------|------|
| [edit-article](edit-article/) | 글 편집 — 명확성, 간결성, 섹션 구조 개선 |
| [report-notice-writing](report-notice-writing/) | 보고·공지·다른 팀 공유 문서를 쉬운 말로 — 참조 대신 풀어 쓰기, 요청은 평서문, 용어 풀기, 전후 예시와 점검표 (자작) |
| [to-spec](to-spec/) | 대화 컨텍스트를 구현 명세로 정리 |
| [to-tickets](to-tickets/) | 계획/명세를 작업 가능한 티켓으로 분해 등록 |
| [request-refactor-plan](request-refactor-plan/) | 리팩터링 계획 수립 및 GitHub 이슈 등록 |
| [improve-codebase-architecture](improve-codebase-architecture/) | 코드베이스 아키텍처 개선 기회 탐색 |
| [writing-for-agents](writing-for-agents/) | 에이전트가 따르기 쉬운 스킬과 지침 작성 |
| [update-skills](update-skills/) | 월간 점검 시 외부 출처 스킬 최신화와 한국어 번역을 수행하고 최근 결과만 기록 (자작) |
| [html-work-report](html-work-report/) | 작업 시작 시 보고서 작성 여부와 변경 유형별 증거를 정하고, 완료 기준·증거·위험도·검수 전용 AI 결과를 담은 HTML 완료 보고서 작성 (자작) |
| [supertonic-tts](supertonic-tts/) | 로컬 Supertonic 3로 한국어 WAV 합성, 미설치 환경 준비와 CLI·HTTP 사용 안내 (자작) |

</details>

<details>
<summary><strong>🤔 기획 / 의사결정</strong></summary>

| 스킬 | 설명 |
|------|------|
| [grill-me](grill-me/) | 계획/디자인을 집요하게 인터뷰하여 의사결정 트리 해결 |
| [grill-with-docs](grill-with-docs/) | 도메인 모델 기반 계획 검증 및 문서 업데이트 |
| [grilling](grilling/) | 질문을 통해 계획의 미결정 사항을 구체화 |
| [domain-modeling](domain-modeling/) | 도메인 언어와 설계 결정을 문서화 |
| [handoff](handoff/) | 대화를 핸드오프 문서로 압축하여 다른 에이전트에 인계 |
| [zoom-out](zoom-out/) | 한 단계 물러나 넓은 맥락/상위 관점 제공 |
| [triage](triage/) | 상태 머신 기반 이슈 분류 |
| [setup-matt-pocock-skills](setup-matt-pocock-skills/) | 이슈 트래커와 문서 경로 등 스킬 사용 환경 설정 |

</details>

<details>
<summary><strong>🔍 검색 / 컨텍스트</strong></summary>

| 스킬 | 설명 |
|------|------|
| [ctx-agent-history-search](ctx-agent-history-search/) | ctx로 로컬 코딩 에이전트 기록 검색 |
| [obsidian-vault](obsidian-vault/) | Obsidian 볼트 노트 검색/생성/관리 |

</details>

<details>
<summary><strong>🌐 브라우저 / 웹</strong></summary>

| 스킬 | 설명 |
|------|------|
| [agent-browser](agent-browser/) | AI 에이전트용 브라우저 자동화 CLI |
| [browser-repro-video](browser-repro-video/) | 전후 비교·작동 시연 영상을 캡션·강조·커서가 보이는 mp4로 녹화(자막·내레이션 지원)하고 정지 화면 검수, 보고서 프레젠테이션 영상 제작 (자작) |

</details>

<details>
<summary><strong>📖 번역 / 전자책</strong></summary>

| 스킬 | 설명 |
|------|------|
| [translate-long-text](translate-long-text/) | 병렬 하위 에이전트로 긴 글(PDF/DOCX/EPUB/TXT/MD) 번역 |
| [epub-for-ridi](epub-for-ridi/) | 리디북스용 EPUB 생성·검증·보정 — NCX 누락, 제목 위계, 왼쪽 정렬 (자작) |

</details>

<details>
<summary><strong>💚 웰빙 / 응원</strong></summary>

| 스킬 | 설명 |
|------|------|
| [life-cheer](life-cheer/) | 심리학 근거 기반 응원 메시지 생성 — 힘든 날부터 평온·심심·기분 좋은 날까지. 최신 연구 출처·메시지 116개·CLI 포함 (자작) |

</details>

<details>
<summary><strong>⚡ 기타</strong></summary>

| 스킬 | 설명 |
|------|------|
| [caveman](caveman/) | 초압축 커뮤니케이션 모드 (토큰 75% 절감) |

</details>

최신 mattpocock 스킬에서 호출 이름이 변경되었습니다: `design-an-interface` → `codebase-design`, `diagnose` → `diagnosing-bugs`, `review` → `code-review`, `to-issues` → `to-tickets`, `to-prd` → `to-spec`, `write-a-skill` → `writing-for-agents`.

## 📋 출처

각 스킬의 원본 저장소와 저자입니다.

| 출처 | 스킬 |
|------|------|
| [mattpocock/skills](https://github.com/mattpocock/skills) (21개, 원본 `49dd158`) | caveman, code-review, codebase-design, diagnosing-bugs, domain-modeling, edit-article, grill-me, grill-with-docs, grilling, handoff, improve-codebase-architecture, obsidian-vault, prototype, request-refactor-plan, setup-matt-pocock-skills, tdd, to-spec, to-tickets, triage, writing-for-agents, zoom-out. 원본에서 사라진 기존 5개(caveman, edit-article, obsidian-vault, request-refactor-plan, zoom-out)는 이전 번역을 유지 |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) (3개, 원본 `717446e`) | design-taste-frontend, full-output-enforcement, image-to-code |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) (원본 `44af398`) | agent-browser |
| [anthropics/skills](https://github.com/anthropics/skills) (원본 `dbd4588`) | frontend-design |
| [ctxrs/ctx](https://github.com/ctxrs/ctx) (원본 `56aaf352`) | ctx-agent-history-search (사용 목적에 맞춘 재구성) |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) (2개, 원본 `35fc3e2`) | open-code-review, open-code-review-delegate |
| [deusyu/translate-book](https://github.com/deusyu/translate-book) (원본 `bd5424b`) | translate-long-text (TXT 처리 등 로컬 확장 유지) |

## 🔗 관련 링크

- GitHub: https://github.com/mytory/mytory-skills
- pi coding agent: Agent용 스킬 시스템
