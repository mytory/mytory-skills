---
name: design-taste-frontend
description: 랜딩페이지, 포트폴리오, 리디자인을 위한 반-슬롭 프론트엔드 스킬. 에이전트가 브리프를 읽고 올바른 디자인 방향을 추론하며 템플릿처럼 보이지 않는 인터페이스를 제공합니다. "고급 랜딩페이지", "프리미엄 포트폴리오", "디자인 리뉴얼", "안티 슬롭"이 필요할 때 사용합니다.
---

# tasteskill: 반-슬롭 프론트엔드 스킬

> 랜딩페이지, 포트폴리오, 리디자인 대상. 대시보드, 데이터 테이블, 다단계 제품 UI 아님.
> 아래 모든 규칙은 **맥락적**. 자동으로 발동되지 않음. 먼저 브리프를 읽고 맞는 것만 선택.

## 0. 브리프 추론 (무엇보다 먼저 방 읽기)

코드나 다이얼을 건드리기 전에 **사용자가 실제로 원하는 것을 추론**. 페이지 종류(SaaS/소비자/에이전시/이벤트 랜딩, 포트폴리오, 에디토리얼), 분위기 단어(미니멀/차분/Linear스타일/Awwwards/브루탈리스트/프리미엄 소비자), 레퍼런스 신호, 대상 독자, 기존 브랜드 자산, 조용한 제약(접근성 우선, 공공부문, 규제 산업) 파악.

코드 생성 전 한 줄 "디자인 읽기" 선언: *"Reading this as: \<페이지 종류> for \<독자>, with a \<분위기> language..."*

모호하면 **하나의** 명확화 질문. 자신 있게 추론 가능하면 묻지 말고 디자인 읽기만 선언하고 진행.

디자인 읽기 예시:
- 기술 구매자를 위한 B2B SaaS 랜딩이라면 Linear식 절제, Tailwind + Geist, 낮은 모션.
- 채용 담당자가 볼 개인 디자이너 포트폴리오라면 에디토리얼 타이포그래피, 네이티브 CSS, 스크롤 기반 모션.
- 공공 서비스 리디자인이라면 신뢰와 접근성을 우선하고 GOV.UK Frontend 또는 USWDS를 검토.

독자가 미감을 결정한다. 기존 로고, 색상, 서체, 사진은 리디자인의 출발점이다. 공공부문, 규제 산업, 어린이 대상, 접근성 우선 제약은 미적 취향보다 우선한다. 디자인 방향이 실제로 갈릴 때만 `Linear처럼 절제할까요, Awwwards처럼 실험적으로 갈까요?`와 같은 질문 하나를 한다.

안티 기본 규율: AI-보라 그라데이션, 어두운 메시 위 중앙 히어로, 세 개의 동등 기능 카드, 모든 것에 제네릭 글래스모피즘, 모든 것에 무한 루프 마이크로 애니메이션, Inter + slate-900으로 기본값 설정 금지.

## 1. 세 가지 다이얼 (핵심 설정)
- **`DESIGN_VARIANCE: 8`** — 1=완벽 대칭, 10=예술적 혼돈
- **`MOTION_INTENSITY: 6`** — 1=정적, 10=시네마틱/물리
- **`VISUAL_DENSITY: 4`** — 1=아트 갤러리/에어리, 10=칵핏/데이터 밀집

기준선: `8 / 6 / 4`. 브리프가 재정의하지 않는 한 이것 사용.

다이얼 추론: "미니멀/깨끗/차분" → 5-6/3-4/2-3. "프리미엄 소비자/Apple-y" → 7-8/5-7/3-4. "와일드/Awwwards/실험적" → 9-10/8-10/3-4. "신뢰 우선/공공부문" → 3-4/2-3/4-5.

| 용도 | `DESIGN_VARIANCE` | `MOTION_INTENSITY` | `VISUAL_DENSITY` |
|---|---:|---:|---:|
| 일반 SaaS 랜딩 | 7 | 6 | 4 |
| 에이전시/창작 랜딩 | 9 | 8 | 3 |
| 프리미엄 소비재 랜딩 | 7 | 6 | 3 |
| 디자이너/스튜디오 포트폴리오 | 8 | 7 | 3 |
| 개발자 포트폴리오 | 6 | 5 | 4 |
| 에디토리얼/블로그 | 6 | 4 | 3 |
| 공공 서비스 | 3 | 2 | 5 |
| 보존형 리디자인 | 기존값 | 기존값 + 1 | 기존값 |
| 전면 리디자인 | 기존값 + 2 | 기존값 + 2 | 기존값 |

대화에서 값을 조정하되 변수 이름은 정확히 유지한다. `LAYOUT_VARIANCE`, `ANIM_LEVEL` 같은 별칭을 만들지 않는다.

## 2. 브리프 → 디자인 시스템 맵
실제 디자인 시스템이 적합할 때 공식 패키지 사용:
- Microsoft/엔터프라이즈 → `@fluentui/react-components`
- Google/Material → `@material/web`
- IBM/B2B → `@carbon/react`
- Shopify 앱 → `polaris.js`
- GitHub 스타일 → `@primer/css` 또는 `@primer/react-brand`
- 영국 공공부문 → `govuk-frontend`
- 미국 공공부문 → `uswds`
- 모던 React → `@radix-ui/themes` 또는 shadcn/ui
- Atlassian/Jira → `@atlaskit/*`와 `@atlaskit/tokens`
- 지역 사업자/에이전시 MVP → Bootstrap 5.3
- Tailwind 기반 소규모 SaaS/AI 마케팅 → Tailwind v4와 `dark:` 변형

미학적 방향(글래스모피즘, 벤토, 브루탈리즘, 에디토리얼 등)은 단일 공식 패키지 없음 — 네이티브 CSS + Tailwind + 유지보수된 컴포넌트 라이브러리로 구축.

| 미학적 방향 | 구현 기준 |
|---|---|
| 글래스모피즘 | `backdrop-filter`, 겹친 테두리, 하이라이트와 `prefers-reduced-transparency` 대안 |
| 벤토 | 크기가 다른 셀을 가진 CSS Grid |
| 브루탈리즘 | 네이티브 CSS, 고정폭 서체, 거친 테두리 |
| 에디토리얼 | 근거 있는 세리프, 비대칭 그리드, 충분한 여백 |
| 다크 테크 | 고정폭 서체, 한 가지 네온 강조, 터미널 모티프 |
| 오로라/메시 | SVG 또는 여러 겹의 방사형 그라데이션 |
| 키네틱 타이포그래피 | CSS 애니메이션, 스크롤 기반 애니메이션, 필요할 때 GSAP |

영감을 받은 디자인과 공식 시스템을 코드 주석에서도 구별한다. 공식 토큰을 가져온 뒤 대부분을 덮어쓰지 않는다.

**정직 규칙:** 시스템이 맞으면 공식 패키지 설치 및 사용. CSS를 수동 재현하지 말 것. 프로젝트당 하나의 시스템.

## 3. 기본 아키텍처 & 관례
- **프레임워크:** React/Next.js. 기본 Server Components. 인터랙티브 컴포넌트는 `'use client'` 리프로 격리.
- **RSC 안전성:** 전역 상태 공급자는 Client Component에 둔다. Motion, 스크롤, 포인터 물리를 사용하는 컴포넌트도 별도의 클라이언트 리프로 둔다.
- **스타일링:** Tailwind v4 기본.
- **Tailwind v4:** PostCSS에서 `tailwindcss` 플러그인이 아닌 `@tailwindcss/postcss` 또는 Vite 플러그인을 사용한다. 기존 프로젝트가 v3이면 존중한다.
- **애니메이션:** Motion(`motion/react`). `framer-motion`은 레거시 별칭.
- **폰트:** `next/font` 또는 `@font-face` + `font-display: swap`으로 자체 호스팅.
- **상태:** 로컬 `useState`/`useReducer`. 전역은 깊은 prop 드릴링 회피에만. 연속값(마우스 위치 등)에 `useState` 절대 금지 — `useMotionValue`/`useTransform` 사용.
- **아이콘:** 우선순위 - `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`. `lucide-react` 비권장. SVG 아이콘 직접 그리기 금지.
- **아이콘 일관성:** 프로젝트에서 한 계열만 쓰고 `strokeWidth`도 통일한다. Lucide는 기존 의존성이 있거나 사용자가 요청했을 때 허용한다.
- **이모지:** 기본 비권장. 사용자가 명시적 요청 시에만 절제 사용.
- **반응형:** `min-h-[100dvh]` (절대 `h-screen` 금지). Flex-Math보다 CSS Grid.
- **레이아웃 기준:** `sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`; 컨테이너는 `max-w-[1400px] mx-auto` 또는 `max-w-7xl`. `w-[calc(33%-1rem)]` 대신 `grid grid-cols-1 md:grid-cols-3 gap-6`.
- **의존성 확인(필수):** 패키지를 제안하거나 가져오기 전에 실제 설치 여부와 프로젝트 버전을 확인한다. 존재하지 않는 패키지 이름이나 API를 추측하지 않는다.

## 4. 디자인 엔지니어링 지침 (편향 보정)

### 4.1 타이포그래피
- **디스플레이:** `text-4xl md:text-6xl tracking-tighter leading-none`.
- **본문:** `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
- **산세리프:** `Inter` 기본값 비권장. `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi` 선호.
- Inter는 중립적/표준적/Linear식 디자인을 사용자가 요청하거나 공공부문·접근성 우선 사이트일 때 허용한다. 짝 예시: `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.
- **세리프 규율:** 세리프는 기본값으로 매우 비권장. 에디토리얼/럭셔리/출판/유산 브랜드이고 특정 세리프가 특정 브랜드에 맞는 이유를 설명할 수 있을 때만 허용. `Fraunces`와 `Instrument_Serif`는 LLM 선호 디스플레이 세리프로 금지. 강조는 동일 폰트의 이탤릭/볼드로, 무작위 세리프 단어 주입 금지.
- **이탤릭 디센더 클리어런스:** `y g j p q`가 있는 이탤릭 단어는 `leading-[1.1]` 최소 + `pb-1` 예약.
- 세리프가 정당화되더라도 연속 프로젝트에 같은 서체를 반복하지 않는다. 후보: PP Editorial New, GT Sectra Display, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, Canela, Domaine Display. 서체 선택 이유를 해당 브랜드에 맞춰 설명한다.

### 4.2 색상 보정
- 최대 1개 강조색. 채도 < 80%.
- **LILA 규칙:** "AI 보라/파랑 글로우" 미학 기본 비권장. 중립 베이스 + 고대비 단일 강조. 브랜드가 명시적 요청 시에만 보라 수용.
- **색상 일관성 잠금(필수):** 하나의 강조색이 전체 페이지에 사용. 페이지 중간에 강조색 변경 금지.
- **프리미엄 소비자 팔레트 금지:** 베이지+크림+황동+클레이+옥스블러드+에스프레소 팔레트 금지. 대안: 콜드 럭셔리(실버그레이+크롬), 포레스트(딥그린+본+앰버), 블랙앤탄(오프블랙+웜탄), 코발트+크림, 테라코타+슬레이트, 올리브+브릭+페이퍼, 순수 모노크롬+단일 채도 팝.
- 관성적으로 반복되는 구체적 색상 예시는 배경 `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb`; 강조 `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621`; 글자 `#1a1714`, `#1a1814`, `#1b1814`다. 브랜드 지정이 없으면 기본 선택으로 쓰지 않고, 이전 프리미엄 소비재 프로젝트와 같은 팔레트도 반복하지 않는다.
- 브랜드가 보라색이나 따뜻한 공예 팔레트를 명시한다면 사용해도 된다. 이 경우 브랜드 색을 존중하며 절제된 그라데이션과 일관된 중립색을 사용한다. 프로젝트 내에서 따뜻한 회색과 차가운 회색을 임의로 섞지 않는다.

### 4.3 레이아웃 다양화
- `DESIGN_VARIANCE > 4`일 때 중앙 정렬 히어로 회피.
- 메시지 자체가 디자인인 에디토리얼 선언문이나 출시 발표에서는 중앙 히어로를 허용한다. 그 외에는 분할 화면, 좌측 문안과 우측 자산, 비대칭 여백, 스크롤 고정 구조를 검토한다.
- 상승이 실제 계층을 전달할 때만 카드 사용.
- 그림자를 사용한다면 배경색에 맞춰 색조를 섞는다. 밝은 배경에 순수 검정 그림자를 쓰지 않는다. `VISUAL_DENSITY > 7`이면 제네릭 카드 대신 여백과 1px 구분선으로 데이터를 나눈다.
- **형태 일관성 잠금:** 하나의 코너 반경 시스템 선택 및 고수.
- **히어로 스택 규율 (최대 4개 텍스트 요소):** 아이브로우(또는 브랜드 스트립) + 헤드라인(최대 2줄) + 서브텍스트(최대 20단어, 최대 4줄) + CTA(기본 1개 + 최대 보조 1개). CTA 아래 작은 태그라인, 신뢰 마이크로 스트립, 기능 글머리 목록 히어로 내 금지.
- **첫 화면 맞춤:** CTA까지 스크롤 없이 보여야 한다. 이미지가 크고 헤드라인이 6단어를 넘으면 `text-7xl`/`text-8xl`부터 시작하지 않는다. 보통 `text-4xl md:text-5xl lg:text-6xl`, 3-5단어 헤드라인에만 더 큰 글꼴을 쓴다. 데스크톱 히어로 상단 패딩은 최대 `pt-24`.
- **내비게이션 높이:** 최대 80px 데스크톱, 기본 64-72px.
- 데스크톱 내비게이션은 한 줄이어야 한다. 1024px에서 넘치면 항목을 줄이거나 보조 항목을 메뉴로 옮긴다.
- **아이브로우 절제:** 3섹션당 최대 1개 아이브로우. 기계적 사전 점검: `uppercase tracking` 인스턴스 수 ≤ ceil(sectionCount/3).
- **분할 헤더 금지:** "왼쪽 큰 헤드라인 + 오른쪽 작은 설명 문단" 패턴 기본 금지. 수직 스택 선호.
- **지그재그 교대 제한:** 이미지+텍스트 분할 레이아웃 최대 연속 2섹션.
- **섹션 레이아웃 반복 금지:** 동일 레이아웃 패밀리는 페이지당 최대 1회.
- **벤토 셀 수 규칙:** 정확히 콘텐츠 수만큼 셀. 빈 셀 금지.
- **벤토 배경 다양성:** 최소 2-3개 셀이 실제 시각적 변이(이미지, 그라데이션, 패턴).
- 벤토는 타일 크기와 섹션 리듬도 달라야 한다. 한 방향의 이미지+텍스트 행을 여섯 개 쌓지 않는다. 모든 다열 레이아웃은 같은 컴포넌트 안에 768px 미만의 단일 열 동작을 명시한다.

### 4.4 카드와 물성

카드는 실제 계층을 드러낼 때만 사용한다. 대신 여백, 상단 테두리, 행 사이 구분선을 쓸 수 있다. 하나의 모서리 반경 체계를 고수한다. 버튼은 필, 카드는 16px, 입력란은 8px처럼 역할별로 다르게 정할 수 있지만 그 규칙을 문서화하고 모든 섹션에서 지킨다.

### 4.5 인터랙티브 상태
- 로딩: 최종 레이아웃 형태와 일치하는 스켈레톤 로더. 일반 원형 스피너 회피.
- `:active`에서 `-translate-y-[1px]` 또는 `scale-[0.98]`.
- **버튼 대비 체크(필수):** 모든 CTA 텍스트가 배경 대비 읽을 수 있어야 함(WCAG AA 4.5:1).
- **CTA 버튼 줄바꿈 금지:** 버튼 텍스트는 데스크톱에서 한 줄에 맞아야 함.
- **중복 CTA 의도 금지:** 동일 의도의 두 CTA 금지.
- `Get in touch`/`Contact us`/`Let's talk`는 모두 연락 목적이다. `Try free`/`Get started`는 가입 목적이다. `View work`/`Browse projects`는 작품 보기 목적이다. 목적당 한 문구를 골라 내비게이션, 히어로, 푸터에서 일치시킨다.
- **폼 대비 체크:** 입력란, 플레이스홀더, 레이블, 포커스 링이 섹션 배경에서 WCAG AA 대비를 충족해야 한다.
- 폼은 레이블을 입력란 위에, 오류를 아래에 둔다. 설명문은 필요에 따라 넣되 마크업에서 접근 가능하게 한다. 플레이스홀더를 레이블 대신 쓰지 않는다. 입력 블록 간격 기본값은 `gap-2`.
- **상태 완성:** 빈 상태, 로딩 상태, 오류 상태와 키보드 포커스 상태를 해당 인터랙션에 제공한다.

### 4.6 폼과 데이터

레이블은 입력란 위, 오류는 아래에 둔다. 설명문은 선택 사항이지만 필요할 때 접근 가능한 마크업으로 제공한다. 플레이스홀더가 레이블을 대체해서는 안 된다.

### 4.7 배치의 엄격한 규칙

첫 화면 히어로, 한 줄 내비게이션, 벤토의 정확한 셀 수, 섹션 레이아웃 반복 제한, 아이브로우 개수, 768px 미만 축소, CTA 목적 통일은 모두 출고 기준이다. 하나라도 실패하면 디자인을 수정한다.

### 4.8 이미지 & 시각적 자산 전략
우선순위: 1) 이미지 생성 도구 우선, 2) 실제 웹 이미지(picsum.photos), 3) 최후 수단으로 사용자에게 명확한 플레이스홀더 슬롯 + 필요한 이미지 목록 알리기.

이미지 생성 도구가 있다면 섹션별 목적과 종횡비에 맞춰 히어로 사진, 제품 사진, 텍스처, 분위기 이미지를 생성한다. 생성 도구가 없다면 실제 브랜드 자산이나 허용된 스톡 이미지, `https://picsum.photos/seed/{설명하는-시드}/{너비}/{높이}`를 사용한다. 둘 다 불가하면 `<!-- TODO: hero product photo, 1600x1200 -->`처럼 슬롯을 표시하고 필요한 이미지 목록을 알린다. 절제된 디자인에도 히어로와 보조 섹션 등에 2-3개의 실제 이미지가 필요하다.

div 기반 가짜 스크린샷 금지. 로고 월은 실제 SVG 로고 사용(Simple Icons), 일반 텍스트 워드마크 금지. SVG 아이콘 직접 그리기 강력 비권장.

이미지 위에 내용 없는 필이나 라벨을 올리지 않는다. 로고 월은 히어로 안이 아니라 아래에 둔다. 실존 브랜드 로고를 쓸 때 실제 로고 자산을 확인한다.

로고 출처는 Simple Icons 또는 기술 스택에 적합한 devicon을 사용한다. 가상의 브랜드라면 텍스트 워드마크만 나열하지 말고 단순한 SVG 마크도 만든다. 밝은 모드와 어두운 모드 모두에서 보이게 한다. 로고 아래에 업종 설명을 붙이지 않는다. 실제 제품을 보여줄 때는 실제 스크린샷, 생성 이미지, 작동하는 축소 UI를 사용한다. 장식용 `<div>` 목록으로 가짜 제품 화면을 만들지 않는다. 장식 SVG는 명시적 요청이나 품질을 보장할 수 있는 단순 기하학 마크에만 사용한다.

### 4.9 콘텐츠 밀도
- 섹션당 기본 콘텐츠 형태: 짧은 헤드라인(≤ 8단어) + 짧은 서브문단(≤ 25단어) + 하나의 시각적 자산 또는 CTA.
- 긴 목록(> 5개 항목)은 다른 UI 컴포넌트 사용: 2열 분할 그리드, 카드 그리드, 탭/아코디언, 수평 스크롤 스냅 필, 캐러셀, 마키.
- 20행 출판물 표, 30행 수상 목록, 거대한 가격 행렬은 상위 3-5개와 전체 목록 링크로 줄이거나 별도 페이지로 옮긴다. 제품 사양 10행 모두에 `border-b`를 반복하지 않는다. 사양별 2열 카드, 가로 스냅 필, 2-3개 묶음, 대표 사양과 나머지 펼치기 중 콘텐츠에 맞는 형태를 선택한다.
- **카피 자체 감사(필수):** 모든 가시 문자열 재검토. 문법적으로 깨졌거나, 가리키는 대상이 불분명하거나, AI 환각처럼 들리는 문자열 플래그 및 재작성.
- **가짜 정밀 숫자 플래그:** `92%`, `4.1×` 등은 실제 데이터나 명시적 모의 레이블이 없으면 금지.
- 페이지의 카피 어조는 하나로 유지한다. 기술적 고정폭 숫자, 에디토리얼 산문, 광고 문구를 브랜드 이유 없이 한 구성에 섞지 않는다.

### 4.10 인용문 & 추천사
- 인용 본문 최대 3줄. 속성: 이름 + 역할 + (선택) 회사. 실제 타이포그래픽 따옴표 사용.
- 긴 원문은 의미를 유지하며 발췌한다. 이름만 적거나 장식용 긴 대시로 출처를 시작하지 않는다.

### 4.11 페이지 테마 잠금
페이지는 하나의 테마. 섹션이 반전되지 않음. 다크모드 페이지 중간에 라이트 섹션 끼워넣기 금지.

예외는 사용자가 의도적인 색 블록 이야기나 스크롤 테마 전환을 요청한 경우 한 번만 허용한다. 같은 테마 안에서 밝기가 가까운 배경색은 허용한다. 테마는 페이지 루트에서 한 번 설정한다.

## 5. 맥락 인식 선제성
글래스모피즘, 마그네틱 마이크로 물리, 지속적 마이크로 인터랙션은 디자인 읽기가 요구할 때만 사용. 자동 발동 금지.

글래스모피즘은 프리미엄 소비자, Apple 인접 브랜드, 미디어 오버레이에 맞고 공공 서비스나 절제된 B2B에는 맞지 않을 수 있다. 사용할 때는 흐림뿐 아니라 1px 안쪽 테두리와 약한 내부 그림자로 물성을 만들고 불투명 대안을 둔다. 마그네틱 상호작용은 `MOTION_INTENSITY > 5`이면서 프리미엄·장난기·에이전시 맥락일 때 Motion 값으로 구현한다. 펄스, 타이프라이터, 떠다님, 쉬머, 캐러셀도 해당 섹션이 실제로 움직임에서 이득을 볼 때만 사용한다. 스프링의 예시는 `type: "spring", stiffness: 100, damping: 20`이다.

**모션은 동기가 있어야 함(필수):** 모든 애니메이션은 계층/스토리텔링/피드백/상태 전환 중 하나로 정당화 가능해야 함.

**마키 최대 페이지당 1개.** `window.addEventListener('scroll')` 금지.

`MOTION_INTENSITY > 4`라고 선언했다면 실제로 히어로 진입, 핵심 섹션 등장, CTA 피드백 등에 모션이 보여야 한다. 구현 범위에서 안정적인 모션을 만들 수 없다면 다이얼을 3으로 낮춘다. 중단되는 ScrollTrigger, 불연속적인 진입 효과, 정리 함수 없는 모션을 남기지 않는다.

스크롤 상호작용은 Motion `useScroll()`, GSAP ScrollTrigger, IntersectionObserver, CSS 스크롤 기반 애니메이션 중 맞는 방법을 선택한다. GSAP 고정 스택과 가로 이동은 `start: "top top"`, `pin: true`, 올바른 `scrub` 및 정리 함수를 사용한다. 가벼운 스크롤 등장 효과에는 IntersectionObserver나 Motion을 우선한다. 모션 라이브러리 선택은 필요한 효과와 기존 프로젝트 의존성에 맞춘다.

고정 스택은 마지막 카드를 제외한 각 카드를 뷰포트 맨 위에 고정한다. 다음 카드가 들어올 때 이전 카드의 `scale`과 `opacity`가 변하도록 다음 카드를 트리거로 쓴다. 가로 이동은 래퍼를 고정하고 내부 트랙만 움직인다. 이동 거리는 `track.scrollWidth - window.innerWidth`, 종료 지점은 `` `+=${distance}` ``, `scrub: 1`, `invalidateOnRefresh: true`로 둔다. 단순 등장 순서에는 Motion의 `whileInView`, `viewport={{ once: true, amount: 0.3 }}`를 사용한다. 세 패턴 모두 모션 감소를 존중하고 GSAP 컨텍스트는 `ctx.revert()`로 정리한다.

`window.scrollY`를 React 상태로 계속 계산하거나 `requestAnimationFrame` 루프에서 상태를 바꾸지 않는다. 보이는 순서 변경과 모달 확장에는 Motion `layout`/`layoutId`를 쓰되 정적 콘텐츠에 무분별하게 붙이지 않는다. 순차 등장은 `staggerChildren` 또는 CSS `animation-delay`를 사용한다. Motion의 부모·자식 variant는 같은 Client Component 트리에 있어야 한다.

### 5.A 고정 카드 스택 구현 골격

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div key={i} className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center">
          {card}
        </div>
      ))}
    </div>
  );
}
```

### 5.B 가로 이동 구현 골격

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",
          end: () => `+=${distance}`,
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">{children}</div>
    </section>
  );
}
```

### 5.C 가벼운 순차 등장 구현 골격

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

## 6. 성능 & 접근성 가드레일
- `transform`과 `opacity`로만 애니메이션. `prefers-reduced-motion` 필수.
- `top`, `left`, `width`, `height`는 애니메이션하지 않는다. `will-change: transform`은 실제로 움직일 요소에만 준다. 모션 강도 3 초과라면 `useReducedMotion()`이나 CSS 미디어 쿼리로 무한 반복, 시차, 스크롤 고정, 마그네틱 물리를 정적/즉시 상태로 바꾼다.
- 다크모드: 소비자 대상 페이지는 기본적으로 양쪽 모드.
- 그레인/노이즈 필터는 고정 `pointer-events-none` 의사 요소에만.
- 목표 Core Web Vitals: LCP < 2.5초, INP < 200ms, CLS < 0.1. 긴 DOM, 불필요한 합성 레이어, 무분별한 `z-index` 증가를 피한다.
- 히어로 이미지는 `next/image priority` 또는 preload를 적용하고 이미지·폰트·임베드 공간을 예약한다. 메인 스레드의 무거운 작업을 줄이고 첫 화면 밖의 Motion·Three.js는 지연 로딩한다. 완료 전 Lighthouse를 실행한다.
- `z-index`는 내비게이션, 모달, 오버레이, 그레인처럼 체계적인 레이어에만 쓰고 프로젝트 상수에 계층을 문서화한다.
- `useEffect`로 등록한 타이머, 관찰자, 애니메이션, 이벤트 리스너는 정리 함수에서 해제한다.

## 7. 다이얼 정의 (기술 참조)
- VARIANCE 1-3: 대칭 그리드. 4-7: 오프셋, 겹침. 8-10: 메이슨리, 분수 그리드, 거대 빈 영역. 모바일 오버라이드: `< 768px`에서 단일 열.
- 4-7의 예시는 `margin-top: -2rem` 겹침, 서로 다른 이미지 종횡비, 좌측 정렬 헤더와 중앙 정렬 데이터다. 8-10의 예시는 `grid-template-columns: 2fr 1fr 1fr`, `padding-left: 20vw`다. 768px 미만에서는 `w-full px-4 py-8` 단일 열로 정리한다.
- MOTION 1-3: 정적. 4-7: 유체 CSS. 8-10: 고급 안무.
- 1-3은 `:hover`/`:active`만 쓴다. 4-7은 주로 `transform`/`opacity` 전환과 시간차 등장을 사용한다. 8-10은 스크롤 기반 연출과 시차를 허용하되 금지된 직접 스크롤 리스너는 사용하지 않는다.
- DENSITY 1-3: 아트 갤러리. 4-7: 일상 앱. 8-10: 칵핏, 고정폭 숫자 필수.
- 1-3은 대략 `py-32`-`py-48`, 4-7은 `py-16`-`py-24`, 8-10은 촘촘한 간격과 1px 데이터 구분선을 쓴다.

## 8. 다크모드 프로토콜
기본적으로 듀얼 모드. 브랜드가 고집하지 않는 한 `prefers-color-scheme` 존중. 순수 `#000000`과 순수 `#ffffff` 금지.

프로젝트의 기존 토큰 체계 하나를 선택해 라이트/다크를 함께 정의하고 두 모드를 모두 확인한다. 다크 모드 때문에 섹션마다 테마를 반전하지 않는다.

Tailwind 중심 프로젝트라면 색상마다 `dark:` 변형을 함께 두고, 테마를 제공하는 컴포넌트 라이브러리라면 `--surface`, `--surface-elevated`, `--text-primary`, `--accent` 같은 의미 토큰을 한 곳에서 교체한다. 브랜드 색의 인지성을 보존하고 본문은 WCAG AA 이상, 히어로는 AAA를 목표로 한다. 한 모드에서 CTA가 두드러지면 다른 모드에서도 두드러져야 한다. 필요하면 수동 전환을 제공한다. 두 모드를 실제로 열어 확인한다.

## 9. AI 표시 (금지 패턴)
생산 테스트에서 나온 실제 LLM 생성 랜딩페이지 테스트 패턴을 하드 금지로 취급.

주요 금지: 네온/외부 글로우, 순수 검정, 과채도 강조, 과도한 그라데이션 텍스트, Inter 기본값, 3열 동등 기능 카드, 제네릭 이름, AI 카피 클리셰, 가짜 정밀 숫자, div 기반 가짜 스크린샷, 히어로의 버전 라벨(V0.6, BETA), 섹션 번호 아이브로우(00/INDEX), 중간점(·) 남용, 장식 상태 점, **EM-DASH(`—`) 완전 금지**, 장식 텍스트 스트립, 스크롤 큐, 사진 크레딧 캡션, 버전 푸터, 로케일/날씨 스트립.

**EM-DASH 금지(가장 위반되는 표시):** Em-dash(`—`) 완전 금지. 헤드라인, 아이브로우, 필, 본문, 인용문, 속성, 캡션, 버튼 텍스트, 대체 텍스트 모든 곳에서. 일반 하이픈(`-`)만 허용.

### 9.A 시각 스타일과 타이포그래피

- 기본값으로 네온 외부 광선, 순수 검정, 과채도 강조색, 큰 제목의 과도한 그라데이션, 사용자 지정 마우스 커서를 쓰지 않는다.
- 큰 글꼴만으로 소리치는 H1 대신 굵기와 색상으로 위계를 만든다. 세리프는 앞의 정당화 조건에 따르고, 한 헤드라인에 다른 계열의 세리프 단어를 장식처럼 끼우지 않는다.
- 세 개의 똑같은 기능 카드를 한 줄에 놓지 않는다. 분할 레이아웃, 비대칭 그리드, 스크롤 고정, 가로 이동 등 콘텐츠에 맞는 구성을 선택한다.
- `John Doe`, `Sarah Chan`, `Jack Su` 같은 이름, 제네릭 아바타, `Acme`, `Nexus`, `SmartFlow`, `Cloudly` 같은 브랜드 이름을 기본값으로 쓰지 않는다. 지역과 맥락에 맞는 실감나는 가상 데이터를 사용한다.
- `Elevate`, `Seamless`, `Unleash`, `Next-Gen`, `Revolutionize` 같은 빈 동사 대신 실제 행동을 설명한다. `99.99%`처럼 지나치게 완벽한 수치나 근거 없는 유기적 수치를 모두 피한다.
- shadcn/ui는 프로젝트의 반경, 색상, 그림자, 서체에 맞춰 조정한다. 기본 테마 그대로 납품하지 않는다.

### 9.B 히어로, 번호, 구분자

- `V0.6`, `BETA`, `INVITE-ONLY`, `EARLY ACCESS`는 실제 출시 상태가 브리프의 중심일 때만 히어로에 쓴다. `Brand · No. 01` 같은 미세 메타 라벨도 쓰지 않는다.
- `00 / INDEX`, `001 · Capabilities`, `01 / 4` 등 섹션 번호를 아이브로우나 이미지 페이지 표기로 장식하지 않는다. `2018-2026` 같은 범위 라벨도 단순 섹션명으로 바꾼다.
- 가운데 점(`·`)은 메타데이터 한 줄에 최대 하나만 쓴다. 기본 구분자처럼 반복하지 않는다. 색 점은 실제 서버 상태나 실시간 가용성처럼 의미가 있을 때만 제한적으로 사용한다.
- `<br>`로 강제 분할한 뒤 한 단어를 이탤릭으로 만드는 제목, 회전한 세로 글씨, 장식용 십자선/격자선은 기본 패턴으로 쓰지 않는다. 브리프가 실험적이고 구도상 이유가 있을 때만 검토한다.

### 9.C 제품 미리보기와 마케팅 문구

- 히어로에 `<div>`로 만든 가짜 작업 목록, 터미널, 대시보드를 놓지 않는다. 실제 스크린샷, 생성 이미지, 작동하는 축소 컴포넌트를 사용한다. 가짜 화면에 버전이나 동기화 시간을 덧붙이지 않는다.
- `Quietly in use at`, `Quietly trusted by` 대신 자연스러운 고객 표제를 쓰거나 표제를 생략한다. `From the field`, `Field notes`, `On our desks`처럼 공예가 흉내를 내는 시적 섹션명도 기본값으로 쓰지 않는다.
- `Stage 1`, `Step 2`, `Phase 03` 대신 `설치`, `설정`, `배포`처럼 실제 단계를 이름으로 쓴다. 아이브로우 아래에 의미 없는 설명 문장을 추가하지 않는다.
- 실제 장소와 시간대가 중요하지 않다면 도시명·현지 시각·날씨를 분위기 장식으로 쓰지 않는다. 푸터의 실제 연락처 주소는 허용한다.

### 9.D 이미지 장식, 목록, 스크롤 신호

- 사진 위에 `Plate · Brand` 같은 필을 겹치지 않는다. 필요한 캡션은 사진 아래에 기능적으로 적는다. 실제 사진가를 정당하게 표기하는 경우 외에는 `Field study no. 12` 같은 가짜 사진 크레딧을 만들지 않는다.
- 마케팅 페이지 푸터에 `v1.4.2`, `Build 0048`, `last sync 4s ago` 같은 버전 표기를 넣지 않는다. 실제 한정 수량 데이터가 없다면 `Reservation 412 of 800` 같은 재고 카운터도 만들지 않는다.
- 히어로 하단에 `BRAND. MOTION. SPATIAL.` 같은 장식 텍스트 줄을 넣지 않는다. 실제 탐색 링크나 상태 정보가 있을 때만 하단 스트립을 둔다.
- 섹션 제목 오른쪽 위에 정렬 근거 없는 작은 설명문을 띄우지 않는다. 필요하면 제목 아래에 두거나 내용상 정당한 2열 구성을 만든다.
- 긴 목록의 모든 행에 `border-t`와 `border-b`를 함께 두지 않는다. 비교용 채워진 트랙형 점수 막대 대신 숫자와 작은 기호 또는 배경 트랙 없는 짧은 막대를 검토한다.
- `Scroll`, `↓ scroll`, `Scroll to explore` 같은 스크롤 안내와 장식용 마우스 아이콘은 넣지 않는다.

### 9.E 대시 문자 검사

사용자에게 보이는 페이지 문구에는 `—`와 구분자로 쓰인 `–`를 모두 금지한다. 문장은 마침표, 쉼표, 괄호, 콜론으로 다시 쓰고 날짜·숫자 범위에는 일반 하이픈(`-`)을 쓴다. 이 금지는 스킬 지침 자체의 문장부호가 아니라 **생성된 페이지에 표시되는 문자열**에 적용된다.

## 10. 레퍼런스 어휘 (패턴명)
히어로: 비대칭 분할, 에디토리얼 선언문, 키네틱 타이포그래피, 몰입형 미디어. 내비게이션: 메가 메뉴, 플로팅 내비게이션, 단순 헤더. 레이아웃: 벤토, 지그재그, 고정 스택, 가로 이동. 미디어: 갤러리, 콜라주, 제품 데모. 효과: 스크롤 등장, 자기식 버튼, 시차 이동. 패턴을 선택할 때 이름만 빌리지 말고 콘텐츠와 인터랙션 요구를 확인한다.

이 목록은 구현 라이브러리가 아니라 패턴을 설명할 공통 어휘다. 실제 블록 구현은 12절 계약을 따른다.

| 범주 | 원본 패턴과 의미 |
|---|---|
| 히어로 | **Asymmetric Split Hero**(한쪽 문안, 한쪽 자산), **Editorial Manifesto Hero**(포스터 같은 큰 글씨), **Video / Media Mask Hero**(영상 위 텍스트 마스크), **Kinetic-Type Hero**(움직이는 타이포그래피), **Curtain-Reveal Hero**(스크롤 커튼), **Scroll-Pinned Hero**(고정 히어로) |
| 탐색 | **Mac OS Dock Magnification**(호버 확대), **Magnetic Button**(커서 방향으로 당김), **Gooey Menu**(점성 메뉴), **Dynamic Island**(변형되는 상태 필), **Contextual Radial Menu**(클릭 지점 원형 메뉴), **Floating Speed Dial**(펼쳐지는 빠른 동작), **Mega Menu Reveal**(전면 드롭다운) |
| 레이아웃 | **Bento Grid**(비대칭 타일), **Masonry Layout**(높이 다른 격자), **Chroma Grid**(은은한 색 변화 테두리), **Split-Screen Scroll**(반대 방향으로 움직이는 양쪽 화면), **Sticky-Stack Sections**(고정되어 쌓이는 섹션) |
| 카드 | **Parallax Tilt Card**(포인터 기반 3D 기울기), **Spotlight Border Card**(포인터 주변 밝은 테두리), **Glassmorphism Panel**(반투명 굴절), **Holographic Foil Card**(호버 무지갯빛), **Tinder Swipe Stack**(밀어내는 카드 더미), **Morphing Modal**(버튼에서 확장되는 대화상자) |
| 스크롤 | **Sticky Scroll Stack**(겹쳐지는 카드), **Horizontal Scroll Hijack**(세로 스크롤을 가로 이동으로 전환), **Locomotive / Sequence Scroll**(스크롤 연동 영상/3D 시퀀스), **Zoom Parallax**(중앙 이미지 확대), **Scroll Progress Path**(스크롤 따라 그려지는 SVG), **Liquid Swipe Transition**(점성 화면 전환) |
| 미디어 | **Dome Gallery**(3D 파노라마), **Coverflow Carousel**(기울어진 3D 캐러셀), **Drag-to-Pan Grid**(드래그 캔버스), **Accordion Image Slider**(호버로 확장되는 이미지), **Hover Image Trail**(커서 이미지 궤적), **Glitch Effect Image**(RGB 채널 이동) |
| 텍스트 | **Kinetic Marquee**(움직이는 글자 띠), **Text Mask Reveal**(영상 창 역할을 하는 큰 글자), **Text Scramble Effect**(글자 해독 효과), **Circular Text Path**(원형 글자), **Gradient Stroke Animation**(움직이는 윤곽선), **Kinetic Typography Grid**(커서를 피하는 글자) |
| 미세 효과 | **Particle Explosion Button**(성공 시 입자), **Liquid Pull-to-Refresh**(물방울 새로고침), **Skeleton Shimmer**(스켈레톤 반사광), **Directional Hover-Aware Button**(커서 진입 방향의 채움), **Ripple Click Effect**(클릭 파문), **Animated SVG Line Drawing**(선 그리기), **Mesh Gradient Background**(유기적 그라데이션), **Lens Blur Depth**(전경 집중을 위한 배경 흐림) |

UI·상태 변화 모션은 Motion, 페이지 규모의 스크롤 연출과 고정/스크럽은 GSAP + ScrollTrigger, 3D 장면은 Three.js/WebGL을 검토한다. GSAP·Three.js와 Motion이 같은 컴포넌트에서 같은 프레임을 제어하게 만들지 않는다. 각 외부 엔진은 클라이언트 리프에 격리하고 해제한다.

## 11. 리디자인 프로토콜
그린필드 vs 리디자인-보존 vs 리디자인-전면개편 감지. 감사 우선: 브랜드 토큰, 정보 아키텍처, 콘텐츠 블록, 보존할 패턴, 제거할 패턴, 기존 사이트 다이얼 판독.

그린필드는 사이트가 없거나 전면 개편이 승인된 경우다. 보존형 리디자인은 브랜드를 유지하며 점진적으로 현대화한다. 전면 리디자인은 시각 언어를 새로 만들되 기존 콘텐츠와 정보 구조를 보존한다. 모호하면 `기존 브랜드를 유지하면서 개선할까요, 시각적으로 새로 시작할까요?`라고 한 번 묻는다.

작업 전 현재 사이트의 주·강조 색, 서체, 로고 사용법, 반경; 페이지 구조와 주요 전환 경로; 작동하는 콘텐츠와 불필요한 콘텐츠; 유지할 대표 상호작용과 카피 어조; 폐기할 망가진 레이아웃·죽은 링크·제네릭 이미지·성능 문제를 기록한다. 기존 사이트의 세 다이얼 값도 읽는다. SEO 순위 페이지, 메타 제목, 구조화 데이터, OG 카드 역시 기준선으로 기록한다. SEO 이전은 리디자인의 주요 위험이다.

현대화 레버(우선순위): 1) 타이포그래피 새로고침, 2) 간격/리듬, 3) 색상 재보정, 4) 모션 레이어, 5) 히어로/주요 섹션 재구성, 6) 전체 블록 교체.

절대 조용히 변경하지 말 것: URL 구조, 기본 내비 라벨, 폼 필드명/순서, 브랜드 로고/워드마크, 법적/동의/쿠키 카피.

기존 분석 이벤트와 섹션 ID도 보존한다. 정보 구조와 콘텐츠가 건전하면 타이포그래피, 간격, 색상, 모션 중심으로 진화시킨다. 구조 자체가 무너지거나 모바일이 깨졌다면 콘텐츠를 보존하면서 전면 개편한다. 브랜드 변경은 별도 그린필드 작업으로 판단한다.

정보 구조, URL 슬러그, 앵커, 주요 내비게이션은 요청 없이는 바꾸지 않는다. 색상 교정 전 브랜드 색을 먼저 추출한다. 보라색 브랜드에는 앞의 LILA 예외를 적용한다. 카피 재작성 요청이 없으면 어조를 지키고, 포커스·대체 텍스트·키보드 조작·대비 등 기존 접근성을 후퇴시키지 않는다. 분석 이벤트가 걸린 버튼·폼 필드·섹션 ID도 유지한다.

## 12. 블록 라이브러리 계약

재사용 블록을 추가한다면 `blocks/<category>/<name>.md`에 하나씩 둔다. 프론트매터에 `name`, `category`, 세 다이얼의 호환 범위, `when_to_use`, `not_for`, `stack`을 적는다. 본문에는 시각적 스케치, props API, 작동하는 코드 스케치, 768px 미만의 모바일 동작, 모션 강도별 변형과 모션 감소 대안, 다크 모드 토큰, 안티 패턴, 실제 참고 링크를 포함한다. 블록은 단독으로 작동하고 최종 사전 점검을 통과해야 한다. 특정 디자인 시스템 전용 블록은 파일 이름에 해당 시스템을 표시한다.

원본 블록 분류는 `hero/`, `feature/`, `social-proof/`, `pricing/`, `cta/`, `footer/`, `navigation/`, `portfolio/`, `transition/`이다. 예를 들어 `hero/asymmetric-split.md`, `feature/bento-grid.md`, `feature/sticky-scroll-stack.md`처럼 둔다. 특정 시스템 전용이면 `feature/bento-grid--material.md`처럼 이름에 시스템을 붙인다.

```yaml
---
name: asymmetric-split-hero
category: hero
dial_compatibility:
  variance: [6, 10]
  motion: [3, 10]
  density: [2, 5]
when_to_use: "강한 시각 자산 하나와 핵심 메시지 하나가 있는 랜딩페이지. SaaS, 에이전시, 프리미엄 소비재에 적합."
not_for: "메시지 자체가 디자인인 에디토리얼 선언문 출시."
stack: ["react", "next", "tailwind", "motion"]
---
```

## 13. 적용 범위 밖

밀도 높은 대시보드와 관리 UI, 데이터 테이블, 다단계 폼, 코드 편집기, 네이티브 모바일, 실시간 공동 작업 UI는 이 스킬의 주요 대상이 아니다. 해당 부분에는 각 제품 및 플랫폼의 전용 디자인 시스템을 사용하고, 이 스킬은 마케팅 페이지나 소개 페이지에만 적용한다.

대시보드는 Fluent/Carbon/Atlassian/Polaris, 표는 TanStack Table/AG Grid, 편집기는 Monaco/CodeMirror, 네이티브 모바일은 Apple HIG/Material을 검토한다. 적용 범위 밖 요청이면 그 사실과 맞는 도구를 분명하게 설명한다.

## 14. 최종 사전 점검 (필수, 선택 아님)
모든 체크박스 실행. 하나라도 실패하면 출력 완료되지 않음.

- [ ] 브리프를 한 줄로 읽고 독자, 분위기, 시스템 또는 미학적 방향을 선언했는가?
- [ ] 세 다이얼 값을 브리프에 맞춰 명시했는가?
- [ ] 적합한 공식 디자인 시스템을 사용하거나 미학적 영감임을 정직하게 표시했는가? 시스템은 하나인가?
- [ ] 리디자인이라면 모드를 감지하고 기존 브랜드, 콘텐츠, SEO, 분석, 접근성을 감사했는가?
- [ ] 사용자에게 보이는 문자열에 `—`나 구분자로 쓰인 `–`가 없는가?
- [ ] 페이지 테마, 강조색, 코너 반경이 처음부터 끝까지 일관되는가?
- [ ] 모든 CTA의 텍스트가 배경과 WCAG AA 대비를 만족하고 데스크톱에서 한 줄인가?
- [ ] 폼 입력란, 플레이스홀더, 레이블, 도움말, 오류, 포커스 링의 대비가 적절한가?
- [ ] 세리프가 브랜드상 정당화되며 `Fraunces`/`Instrument_Serif`를 관성으로 사용하지 않았는가?
- [ ] 프리미엄 소비재에서 AI식 베이지·황동·옥스블러드·에스프레소 팔레트를 관성으로 사용하지 않았는가?
- [ ] `y g j p q`가 있는 이탤릭 제목의 디센더 공간을 확보했는가?
- [ ] 히어로 제목이 최대 두 줄, 보조 문구가 20단어·네 줄 이하이며 CTA가 첫 화면에 보이는가?
- [ ] 이미지 크기와 글꼴 크기를 함께 조정하고 히어로 데스크톱 상단 패딩이 `pt-24` 이하인가?
- [ ] 히어로에 아이브로우 또는 브랜드 스트립, 제목, 설명, CTA까지만 있고 신뢰 로고는 아래 섹션에 있는가?
- [ ] 아이브로우 수가 `ceil(sectionCount / 3)` 이하인가? `uppercase tracking` 형태를 실제로 셌는가?
- [ ] 제목 왼쪽·설명 오른쪽의 장식적 분할 헤더가 없는가?
- [ ] 이미지+문안 지그재그가 세 섹션 연속 반복되지 않는가?
- [ ] 연락·가입·작품 보기 같은 CTA 목적마다 문구가 하나인가?
- [ ] 로고 월에 실제 로고만 있고 업종 라벨이 없는가? 히어로 아래에 있는가?
- [ ] 벤토에 콘텐츠 수만큼의 셀만 있고 빈 셀이 없는가? 최소 2-3셀에 이미지·패턴·색조 변이가 있는가?
- [ ] 모든 표시 문자열을 다시 읽어 문법 오류, 불명확한 지시 대상, AI식 문장을 고쳤는가?
- [ ] 모든 모션의 목적을 한 문장으로 설명할 수 있는가? 마키는 페이지당 하나 이하인가?
- [ ] 내비게이션이 데스크톱에서 한 줄이고 높이 80px 이하인가?
- [ ] 각 섹션의 레이아웃 계열이 반복되지 않는가? 여덟 섹션이면 최소 네 계열인가?
- [ ] 다섯 항목 초과 목록에 적절한 다른 UI를 사용했는가?
- [ ] 실제 또는 생성 이미지를 사용했는가? 가짜 `<div>` 스크린샷과 장식용 직접 제작 SVG를 피했는가?
- [ ] 이미지 위 필·라벨, 장식용 사진 크레딧, 마케팅용 버전 푸터가 없는가?
- [ ] 아이브로우 아래 미세 메타 문장, 히어로 아래 장식 문구, 제목 오른쪽 위 떠 있는 설명이 없는가?
- [ ] 비교에 배경 트랙이 채워진 점수 막대를 쓰지 않았는가?
- [ ] 장소·도시·시간·날씨 스트립은 실제 브리프 근거가 있을 때만 썼는가?
- [ ] 스크롤 안내, 히어로 버전 라벨, 섹션 번호 아이브로우, 장식 상태 점이 없는가?
- [ ] 긴 표의 모든 행에 `border-t`와 `border-b`를 함께 반복하지 않았는가?
- [ ] 섹션 내용이 짧고 가짜 정밀 수치가 없으며 추천사 본문이 세 줄 이하인가?
- [ ] `MOTION_INTENSITY > 4`라면 실제 모션이 동작하는가?
- [ ] GSAP 고정 스택/가로 이동은 `start: "top top"`, `pin: true`, 적절한 `scrub`를 따르는가?
- [ ] `window.addEventListener('scroll')`와 React 상태 기반 스크롤 위치 추적이 없는가?
- [ ] 강도 3 초과 모션에 `prefers-reduced-motion` 대안이 있는가?
- [ ] 라이트/다크 토큰이 모두 정의되고 두 모드에서 확인되었는가?
- [ ] 다열 섹션마다 768px 미만 단일 열 동작이 명시되었는가?
- [ ] `h-screen` 대신 `min-h-[100dvh]`를 사용했는가?
- [ ] `useEffect` 애니메이션·관찰자·리스너를 정리하는가?
- [ ] 빈 상태, 로딩 상태, 오류 상태가 필요한 곳에 있는가?
- [ ] 불필요한 카드를 여백으로 대체하고 아이콘을 승인된 한 계열에서 가져왔는가?
- [ ] Motion이 `'use client'` 리프에 격리되어 있는가?
- [ ] AI식 서체·색·카드·이름·카피를 제거했는가?
- [ ] LCP < 2.5초, INP < 200ms, CLS < 0.1을 달성할 설계이며 Lighthouse로 확인했는가?

하나라도 정직하게 체크할 수 없다면 수정한 뒤 전달한다.

## 부록: 공식 자료와 웹 근사

디자인 시스템 패키지와 사용법은 해당 프로젝트의 공식 문서를 확인한다: [Material Web](https://material-web.dev/), [Fluent UI](https://fluent2.microsoft.design/), [Carbon](https://carbondesignsystem.com/), [Polaris](https://shopify.dev/docs/api/app-home/web-components), [Atlassian](https://atlassian.design/), [Primer](https://primer.style/), [GOV.UK](https://design-system.service.gov.uk/), [USWDS](https://designsystem.digital.gov/), [Bootstrap](https://getbootstrap.com/docs/5.3/), [Tailwind](https://tailwindcss.com/docs), [Radix Themes](https://www.radix-ui.com/themes/docs), [shadcn/ui](https://ui.shadcn.com/docs).

### 부록 A. 디자인 시스템 설치 명령

프로젝트에서 실제로 사용할 시스템 하나만 설치한다. 기존 잠금 파일과 패키지 관리자를 먼저 확인한다.

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS / Primer Brand
npm install --save @primer/css
npm install @primer/react-brand

# GOV.UK Frontend / USWDS
npm install govuk-frontend
npm install uswds

# Atlassian Design System
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap
```

Shopify Polaris Web Components는 Shopify 앱에서만 사용한다. 앱의 HTML `<head>`에 다음 메타 태그와 스크립트를 넣는다.

```html
<meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
<script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

### 부록 B. 공식 구현 자료

패키지 사용법, 토큰, 구성 요소는 원본 저장소의 예제보다 해당 프로젝트 공식 문서를 우선 확인한다.

- Material Web: [소스](https://github.com/material-components/material-web), [테마](https://material-web.dev/theming/material-theming/), [Material 3 웹](https://m3.material.io/develop/web)
- Fluent UI: [시작](https://fluent2.microsoft.design/get-started/develop), [React 구성 요소](https://fluent2.microsoft.design/components/web/react/), [소스](https://github.com/microsoft/fluentui), [Web Components](https://learn.microsoft.com/en-us/fluent-ui/web-components/)
- Carbon: [디자인 시스템](https://carbondesignsystem.com/), [소스](https://github.com/carbon-design-system/carbon), [React 자습서](https://carbondesignsystem.com/developing/react-tutorial/overview/), [Web Components 자습서](https://carbondesignsystem.com/developing/web-components-tutorial/overview/)
- Shopify Polaris: [웹 구성 요소](https://shopify.dev/docs/api/app-home/web-components), [React 소스](https://github.com/Shopify/polaris-react), [React 구성 요소](https://polaris-react.shopify.com/components)
- Atlassian: [시작](https://atlassian.design/get-started/develop), [버튼](https://atlassian.design/components/button/examples), [Atlaskit 버튼 예시](https://atlaskit.atlassian.com/packages/design-system/button/example/disabled), [토큰](https://atlassian.design/tokens/design-tokens)
- Primer: [디자인 시스템](https://primer.style/), [CSS 소스](https://github.com/primer/css), [브랜드 소스](https://github.com/primer/brand)
- GOV.UK: [버튼](https://design-system.service.gov.uk/components/button/), [레이아웃](https://design-system.service.gov.uk/styles/layout/), [소스](https://github.com/alphagov/govuk-frontend)
- USWDS: [개발자 안내](https://designsystem.digital.gov/documentation/developers/), [버튼](https://designsystem.digital.gov/components/button/), [카드](https://designsystem.digital.gov/components/card/), [소스](https://github.com/uswds/uswds)
- Bootstrap: [그리드](https://getbootstrap.com/docs/5.3/layout/grid/), [카드](https://getbootstrap.com/docs/5.3/components/card/)
- Tailwind: [다크 모드](https://tailwindcss.com/docs/dark-mode), [v4 소개](https://tailwindcss.com/blog/tailwindcss-v4)
- Radix Themes: [Theme](https://www.radix-ui.com/themes/docs/components/theme), [Card](https://www.radix-ui.com/themes/docs/components/card), [소스](https://github.com/radix-ui/themes)
- shadcn/ui: [문서](https://ui.shadcn.com/docs), [카드](https://ui.shadcn.com/docs/components/card), [소스](https://github.com/shadcn-ui/ui)
- 웹 표준: [backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter), [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme), [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion), [CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout), [스크롤 기반 애니메이션](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations), [CSSWG 초안](https://drafts.csswg.org/scroll-animations-1/)
- Apple 재질: [HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials), [Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass), [도입 지침](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass), [SwiftUI Material](https://developer.apple.com/documentation/SwiftUI/Material)

### 부록 C. Apple Liquid Glass의 웹 근사

Apple Liquid Glass는 Apple 플랫폼의 공식 재질이며 일반 웹사이트용 공식 `liquid-glass.css` 패키지는 없다. 웹에서 `backdrop-filter`, 반투명 배경, 테두리, 하이라이트를 사용하면 **웹 글래스모피즘 근사**라고 명확히 표시한다. 흐림 효과가 없어도 대비를 확보하고 `prefers-reduced-transparency` 대안을 제공한다. [Apple 재질 지침](https://developer.apple.com/design/human-interface-guidelines/materials)과 [MDN `backdrop-filter`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter)를 참고한다.

아래 CSS는 공식 Apple 구현이 아니라 웹에서 재질을 근사하는 예시다.

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

`prefers-reduced-transparency` 지원은 브라우저마다 다르므로 직접 시험한다. 흐림 효과가 적용되지 않아도 읽을 수 있는 대비를 확보한다.
