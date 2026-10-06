# mytory-skills

> 개인적으로 모은 AI 코딩 에이전트용 스킬 모음입니다.
>
> 원본 스킬들을 한국어로 번역하여 개인 용도로 사용하고 있습니다.

## 📂 스킬 목록 (총 32개)

<details>
<summary><strong>🛠️ 개발 워크플로우</strong></summary>

| 스킬 | 설명 |
|------|------|
| [open-code-review](open-code-review/) | `ocr` CLI로 Git 변경사항 AI 기반 코드 리뷰 수행 |
| [open-code-review-delegate](open-code-review-delegate/) | OCR은 파일 선택·규칙 해석만, 리뷰는 호스트 에이전트가 직접 수행 |
| [review](review/) | 기준점 이후 변경사항을 표준/명세 두 축으로 검토 |
| [diagnose](diagnose/) | 버그와 성능 저하를 위한 규율 있는 진단 루프 |
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
| [design-an-interface](design-an-interface/) | 모듈에 대한 복수 인터페이스 설계안 생성 |

</details>

<details>
<summary><strong>📝 문서 / 글쓰기</strong></summary>

| 스킬 | 설명 |
|------|------|
| [edit-article](edit-article/) | 글 편집 — 명확성, 간결성, 섹션 구조 개선 |
| [to-prd](to-prd/) | 대화 컨텍스트를 PRD로 변환하여 이슈 트래커에 게시 |
| [to-issues](to-issues/) | 계획/명세를 작업 가능한 이슈로 분해 등록 |
| [request-refactor-plan](request-refactor-plan/) | 리팩터링 계획 수립 및 GitHub 이슈 등록 |
| [improve-codebase-architecture](improve-codebase-architecture/) | 코드베이스 아키텍처 개선 기회 탐색 |
| [write-a-skill](write-a-skill/) | 새 에이전트 스킬 생성 (구조, 점진적 공개, 번들 리소스) |
| [html-work-report](html-work-report/) | 작업 시작 시 작성 여부를 확인하고 HTML 완료 보고서와 검증 증거 정리 (자작) |
| [supertonic-tts](supertonic-tts/) | 로컬 Supertonic 3로 한국어 WAV 합성, 미설치 환경 준비와 CLI·HTTP 사용 안내 (자작) |

</details>

<details>
<summary><strong>🤔 기획 / 의사결정</strong></summary>

| 스킬 | 설명 |
|------|------|
| [grill-me](grill-me/) | 계획/디자인을 집요하게 인터뷰하여 의사결정 트리 해결 |
| [grill-with-docs](grill-with-docs/) | 도메인 모델 기반 계획 검증 및 문서 업데이트 |
| [handoff](handoff/) | 대화를 핸드오프 문서로 압축하여 다른 에이전트에 인계 |
| [zoom-out](zoom-out/) | 한 단계 물러나 넓은 맥락/상위 관점 제공 |
| [triage](triage/) | 상태 머신 기반 이슈 분류 |

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
| [browser-repro-video](browser-repro-video/) | 수정 전후를 브라우저에서 재현해 캡션·강조·커서가 보이는 mp4로 녹화(자막 파일도 지원)하고 정지 화면 5초 초과 검수, 날짜 붙은 보고서 폴더의 HTML에 embed (자작) |

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

## 📋 출처

각 스킬의 원본 저장소와 저자입니다.

| 출처 | 스킬 |
|------|------|
| [mattpocock/skills](https://github.com/mattpocock/skills) (18개) | caveman, design-an-interface, diagnose, edit-article, grill-me, grill-with-docs, handoff, improve-codebase-architecture, obsidian-vault, prototype, request-refactor-plan, review, tdd, to-issues, to-prd, triage, write-a-skill, zoom-out |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) (3개) | design-taste-frontend, full-output-enforcement, image-to-code |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | agent-browser |
| [anthropics/skills](https://github.com/anthropics/skills) | frontend-design |
| [ctxrs/ctx](https://github.com/ctxrs/ctx) | ctx-agent-history-search |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) (2개) | open-code-review, open-code-review-delegate |
| [deusyu/translate-book](https://github.com/deusyu/translate-book) | translate-long-text |

## 🔗 관련 링크

- GitHub: https://github.com/mytory/mytory-skills
- pi coding agent: Agent용 스킬 시스템
