# 섹션 라이브러리

`sections.md`의 모든 섹션 id별 레시피입니다. 쓰는 레시피만 읽습니다. 각 레시피는 역할, 1440과 390에서의 수치,
예시가 딸린 문구, 시각 요소, 모션, 그리고 검사기나 검토자가 잡아내는 실수를 줍니다. 장소 페이지는 `sections.md`
4절과 다른 부분에서 그 절을 따릅니다.

## 모든 레시피의 전제

- **프레임.** 1440에서 `system.css`: `.wrap` 1280(x 80에서 시작, 장소는 1200, x 120), 거터 24, h1 72,
  h2 48. 390에서는 342, x 24. 모든 섹션은 한 화면 또는 두 화면이며, h2가 맨 먼저 오고 섹션 상단 아래에
  `--padt`를 둡니다(`layout-v4.md`). 시스템에 없는 수치는 추가하지 않습니다. 없는 값은 토큰이 됩니다.
- **분할**은 페이지의 유일한 분할 쌍이며, 텍스트는 왼쪽, 시각 요소는 오른쪽, 위쪽 정렬입니다(`.grid`, 분할에는
  `.grid--middle`을 쓰지 않습니다). 좌우를 뒤집지 않으며, 폰에서는 텍스트가 먼저 옵니다.
- **카드.** `cards.md`가 카드, 그 패널, 바탕, 그 위의 UI를 만들며, 깊이 규칙(상자는 많아야 둘)을 제외하면 여기의
  어떤 내용보다 우선합니다. 패널에 UI가 들어가는 카드는 `.card--open`(상자 없음: 문구는 페이지 바탕 위에, 패널은
  그 아래에 네 모서리를 둥글게) 이거나 패널을 끝까지 채웁니다(`.panel--flush`). 안쪽에 들어간 패널에는 그림만
  넣습니다. 640~1023에서는 패널이 있는 카드가 한 행 전체를 차지하고, 1024~1279에서는 패널이 있는 span-4 카드가
  두 개씩 놓이므로 span-4 패널은 304px 아래로 내려가지 않습니다.
- **프레임 안의 바탕(테크).** 페이지에는 효과 하나와 카드 그룹 하나의 정지 바탕이 있습니다(`effects-usage.md`). 아래
  레시피가 "카드 바탕"이라고 하면, 그 그룹에서 뽑은 id에 패널마다 고유 시드를 준 것을 뜻합니다. "효과"는 페이지의
  유일한 효과이며 히어로 또는 단 하나의 `[data-visual]` 프레임에만 씁니다. 그 밖의 모든 프레임은 조명 바탕을
  그대로(`.frame--lit`), 평평한 `--g-alt` 패널, 사진, 다이어그램 중 하나를 씁니다. 제품, 서비스, 장소 프레임은 평평한
  색 위에 사진을 담으며, 코드 바탕은 절대 쓰지 않습니다.
- **조각(fragment)**은 `assets/ui/<name>/fragment.html`에서 붙여 넣어 슬롯에 놓고 다시 씁니다. 이름, 숫자, 주제,
  앱, 로고는 모두 클라이언트의 것이 됩니다(`data-ui-load`는 키트의 샘플 문구를 보여 주며, 초안용일 뿐입니다). 조각은
  `.stage` 안에 실제 크기(`meta.json`의 `size`, `fluid`)로 놓으며 절대 축소하지 않고, 레시피가 정한 자리(없으면
  `meta.json`의 `place`)에 둡니다. `.fit` 슬롯에는 최소 너비가 맞는 조각만 들어갑니다(`cards.md`): 1024에서 2x2
  카드는 324, span-4 카드는 256. 가장자리 규칙(모든 가장자리를 24px 비우거나, 24px 이상 잘라 페이드를 줌)은 1440,
  1280, 1024, 768에서 지켜져야 하며, 지켜질 때까지 `--ax`/`--ay`를 옮깁니다. 폰에서는 cards.css가 각 조각을 16px
  안쪽에, 상단을 `--ay-sm`(지정하지 않으면 24px)에 놓습니다.
- **모션.** 조각은 완성된 그림을 유지합니다. 카드 그룹, 분할 또는 와이드 프레임의 루프 하나에는 `data-ui-loop`와
  일시정지 버튼이 붙습니다. 히어로 아래에서는 한 화면에 루프가 둘 있으면 안 되고, 스크롤했다는 이유로 움직이는
  것은 없습니다. 모든 타이밍은 `motion.md`를 따릅니다. 다른 종류에는 루프가 없습니다.
- **클래스.** 시스템, cards.css, 키트의 클래스만 씁니다. 레시피에 규칙이 하나 더 필요하면 "page CSS"라고 적으며,
  그것은 시각 요소 안쪽에만 둘 수 있고 장소의 방문 패널(`sections.md` 4절)만 예외입니다.
- **사진**은 제품, 장소, 서비스 페이지의 모든 주요 섹션을 이끕니다. 클라이언트 자신의 사진, 없으면 `photos.mjs`로
  고르고(`photos.md`), 하나의 룩으로, 그대로 보여 주며, 하나뿐인 푸터 줄에 출처를 밝힙니다. 맨 사진 아래에는
  캡션, 이름, 가격, 링크 줄을 두지 않습니다. 판매 품목의 이름과 가격은 그 카드의 패딩 안에 둡니다.
- 예시의 **이름**(Ferrow, Rotaro, Kestrow, Ledgewick, Clausewise, Fenn, Halden...)은 형식을 보이려고 지어낸
  것입니다. 쓰인 방식을 따라 하되 단어를 베끼지 않습니다. 증거, 인용, 고객, 수치는 브리프에서만 가져옵니다
  (`copy.md`).
- **로고, 버튼, 링크.** `.nav__logo`에는 클라이언트의 SVG를 넣고, 없으면 뽑은 마크와 이름을 넣습니다(푸터도
  같습니다). 버튼은 `<html data-buttons>`에서 뽑은 룩을 따르며, 내비게이션의 주 행동은 단일 버튼 높이의
  `.btn.btn--primary`입니다(`system.md` 내비게이션). 내비게이션 단어, 버튼, 푸터 링크는 `#id`로 가고, 로고는
  `#top`, Contact는 `#contact`로 갑니다. Privacy와 Imprint는 직접 작성한 페이지로 가거나 생략합니다.

# 내비게이션

넷 모두 `system.md`의 바를 공유합니다. 고정, 불투명, 72px(폰에서는 56), 1px 헤어라인이며 어느 깊이에서나
같습니다. 패널은 호버 150ms 뒤에 페이드와 6px 내려오는 움직임으로 열리고, 단어를 클릭하면 해당 섹션으로
가며 `preventDefault`를 쓰지 않습니다. system.js가 폰 시트, Esc, `aria-expanded`를 더하므로 두 번째 핸들러를
작성하지 않습니다.

## nav-mega

**쓰임새.** 호버 한 번이면 보이는 회사의 지도입니다. 제품을 방문자가 원하는 것별로 묶고, 각 링크에 이름과
회색 한 줄 설명을 달고, 최신 릴리스를 그림 카드 하나로 보여 줍니다. 기능 페이지가 6~12개인 소프트웨어 또는
제품군이 여럿인 회사에 씁니다.

**1440에서.** `header.nav` > `.wrap.nav__bar`: 로고, 한 단어짜리 `.nav__link` 4~6개(메뉴가 열리는 것에만
`.chev`), 그다음 Sign in(일반 `.nav__link`이며 계정이 있는 앱에만)과 주 행동이 있는 `.nav__actions`. 메뉴는 그
항목의 `.nav__menu`이며 바 아래 전체 너비를 차지하고 `.wrap.grid`를 담습니다. `.menu-col.span-3` 두세 개, 그다음
x 1360에서 끝나는 `a.menu-card.span-3` 하나(열이 둘이면 `start-10`). 열은 3~4개의 링크 위에 `.t-label` 제목이
오며, 각 링크는 기능 이름과 최대 30자의 회색 한 줄입니다. 작은 메뉴(Resources, Company)는 같은 패널을 카드
없이 일반 열로 엽니다.

**390에서.** 시스템의 시트: 행 높이 56px. 메뉴가 있는 단어는 탭하면 그 아래에서 제자리에 링크가 열리고
(system.js의 `.nav__expand`. 즉시 열리며 높이는 애니메이션하지 않습니다), 메뉴 카드는 일반 행이 되고, 두 버튼은
하단에서 전체 너비입니다.

**문구.** 바 라벨: 구매자의 말로 쓴 일반 단어 하나. 링크: 기능 이름(1~3단어)과 그것이 하는 일(3~7단어). 예시,
Ferrow(물리치료 클리닉용 예약·노트 소프트웨어): 바는 Product, Clinics, Pricing, Resources, Company. Product는
Front desk(Online booking / Patients book a free slot; Reminders / Texts before each visit)와 Treatment(Patient
notes / Templates for every treatment). 카드: New / Online payments / Take a deposit at booking.

**시각 요소.** 메뉴 카드만 해당합니다. `.panel`(160px)에 `.stage.stage--fade-br`를 담고, 거기에 최신 기능으로 다시 쓴
조각 하나를 `.at-corner`(24px 안쪽)로 오른쪽과 아래가 잘리게, 정지 상태로, 조명 바탕 그대로 놓습니다. 열에는
아이콘을 넣지 않습니다.

**흔한 실수.** `.wrap`보다 좁은 바 또는 줄바꿈되는 링크, 일반 링크에 붙은 쉐브론, 그리드를 벗어난 메뉴, 두 번째
그림 카드, 30자를 넘는 회색 줄, 모호한 라벨("Solutions", "Platform").

## nav-cards

**쓰임새.** 서로 다른 제품 둘에서 넷을 일반 이름과 한 줄이 붙은 그림 카드로 보여 주고, 리소스는 일반 링크
열로 둡니다. 각각 화면이나 실제 사진이 있는 제품이 둘에서 넷인 회사, 서비스 라인이 셋이고 실제 작업물이 있는
스튜디오, 또는 장소의 제안(사진 카드 넷)에 씁니다.

**1440에서.** 바는 nav-mega와 같습니다. Product의 `.nav__menu`는 `.wrap.grid`에 `a.menu-card.span-4`(너비
410) 셋을 담습니다. `.panel`(page CSS `.menu-card .panel { --p-h: 200px }`)에 그 제품의 조각을
`.stage.stage--fade-br` 안의 `.at-corner`로 두거나 사진으로 패널을 채웁니다. 제목은 `.t-card`, 회색 한 줄은 최대
52자이며 카드 안에 둡니다. 장소: 384x288(4:3)의 span-4 카드 셋, 각각 클라이언트의 사진이고 16/500의 이름과
시작 가격을 두며 조각, 바탕, 그림자는 없습니다.

**390에서.** 시트는 각 메뉴 카드를 제목 위에 한 줄이 놓인 행으로 보여 주며 그림은 숨깁니다.

**문구.** 카드 제목: 제품의 이름 또는 평이한 역할, 줄은 그것이 하는 일. 예시, Ferrow: Online booking / Patients
book a free slot from your website; Patient notes / Notes from your own templates.

**흔한 실수.** 세 카드에 같은 시드, 높이가 다른 패널, 패널 위의 글자, 줄바꿈되는 제목, 단독으로는 의미 없는
이름("Flow", "Pulse").

## nav-centre

**쓰임새.** 가장 조용한 바입니다. 단어는 바의 가운데에, 로고는 왼쪽 라인에, 주 행동은 오른쪽 라인에 둡니다.
평이한 단어가 넷 또는 다섯인 소프트웨어와 서비스에 씁니다.

**1440에서.** `header.nav.nav--centre`: system.css가 `.nav__links` 그룹을 페이지 축에 가운데 정렬하고, 로고와
행동은 `.wrap` 라인을 유지합니다. 단어는 넷 또는 다섯이며 1024에서 줄바꿈되지 않습니다. 메뉴는 nav-mega의 작은
메뉴와 같습니다.

**390에서.** 로고는 왼쪽, 토글은 오른쪽. 시스템의 시트.

**흔한 실수.** 1024에서 로고나 버튼에 닿을 만큼 넓은 그룹, 두 번째 행.

## nav-split

**쓰임새.** 사람들이 찾아가는 장소, 가게, 식당, 스튜디오에 씁니다. 이름은 가운데, 짧은 단어 셋은 왼쪽, 주
행동은 오른쪽입니다. 한 단어(Rooms, Menu, Classes, Shop)는 제공하는 것의 사진 카드가 담긴 패널을 엽니다.

**1440에서.** `header.nav.nav--split`: system.css가 링크를 왼쪽 3분의 1에, 로고(마크와 이름, 디스플레이 서체
28px)를 페이지의 중심선에, 행동을 오른쪽 3분의 1에 놓습니다. 단어는 넷이며, 왼쪽 3분의 1을 나눠 쓰므로
`system.md` Nav의 넷~여섯 중 하한입니다. 1024에서도 단어는 줄바꿈되지 않습니다.
메뉴 단어의 `.nav__menu`는 `.wrap.grid`에 `a.menu-card.span-3` 셋 또는 넷(장소에서는 282x212, 4:3 넷)을 담고,
각각 클라이언트의 사진(`img.frame__img`, 효과 없음)에 `.t-card`의 이름과 카드 안의 시작 가격을 둡니다. 행동: 주
행동("Book a table")과, 클라이언트에 실제로 있는 일반 단어 최대 하나(판매하는 경우 Gift cards), 없으면 없음.

**390에서.** 로고는 왼쪽으로, 토글은 오른쪽으로 옮겨 갑니다. 시트에는 장소라면 하단에 도로명 주소와 그 주의
영업시간을 더합니다.

**문구.** 예시, Fenn(라이프치히의 도자기 스튜디오): Classes(메뉴: Taster evening / from €39; Six-week course /
from €260; Open studio / €18 a day), Shop, Studio, Visit; "Gift cards", "Book a class".

**흔한 실수.** 3분의 1 폭이 고르지 않아 로고가 중심에서 밀림, 단어가 넷을 넘음, 메뉴 안의 UI 조각, 링크 두 번째
행, 열린 패널의 그림자.

# 히어로

열 가지 히어로와 장소 히어로의 1440 및 390 수치는 `layout-v4.md` 3절에 있습니다. 뽑은 것을
`assets/layout/hero-<id>.html`에서 붙여 넣고 그 문구와 그림을 다시 씁니다. 레시피가 더하는 것은 다음과 같습니다.

- **문구**(`copy.md`): h1은 2~8단어로 범주와 구매자 또는 장소를 지칭하고, 부제는 15~30단어로 작동 방식과 주된
  이점을 하드 팩트 하나와 함께 말합니다(장소: 오늘의 영업시간이 담긴 80자). 주 행동은 동사와 목적어이며 내비게이션,
  마무리 구역, 폰 바에서 글자 그대로 같고, 더 조용한 행동 하나가 있습니다(장소: 없음). 예시, Halden Dental(말뫼의
  클리닉): "Dental clinic in central Malmö"; "Check-ups, cleaning and fillings from €95. Book online, most visits
  within a week."; "Book a check-up", "See prices".
- **그림**이 작업물입니다. 사용 중인 제품, 장소, 사람들의 사진(제품, 장소, 서비스), 앱이라면 폰(page CSS로 만든
  `.device` 280x570, 베젤 8px, 반경 32, 폰 레이아웃의 조각 하나, `role="img"`), 웹 앱이라면 창 하나(`window`
  `.at-corner.to-edge` 56/56의 `.frame--split`에 `cursor` 또는 `notify`를 그 오른쪽 아래 가장자리 `.at-over`로),
  기술 제품이라면 그 제품의 오브젝트(조명 바탕 위의 `<div data-print="print-…">`, 테크 전용). 앱 버튼은 글자로
  ("Download for iPhone") 쓰며 시스템 버튼 옆에 스토어 배지를 두지 않습니다.
- **창 히어로**(`centred`, `collage`, 분할 창): 조각을 붙여 넣고 클라이언트의 이름으로 다시 씁니다. 주된 것은
  루프할 수 있고(테크, 프레임의 일시정지 버튼 포함), 두 번째는 정지합니다. 조각은 둘을 넘지 않으며, 기울이거나
  확대하지 않고, 키트의 샘플 문구를 쓰지 않으며, 프레임 한가운데 홀로 떠 있는 조각은 두지 않습니다.
- **도면**(`figure.drawing`, `starter.html`): 사진이 이미 제품을 보여 주는 페이지에서 제품 사양 옆의 치수 도해로만
  씁니다. 제품의 측면도를 실제 비율의 인라인 SVG 하나로(단위 하나가 1mm, `viewBox`는 제품에 6%를 더한 크기,
  `--ar`은 너비를 높이로 나눈 값), 치수선(`.dim`) 둘 또는 셋과 그 수치를 `span.drawing__dim`으로 둡니다. 히어로로
  쓰지 않으며, 제품의 유일한 그림으로도, 하드웨어에도, 사진이 없는 페이지에도 쓰지 않습니다. 그런 페이지는 그
  종류의 대체 사진을 보여 줍니다(`sections.md` 3절 제품. 테스트에서: 로봇 제작사의 히어로로 그린 SVG 팔).

# 근거

증거는 브리프에서만 가져옵니다. 실제 고객, 인용, 후기, 보도, 수치입니다(`copy.md`). 없으면 증거를 빼며 절대
지어내지 않습니다.

## logo-row

**쓰임새.** 제품을 쓰는 실제 조직으로, 히어로 내용 아래에 붙입니다(소프트웨어와 제품 전용). 로고를 보여도
되는 클라이언트의 실제 고객만 씁니다.

**1440에서.** 히어로에 붙은 행(`layout-v4.md`, 최대 96px): `p.t-small.muted`(14px, 회색, 왼쪽 라인, 행 위 24px),
그다음 x 80에서 1360까지 한 줄의 `.logos`: 높이 28px의 로고 최대 여섯 개이며, 각각 고객 자신의 SVG를 원래 색
그대로 씁니다(규칙 7, `icons.md`). 정지 상태: 마키, 밝은 띠, 페이드, 타일 없음. 로고는 절대 움직이지 않습니다
(MO-57).

**390에서.** 숨깁니다. 히어로가 여전히 H - 24 - bar에서 끝나는 경우에만 3열 그리드로 보입니다.

**문구.** 행 위의 줄: 누가 쓰는지를 평이하게("Clinics using Ferrow").

**흔한 실수.** 고객이 아닌 곳의 로고 또는 지어낸 워드마크, 마키, 단색이거나 흐린 마크, 자랑하는 줄, 서비스 또는
장소 페이지의 로고 행.

## quote-stat

**쓰임새.** 브리프가 주는 실명 고객이 무엇이 바뀌었는지 말하고, 그것을 뒷받침하는 숫자 하나가 옆에
옵니다. 495px 아래로 들어가면 위 섹션에 합칩니다(`sections.md`).

**1440에서.** 위 섹션의 마지막 블록으로 두거나 자체 `section.section.ground-surface`로 둡니다. `.grid`:
`figure.quote.span-8`과 `div.stat-aside.span-3.start-10`이 같은 상단 라인에서 시작합니다. `blockquote`(28px,
최대 40단어), 그 아래 32px에 `div.person`(`div`이며 `figcaption`은 절대 아님): 사람의 40px 사진(인용에는 얼굴이
필요합니다) 또는 회사 로고, 이름 위에 직책과 회사. 수치: `p.t-stat`(1440에서 38, 390에서 28)와 최대 여덟
단어의 회색 줄.

**390에서.** 인용, 사람, 그다음 수치이며, 수치 위에 1px 헤어라인과 24px 간격을 둡니다.

**문구.** 전과 후, 칭찬하는 단어 없음. 예시 형식: "We used to rebuild the rota every Sunday night. Now it
takes twenty minutes on Friday." / 이름, 직책, 소속 / "20 min", "to plan a week of shifts".

**시각 요소와 모션.** 정지. 테크에서는 이것이 페이지의 유일한 효과일 때에 한해 숫자를 효과로 채울 수 있습니다
(`fx-stat`).

**흔한 실수.** 브리프에 없는 인용, 스톡 또는 빠진 초상, 슬로건인 수치, 카운트업.

## customer-proof-row

**쓰임새.** 브리프의 실명 고객 셋, 각각 측정된 결과 하나. B2B 소프트웨어, 스튜디오, 기업에 판매하는 제품에
씁니다.

**1440에서.** `.section-head.section-head--row`: h2는 왼쪽, `a.link` "All customer stories"는 오른쪽의 아래쪽
라인에 둡니다. 48px 아래에 `article.card.span-4` 셋: 높이 28px의 `img`인 고객 로고 또는 `p.t-card`인 이름, 24px,
스토리 제목(한 줄, 최대 7단어), 한 줄, `a.link` "Read the story", 그다음 `.stage.stage--fade-br` 안에 `stat`
`.at-corner.to-edge`(`--ax: 24px; --ay: 40px`, `data-ui-opts='{"fill":true}'`)를 둔 `.panel.panel--flush`
로, 오른쪽과 아래가 잘리며 숫자와 변화가 보입니다. 서비스 또는 스튜디오: 각 고객 작업물의 사진이 대신 패널을
채웁니다.

**1024~1279에서.** 카드 둘, 그다음 셋째가 행 전체를 차지합니다. **768과 390에서.** 한 열.

**문구.** 제목: 누가 무엇을 했는지. 수치: 센 대상(최대 28자), 정수, 변화 칩, "Before x · After y".

**모션.** 테크: 첫 카드의 수치가 루프하고, 나머지 둘은 정지합니다.

**흔한 실수.** 브리프가 이름을 대지 않은 고객, 건수 대신 퍼센트, 캐러셀, 인용 카드로 바뀐 카드.

# 기능

## product-statement

**쓰임새.** 제품이 무엇이며 무엇이 다른지 평이한 한 문단으로 쓰고, 그다음 제품을 와이드 그림 하나와 팩트
셋으로 보여 줍니다. 제품 전용(장소에는 절대 쓰지 않습니다). 같은 너비의 히어로 프레임 바로 뒤에는 오지
않습니다.

**1440에서.** 설명문은 `span-8`: h2(48px, 최대 4줄), 첫 문장은 잉크색, 나머지는 `<span class="muted">`. 48px 아래에
`span-12`의 `.frame.frame--hero`(page CSS `aspect-ratio: 2 / 1`)가 누끼 사진을 가운데에 모든 가장자리에서 최소
64px 떨어지게 담고, 48px 아래에 `span-4`의 팩트 셋: 1px 헤어라인, 단위가 붙은 28px의 값, 회색 한 줄. 기술 제품은
클라이언트의 렌더 또는 그 종류의 자체 오브젝트를 대신 보여 줄 수 있습니다(`.frame--lit`에 `<div
data-print="print-…">`, 그 `hero` 프리셋을 크게 가운데 오른쪽에, 팩트는 왼쪽 아래의 `div.frame__text`에). 사진이
없는 제품이나 하드웨어는 프레임에 그 종류의 대체 사진을 보여 줍니다(`sections.md` 3절 제품. `photos.md`). 제품
렌더(`data-product`, 자리 `stage`, 페이지의 평평한 바탕 위, 하드웨어는 조명 바탕)는 브리프가 3D를 요청할 때만
씁니다(`effects-objects.md`, 제품 렌더).

**390에서.** h2는 30px, 프레임은 정사각형, 팩트는 그 아래 목록으로.

**문구.** 예시, Pellum(책상 램프): "Pellum lights a whole desk without glare. <grey>One dial dims it and turns it
from warm light to daylight.</grey>"; 팩트 "1,100 lm" Brightness, "2,700 to 6,500 K" Colour, "9 W" Power.

**모션.** 누끼: 없음. 기술 제품의 오브젝트: 느린 회전과 포인터에 대한 반응(페이지의 효과), 자체 일시정지
버튼 포함.

**흔한 실수.** 슬로건, 회색 부분을 둘째 문단으로 분리, 상자에 넣거나 가장자리에 닿은 누끼, 클라이언트의 제품
종류가 아닌 오브젝트, 주장에 불과한 팩트.

## features-2x2

**쓰임새.** 한 화면에 그것이 하는 일: 비중이 같은 기능 넷, 각각 작동하는 작은 시각 요소를 가집니다(2x2:
헤드라인, 두 줄, 더 작은 카드가 놓인 안쪽 패널). 한 기능이 더 중요하다면 벤토를 씁니다.

**1440에서.** `.section-head`에 회색으로 이어지는 h2. 48px 아래에 `.grid`와 `article.card.card--row.span-6` 넷,
상자 깊이는 둘: 밝은 페이지에서는 `.card--open`(제목과 줄은 페이지 바탕 위에, 패널은 그 아래), 어두운 페이지에서는
`.panel.panel--flush`가 있는 카드의 상자(x.ai의 카드). 각 카드: 제목, 잉크색 두 줄(16~20단어), 그다음 패널(page CSS
`#<section> .panel { --p-h: 336px }`)에 `.stage.stage--fade-b`와 붙여 넣은 조각 하나:
- `chat` `.at-rise.fit`(`--fit-max: 400px; --ax: max(24px, 50% - 200px)`, `--ay`와 `--ay-sm` 56px): 아래로 24px
  이상 잘려 나갑니다. `search` 또는 `stat`도 `.to-edge`와 함께 같습니다(`stat`은
  `data-ui-opts='{"fill":true}'`).
- 짧은 스택(제목이 최대 26자인 `notify`, `checklist`, `integrations`)은 `.at-rise.fit`로 낮게, `--ay`와 `--ay-sm`은
  `calc(100% - 180px)`, 마지막 행이 잘립니다.
- `toggles` `.at-right.to-edge`(`--ax: 32px; --ay: 56px`), 아래가 잘립니다.
- `window`(`{"compact":true}`) `.at-corner` 24/28을, 바에 앱과 그 상태를 적은 flush `.panel--device`에 둡니다.
- 다이어그램 카드(`diagrams.md`): 패널을 채우는 `<div class="dg" data-diagram="<preset>">`.
`calendar`(그 달이 전부 보여야 합니다), `doc` 또는 `code`(1024에서 324px 슬롯보다 넓습니다)는 쓰지 않습니다.

**1024에서.** 패널은 너비 372: `.fit` 조각은 324로 좁아지고 나머지는 잘린 채 둡니다.
**768과 390에서.** 행마다 카드 하나, 각 조각은 자신의 레이아웃으로 모서리에 놓입니다.

**문구.** h2는 회색 부분을 포함해 최대 12단어. 제목: 동사와 구체적인 목적어. 줄: 구체적 세부 하나가 든 한두
문장. 카드에 버튼 없음. 예시, Ferrow: "Run your practice from one app. <grey>Bookings, notes and
payments.</grey>"; "Takes online bookings", "Takes card payments", "Builds treatment plans", "Sends text
reminders".

**시각 요소.** 테크: 카드 바탕, 패널마다 시드 하나, `data-fx-params='{"drift":0}'`, system.js가 조명을 줍니다. 서로
다른 조각 또는 다이어그램 넷, 앱을 말하는 곳에는 실제 앱 아이콘. 제품 또는 서비스: 각 기능의 사진이 패널을
채웁니다.

**모션.** 테크: 첫 카드의 조각 또는 다이어그램이 루프하고(`data-ui-loop`), 나머지는 정지해 있다가 포인터가 그
카드에 머무는 동안 재생됩니다. 링크가 있는 카드는 2px 올라옵니다.

**흔한 실수.** 스크롤로 움직이는 카드, 줄이 맞지 않는 패널, 넷째 줄의 글자, 키트의 샘플 문구, 명사 제목("Peace of
mind"), 상자 깊이 셋, 한가운데 죽어 있는 위젯, 조각 아래 1~23px의 바탕 띠.

## bento

**쓰임새.** 주된 기능 하나를 크게, 작은 것 넷. 주력 기능이 하나인 소프트웨어, 또는 주요 부품과 세부 넷의
실제 사진이 있는 제품에 씁니다.

**1440에서.** `.grid`: 첫 행은 `article.card.card--row.span-8`과 `.span-4`, 둘째 행은 `.span-4` 셋. 모든 카드:
제목, 잉크색 두 줄, 그다음 features-2x2처럼 상자 깊이 둘의 패널이며, 그룹이 `--p-h` 하나(336px)를 씁니다. 큰
카드: `window` `.at-corner`(40/48, 오른쪽과 아래가 잘림, `.stage--fade-br`) 또는 `files`
`.at-corner.wide`(`--w: 680px`). 작은 카드(1440에서 패널 347, `.fit` 슬롯 256): 아래가 잘린 조각 하나. 256으로
좁아지는 것은 가운데 `.at-rise.fit`(`chat`, `.to-edge`가 붙은 `search`, 낮게 놓은 짧은 스택), `toggles`
`.at-right.to-edge`, 또는 더 넓은 것(`stat`, `notify`, `cursor`)을 실제 너비로 `.at-corner`(`--ax: 24px; --ay:
40px`)에 오른쪽과 아래가 잘리게 둡니다. `voice` 통화는 그 `meta.json`이 말하는 곳에 가며 그룹의 루프가 됩니다.

**1024~1279에서.** 큰 카드는 행 전체, 작은 넷은 2x2.
**768과 390에서.** 행마다 카드 하나.

**문구.** 큰 카드: 주된 기능을 동사와 목적어로. 작은 것은 2~4단어. 예시, Ledgewick(프리랜서 디자이너를 위한
장부): "Reads every receipt" / "Drop in PDFs or phone photos. The date, amount and VAT are filled in."; 작은 것:
"Matches bank payments", "Tracks VAT", "Sends invoices", "Exports for your accountant".

**시각 요소.** features-2x2와 같습니다. 제품: 모든 패널에 사진, 하나의 룩.

**모션.** 테크: 큰 카드가 루프하고, 작은 넷은 정지합니다. 한 벤토에 루프 둘은 절대 없습니다.

**흔한 실수.** 카드마다 글자 위치가 다름, 두 줄을 넘는 작은 카드 문구, 작은 카드의 `calendar`, `doc`, `code`, 다른
카드 그리드 옆의 벤토.

## split-text-left

**쓰임새.** 제품이 하는 일 하나를 몇 문장과 팩트 셋으로, 정확히 그것을 보여 주는 그림 옆에 둡니다. 소프트웨어,
제품, 스튜디오의 주력입니다.

**1440에서.** `.grid`, 위쪽 정렬: 텍스트는 `span-5`(h2, 24px, 20px의 두세 문장, 24px, 일반 줄로 짧은 팩트 최대
셋, 24px, `.link` 하나)이고 `.frame.frame--split.span-6.start-7`(5:4, 폰에서는 정사각형)이
`.stage.stage--fade-br`를 담습니다. 주된 조각은 아래가 잘리며, 네 면에 바탕이 있는 채로 떠 있지 않습니다.
- `window` 또는 클라이언트의 스크린샷 `.at-corner.to-edge`를 `--ax`/`--ay` 56px로, 오른쪽과 아래가 잘리게.
  `files`도 `.wide`(`--w: 680px`)로 같게.
- 더 좁은 조각(`doc`, `code`, `chat`, `search`, `checklist`)은 `.at-rise.to-edge`로, `--w`로 가운데 맞추고 56px
  아래로. 짧은 것(`slider`, `toggles`)은 `.at-rise.fit`로 40px 아래, 둘째 행 아래가 잘리게.
결과를 보여 주는 작은 조각 하나(`cursor`, `notify`)는 `window` 또는 스크린샷 위에만, 그 오른쪽 아래 가장자리
`.at-over`(`--bx: 24px; --by: -40px`)로 두며, 첫 행들 위에는 절대 두지 않습니다(제품 UI 위에 작은 카드가 얹힌
Figma의 패널).
제품 또는 서비스: 프레임에는 텍스트가 이름을 대는 부품이나 작업물의 사진(`.frame--photo`, 628x471)을 담으며 UI는
절대 담지 않습니다.

**1024~1279에서.** 프레임은 너비 436~564: 주된 조각만 둡니다.
**768과 390에서.** 텍스트가 먼저, 프레임은 48px 아래에 전체 너비로.

**문구.** 제목: 일과 그 결과. 문장은 그림이 재생되는 순서대로. 예시, Clausewise(소규모 로펌용 계약 검토): "Finds
risky clauses in contracts"; "Upload a contract and every clause is checked against your firm's playbook.";
링크 "See how review works"; "unlimited liability"가 표시된 `doc`이 아래에서 올라옵니다.

**시각 요소.** 테크: 이 프레임이 페이지의 `[data-visual]`이면 효과, 아니면 조명 바탕 그대로. 주된 조각이 텍스트를
단계마다 보여 주고, 작은 조각이 결과로 나오는 것을 보여 줍니다.

**모션.** 테크: 루프 하나, 작은 조각 또는 주된 조각에서.

**흔한 실수.** 텍스트와 프레임의 위쪽 정렬이 어긋남, 4줄 h2, 텍스트가 말하지 않는 것을 보여 주는 그림, 링크
하나 대신 버튼 쌍, 반대편의 두 번째 분할.

## tabs-tour

**쓰임새.** 소프트웨어 전용: 작업 셋에서 여섯을 한 번에 하나씩, 고정된 프레임에서 보여 줍니다. 클릭만, 타이머는
절대 쓰지 않습니다.

**1440에서.** `.grid`, 위쪽 정렬: 왼쪽 `span-5`에 `.section-head`(h2, 회색 줄), 그다음 `button.tab[role=tab]`
3~6개가 든 `div.tabs[role=tablist]`로, 각각 `aria-controls`가 자신의 `[role=tabpanel]`(두 문장과 `.link`)과 그
화면을 가리킵니다(`aria-controls="tab-1 screen-1"`). 오른쪽에 `.stage.stage--fade-br`가 든
`.frame.frame--split.span-6.start-7`: 탭마다 슬롯 하나(첫째를 뺀 나머지는 `hidden`), 각각 split-text-left의 주된
조각처럼 놓고 아래가 잘리며, 모든 패널은 높이가 하나로 고정되어 프레임 크기가 바뀌지 않습니다. system.js가 탭의
패널과 화면을 함께 보여 줍니다.

**390에서.** 탭은 여러 행으로 줄바꿈되고(스와이프 행은 절대 안 됨), 프레임은 활성 패널 48px 아래에 둡니다.

**문구.** 탭 라벨: 동사와 목적어 2~3단어, 문법은 하나. 예시, Ferrow: "Book a session", "Move an
appointment", "Pay by card", "Follow exercises".

**모션.** 인디케이터는 클릭 시 미끄러집니다(`motion.md`). 보이는 화면만 루프합니다.

**흔한 실수.** div로 만든 탭, 명사 라벨, 크기가 바뀌는 프레임, 두 탭에 같은 조각, 제품·서비스·장소 페이지의 탭.

## chapter

**쓰임새.** 한 기능 영역을 깊이 다룹니다. 문단 하나, 링크 하나, 제품이 그것을 하는 와이드 프레임, 기능 이름
넷. 플랫폼이라면 둘에서 넷을 연달아 둡니다. 챕터 시리즈는 이웃끼리 레이아웃을 공유하는 유일한 자리입니다. 보통
두 화면짜리 섹션(`.g2`)입니다.

**1440에서.** `.grid`, 위쪽 정렬: `span-5`에 h2, `span-6 start-7`에 회색 문단(약 25단어)과 `.link`. 64px 아래에
`.stage`(16:7)가 든 `.frame.frame--hero`: 그 영역의 주된 화면(`window`, `code`, `doc` 또는 `files`)을
`.at-rise.to-edge`로 64px 아래에, 그리고 하나의 행동(`cursor`, `notify`, `stat`, `search`)을 그 오른쪽
가장자리에 `.at-over`로. 48px 아래에 `div.span-3` 넷: 기능 이름과 회색 한 줄.

**390에서.** 텍스트가 먼저, 정사각형 프레임은 주된 화면을 유지하고, 네 이름은 목록으로.

**문구.** 예시, Kestrow(운송업체용 화물 예약): "Book loads in one place"; "See every load your customers
send, quote it and book a truck from one screen."; 이름 "Imports orders" / "From email or a CSV file".

**모션.** 챕터마다 루프 하나. 시리즈에서는 한 챕터 걸러 루프합니다. 스크롤로 드러나거나 스크럽되는 것은
없습니다.

**흔한 실수.** 반투명하거나 기울어진 조각, 주된 화면의 유일하게 읽히는 행을 가리는 행동, 템플릿을 바꿔 버리는
반복.

## app-frame

**쓰임새.** 제품 그 자체를 Linear, Cursor, Vercel이 보여 주는 방식으로 크게 보여 줍니다. `.wrap` 전체에 걸친
실제 앱 창 하나로, 열린 항목 옆의 목록과 앱 고유의 크롬을 담습니다. 모든 소프트웨어 페이지에는 하나가 있으며,
히어로 또는 처음 세 섹션 안에 둡니다(테스트에서: 세이지색 패널 한가운데 작은 diff 카드 하나가 리뷰의 전부였던
코드 리뷰 페이지는, 풀 리퀘스트 목록을 전체 너비 diff 옆에 하나의 앱 프레임으로 둔 Linear의 리뷰 띠보다 약 3.5점
낮게 받았습니다). 게임, 제품, 서비스, 장소에는 절대 쓰지 않습니다.

**두 개의 창.** (키트 조각을 클라이언트의 이름으로 다시 씁니다. 목록은 언제나 `window`입니다.)

| Product | List pane | Open pane |
|---|---|---|
| 코드 리뷰 | `window`: 풀 리퀘스트 | `diff-review`(위쪽 250px 안에 코멘트와 Apply) |
| 지원, 받은편지함, CRM, 에이전트 | `window`: 대화 | `chat`(열린 스레드) |
| 문서, 계약, 지식 | `window`: 문서 | `doc`(표시된 문구가 있는 페이지) |
| CI, 배포 | `window`: 실행 | `pipeline-board`(와이드: 노드와 로그) 또는 `terminal-run` |
| 예약, 일정 | `window`: 예약 | `calendar` |

`window`의 행: `.ui-win__who`는 사람(작성자, 고객, 소유자), `.ui-win__sub`는 항목과 그 세부("Retry settle jobs ·
+4 −3"), 상태 칩은 제품 고유의 상태(`data-open`, `data-work`, `data-done`), 사이드바 라벨은 각각 한 단어입니다.
행을 9개 이상, 열린 항목에는 충분한 줄(diff는 24줄 이상)을 써서 두 창이 모두 프레임의 아래쪽을 넘어 흐르게
합니다. 프레임이 페이드 아래에서 그것을 자르며, 마지막 행 밑에 창이 비어 있는 띠가 생기지 않게 합니다.

**1440에서.** 한 화면. `.grid`, 위쪽 정렬: `span-5`에 h2, `span-6 start-7`에 회색 문단(약 25단어)과 `.link` 하나.
48px 아래에 프레임이 화면의 나머지를 `.fill`(약 1280 x 550)로 차지합니다.

```html
<div class="ui app fill" role="img" aria-label="[what the window shows]" data-ui-pause-host>
  <div class="app__pane app__pane--list"> [window fragment] </div>
  <div class="app__pane app__pane--open" data-ui-loop> [the open item's fragment] </div>
</div>
```

`class="ui"`는 프레임에 키트의 토큰을 주고, 그것이 그려진 창 하나임을 검사에 알립니다. Page CSS(레시피
전부):

```css
.app.ui { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); margin-top: var(--s-7); background: var(--u-bg); border: 1px solid var(--u-border); border-radius: var(--u-r); box-shadow: var(--u-shadow); }
.app > .app__pane { position: relative; min-width: 0; min-height: 0; overflow: hidden; }
.app > .app__pane + .app__pane { border-left: 1px solid var(--u-line); }
.app > .app__pane > .ui-panel { width: 100%; border: 0; border-radius: 0; box-shadow: none; }
.app > .app__pane::after { content: ""; position: absolute; inset: auto 0 0 0; height: 64px; background: linear-gradient(transparent, var(--u-bg)); pointer-events: none; }
@media (min-width: 1024px) and (max-width: 1279px) { .app.ui { grid-template-columns: minmax(0, 4fr) minmax(0, 8fr); } }
@media (max-width: 1023px) {
  .app.ui { grid-template-columns: minmax(0, 1fr); grid-template-rows: auto minmax(0, 1fr); }
  .app > .app__pane--list { max-height: 252px; }
  .app > .app__pane--list::after { display: none; }
  .app .ui-win__side { display: none; }
  .app .ui-win__body { grid-template-columns: minmax(0, 1fr); }
  .app > .app__pane + .app__pane { border-left: 0; border-top: 1px solid var(--u-line); }
}
@media (max-width: 639px) {
  .app.ui { grid-template-rows: minmax(0, 1fr); }
  .app > .app__pane--list { display: none; }
  .app > .app__pane + .app__pane { border-top: 0; }
}
```

`window`는 자기 창에 맞춰 스스로 배치됩니다(1440에서는 이름 위에 항목을 쌓은 행, 태블릿에서는 열). 조각은 자연
높이를 유지하며, 자르는 것은 창이지 조각 자신의 상자가 아닙니다. 상자는 하나입니다. 프레임이 곧 창이고, 창들은
그 열이며, 그 뒤에 패널, 카드, 바탕은 없습니다(섹션의 바탕 위에 놓이며, `dark-band`에서는 키트의 어두운 면 위에
놓입니다). 그 위에 올리는 두 번째 조각(`cursor`, `notify`)은 열린 창의 오른쪽 아래에만 `.at-over`로 두며, 목록
위에는 절대 두지 않습니다.

**1024~1279에서.** 목록은 4열로 좁아지고(사이드바가 빠짐), 열린 항목이 8열을 차지합니다.
**768~1023에서.** 목록이 위에(그 바, 열 머리, 온전한 행 넷, 252px), 열린 항목이 그 아래로 섹션 끝까지.
**390에서.** 열린 항목만, 자체 헤더를 크롬으로 씁니다.

**문구.** h2는 창이 보여 주는 것을 말합니다("Every pull request, reviewed in one place"). 문단은 창이 보여
주는 순서대로 단계를 말합니다.

**모션.** 루프 하나: 열린 항목(그 창의 `data-ui-loop`: Apply를 누르고 답이 쓰입니다). 목록은 정지합니다. 창
안에서 스크롤되는 것은 없습니다.

**흔한 실수.** 조명 패널 위에 열린 항목만 둠(그것은 제품이 아니라 카드입니다), 목록과 항목을 사이에 바탕을 둔 두
상자로 나란히 둠, 빈 흰색으로 끝나는 창, 키트의 샘플 행, 창 높이까지 늘린 조각(그러면 자체 오버플로가 그 글자를
자릅니다).

## steps

**쓰임새.** 제품을 어떻게 쓰는지를 순서대로, 각 단계의 결과를 보여 주며 설명합니다. 실제 단계가 셋일 때만
씁니다.

**1440에서.** `.section-head`, 그다음 `article.card.card--row.span-4` 셋이 든 `.grid`: `span.step-num`, 제목(동사와
목적어, 한 줄), 잉크색 한두 줄, 그다음 상자 깊이 둘의 패널(336px. 서비스: 그 단계의 사진이 채웁니다)에 벤토의 작은
카드처럼 놓은 조각 하나. `calendar`, `files`, `doc`, `cursor`는 쓰지 않습니다. 카드 사이에 화살표나 선은 없습니다.

**1024~1279에서.** 카드 둘, 그다음 셋째가 행 전체를 차지합니다. **768과 390에서.** 한 열.

**문구.** 제목에 개수를 넣습니다. 예시, Ledgewick: "Set up Ledgewick in 3 steps"; "Upload your receipts" /
"Drop in PDFs or phone photos."; "Check the matches" / "You confirm the few it is unsure about."

**모션.** 테크: 첫 카드가 루프하고 나머지는 정지합니다. 연쇄하거나 시차를 두는 일은 절대 없습니다.

**흔한 실수.** 화살표 또는 계단식 카드, 거대한 디스플레이 숫자, 높이가 다른 패널.

# 사진, 객실, 서비스, 사람

## photo-band

**쓰임새.** 페이지의 미디어 섹션(리듬 `media-band`, 제품과 서비스이며 장소에는 절대 쓰지 않습니다). 섹션의
레이어로서 화면 전체에 걸친 사진 한 장과, 그 사진의 고요하고 어두운 부분 위의 헤드라인.

**1440에서.** `main`에 한 화면의 `section.photo-band.photo-band--bleed`: 레이어로서의 `img`, 그다음 `.wrap` 안에
`div.photo-band__text`: 최대 여덟 단어의 h2, 한 줄, 선택적인 `.link`를 사진의 고요한 쪽에 둡니다(`--left`, 또는
옅은 크롭 위의 어두운 글자는 `--light`). 스크림, 그라디언트, 상자는 없습니다. 음소거된 필름(테크 전용)은 일시정지
버튼과 함께 재생됩니다.

**390에서.** 고요한 영역이 있는 사진의 폰용 크롭, 또는 그 아래 바탕 위에 글자.

**문구.** 예시, Brinwood(포르투에서 만든 스탠딩 데스크): "Built to order in Porto"; "Each desk is cut, oiled and
tested in our workshop before it ships."

**흔한 실수.** 한 페이지에 띠 둘, 피사체나 복잡한 영역 위의 글자, 히어로의 사진을 다시 씀.

## photo-pair

**쓰임새.** 사진 둘을 나란히: 안과 밖, 디테일과 전체, 작업 사례 둘. 무거운 섹션 사이의 가벼운 섹션.

**1440에서.** 위에 h2와 한 줄, 그다음 `span-6`의 사진 둘이 든 `.grid`, 4:5 또는 4:3, 비율 하나, 빛 하나. 그 아래에는
아무것도 없으며, 그것들이 보여 주는 것은 위의 줄에서 말합니다.

**390에서.** 한 열.

**흔한 실수.** 빛이 다른 사진 둘, 그림 아래의 캡션이나 제목, 셋 이상(셋짜리 행을 쓰세요).

## line-up

**쓰임새.** 제품의 모델이나 크기를 그림이 먼저, 각각 시작 가격과 함께 보여 구매자가 고를 수 있게 합니다(좋은
제품 사이트 15곳 중 8곳이 라인업을 일찍 보여 줍니다).

**1440에서.** `.section-head.section-head--row`(h2 "Three sizes", `.link` "Compare sizes"), 그다음
`a.tile.span-4` 셋(넷이면 `span-3` 넷)이 든 `.grid`로, 각각 카드입니다. `--g-alt` 위의 누끼(`object-fit:
contain`, 32px 안쪽) 또는 한 각도에서 찍은 사진이 위에 오고, 그다음 카드의 패딩 안에 `h3`의 이름, "from €1,290",
팩트 한 줄("Top 140 x 70 cm · 65 to 130 cm")이 옵니다.

**390에서.** 한 열, 또는 165의 2열.

**시각 요소.** 모든 모델이 한 배경에서 한 축척으로, 또는 한 카메라 각도로. 기술 제품은 크기별로 클라이언트의 렌더를
보여 줄 수 있습니다. 모든 모델의 그림이 없는 라인업은 두지 않습니다.

**흔한 실수.** 체크 표시와 추천 배지가 있는 요금제 카드, 월 요금, 뒤섞인 각도와 축척.

## rooms-list

**쓰임새.** 임대하는 방, 캐빈, 스튜디오. 장소에서 방은 `sections.md` 4절(객실: 타일, 행 또는 측면)입니다.
방이 있는 서비스나 제품(코워킹 공간)도 같은 타일을 씁니다. 방 전체의 4:3 사진, 이름, 팩트, 시즌이 붙은 시작
가격, "Book this room".

**흔한 실수.** 체크나 배지가 있는 요금제 카드로 만든 방, 사진 대신 들어선 캘린더, 시즌 없는 가격, 좌우가 교대되는
방.

## services-list

**쓰임새.** 클리닉, 회사, 업종이 하는 일을 서비스마다 한 줄과 시작 가격으로: 작업물 사진 한 장 옆의 목록이며
아이콘 카드 그리드는 절대 아닙니다.

**1440에서.** `.grid`, 위쪽 정렬: `span-5`에 h2, 한 줄, `ul.rows`(서비스마다 `span.rows__name`, `<p>` 줄,
`span.rows__value` "from €95". 목록 아래에 `.link`), `span-6 start-7`에 사진(`.frame.frame--photo`, 4:5 또는
4:3).

**390에서.** 텍스트와 목록이 먼저, 사진은 그 아래 48px.

**문구.** 예시, Halden Dental: "Check-up and clean" / "Every six months, 40 minutes" / "from €95".

**흔한 실수.** 아이콘 카드로 만든 서비스, 빠진 가격, 여덟 행 초과(페이지로 링크하세요).

## peek-list

**쓰임새.** 포인터, 포커스, 탭이 닿은 행에 따라 바뀌는 사진 한 장 옆의 짧은 목록: 스튜디오의 방, 클리닉의
치료, 빵집의 빵 종류. 모든 행에 자신의 사진이 필요하며, 더 적다면 services-list를 씁니다.

**1440에서.** `starter.html` `peek-list`: `.grid[data-peek]`, 위쪽 정렬: `span-5`에 세 개에서 여섯 개의
`li[data-peek-to][tabindex="0"]`(이름, 잉크색 한 줄, 오른쪽에 값)가 든 `ul.rows`, `span-6 start-7`에 행마다
`img.frame__img[data-peek-for]` 하나를 담은 사진 프레임(첫째를 뺀 나머지는 `hidden`, 지연 로딩 없음). system.js가
사진을 교체하고(다른 종류에서는 즉시, 테크에서는 200ms 페이드) 보이는 행에 표시합니다.

**768과 390에서.** 목록이 먼저, 사진은 그 아래 48px. 행을 탭하면 바뀝니다.

**흔한 실수.** 자기 사진이 없는 행, 같은 사진 두 번, 사진 위의 캡션, 여섯 행 초과, 오른쪽에 둔 목록.

## people-row

**쓰임새.** 고객이 만나게 될 사람들을 서비스나 소규모 제작자에 맞게 각각 초상과 함께 보여 줍니다. 브리프가
주는 실제 팀만 씁니다.

**1440에서.** `.section-head`, 그다음 `.tile.tile--portrait.span-3` 카드 넷이 든 `.grid`: 위에 초상(4:5), 그다음
카드의 패딩 안에 `h3`의 이름, 직책, 하는 일에 대한 한 줄.

**390에서.** 165의 2열, 이름은 카드 안 그 아래에.

**흔한 실수.** 스톡 또는 지어낸 초상, 뒤섞인 빛과 바탕, 여덟 명 초과.

# 콘텐츠 종류별 섹션

## integrations-grid

**쓰임새.** 제품이 어떤 도구와 파일 형식과 함께 작동하는지를 실제 원색 아이콘으로 보여 줍니다(하우스 규칙).
무엇이 제품에 데이터를 공급하는지가 핵심이라면 기능 섹션 안에, 스포크에 실제 아이콘을 단 `fanin-warehouse` 또는
`hub-tools` 다이어그램 카드를 씁니다. 도구가 여덟 개까지면 카드 넷, 큰 그리드는 브리프가 나열한 도구가 9개 이상일
때만 씁니다.

**1440에서.** 카드 넷: `.section-head`, 그다음 `article.card.card--row.span-6` 넷이며, 각각 도구를 이름으로 댄
제목("Syncs with Notion and Dropbox"), 두 줄, 그리고 조각 하나가 든 패널(336px). `integrations`는 앱을
클라이언트의 실제 도구로 바꿔 `.at-rise.fit`로 낮게(`--fit-max: 380px`, `--ay`와 `--ay-sm`은
`calc(100% - 180px)`), `files`는 실제 파일과 아이콘으로 `.at-corner.wide`(`--w: 680px`), 또는 중앙에 제품, 스포크에
실제 도구를 둔 허브 다이어그램(`hub-tools`). 큰 그리드: `span-12`의 `.frame`(패딩 48px)에 72px 타일 여덟 개를
가로로 놓고(열 간격 24px, 행 간격 32px), 각각 실제 아이콘 아래 `.t-label`의 도구 이름. "See all integrations" 링크는
없습니다(한 페이지짜리 사이트에는 보낼 곳이 없습니다).

**390에서.** 카드는 한 열, 타일은 64px로 가로 넷.

**시각 요소.** `icons.mjs fetch`로 받은 아이콘을 원래 색으로 씁니다(`icons.md`). 직접 그리거나 색을 입히지 않습니다.

**모션.** 테크: 첫 카드가 루프하고(또는 허브가 맥박칩니다), 나머지는 정지합니다.

**흔한 실수.** 직접 그렸거나 색을 바꾼 로고, 제품이 지원하지 않는 도구, 카드 하나에 타일 다섯 개 초과.

## calendar-frame

**쓰임새.** 제품이 다루는 날짜를 클라이언트의 실제 달에, 그 용도 옆에 보여 줍니다. 테크 전용이며 실제 날짜를
씁니다.

**1440에서.** split-text-left와 같되, 달이 온전히 보이도록 프레임을 모든 너비에서 한 높이로 둡니다(page CSS
`#dates .frame--split { --ratio: 0px; min-height: 600px }`). 붙여 넣은 `calendar` 하나만 `.at-rise.fit.to-edge`로
48px 아래에 둡니다(`--fit-max: 440px; --ax: max(48px, 50% - 220px)`). 두 번째 조각은 없습니다.

**390에서.** 텍스트가 먼저, 프레임은 높이 600, 캘린더는 폰 레이아웃으로.

**문구.** 그 날짜가 무엇을 위한 것인지 말하는 제목. 예시, Keelday(요트 학교용 예약): "Plan the season's
courses".

**시각 요소.** 캘린더의 `meta.json`이 말하는 대로 달 라벨, `data-month`, 1일의 요일에 맞춘 앞쪽 `.is-out` 날짜,
모든 실제 날짜의 `data-d`, `data-start`/`data-end`, `is-mark` 하나, `[data-ev]` 행 셋을 설정합니다. `is-today`는
현재 달에만 씁니다.

**흔한 실수.** 1일의 요일이 틀림, 키트의 샘플 달, 확대되었거나 행 중간이 잘린 캘린더.

## timeline-rail

**쓰임새.** 날짜가 붙은 순간 넷을 한 줄에 순서대로, 각각 작은 패널과 함께: 릴리스, 연혁. 소프트웨어와 제품
전용이며 장소에는 절대 쓰지 않습니다.

**1440에서.** h2와 `.link`가 있는 `.section-head--row`. 48px 아래에 `ol.grid.rail`: `li.span-3` 넷, 각각 위에
`.panel`(200px), 그다음 레일 행(page CSS: 다음 열까지 이어지는 1px 선, 8px의 정지한 점, 최신은 `--accent`), `.t-label`의
날짜, `.t-card`의 제목, 최대 10단어의 한 문장.

**390에서.** 한 열, 레일은 세로.

**모션.** 루프는 많아야 하나, 최신 패널에서(테크). 레일의 어떤 것도 움직이지 않습니다.

**흔한 실수.** 지그재그로 놓인 점, 맥박치는 점, 높이가 다른 패널.

## menu-in-type

**쓰임새.** 사진 옆에 읽기 좋은 글자로 쓴 메뉴 또는 가격표. 장소에서는 `sections.md` 4절(메뉴 또는 가격: 열린
그룹, 탭 없음)입니다. 무게나 크기로 파는 제품도 같은 방식으로 읽힙니다("250 g · €14").

**흔한 실수.** 들쭉날쭉한 가격 또는 두 가지 통화 형식, 카드 하나에 요리 하나씩, PDF나 이미지로만 둔 메뉴, 탭 또는
아코디언.

## visit-map

**쓰임새.** 장소가 어디에 있고, 언제 열고, 어떻게 가는지를 실용 정보(주차, 반려견, 단차 없는 접근, 체크인)
두 개에서 여섯 행과 함께 보여 줍니다. 쇼룸, 스튜디오, 문이 있는 서비스에 씁니다. 장소에서 방문 섹션은 `sections.md`
4절(Visit)이며 이 레시피는 지도만 다룹니다.

**1440에서.** 페이지의 분할: 텍스트(h2, 도로명과 지구로 쓴 `<address>`(브리프에 도로명이 없으면 지구, `copy.md`),
`data-tz`가 붙은 `dl.hours`의 영업시간, 브리프가 줄 때만 전화와 이메일, 주 행동과 Get directions(브리프에 도로명이
있을 때. 지구만 있으면 "See the area", 도시만 있으면 지도 링크 없음)). 오른쪽에 거리 지도: 브리프가 주는 도로명에 한해
OpenStreetMap에서 구운 `fx-map`(`effects-creative.md`)에 핀을 도로선 위에 두며, 다른 종류에서는 정지 상태로 둡니다.
그 외에는 가게 앞 사진.

**390에서.** 텍스트가 먼저, 지도 또는 사진은 너비 342.

**문구.** 예시, Fenn(도자기 스튜디오): "Visit the studio"; "Book a class", "Get directions".

**흔한 실수.** 지도 임베드 또는 스크린샷, 브리프가 주지 않은 거리의 지도, 다른 페이지에서 움직이는 경로, 지도 위의
출처 표기(푸터 줄에 합칩니다), 방문자 시계로 계산한 오늘.

## booking-form

**쓰임새.** 장소나 서비스 페이지의 단 하나의 과제: 예약 요청을 보내는 것입니다. 클라이언트가 시스템으로 예약을
받는다면 그 링크가 대신 버튼이 됩니다.

**1440에서.** 페이지의 분할: 왼쪽에 텍스트(h2 "Book a room", 다음에 일어나는 일, 브리프가 줄 때만 전화와 이메일).
오른쪽에 `--g-alt` 위의 폼(패딩 48px, 사진, 질감, 유리 위에는 절대 얹지 않음)이 장소라면 방이나 카운터 사진 옆
또는 아래에 옵니다(`sections.md` 4절 예약): 날짜, 인원, 이름, 이메일, 필드는 많아야 여섯, 주 행동이 있는
`.btn-row`, 상태 줄과 답장 줄. `starter.html` `booking-form`이며 system.js가 구동합니다(`system.md`의 양식).
브리프가 클라이언트의 폼 주소를 주면 `data-endpoint`로 보내고, 아니면 `action`은 `.example`의 `mailto:`이며 보고서에
나열하는 대체물입니다. 보이는 라벨, 필드 아래의 각 오류, 각 필드에 필요한 type과 autocomplete. 영어가 아닌
페이지에서는 `type="date"`가 아닌 텍스트 필드를 씁니다.

**390에서.** 텍스트가 먼저, 폼은 전체 너비에 행마다 필드 하나.

**문구.** 라벨은 들어갈 내용을 말합니다("Arrival", "Guests"). 버튼은 주 행동 단어와 글자 그대로 같습니다. 답장이
언제 오는지를 한 줄로 말합니다("We reply within a day").

**흔한 실수.** 어디로도 보내지 않는 폼, 여섯을 넘는 필드, 뒤에 전송이 없는 성공 메시지, 유일한 라벨로 쓰인
플레이스홀더, 빨간색으로만 또는 맨 위에만 표시한 오류, 모달.

## client-slots

**쓰임새.** 클라이언트 자신의 트레일러, 키 아트, 인엔진 스크린샷, CAD 렌더, 분해 모델 또는 모션 비디오를,
브리프가 클라이언트에게 있다고 말할 때 다룹니다(`sections.md` 1절). 각각은 지금은 완성된 것처럼 읽히고 나중에
클라이언트의 파일이 오면 한 줄만 바꿔 받는 프레임을 얻습니다. 테크 페이지(소프트웨어, 게임, 하드웨어). 제품 페이지의
CAD 프레임도 포함합니다. 대체물은 실시간 검색에서 건진 사진입니다(`photos.mjs search`, `photos.md`: 게임의 배경,
사용 중인 그 종류의 제품). 브리프가 3D를 요청하면 클라이언트 자신의 사양으로 만든 제품 렌더 스틸입니다. 분위기용
스톡, 도면, 비어 있거나 회색인 프레임은 절대 안 되며, 페이지의 어디에도 대체물이라고 말하지 않고, 보고서에
나열합니다.

**주석.** 모든 슬롯은 클라이언트 팀이 검색할 수 있는 주석 하나로 시작합니다.
`<!-- CLIENT FILE trailer: assets/client/trailer.mp4 (1920x1080, H.264, the 60 s trailer) and
assets/client/trailer.jpg (its poster); stand-in poster: <spec>-<view>.webp -->`. 보고서는 각 슬롯을 나열합니다:
그 이름, 파일, 비율, 대체물.

**트레일러 또는 모션 영상 프레임.** 히어로(또는 세계관 섹션) 다음의 자체 섹션으로, 위에 h2를 두고 프레임이 wrap
전체에 걸칩니다: `figure.frame.frame--photo.fit-screen`(page CSS `--ratio: 56.25%`. 16:9에서 wrap 전체에 걸친
프레임은 1440x900에서 높이가 약 700px이며 제목까지 합치면 한 화면보다 크므로, `fit-screen`(`layout.css`: 제목 아래에
한 화면이 남기는 높이이며 최대 720px, 1024px 아래에서는 태블릿과 폰이 16:9를 유지하도록 `auto`) 또는 프레임의
`max-height`가 섹션을 한 화면으로 유지합니다. 그러면 contain된 포스터가 어두운 바탕에 레터박스로 놓입니다)에
`<video class="frame__img" playsinline preload="none" poster="<the stand-in still>">`를 담으며, 포스터는 이미
그 영상의 첫 프레임처럼 읽히는 대체 사진입니다(게임: 그 배경을 가장 넓게 담은 사진. 하드웨어: 작업 중인 같은 종류의
기계). 재생 컨트롤은 실제로 작동하거나 아예 없어야 하며 죽은 컨트롤은 안 됩니다. 파일이 있으면: `controls`,
`preload="metadata"`, `<source src="assets/client/trailer.mp4" type="video/mp4">`, 클라이언트의 포스터. 없으면:
`<source>`와 `controls`가 없고(없는 파일이나 죽은 컨트롤 바는 깨진 프레임입니다), 사진 포스터가 프레임을
덮습니다. 렌더 스틸(브리프가 3D를 요청할 때만)은 투명하므로, 비디오에도 `.slot__poster`와 page CSS
`.frame > .frame__img.slot__poster { object-fit: contain }`을 붙이며(키트의 `cover`는 스틸을 제품의 한 조각으로
잘라 냅니다), 프레임은 세계관 또는 페이지의 어두운 바탕이고 그 스틸도 그 바탕 위에서 만듭니다(`make-posters.mjs
--grounds dark`: 밝은 바탕의 스틸은 어두운 곳에서 옅은 바닥 얼룩이 남습니다). 재생 컨트롤은 `<a
class="ly-play" href="<the trailer's page the brief gives: the store page>" aria-label="Watch the trailer">`와 그
`.ly-play__disc`입니다. `.frame`은 가운데 정렬 flex 상자이지만 system.css의 규칙 `.frame > :not(canvas, .stage,
.loop-pause, .frame__fx, .frame__img, [data-print], [data-scene], .print3d)`가 컨트롤을 `position: relative`로
만들기 때문에, `.ly-play`의 `left`와 `bottom`(각각 `--s-6`)이 디스크를 정중앙에서 오른쪽 위로 32px 옮길 뿐
모서리로 보내지는 않습니다. page CSS `.frame > .ly-play { left: auto; bottom: auto }`가 그것을 가운데에 놓습니다.
그런 page CSS가 없으면 컨트롤도 없으며, 파일이 도착할 때까지 포스터가 섹션의 정지 이미지로 남습니다. 파일이 있으면
테크의 모션 비디오는 대신 음소거되고 반복 재생될 수 있으며(`autoplay muted loop`) 일시정지 버튼을 둡니다
(`motion.md`). 모션 감소 설정과 폰에서는 포스터만 보이고, 소리는 절대 내지 않습니다.

**스크린샷 띠.** 게임이 플레이되는 모습으로 보여 주는 세계: 캡처처럼 프레임을 씌운 셋에서 다섯 프레임, 16:9,
같은 크기(`.wrap`에 `trio` 또는 넷짜리 행. 폰: 한 열), 각진 모서리 또는 페이지 반경, 기기 크롬 없음, 그림자 없음,
캡션 없음. 파일이 있으면: 각
`<img class="frame__img">`를 `figure.frame.frame--photo`에 둡니다. 없으면: 각 프레임에 실시간 검색(`sections.md` 3절 게임. `photos.md`, 라이브 검색)에서 건진 게임 배경의 대체 사진 한 장을 담고, 스트립 전체에 하나의 그레이드를
쓰며, 같은 장소나 같은 시리즈가 둘 들어가지 않게 하고, `object-fit: cover`로 16:9로 크롭합니다. 브리프가 3D를
요청하면 대신 각 프레임에 세계관 사양의 작업 장면 하나를 담고, 프레임 자체가 `[data-product]` 요소입니다
(`div.frame.slot`, page CSS `.frame.slot[data-product] { --ratio: 56.25%; background: <the world's water, fog or
night colour> }`. `layout.css`가 `.frame[data-product]`의 바탕을 지우므로 약한 선택자는 렌더를 흰색 위에 남깁니다).
스틸이며, `data-product-fill`이 1을 넘는 일은 절대 없습니다(테스트에서 프레임이 비어 그려졌습니다). "what you do"
카드로 쓰면 열린 카드 셋에서 다섯이며, 각각 캡처 위에 동사 하나입니다.

**CAD 또는 렌더 프레임.** 제품 전체의 클라이언트 CAD 렌더: 제품 섹션의 분할 프레임(`frame--split`) 또는 `bleed`,
렌더는 밝은 평평한 바탕 위에, 각진 모서리. 그 대체물은 다른 섹션이 쓰지 않는 제품 종류의 대체 사진이며(렌더 뷰는
브리프가 3D를 요청할 때만), 오브젝트의 세 섹션 중 하나로 셉니다. **분해도 프레임:** 부품 섹션의 그림이며,
클라이언트의 분해 모델, 없으면 부품의 클로즈업 사진입니다(`sections.md` 3절 제품).

**키 아트.** 히어로의 그림(`photo` 히어로의 사진, `film` 히어로의 포스터 또는 `product` 스테이지)과 세계관의 띠:
거기에는 배경의 대체 사진(렌더는 브리프가 3D를 요청할 때만), `assets/client/key-art.jpg`를 이름으로 댄 주석.

**흔한 실수.** 브리프가 이름을 댔는데 페이지가 빼 버린 슬롯, 비어 있거나 회색 또는 검은 프레임, 아무것도 하지 않는
재생 버튼, 없는 파일을 가리키는 `<source>`, 파일이 곧 온다고 말하는 캡션, 모든 슬롯에 같은 대체 사진 한 장.

# 가격과 질문

## pricing-three

**쓰임새.** 소프트웨어: 요금제 셋을 나란히, 가운데가 추천이며, 월간 또는 연간 전환은 선택입니다.

**1440에서.** 왼쪽 라인의 `.section-head`: "Pricing", 회색 한 줄, 그리고 전환(`role=tab` 버튼 둘). 48px 아래에
`.card.card--plan.span-4` 셋이며, 가운데가 `.is-featured`로 "Most popular" `.badge`를 달고 있습니다. 각 카드:
이름, 누구를 위한 것인지, "/month"가 붙은 `.price`, 두 모드 모두의 청구 줄, 전체 너비 버튼(`.btn--primary`는
가운데만), 포함 내용 5~7줄. 1024부터 각 카드는 그 행들의 서브그리드이므로 버튼과 줄이 정렬됩니다. 모든 가격에
`data-monthly`와 `data-yearly`를 둡니다.

**390에서.** 요금제 순서대로 한 열.

**문구.** 예시, Rotaro: "Priced per restaurant. Try any plan free for 14 days."; Team: "For restaurants with 15
to 50 staff", €59/month.

**시각 요소와 모션.** 바탕 없음, 정지. 테크에서는 이것이 페이지의 유일한 효과일 때 추천 요금제의 테두리가 빛날
수 있습니다(`fx-pricing`, 또는 `data-glow="edge-glow"`: 호버 또는 포커스 시 가장자리를 도는 빛 하나).

**흔한 실수.** 전환 시 높이가 변하는 카드, 가격과 맞지 않는 절약액, 구독이 아닌 것(제품, 장소)의 요금제.

## pricing-two

**쓰임새.** 무료와 유료 요금제, 또는 서비스의 고정 가격 둘. 둘 다 포함하는 것은 한 번만 말합니다.

**1440에서.** `.grid`: `span-4`에 h2 "Pricing", 회색 한 줄, 모든 요금제가 포함하는 것과 `.link`. `span-4 start-5`와
`span-4 start-9`에 `.card.card--plan` 둘(이름, 누구를 위한 것인지, 가격, 버튼, 5~7줄)이며, 추천은 `.is-featured`.

**390에서.** 한 열.

**흔한 실수.** 높이가 다른 버튼, 카드 안에 반복된 모든 요금제 공통 목록.

## comparison-table

**쓰임새.** 요금제 또는 모델, 혹은 제품과 현재 일하는 방식을 행별로 비교합니다.

**1440에서.** `.section-head`, 그다음 `role=table`과 그 역할이 붙은 `.grid` 행들: 기능은 `span-4`. 옵션 둘은
`span-4 start-5`와 `span-4 start-9`, 셋이면 `span-2`. `--g-main` 위의 헤더 행에 각 옵션의 이름, 가격, 버튼
(`.btn--primary`는 추천에만). 그룹 제목은 `.t-label`, 행은 48px에 각각 1px 규칙으로 닫고, `.sr-only` "Included"가
붙은 체크, 회색 대시("Not included") 또는 짧은 값. 고정되는(sticky) 것은 없습니다.

**390에서.** 각 옵션을 자신의 행 블록으로, 가로 스크롤은 절대 없습니다.

**흔한 실수.** 폰의 가로 스크롤, 그리드를 벗어난 열, 고정 헤더.

## faq

**쓰임새.** 구매자의 마지막 질문(가격, 데이터, 해지, 형식)을 모든 답변이 열린 채로 보여 줍니다. 495px 아래에서는
위 섹션에 합칩니다.

**1440에서.** 페이지의 분할: 왼쪽에 h2 "Questions", 회색 한 줄, `#contact`로 가는 `.link`(`mailto:` 또는 `tel:`은
브리프가 주는 주소나 번호가 있을 때만). 오른쪽에 `.faq`와 `.faq__item` 5~8개(`h3`의 질문, 그 아래 답, 각각 1px
규칙으로 닫음). 아코디언은 없으며 답변은 로드 시 열려 있습니다.

**390에서.** 한 열.

**문구.** 질문은 구매자의 말로 최대 60자, 답은 50단어 미만으로 답부터 시작합니다. 예시, Ferrow: "Can I cancel at
any time?" "Yes. Cancel in Settings and you are not billed again."

**흔한 실수.** 회사가 받고 싶어 하는 질문, 피해 가는 답, 닫힌 답.

# 마무리

마무리는 `footer.closing`의 1행(`layout-v4.md`)이며 푸터 자신의 바탕 위에 놓이고, 자체 띠가 되는 일은 없습니다.
주 행동을 글자 그대로 한 번 더 요청합니다.

## close-type

**쓰임새.** 큰 한 줄과 큰 주 버튼 하나. 어떤 종류에나 쓰며 그림은 없습니다. 버튼이 곧 그림입니다.

**1440에서.** `.closing__cta.close--type`: h2(최대 여덟 단어, 왼쪽 라인), 선택적인 `.t-small.muted` 줄(체험 조건,
영업시간), 그다음 `.wrap` 전체에 걸친 `a.btn.btn--primary.btn--xl`(높이 88px, 라벨은 디스플레이 서체 32px)이며
소프트웨어일 때입니다. 제품과 서비스에서는 너비 640, 높이 72입니다(그만큼 넓은 판은 클리닉에서는 퉁명스럽게
읽힙니다).

**390에서.** 버튼은 전체 너비, 높이 48px에 18px 라벨.

**문구.** 예시, Rotaro: "Plan next week's rota in ten minutes" / "Start free trial" / "Free for 14 days. No card
needed."

**흔한 실수.** 두 번째 버튼, 페이지의 다른 곳에 놓인 큰 버튼, 그 뒤의 바탕.

## close-photo

**쓰임새.** 장소, 제품, 서비스의 마무리: 장소나 사용 중인 제품의 사진 옆에 주 행동. 장소에서는 언제나 이
마무리입니다.

**1440에서.** `.closing__cta.close--photo`: 헤드 행(최대 여덟 단어의 h2, "Open today 7:30 to 16:00" 같은 한
줄, 주 행동), 그다음 링크까지 이어지는 클라이언트의 사진이 라인에서 라인까지, 위에서는 절대 쓰지 않았고 그 위에
글자도 절대 두지 않습니다. 장소: `span-5`의 1:1 사진과 그 옆의 글(`sections.md` 4절 마무리).

**390에서.** 글과 전체 너비 버튼, 그다음 사진.

**문구.** 예시, Fenn: "Book a Saturday wheel class"; "Three hours, €65, clay and firing included."; "Book a
class".

**흔한 실수.** 히어로의 사진을 다시 씀, 사진 위의 글자, 뷰포트까지 뻗은 띠.

## close-word

**쓰임새.** h2와 버튼, 그다음 `.wrap` 전체에 걸쳐 디스플레이 서체로 놓은 클라이언트의 이름. 소프트웨어, 제품,
서비스(장소의 `colour-band`에는 절대 쓰지 않습니다).

**1440에서.** `.closing__cta.close--word`: h2와 버튼이 한 헤드 행에, 그다음 이름이 라인에서 라인까지 한 줄로(중단점별
수작업 크기이며 transform으로 확대하는 일은 절대 없습니다).

**390에서.** 헤드는 쌓이고, 이름은 342에 걸칩니다.

**흔한 실수.** 1024에서 페이지가 담을 수 있는 것보다 큰 이름, 푸터 워드마크로 반복된 이름.

# 푸터

`footer.closing`의 2행: 한 바탕 위의 디렉터리와 법적 행(`system.md`).

## footer-columns

**쓰임새.** 기본 바탕 위의 조용한 푸터: 회사를 평이한 한 줄로, 사이트맵, 법적 행. 소프트웨어, 제품, 서비스.

**1440에서.** `starter.html`처럼: `span-4`의 회사 블록(로고, 그다음 `p.footer__lede`, 디스플레이 서체 28px의 최대
여덟 단어 한 줄), 내비게이션과 같은 이름과 순서의 `.footer__col.span-2` 넷, 각 링크는 페이지의 섹션이며 Contact는
`#contact`. 페이지에 있다면 뉴스레터 필드(한 번, "Subscribe"). 그다음 `.footer__legal`: 브랜드와 연도, Privacy,
Terms(Imprint는 브리프가 회사 자신의 정보를 줄 때만), 비어 있는 `.socials`, 마지막으로 크레딧 줄.

**390에서.** 열은 2열, 법적 행은 쌓입니다.

**흔한 실수.** 내비게이션과 다른 열, 빌드에 없는 페이지로의 링크, 직접 그렸거나 색을 입힌 소셜 아이콘, 푸터의 효과.

## footer-dark

**쓰임새.** Figma와 x.ai의 푸터: 어두운 바탕, 크게 놓은 이름, 링크 열. 소프트웨어와 제품(끝에 오는 하나뿐인
어두운 띠).

**1440에서.** `footer.closing.footer--dark.ground-inverse`: `span-4`의 회사 블록(마크와 디스플레이 서체 48px의 이름),
`.footer__col.span-2` 넷, 법적 행이 있는 `.grid`. 어두운 페이지에서는 system.css가 이것을 페이지보다 한 단계
어둡게, 위에 헤어라인과 함께 유지합니다.

**390에서.** 이름은 30px, 열은 2열.

**흔한 실수.** 그 바로 위의 두 번째 어두운 섹션.

## footer-visit

**쓰임새.** 장소 또는 지역 업체의 푸터: 어디에 있는지를 크게 놓고, 가는 길과 영업시간을 함께 두어 방문자가 다른
것을 필요로 하지 않게 합니다.

**1440에서.** `starter.html`(`links-visit`)의 `footer.closing.footer--visit`: `span-7`에
`address.footer__address`(도로명과 지구를 두 줄로. 브리프가 도로명을 주지 않으면 지구만. 장소에서는 32/40, 그 외에는
48px, 디스플레이 서체), 가는 길에 대한 한 줄(정류장, 도보 몇 분)과 `a.link` "Get directions"(OpenStreetMap 검색,
`copy.md`. 지구만 있으면 "See the area", 도시만 있으면 없음). `span-4 start-9`에 "Opening hours"와 `data-tz`가 붙은
`dl.hours`(system.js가 오늘을 표시). 그다음 내비게이션 행(로고, 내비게이션의 단어들, Contact), 마지막에 크레딧 줄이
있는 법적 행. 그다음 장소에서는 `colour-band`를 제외하고 이름을 디스플레이 서체 400으로 `.wrap` 전체에 넓게 놓습니다.
버튼은 없습니다.

**390에서.** 주소는 24~30px, 영업시간은 그 아래, 내비게이션 행은 줄바꿈됩니다.

**흔한 실수.** 방문 섹션과 다른 영업시간, 방문자 시계로 계산한 오늘, 푸터의 지도, 브리프가 주지 않은 이메일이나
전화번호를 인쇄함.

## footer-statement

**쓰임새.** 마무리와 푸터를 페이지의 조명 바탕(모래, 하늘, 세이지 또는 회화) 위의 설계된 한 덩어리로: 큰 한 줄,
전체 너비 버튼 하나, 그다음 열들(Figma의 마무리와 푸터). 테크 전용.

**1440에서.** `footer.closing.footer--statement`: system.css가 창의 양옆과 아래에서 8px 안쪽으로 `--r-lg` 모서리와
함께 들입니다. 마무리는 close-type과 같고, 열까지 96px, 법적 행.

**390에서.** 가장자리까지, 각진 모서리.

**흔한 실수.** 두 번째 큰 버튼, 그 위의 효과.

# 페이지 계획

종류별로 하나씩 다섯 개의 작동 사례(게임은 소프트웨어와 따로). 여러분의 것은 딜러가 뽑으므로 같은 종류도 매번
다르게 보입니다. 이웃은 레이아웃을 공유하지 않고, 분할은 한쪽을 유지하며, 고요한 섹션은 시각적인 섹션 둘 뒤에만
오고, 카드 레이아웃은 많아야 두 번 나옵니다.

## 소프트웨어

*Fernbill: 직원 2~20명 에이전시를 위한 청구서 발행.* 뽑은 것: 히어로 `split`, `nav-mega`, `footer-dark`, 마무리
`close-type`, 리듬 `dark-band`, 버튼 `pill`, 마크 `ring`. 효과 `painterly-landscape`는 히어로 프레임에, 카드 바탕
`grain-gradient`. 모먼트 하나, `word-highlight`(자체의 설명 섹션 하나).

순서: 히어로(`doc`으로 열린 청구서, 그 가장자리 위에 `notify` "Invoice 2041 paid"),
app-frame(`window`의 청구서 목록 옆에, `chat`으로 열린 청구서의 스레드와 그 고객), features-2x2(카드 바탕.
`notify`는 결제 매칭, `toggles`는 독촉 규칙, 청구서 하나를 원장 셋으로 나누는 lanes 다이어그램, `chat`은 고객의
질문), `word-highlight`가 있는 설명(자체의 한 화면 섹션), split-text-left(실제 영수증이 있는 `files`, 조명 바탕
그대로), 어두운 띠 위의 tabs-tour, 통합(스포크에 실제 아이콘을 단 `fanin-warehouse` 다이어그램 카드를 그 글 옆에),
pricing-three, faq, footer.closing. 로고 행 없음: 브리프가 고객을 지목하지 않습니다. 인용도 없습니다.

## 제품

*Brinwood: 포르투에서 주문 제작하는 원목 오크 스탠딩 데스크.* 뽑은 것: 히어로 `photo`, `nav-cards`,
`footer-columns`, 마무리 `close-photo`, 리듬 `media-band`, 버튼 `arrow`, 마크 `stack`.

순서: 히어로(실제 방 안의 데스크), product-statement(누끼와 팩트 셋: 하중 120 kg, 높이 65~130 cm, 3주 내 배송),
line-up(€1,290부터의 세 가지 크기), split-text-left(오크 상판: 나뭇결 사진), photo-band("Built to order in
Porto"), 다시 split-text-left(프리셋이 있는 핸드셋: 제품이 갖고 있지 않은 UI는 절대 보여 주지 않으므로 사진),
specs(프레임 사진 옆의 `rows--spec`), 증거(브리프가 주는 후기, 합침), faq(질문 넷), footer.closing. 평평한
바탕, 효과 없음. 히어로의 등장 효과와 자체 섹션의 뽑은 모먼트 하나.

**사진이 아직 없을 때**(*Pellum, 책상 램프*): 램프는 사진으로 보여 주며, 숨기지 않고 기본값으로 렌더를 쓰지도
않습니다. `photos.mjs search "desk lamp"`와 `"desk lamp detail"`이 대체 사진을 줍니다. 같은 구조의 책상 램프
전체, 그 다이얼이나 관절 클로즈업, 해 질 녘 책상 위에 켜진 램프, 제조사 이름이 읽히지 않는 것, 하나의 그레이드.
히어로(`deal.mjs --type product --has photo`)는 램프 전체를 담고, product-statement는 팩트 셋과 함께 다이얼
클로즈업을 보여 줍니다(부품). 그것이 하는 일은 분할로(책상 위의 따뜻한 빛 웅덩이, 프레임 가장자리에 잘린 램프.
사용), 사용 방법은 세 단계로, specs는 브리프가 이름을 대는 부품 브랜드의 실제 아이콘이 있는 `rows--spec`으로,
주문은 라이브 주문 카드(이름이 붙은 스와치로 된 마감, 배송, 가격)로. 램프 전체는 두 번, 모든 섹션에는 아니며.
faq, footer.closing. 평평한 바탕, 효과 없음, 도면 없음, 사진이 없다는 문구도 없습니다. 보고서는 모든 대체 사진과
찍어야 할 컷을 나열합니다. 3D를 요청하는 브리프(컨피규레이터, "돌아가는 모습을 보여 줘")만 대신 `product`
스테이지에 제품 렌더(`effects-objects.md`, 제품 렌더)를 받습니다.

## 게임

*Kelpmoor: 가라앉은 해안에서 즐기는 협동 항해 게임, Steam 출시 예정.* 뽑은 것: 히어로 `film`(브리프가 주는
트레일러), `nav-centre`, `footer-dark`, 마무리 `close-word`, 리듬 `media-band`, 버튼 `solid`, 마크 `wordmark`.
효과 없음(트레일러가 히어로의 모션). 모먼트 하나, `letters-assemble`(자체의 설명).

순서: 히어로(시네마 프레임 안의 트레일러 포스터, 클릭하면 재생. h1 "Kelpmoor, a co-op sailing game". "For 1 to 4
players. Coming to Steam in spring.". "Add to Steam wishlist"), 세계관(인엔진 샷 둘을 photo-pair로, 하나의
그레이드), `letters-assemble`이 있는 설명, 하는 일(열린 카드 셋, 각각 동사 하나와 인엔진 샷: 가라앉은 해안을
항해한다, 가라앉은 마을을 인양한다, 항구를 재건한다), 다시 media band로서의 세계관(키 아트를 꽉 채워, h2는 그
고요한 하늘 위에), 플랫폼과 에디션(실제 Steam, PlayStation, Epic Games 마크, `icons.mjs apps --tag gaming`.
Xbox와 Nintendo는 허용된 어떤 세트에도 없습니다. 콘솔은 글자로 이름을 대고 직접 그린 마크는 절대 쓰지 않습니다.
시작 가격), faq, footer.closing. UI 조각, 대시보드, 위젯은 어디에도 없습니다.

**아트 파일이 없을 때**(이름은 댔으나 제공되지 않았거나 아예 없음): 히어로는 배경 사진 위의 글자이며, 그 자리에
효과나 임의의 오브젝트를 두지 않습니다. `photos.mjs search "flooded village"`, `"harbour at dusk"`, `"fishing boat
at night"`이 대체 사진을 주며, 원래 크기를 유지합니다. 하나의 그레이드, 읽히는 것 없음, 얼굴 없음. 뽑기
`deal.mjs --type software --kind gaming --has setting`: 히어로 `photo`, 가장 넓고 고요한 프레임(어두운 하늘 아래
해 질 녘의 물)을 꽉 채워, h1 "Kelpmoor, a co-op sailing game"을 상자 안에 크게 놓고 그 아래 "Coming to Steam in
spring."과 "Add to Steam wishlist". 그다음 트레일러 프레임(client-slots: 항구 프레임이 포스터, 재생 컨트롤은
브리프가 주는 스토어 페이지의 트레일러로). 세계관: 어두운 띠에 꽉 채운 두 번째 프레임, 그 위에 h2. 하는 일:
스크린샷 스트립을 열린 카드 셋으로, 각각 대체 프레임 하나(16:9) 위에 동사 하나(client-slots). 뽑은 모먼트를 담은
섹션 하나. 실제 스토어 아이콘이 있는 플랫폼. faq. footer.closing. 뽑힌 경우 하나뿐인 효과는 자체 섹션에 놓으며
사진 위에는 절대 두지 않습니다. 어디에도 "stand-in"이라고 적지 않으며, 각 슬롯은 주석에 클라이언트의 파일을
이름으로 댑니다. 보고서는 모든 대체 사진과 그것을 바꿀 아트를 이름으로 댑니다. 렌더한 슬루프와 부두
(`effects-objects.md`, 제품 렌더)는 브리프가 3D를 요청할 때만 씁니다.

## 장소

*Fenn: 라이프치히 플라그비츠, 카를하이네 거리의 도자기 스튜디오 겸 가게.* 뽑은 것: `nav-split`, `footer-visit`,
리듬 `surface-pairs`, 버튼 `block`, 마크 `arc`, 제안 `tall-small`, 장소 `trio`, 타입 모먼트 `address`, 방 없음.

순서: 장소 히어로(아침 빛 속의 공방. "Pottery classes in Leipzig-Plagwitz". "Wheel classes on Saturdays, open
studio Tuesday to Sunday from 10.". "Book a class"), 방문(2화면: `.wrap` 전체에 걸쳐 크게 놓고 지도에 링크한
"Karl-Heine-Straße, Plagwitz". 그 주의 영업시간. 단차 없는 입구. 가게 앞 4:3), 서피스 띠 위의 제안(`tall-small`
옆에 두 개의 열린 그룹으로 수업과 가격: 물레 앞의 수업은 크게, 유약 바른 그릇은 작게, 각각 그 수업으로 링크),
장소(`trio`: 공방, 마르고 있는 도자기 선반, 굽을 깎는 손, 상단은 한 줄에), 예약(수업 공간 사진 옆의 폼),
footer.closing(`footer-visit`, 이름은 12vw로 제한, 하나뿐인 크레딧 줄, `data-tz="Europe/Berlin"`). 사진 열네
장은 모두 스튜디오 자신의 것. 효과 없음. 히어로의 등장 효과와 뽑은 모먼트 하나. 링크된 모든 사진은 포인터 아래에서
1.03으로 확대됩니다.

## 서비스

*Halden Dental: 말뫼 중심가의 치과.* 뽑은 것: 히어로 `split`, `nav-mega`, `footer-visit`, 마무리
`close-photo`, 리듬 `surface-pairs`, 버튼 `tonal`, 마크 `dots`.

순서: 히어로(진료실, 4:5), services-list(접수처 사진 옆에 €95부터의 치료 여섯), steps(온라인 예약, 검진, 계획: 각각
사진 한 장), people-row(브리프가 이름을 대는 치과의사 넷), pricing-two(Check-up과 Check-up with cleaning을
고정 가격으로), faq(브리프가 주는 환자의 인용과 합침), 주소와 영업시간이 있는 booking-form, footer.closing. 평평한
바탕, 효과 없음.
