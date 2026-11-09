# 모먼트

모먼트는 페이지에서 어워드 사이트다운 부분입니다(하우스 규칙 8). 방문자가 기억할 만한 일을 페이지가 하는 한두 곳이며, 자기
섹션 안에 있습니다. 그 밖에 페이지에는 히어로의 등장 효과와 호버 계층(`motion.md`, 규칙: 모든 페이지는 세 곳에서 움직입니다)만 있습니다. 각 모먼트는
`assets/moments/<id>/` 폴더(`moment.js`, `moment.css`, `meta.json`, 완전한 `demo.html`)이며, `index.json` 이 목록을 담고
`gallery.html` 이 데모를 링크하고 `moments.js` 가 실행합니다. 폴더는 열여덟 개입니다. 다섯 개는 은퇴했고(`headline-arrives`,
`closing-lift`, `lines-rise`, `window-parallax`, `word-rotate`), 열세 개는 종류별로 뽑습니다(아래).

**해당 페이지: 모든 페이지.** 모든 종류에서 짧은 페이지는 모먼트 하나, 긴 페이지(섹션 여덟 개 이상)는 서로 다른 두 섹션에 둘,
셋은 절대 안 됩니다. 장소의 짧은 페이지(사진 8장 미만, `sections.md` 4절)는 타입 모먼트를 건너뜁니다. 그 하나의 모먼트는
섹션의 사진에 쓰는 `picture-develops` 이고(`--fits section --photo`, `photo-chapters` 가 나오면 `--exclude photo-chapters`
를 붙여 다시 뽑음), 사진이 없으면 자기 한 화면짜리 선언 섹션의 `word-highlight` 이므로 페이지는 네 화면이 됩니다.

| 페이지 종류 | 뽑는 풀 | 룩 |
|---|---|---|
| place (cafe, bakery, guesthouse, shop, gym. 문이 있는 스튜디오는 `--page studio` 가 service로 읽히므로 `--page place` 로 넘김) | `photo-chapters`, `picture-develops` (film), `word-highlight` | 사진과 글자 |
| product (site-kind other) | `photo-chapters`, `pinned-chapters`, `picture-develops` (film), `word-highlight` | 사진과 글자 |
| service (firm, clinic, agency, trade) | `photo-chapters`, `pinned-chapters`, `picture-develops` (film), `word-highlight` | 사진과 글자 |
| software, gaming, tech | 그 종류를 나열한 열한 개: `photo-chapters` 와 `picture-develops` 를 뺀 뽑을 수 있는 모든 모먼트 | 2.5.1 이전과 같음 |

다른 종류에 이것들을 쓰는 이유: 각각 고객 자신의 사진이나 글이 이끌고, 자기 섹션 안에서만 움직이며, WebGL 비용이 없고,
차분하게 읽힙니다(호텔, 법률 사무소, 웨딩 사진가). 쓰지 않는 것: 셰이더, WebGL, 액체나 포인터 효과가 있는 모든 것
(`liquid-hover`, `liquid-type`, `cursor-spotlight`), 그래픽 트릭으로 읽히는 모든 것(`iris-opens`, `line-carries-colour`,
`letters-assemble`, `picture-develops` 의 하프톤, 그리고 `giant-type-pass`: 글자 안의 사진은 템플릿 트릭으로 읽히고 따뜻한
팔레트를 흐리며 패럴랙스입니다), 반복(`marquee-row`), 카운트(`counter-rolls`). 그런 페이지에서 긴 페이지의 둘은 선언 모먼트
(`word-highlight`)와 섹션 모먼트 하나(사진), 또는 chapters 모먼트 옆에서 현상되는 사진(두 종류: 하나는 들어올 때 한 번 실행되고
다른 하나는 스크롤을 따라감)입니다. `photo-chapters` 와 `pinned-chapters` 는 한 페이지에 함께 두지 않으며 역할이 다릅니다.
photo-chapters는 한 번에 한 장이 패널에 얹히는 전체 폭 사진으로 이야기를 들려주고, pinned-chapters는 한 프레임 옆에 나열된
단계(예약이나 주문이 진행되는 방식)를 따라갑니다. 모먼트는 기술 페이지의 큰 장면(`effects-usage.md`)에 대해 그 박자 중
하나로 계산됩니다.

## 뽑습니다. 취향으로 고르지 않습니다

```bash
# a place, product or service page: one on a short page, two on eight sections or more
node <skill>/scripts/moments.mjs pick --page place|product|service --count 1|2 --fits section,statement \
  --photo --history .taste-skill/history.json
# a software, gaming or tech page (less a hero moment)
node <skill>/scripts/moments.mjs pick --page <kind> --count 1|2 --fits section,statement \
  [--scene <id>] [--effects <ids>] [--contexts <n>] [--photo] --history .taste-skill/history.json
# a hero moment on tech (0 or 1): the same with --count 1 --fits hero; kept only when the dealt hero lists it
```

- **`--page`** 는 페이지의 종류입니다(`SKILL.md` 1절: `software`, `gaming`, `tech`, `place`, `product`, `service`.
  `ai`, `saas`, `technical-product`, `cafe`, `bakery`, `guesthouse`, `hotel`, `shop`, `studio`, `agency`, `firm`,
  `clinic` 과 몇 가지 더도 읽습니다). 어떤 종류도 가리키지 않는 단어(`other` 는 세 종류)는 종료 코드 1로 뽑기를 멈춥니다.
  어느 쪽인지 말해 줍니다.
- **`--photo`** 는 모든 place, product, service 페이지에 붙입니다(모두 사진이 있으므로). 없으면 사진 모먼트가 빠지고 긴
  페이지는 둘을 뽑을 수 없습니다.
- **`--fits section,statement`:** 선언은 자기만의 섹션이므로, letters, liquid type, word-highlight, counter는 이것이 있을
  때만 나옵니다. `section` 만 쓰면 그중 어느 것도 뽑지 않습니다.
- **어떤 종류도 `--exclude` 가 필요 없음:** 각 풀은 `meta.json` 에서 그 종류를 나열한 것들입니다(위의 짧은 페이지의
  `photo-chapters` 가 유일한 예외).
  `picture-develops` 는 place, product, service에서 film 룩으로만 뽑습니다. 하프톤 룩은
  `data-moment-opts='{"look": "print"}'` 와 인쇄소 데모로 키트에 남아 있을 뿐 뽑지는 않습니다. 뽑은 장면의 쌍둥이와
  avoidMoments는 `--scene <id>` 자체가 뺍니다.
- **히어로 모먼트**(0 또는 1, 큰 장면 히어로에는 절대 안 둠)는 뽑은 히어로가 `heroes.json`
  (`moments[].id`)에 나열할 때만 유지합니다. `split` 과 `photo` 의 `liquid-hover`, `product`, `collage`, `film`,
  `centred` 의 `cursor-spotlight`, `statement`(기술, 여섯 단어 이하의 제목)의 `liquid-type` 이며 나머지에는 없습니다. 터치가
  아닐 때만. 모션 줄이기에서는 정지. 전체에서 모먼트는 최대 둘입니다.
- **WebGL 예산.** 한 페이지는 라이브 컨텍스트를 최대 4개까지 가집니다(`perf.md`). 뽑기는 페이지가 이미 쓰는
  것을 합산하고, 자신의 `webgl`(`meta.json` 에 있으며 `liquid-hover` 만 1)이 합계를 4 위로 올리는 모먼트는 뽑지 않습니다. 큰
  장면은 `--scene <id>` 로 넘기고(그 `webgl` 은 `assets/scenes/index.json` 에서 읽음), 뽑은 효과는 `--effects a,b` 로(각각
  하나로 계산, 최악의 경우), 그 밖의 것은 `--contexts <n>` 으로(캔버스가 있는 객체, 컴포넌트) 넘깁니다. 뽑기는 도달한
  합계를 출력합니다.
- **뽑기의 나머지.** 서로 다른 섹션에 둡니다. 기록의 `moments` 목록은 주기로 읽습니다. 들어맞는 모든
  모먼트를 한 번씩 뽑고 나면 다음 주기가 빈 상태로 시작하므로, id는 다른 모든 것이 나온 뒤에야 돌아오며 바로 다음에 다시 나오지
  않습니다(마지막에 뽑은 셋은 주기가 끝나도 제외 상태). 같은 종류 둘은 안 됩니다(호버와 liquid는 하나로 계산: 한 페이지에
  포인터 효과 하나). 같은 슬롯 둘도, 서로 피하는 둘도 안 됩니다. 사진이 필요한 모먼트는 `--photo` 가 있을 때만. place,
  product, service 페이지에서는 선언 하나와 섹션 하나, 또는 두 종류(`picture-develops` 와 chapters 모먼트)입니다. 각 id와 그
  섹션과 목적을 계획에 적습니다(`motion.md`, 움직이는 이유). 실을 것이 없는 모먼트를 뽑았다면 `--exclude` 에 더해 다시
  뽑습니다.
- **은퇴**(`meta.retired`, 가중치 0, 절대 뽑지 않음): `headline-arrives`(이제 모든 히어로가 모션 계층을 통해
  등장하며, `motion.md`, 히어로의 등장(모든 종류), 제목도 움직이는 모먼트는 두 번째 등장 효과가 됨)와 `closing-lift`(자기만의
  마무리 띠가 필요하고 그 글자가 사진 위 그라디언트 위에 서 있음). 2.5.1부터는 `lines-rise`(모든 히어로의 줄이 이미 로드 시
  올라옴), `window-parallax`(사진 위 패럴랙스), `word-rotate`(`word` 히어로가 자기 라이브 단어를 지님, `layout-v4.md`)도
  은퇴했습니다. `magnetic-button`(CK-94)은 없어졌습니다.

## 각각 어울리는 곳

| id | 종류 · 어울리는 곳 | 폰과 모션 줄이기 |
|---|---|---|
| word-rotate | retired · 히어로, 세 번 돌고 정지 | 적어 둔 단어가 그대로 있음 |
| lines-rise | retired · 한 섹션 또는 선언, 한 번 | 제목과 그 줄들이 그대로 있음 |
| counter-rolls | text · 근거 수치, 한 번. 카드 안에는 절대 안 둠 | 수치가 그대로 있음 |
| word-highlight | scroll · 선언 하나 | 폰에서 실행됨. 모션 줄이기: 선언 전체를 먹색으로 |
| giant-type-pass | scroll · 중간에서 어두운 톤의 사진이 있는 선언 하나(기술만) | 사진이 글자 안에 서 있고 글자는 더 작게 |
| letters-assemble | scroll · 아주 크게 놓은 2~5단어 선언 하나. 글자가 날아와 한 줄이 됨 | 적은 그대로의 선언 |
| pinned-chapters | scroll · 2~4단계가 있는 기능 섹션 하나, 라이브 두 화면 | 정적 행(또는 각 단계 아래에 그 비주얼) |
| window-parallax | retired · 폭 넓은 사진 하나 | 사진이 프레임 안에 서 있음 |
| marquee-row | scroll · 실제 단어의 행(업종, 도시, 형식. 로고는 절대 안 됨: 로고는 움직이지 않음), 일시정지 버튼 포함 | 단어가 줄바꿈된 행으로 |
| line-carries-colour | transition · 새 바탕 위의 섹션이 끝에서 끝까지 그것을 유지함. 안쪽에서는 옛 바탕색의 인셋 패널(고른 거터, 카드 모서리)이 아래쪽에서 올라오는 선에 의해 치워짐. 각 블록은 선이 지나간 뒤 온전히 보임 | 패널도 선도 없이 섹션이 자기 바탕 위에 있음 |
| iris-opens | transition · 새 바탕 위의 섹션이 끝에서 끝까지 그것을 유지함. 안쪽에서는 옛 바탕색의 인셋 패널(고른 거터, 카드 모서리)이 가는 강조색 고리를 두른 원반으로 열림. 각 블록은 원반이 품은 뒤 온전히 보임 | 패널도 고리도 없이 섹션이 자기 바탕 위에 있음 |
| picture-develops | transition · 뚜렷한 피사체가 있는 큰 사진 하나, 한 번, 1.6초(룩 `film`): 흐린 회색 프린트에서 올라오며 어두운 곳부터, 그다음 색이 나옴. 하프톤 룩 `print` 는 뽑지 않음 | film 룩은 폰에서 실행됨. 모션 줄이기: 사진이 그대로 있음 |
| photo-chapters | scroll · 제목과 리드(h2) 아래의 챕터 3~5개(각각 제목과 두 줄, 사진 한 장)로 된 섹션 하나: 페이지 폭의 사진 한 장, 다음 사진은 아래쪽에서부터 이전 것 위로 드러나고, 챕터는 왼쪽 아래의 패널에 놓임. 챕터당 스크롤 약 화면의 3분의 2이므로 섹션은 라이브 세 화면(챕터가 넷이나 다섯이면 네 화면). place, product, service | 폰을 세로로 든 경우 실행됨. 모션 줄이기: 챕터를 나란히, 각 사진이 그 글 위에(폰에서는 쌓음), 섹션은 그것들만큼 큼 |
| closing-lift | transition · 사진이 있는 마무리 | 평범한 마무리 섹션 |
| cursor-spotlight | hover · 히어로 프레임 | 빛이 가만히 있음 |
| liquid-type | liquid · 히어로나 선언 제목이 포인터 아래에서 물처럼 일렁임. SVG 필터이며 WebGL 없음 | 적은 그대로의 제목 |
| liquid-hover | liquid · 가장자리와 디테일이 있는 사진 하나, WebGL 컨텍스트 하나 | 캔버스 없는 평범한 사진 |

## 정지 규칙(모든 모먼트, 예외 없음)

모든 모먼트에는 **폰**과 **모션 줄이기**용 정지 변형이 있고, 스크립트가 없거나 모듈이 실패할 때의 완성 상태가 있습니다. 로더가
정합니다. 로더는 각 모먼트에 `lib` 를 넘기며, 그 `reduced()` 는 `lib.still()` 에 답합니다. 이것은 `prefers-reduced-motion`
이거나 폰(폭 640px 미만, 또는 옆으로 눕힌 터치 화면에서 높이 500px 미만)일 때 참입니다. `reduced()` 를 기준으로 쓴 모먼트는
그러므로 거기서 완성 상태를 보여 주며, 호스트는 `data-moment-still="reduced"`, `"phone"`, `"card"` 를 지닙니다. **Phones
still get a moment:** 폰에 충분히 가벼운 것들(한 번에 사진 하나나 문단 하나. transform, clip, filter, 색)은 `moment.js` 에
`export const phone = true`, `meta.json` 에 `"phoneRuns": true` 를 적고 거기서 실행됩니다. 모션 줄이기와 카드에서만 정지
상태를 유지합니다. 해당하는 것은 `word-highlight`, `picture-develops`(film), `photo-chapters`(높이 600px부터)이며, 모든
place, product, service 뽑기를 포괄합니다. 답은 모먼트가 마운트될 때 구해집니다(640px를 가로질러 크기를 바꾼 창은 다음 로드에
적용되고, `pinned-chapters` 와 `photo-chapters` 는 크기 변경 시 다시 물음). 각 `meta.json` 은 정지 상태가 무엇을 보여 주는지
말합니다(`reduced`, `phone`). 호버 모먼트는 터치 화면에서도 아무것도 하지 않습니다.

**카드의 어떤 것도 스크롤로 움직이지 않습니다**(하우스 규칙). 모먼트는 히어로, 선언, 한 섹션, 전환, 마무리에 놓이며 카드, 요금제, 결과,
벤토 셀 안에는 절대 놓이지 않습니다. 로더는 그런 것을 정지시키고(`data-moment-still="card"`, `<html>` 의
`data-moments-card`) `moments.mjs check` 는 그것을 결함으로 칩니다.

## 페이지에 하나 올리기

호스트는 페이지의 한 섹션입니다(텍스트 모먼트라면 그 안의 제목이나 행). 모먼트의 헤더 주석이 보여 주는 대로 표시합니다
(`data-moment="<id>"`, 옵션은 `data-moment-opts`). 모든 섹션은 라이브일 때도 정지일 때도 한두 화면 높이를 유지합니다
(`layout-v4.md`, `--h`). 단 두 chapters 모먼트는 예외입니다. `photo-chapters` 는 라이브에서 (hold + 1) 화면입니다(챕터 셋이면
셋, 넷이나 다섯이면 넷. 여기에 `--h` 도 `data-screen` 도 쓰지 않음: 검사기와 레이아웃 검사가 모두 라이브 photo-chapters
섹션을 온전한 화면 수, 최대 넷으로 읽음). 둘 다 정지 상태에서는 내용만큼의 높이입니다. 전환의 호스트는 새 바탕 위에 있는 섹션
전체이고, 선언 모먼트는 h2가 먼저 오는 한 섹션이며, marquee나 counter 행은 위의 섹션에 그 마지막 행으로 합쳐집니다.
`<head>` 에는 한 줄과 로더, 그 lib, 뽑은 모먼트의 `modulepreload` 를 둡니다.

```html
<script>document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)</script>
<link rel="modulepreload" href="assets/moments/moments.js"><link rel="modulepreload" href="assets/moments/lib.js"><link rel="modulepreload" href="assets/moments/<id>/moment.js">
```

그다음 로더를 한 번 둡니다. `system.js` 가 있는 페이지에서는 `system.js` 가 그것을 import하고 기다립니다. 없는 페이지에서는 데모
페이지의 태그를 `<body>` 끝에 둡니다.

```html
<script type="module" src="assets/moments/moments.js"></script>
```

로더는 각 모먼트의 CSS를 링크하고 시작시키며, `<html data-moments-ready>` 가 그 시점을 알립니다. 실패한 모듈은 자기 요소에
`data-moment-failed` 와 클래스 `mo-safe` 를 받고, 모먼트의 CSS는 이를 "지금 완성 상태를 보여라"로 읽습니다. 데모의 문구와 사진은
자리표시자입니다. 모든 모먼트는 페이지의 토큰(`--bg`, `--ink`, `--muted`, `--accent`, `--line`, 디스플레이 서체)을 받습니다.

페이지 안의 모먼트 섹션은 두 페이지 모델 중 하나에서 복사합니다. 두 모델은 시작 페이지 안에 모먼트를 마운트하고 검사기를
통과합니다. `assets/moments/_demo/in-page.html`(place: `photo-chapters`, `word-highlight`)과 `in-page-service.html`(service:
`pinned-chapters`, film 룩의 `picture-develops`)입니다. 모먼트 자체의 `demo.html` 은 그것만 보여 줄 뿐 페이지 모델이
아닙니다.

## 규칙

- **종류별 개수, id는 한 번.** `<html>` 의 `data-moments-over` 와 `data-moments-repeat` 는 결함입니다.
- **스크롤하며 무작위 효과 금지.** 스크롤 모먼트는 자기 섹션 안에서 스크롤바에 맞춰 재생되며
  그 섹션은 한두 화면 높이(`photo-chapters` 는 셋이나 넷)이고 목적 있는 일 하나를 합니다. 섹션의 위와 아래에서는 완성 상태를
  보여 줍니다(모든 전환과 `letters-assemble` 은 섹션 위쪽이 화면의 5분의 1 내려오기 전에 끝남). 그래서 각 심사 타일은 온전한
  섹션 하나를 보여 줍니다. 카드, 행, 타일은 스크롤로 등장하지 않습니다. `consistency.mjs` 는 뽑은 `[data-moment]` 섹션 안의
  스크롤 발견을 보고하며, 그것은 예상된 것이고 다른 것은 결함입니다.
- **모션 없이도 내용이 읽힘:** 글은 HTML 안에 완성된 자리에 있습니다. 모먼트는 로드 시
  제목을 절대 숨기지 않습니다(히어로 자체의 등장 효과는 모션 계층의 것, `motion.md`).
- **다른 종류에서는 사진이 이끎:** place, product, service 페이지의 모먼트는 고객 자신의
  사진(또는 `photos.md` 를 통과한 라이브러리 사진)을 싣고 각각 페이지에서 한 번만 쓰며, 그 글은 페이지의 실제 문구입니다.
  모먼트에 움직일 것을 주려고 대체 사진을 쓰지 않습니다.
- **한 페이지에 카운트 하나:** `counter-rolls` 또는 `data-m-count`(`motion.md`) 중 하나이며 둘 다는 안 됩니다.
- **깜빡이지도 튀지도 넘치지도 않음.** 이즈 아웃(안착에는 cubic-bezier(.22,1,.36,1)),
  드러남은 600~1,000ms, 현상되는 사진은 1.6~1.8초. 스크럽되는 와이프나 변화는 자기 챕터의 스크롤 몫의 약 절반이 걸리고 나머지
  동안 유지됩니다. 반복은 정해진 횟수를 돌고 정지하거나 일시정지 버튼을 지닙니다.
- **페이지의 가장자리.** 모먼트의 글은 다른 모든 섹션처럼 `.container` 나 `.wrap` 안에 놓입니다. 그 글은
  페이지의 왼쪽과 오른쪽 가장자리에서 끝납니다. 전환의 덮개는 호스트 섹션 안의 인셋 패널이며 사방에 고른 거터가 있고(카드
  모서리, 섹션 가장자리에 닿지 않음) 그 선이나 고리는 패널 안에 있습니다. 모든 제목, 문단, 버튼, 사진은 온전히 나타나며 선이나
  원반에 잘리지 않습니다(각 모먼트의 `meta.json`, `look` 이 방법을 말함).
- **비용:** `liquid-hover`(기술만) 외에는 WebGL이 없습니다(컨텍스트 하나, 화면 근처에서만. WebGL이 없거나 셰이더가
  실패하면 평범한 사진). `liquid-type` 은 제목 하나에 걸린 SVG 필터 하나이며 파문이 살아 있는 동안만 켜집니다. 나머지 모든
  모먼트는 CSS 변수, transform 또는 clip, 패시브 리스너만 듭니다.
- **한 페이지에 포인터 효과 하나:** 호버나 liquid 모먼트는 `fx-button`, `fx-spotlight`, 포인터를
  향해 도는 객체를 배제하고 그 반대도 마찬가지이며, `pick` 은 둘을 함께 뽑지 않습니다.
- **사진:** `giant-type-pass` 와 `liquid-hover`(기술)는 가장자리와 디테일이 있는 중간에서 어두운 톤을 원합니다.
  옅은 황혼 하늘은 글자 안에서 라벤더색으로 읽히고 평평한 바다는 파문이 보이지 않습니다. 보라나 라벤더는 쓰지 않습니다.
- **캡션 없음;** 사진의 출처 표기는 푸터 줄에 둡니다.

## 검사하기

- `node <skill>/scripts/moments.mjs check <page.html> --page <kind> [--scene <id>] [--effects a,b] [--contexts n]`
  는 빌드된 페이지를 읽습니다. 모먼트가 몇 개인지, 두 번 쓰인 것, 은퇴한 것, 페이지 종류에서 벗어난 것(place의 WebGL이나
  효과 모먼트는 종류에서 벗어남), 카드 안에 있는 것, figcaption을 지닌 것, 서로 피하는 둘, place·product·service 페이지의
  같은 슬롯 둘, 4에 대한 WebGL 합계, 빠진 로더. 결함이면 종료 코드 1.
- `node <skill>/scripts/moments.mjs shoot --out shots/moments --profile <own chrome dir> --port 5720 --only <id> [--reduced]`
  는 스킬의 헤드리스 Chrome(WebGL은 CPU로)에서 데모의 시작, 중간, 끝 상태를 1440과 390에서 촬영합니다. 끝은 완성된
  섹션이어야 합니다. `--reduced` 일 때, 그리고 `phoneRuns` 가 없는 모먼트의 390에서는 정지 규칙도 확인합니다. 호스트가
  `data-moment-still` 을 말해야 하고 그 안에서 어떤 애니메이션도 돌면 안 됩니다(아니면 `STILL?` 줄). `--probe "<js
  expression>"` 은 각 상태 뒤에 값을 출력합니다.
- 헤드리스 Chrome은 WebGL을 CPU로 그리므로 `liquid-hover` 는 거기서 GPU보다 옅은 파문을 보이고 그 끝 상태는 평범한 사진이
  되기까지 6초를 기다립니다. 텍스트나 스크롤 모먼트는 둘에서 똑같이 보입니다.
