# HTML 보고서 형식

아키텍처 리뷰는 OS 임시 디렉터리의 단일 자기완결 HTML 파일로 렌더링. Tailwind와 Mermaid 모두 CDN에서 제공. Mermaid는 그래프 형태 다이어그램을 안정적으로 처리; 수제 div와 인라인 SVG는 더 에디토리얼한 비주얼(질량 다이어그램, 단면도) 처리. 둘을 혼합 — 모든 것에 Mermaid 의존 금지, 제네릭해 보이기 시작할 것.

## 스캐폴드

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <title>아키텍처 리뷰 — {{저장소명}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 헤더

저장소명, 날짜, 컴팩트 범례: 실선 박스 = 모듈, 점선 = 이음새, 빨간 화살표 = 누수, 두꺼운 어두운 박스 = 깊은 모듈. 소개 문단 없음 — 바로 후보로.

## 후보 카드

다이어그램이 무게를 지탱. 산문은 드물고, 평이하며, [LANGUAGE.md](LANGUAGE.md)의 용어집 용어를 의례 없이 사용.

각 후보는 하나의 `<article>`:

- **제목** — 짧게, 심화를 명명 (예: "Order intake 파이프라인 축소").
- **배지 행** — 권장 강도 (`Strong` = 에메랄드, `Worth exploring` = 엠버, `Speculative` = 슬레이트), 의존성 카테고리 태그 (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **파일** — 고정폭 목록, `font-mono text-sm`.
- **전/후 다이어그램** — 중심부. 두 열, 나란히. 아래 패턴 참조.
- **문제** — 한 문장. 무엇이 아픈지.
- **해결책** — 한 문장. 무엇이 바뀌는지.
- **이점** — 글머리, 각 ≤6단어. 예: "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR 콜아웃** (해당 시) — 엠버 틴트 박스에 한 줄.

설명 문단 없음. 다이어그램이 문단을 필요로 하면 다이어그램을 다시 그릴 것.

## 다이어그램 패턴

후보에 맞는 패턴 선택. 혼합. 모든 다이어그램이 같아 보이지 않게 — 다양성이 요점의 일부.

### Mermaid 그래프 (의존성/호출 흐름용 주력)

요점이 "X가 Y를 호출하고 Y가 Z를 호출, 보라 이 난장판"일 때 Mermaid `flowchart` 또는 `graph` 사용. Tailwind 스타일 카드로 감싸 낙하산처럼 느껴지지 않게. classDef로 누수 엣지는 빨강, 깊은 모듈은 어둡게 스타일링. 시퀀스 다이어그램은 "전: 6회 왕복; 후: 1회"에 잘 작동.

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 수제 박스와 화살표 (Mermaid 레이아웃이 거슬릴 때)

보더와 라벨이 있는 `<div>`로 모듈 표현. 화살표는 상대 컨테이너 위 절대 위치된 인라인 SVG `<line>` 또는 `<path>` 요소. "후" 다이어그램이 회색으로 처리된 내부가 있는 하나의 두꺼운 보더 깊은 모듈처럼 느껴지게 하고 싶을 때 사용 — Mermaid는 적절한 무게로 렌더링하지 않음.

### 단면도 (계층화된 얕음에 좋음)

호출이 통과하는 계층을 보여주는 수평 밴드(`h-12 border-l-4`) 스택. 전: 아무것도 하지 않는 6개 얇은 계층. 후: 통합된 책임이 라벨링된 1개 두꺼운 밴드.

### 질량 다이어그램 ("인터페이스가 구현만큼 넓은" 경우에 좋음)

모듈당 두 개의 직사각형 — 인터페이스 표면적, 구현. 전: 인터페이스 직사각형이 구현 직사각형만큼 거의 큼(얕음). 후: 인터페이스 직사각형은 짧고, 구현 직사각형은 큼(깊음).

### 호출 그래프 축소

전: 중첩 박스로 렌더링된 함수 호출 트리. 후: 동일 트리가 하나의 박스로 축소, 내부에 희미하게 표시된 지금은 내부 호출들.

## 스타일 가이드

- 기업 대시보드가 아닌 에디토리얼. 넉넉한 화이트스페이스. 헤딩에 세리프 선택적 (`font-serif`가 스톤/슬레이트와 잘 어울림).
- 색상 절제: 하나의 강조색(에메랄드 또는 인디고) + 누수 빨강 + 경고 엠버.
- 다이어그램을 ~320px 높이로 유지하여 전/후가 스크롤 없이 나란히 편안하게.
- 다이어그램 내 모듈 라벨에 `text-xs uppercase tracking-wider` 사용 — UI가 아닌 도식으로 읽혀야 함.
- 유일한 스크립트는 Tailwind CDN과 Mermaid ESM 임포트. 보고서는 그 외 정적 — 앱 코드 없음, Mermaid 자체 렌더링 이상의 인터랙티비티 없음.

## 최상위 권장 섹션

하나의 더 큰 카드. 후보명, 이유 한 문장, 카드로의 앵커 링크. 그게 전부.

## 어조

평이한 영어, 간결 — 그러나 건축적 명사와 동사는 [LANGUAGE.md](LANGUAGE.md)에서 직접. 간결함은 이탈의 변명이 아님.

**정확히 사용:** 모듈, 인터페이스, 구현, 깊이, 깊음, 얕음, 이음새, 어댑터, 레버리지, 지역성.

**절대 대체 금지:** 컴포넌트, 서비스, 유닛(모듈 대신) · API, 시그니처(인터페이스 대신) · 경계(이음새 대신) · 레이어, 래퍼(모듈 대신, 모듈을 의미할 때).

**스타일에 맞는 표현:**

- "Order intake 모듈이 얕음 — 인터페이스가 구현과 거의 일치."
- "Pricing이 이음새를 넘어 누수."
- "심화: 하나의 인터페이스, 테스트할 하나의 장소."
- "두 개의 어댑터가 이음새를 정당화: 프로덕션에서 HTTP, 테스트에서 인메모리."

**이점 글머리**는 용어집 용어로 이득 명명: *"지역성: 버그가 하나의 모듈에 집중"*, *"레버리지: 하나의 인터페이스, N개 호출 지점"*, *"인터페이스 축소; 구현이 래퍼 흡수"*. *"유지보수 쉬워짐"*이나 *"더 깔끔한 코드"* 사용 금지 — 용어집에 없고 설 자격 없음.

헤징 금지, 목청 가다듬기 금지, "주목할 만한 점은..." 금지. 문장이 글머리가 될 수 있으면 글머리로. 글머리가 잘릴 수 있으면 자르기. 용어가 [LANGUAGE.md](LANGUAGE.md)에 없으면 새로 발명하기 전에 있는 것으로.
