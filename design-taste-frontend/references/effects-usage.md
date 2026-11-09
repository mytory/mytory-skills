# 효과 사용법

누가 효과를 쓰는지, 몇 개를 쓰는지, 어떻게 뽑는지, 어디에 두는지를 다룹니다. 효과란 셰이더,
캔버스, WebGL, 프린트 패스, 스크롤 구동이 만드는 모든 것입니다. 효과 배경(`data-fx`,
`assets/effects`), WebGL 크리에이티브 부품(`effects-creative.md`), 오브젝트와 프린트
(`effects-objects.md`), 큰 장면(`scenes.md`), 기술 모먼트(`moments.md`. 모든 유형이 뽑는 사진 중심·타입
중심 모먼트는 효과가 아닙니다), 영상이나 3D 히어로, 시간 루프가 여기에 속합니다. 카드 세부 사항은
`cards.md`가 우선하고, 모든 타이밍은 `motion.md`에 있습니다.

## 게이트(하우스 규칙 8)

효과는 site-kind가 tech, software, gaming(AI와 개발자 도구는 software로 칩니다)인 페이지와,
기술적 주제(하드웨어, 기기)를 가진 제품 페이지에만 씁니다. 장소, 평범한 제품 브랜드나 가게, 서비스
회사, 에이전시, 스튜디오에는 절대 쓰지 않습니다. 이들은 site-kind other입니다.

other에서는 사진, 글자, 단색 면이 페이지를 이끕니다. 거기서 금지하는 것은 canvas와 WebGL,
자동재생 영상, 모든 CSS 그라디언트(배경, 패널, 글로우, 스크림), SVG 패턴이나 텍스처 배경,
`backdrop-filter`(내비게이션 포함), `filter`, `mix-blend-mode`, `mask-image`, 글라스, 그레인,
하프톤, 디더, 듀오톤, 프린트, `[data-fx]`, `[data-print]`, `[data-scene]`, `[data-big-scene]`,
`[data-ui-loop]`, `[data-m-loop]`, `[data-m-count]`, SVG 애니메이션, GIF, Lottie, 커스텀 커서,
모든 스크롤·애니메이션 라이브러리입니다. 허용하는 것은 히어로의 등장 효과와 뽑은 사진 중심·타입
중심 모먼트 하나나 둘(`photo-chapters`, `pinned-chapters`, 필름 룩의 `picture-develops`,
`word-highlight`: `moments.md`), 구워 둔 정지 상태의 `fx-map`, 평범한 사진으로서의 `fx-photo`, 진짜
아이콘, 정지 다이어그램(장소에는 안 됨), 그리고 브리프가 3D를 요청한 물리적 제품의 제품 렌더
(`[data-product]`, `effects-objects.md`)입니다. 제품 렌더는 제품의 그림이지 효과가 아닙니다. 기본은
정지 이미지이고, 요청이 있을 때만 라이브(`data-product-mode="live"`)이며, 라이브 컨텍스트는 최대
하나이고, 평평한 바탕 위에 두며, 그 밑에 포스터를 깝니다. 그 요청이 없으면 사진이 없는 제품은 대체
사진으로 보여 줍니다(`photos.md`).

## 유형별로 받는 것

| | tech | 제품, 서비스(other) | 장소 |
|---|---|---|---|
| 대표 그림 | 고객의 UI(하드웨어: 그 사진이나 CAD 렌더, 없으면 같은 종류의 대체 사진이며 효과나 주문 폼만 두는 일은 없음. 게임: 이름과 아트, 없으면 배경 세계의 대체 사진 위의 이름. 렌더는 브리프가 3D를 요청할 때만) | 그 사진. 사진이 없는 제품은 같은 종류의 대체 사진(렌더는 브리프가 3D를 요청할 때만) | 그 사진(외딴 장소는 그 지역의 풍경) |
| 유일한 효과 | 라이브 배경, WebGL 부품, 오브젝트 또는 큰 장면 | 없음 | 없음 |
| 카드 패널 배경 | 효과 계열의 정지 상태 카드 그룹 하나. 큰 장면이 있으면 조명 배경(`data-ground`)이며 `data-fx`는 없음 | 고객의 사진 | 없음 |
| 모먼트 | 한 페이지에 1개나 2개, 전체 합쳐 최대 2개. 섹션에 두며 그중 하나는 히어로에 둘 수 있음 | 섹션에 1개나 2개, 사진 중심 또는 타입 중심(`moments.md`) | 섹션에 1개나 2개, 사진 중심 또는 타입 중심(`moments.md`) |
| 큰 장면 | 0개나 1개(그것이 효과임) | 없음 | 없음 |
| 다이어그램 카드 | 0~2개, 맥동 | 0개나 1개, 정지 | 없음 |
| 루프 | 시간 루프 하나, 카드 그룹당 하나 | 없음 | 없음 |
| CSS 배경 | 0~2개(`backgrounds.md`) | 평평한 토큰 | 평평한 토큰 |

**효과보다 대상이 먼저입니다**(테스트에서 로봇 팔을 실크 셰이더와 주문 폼으로 보여 준 페이지, 이름 없는
게임을 추상적인 효과로 보여 준 페이지가 모두 그 물건을 보여 준 페이지에 졌습니다). 효과는 제품, 기기,
게임의 세계가 있어야 할 자리에 서지 않습니다. 사진이나 고객 렌더가 없는 하드웨어는 같은 종류의
기계가 일하는 대체 사진을 쓰고, 아트 파일이 없는 게임은 배경 세계의 대체 사진 위에 이름을 크게 얹어
세계 섹션에 전폭으로 둡니다(`photos.md`, 라이브 검색. `sections.md` 3절 제품과 게임). 브리프가
3D를 요청하면 제품 렌더(`effects-objects.md`, 제품 렌더)가 효과가 아니라 그림 자리를 차지합니다.
페이지의 유일한 효과는 그 뒤 무대의 바탕으로 둘 수 있고(모든 렌더 배치는 프레임 위에서 투명합니다),
그것이 비트로 세어지며 컨텍스트 넷을 렌더와 나눠 씁니다. 효과가 그림을 대체하는 일도, 그 옆에서 두
번째 시선 끌기 시각물이 되는 일도 없습니다.

효과, 카드 배경, 모먼트, 장면, 제품 렌더가 아닌 모든 시각물은 진짜 UI 캡처나 진짜 사진입니다. 어떤
페이지에서도 사진에 필터, 프린트, 디더, 보정을 걸지 않습니다.

## 기술 예산

- **효과 하나:** 라이브 배경 하나(히어로 배경, 또는 h2 아래의 프레임을 두른 `[data-visual]` 창 안의
  배경), 또는 WebGL 부품 하나(컨텍스트를 쥐는 `fx-*`: 버튼 채움, 검색이나 프롬프트 글로우,
  엣지 글로우 계획, 스포트라이트, 지구본, 아바타, 로고, 진행률, 디더 오브젝트, 채워진 제목이나
  수치), 또는 오브젝트 하나, 또는 큰 장면 하나입니다. 그레인, 디더, 텍스처 CSS 배경도 이것으로
  칩니다. 고정 레이어에 두지 않고, 본문 뒤에 두지 않으며, 페이지 전체 길이의 캔버스도 쓰지
  않습니다. 3D 세계는 히어로에만 둡니다.
- **카드 배경**(하우스 규칙: "gradients and effects ... as a card's background with a smaller
  card of text or UI on top"): 카드 그룹 하나는 효과 계열의 조용한 배경을 가질 수 있으며, 한 번
  그려 그림으로 고정합니다(system.js가 그 컨텍스트를 해제합니다). 두 번째 라이브 효과가 아닙니다.
  큰 장면이 있으면 모먼트 밖에는 `data-fx`가 없고(검사기가 FAIL로 처리합니다, MO-16, MO-23),
  카드 패널은 조명 배경(`data-ground`)을 씁니다.
- **모먼트**(하우스 규칙): 스크롤을 따라갈 수 있는 섹션 모먼트(글자, 액체, 섹션 전환, 카운터, 마키
  행)는 최대 둘이며 각각 자기 섹션에 두고, 스크롤과 무관한 모먼트(로드, 호버, 클릭)는 히어로나
  `[data-visual]`에 최대 하나이되 장면의 섹션 안이나 옆에는 두지 않으며, 합쳐 최대 둘입니다.
  `fx` 부품으로 만든 모먼트는 자기 섹션에 자기 `data-fx` id를 달며, 두 번째 배경이 아닙니다.
- **비트:** 효과, 장면, 모먼트가 페이지의 비트이며 tech에서는 최대 셋입니다. 계획에 각각과 그 섹션을
  적습니다. 한 섹션이나 이웃 섹션에 둘을 두지 않고, 그 사이에 차분한 섹션을 두며, 페이지 뒷
  3분의 1은 마무리 전에 차분하게 둡니다. CSS 배경, 카드 배경, 다이어그램, 카드 루프, 호버는 비트가
  아닙니다.
- **포인터 효과는 한 페이지에 하나:** 호버나 액체 모먼트, `fx-button`, `fx-spotlight`, 포인터를
  향해 도는 오브젝트 중 하나이며 둘은 안 됩니다. 커서 교체도, 자석 버튼도 안 됩니다.
- **라이브 WebGL 컨텍스트는 동시에 최대 넷**(하우스 규칙): 효과와 모먼트 자체 캔버스를 합쳐
  셉니다. `perf.mjs`는 넷을 넘으면 실패시킵니다.

## 효과를 뽑습니다. 취향으로 고르지 않습니다

`node <skill>/scripts/effects.mjs list`는 각 id를 계열, `quiet`/`focal`, 슬롯과 함께 보여 줍니다.
`<kind>`는 페이지의 바탕으로 `light`, `dark`, `colour` 중 하나이고, `<site-kind>`는 software, gaming,
tech 중 하나입니다.

```bash
# the effect: an effect hero takes --slots hero; a photograph or UI hero puts it in the one [data-visual] frame: --slots band
node <skill>/scripts/effects.mjs pick --page <site-kind> --palette <kind> --slots hero --quiet --seed <S> --history .taste-skill/effects-history.json
# one card group's still grounds, same family (a pattern or dither effect: --family mesh)
node <skill>/scripts/effects.mjs pick --page <site-kind> --palette <kind> --slots card --family <the effect's family> --exclude <the effect>,<NOUI> --quiet --seed <S> --history .taste-skill/effects-history.json
```

`--quiet`는 패턴이 아니라 focal 배경만 뺍니다. 슬롯이 UI(창, 조각, 카드 그룹)를 담을 때는 패턴과
프린트를 `--exclude`에 더합니다. `<NOUI>`는
`ruled-grounds,grid-pulse,contour-lines,dot-terrain,dotted-globe,ridgeline,halftone-screen,bayer-dither,ascii-shade,line-engraving,duotone-grade`입니다.

- **Quiet** 배경은 UI를 담는 고른 면입니다(`grain-gradient`, `painterly-landscape`,
  `gradient-mesh`, `silk-folds`, `fluted-glass`). UI 뒤의 부드러운 면이며 패턴이 아닙니다.
  **Focal** 배경은 주제가 있습니다(`orb-sphere`, `spotlight-cone`, `god-rays`, `aurora-curtains`,
  `caustics`). 히어로에 단독으로 놓고 그 위에 아무것도 얹지 않습니다.
- 모먼트 밖에서 한 페이지에 id는 최대 둘이며, 패널마다 자기 `data-fx-seed`를 갖습니다. 마무리에
  효과를 되울리지 않고, 패턴 패널도, focal 타일도 두지 않습니다. `dotted-globe`는 전 세계에 닿는
  경우에 한해 이름을 지정해 효과로만 쓰고, `duotone-grade`는 고객의 사진에 절대 쓰지 않습니다.
  `pick`이 슬롯에 맞는 것이 없다고 하면 그 슬롯을 버립니다.
- `.ground-inverse` 위의 시각물은 그 종류용 id(`--palette dark`)를 씁니다.
- 폐기되거나 이름이 바뀐 id는 쓰지 않습니다. `mesh-gradient`는 `gradient-mesh`, `iridescent-foil`은
  `fluted-glass`가 되었고, `riso-print`, `paper-texture`, `liquid-chrome`은 없어졌습니다.

## 모먼트와 장면을 뽑습니다

**모먼트**(모든 유형에서 1개나 2개): `moments.mjs pick --page <kind>`로 뽑고, 제외 목록과 히어로
규칙은 `moments.md`(뽑습니다. 취향으로 고르지 않습니다)가 말하는 그대로 따릅니다. WebGL 합계가 넷 이내가 되도록 장면과
효과를 넘깁니다. 장면의 섹션 안이나 그 옆에는 모먼트를 두지 않습니다.

**큰 장면**(0개나 1개, 페이지의 효과): `assets/scenes/index.json`의 `types`에 페이지의 site-kind가
있고 브리프가 `needs`를 충족하는 장면(`scenes.md`의 표) 가운데 무작위로 하나를 뽑되, 최근 셋은
피합니다.

```bash
node -e "const fs=require('fs'),f='.taste-skill/scenes-history.json';let h=[];try{h=JSON.parse(fs.readFileSync(f))}catch{}const a=process.argv.slice(1),k=Math.min(3,a.length-1),p=a.filter(i=>!(k?h.slice(-k):[]).includes(i));const id=p[Math.floor(Math.random()*p.length)];fs.mkdirSync('.taste-skill',{recursive:true});fs.writeFileSync(f,JSON.stringify([...h,id]));console.log(id)" <the fitting ids>
```

뽑은 장면의 `needs`가 충족되지 않는 것으로 드러나면 그 id를 빼고 다시 뽑으며, 남은 id가 없으면
장면은 없습니다. 장면은 `restH`가 1일 때만 히어로가 됩니다. 히어로용 장면 셋은 지금 두 화면으로
정지하므로, 뽑은 히어로 아래의 두 화면 섹션으로 들어갑니다(`scenes.md`, 누가 쓰는가). `avoidMoments`
(`index.json`)에 올라 있는 모먼트나 그 쌍둥이와는 장면을 함께 쓰지 않습니다. 모먼트 뽑기에 장면을
`--scene <id>`로 넘기면 `pick`이 그 avoidMoments와 쌍둥이를 스스로 제외합니다. 마크업과 검사는
`scenes.md`에 있습니다.

**높이(규칙 3):** `scenes.md`(높이)의 말대로 `{"hold": 1}`과 `--h` = 장면의 `restH`이며 페이지
CSS는 없고, 장면의 섹션은 다른 섹션처럼 한 화면이나 두 화면에 머뭅니다.

## 두는 곳

- **효과:** 히어로(`.stage.stage--fade-b`를 담은 `.frame.frame--hero`, 또는 히어로의 레이어), 또는
  h2 아래의 `[data-visual]` 프레임 하나(1440에서 최대 1280x540, 390에서 342x256의 창), 또는 장면
  자신의 섹션입니다. 한 페이지에 `[data-visual]`은 하나입니다. 프레임 안에 효과를 둔 히어로는
  오른쪽에 시각물을 둔 5/7이나 6/6 분할이거나, 효과를 자기 섹션으로 옮깁니다. 히어로의 레이어로 둔
  효과(게임의 세계, focal 배경)는 글자를 그 차분한 부분 위에 4.5:1로 둡니다.
- **분할 프레임:** `.stage`를 담은 `.frame.frame--split`이며, 창은 `.at-corner.to-edge`로 56/56에
  오른쪽과 아래가 잘립니다. 두 번째 조각(`cursor`, `notify`)은 창의 오른쪽 아래 가장자리 위
  (`.at-over`)에만 두고, 1024~1279에서와 폰에서는 숨깁니다. 글자와 UI는 한 쪽 절반을 나눠 쓰지
  않습니다.
- **카드 패널:** `cards.md`(패널, 그 위의 조각, 페이드, 조명 팔레트, 루프).
- **효과 위의 글자**는 그 조용한 부분 위에서 4.5:1 이상일 때만 둡니다. 노이즈나 안개 배경은 콘텐츠를
  담지 않습니다.
- **영상**(tech의 히어로나 `[data-visual]`에서만, 효과나 루프로): 음소거, 인라인, 포스터 먼저,
  6~12초 루프 또는 한 번 재생하고 마지막 프레임에서 멈추는 이야기, 일시정지 버튼, 폰용과 데스크톱용
  파일을 따로 둡니다. other에서는 클릭하면 영상을 여는 정지 이미지를 둡니다.
- **조명 배경**(`<html data-ground>`, tech): system.js가 UI를 담는 모든 배경에 이를 주므로, 페이지,
  카드, 패널, UI가 거의 검은 레이어 넷이 되는 일은 없습니다.

## 모션과 비용

- 효과는 포인터나 시간에 반응합니다(장면과 모먼트는 스크롤에 반응할 수 있습니다). 조립된 뒤에는
  멈추고 끊임없는 요동은 없습니다. 주변 사이클은 4초 이상, 흐름은 초당 몇 px, 0.9초 동안 바뀌는
  픽셀은 2~10%입니다. 정지 상태이거나 일시정지 버튼이 있고, 포스터를 먼저 보여 주며, 모션 축소,
  폰, WebGL 실패 때는 정지 대체물을 보여 줍니다. 진입 시 소리는 내지 않고, 터치에서는 포인터 놀이를
  끕니다.
- 효과는 박스보다 20~25px 크게 그리고 잘라 냅니다. CSS px당 샘플은 하나 이하(클 때는 0.75), 약
  1.5메가픽셀, 픽셀 비율은 최대 1.5이며, 노이즈, 파티클, 레이 마칭은 절반 해상도와 30fps 이하로
  돌립니다. 노이즈 배경은 시간에 따라 흐르는 구워 둔 텍스처 하나이고, 코스틱 그물은 평평한 바닥
  그물만 씁니다.
- 블렌드 모드는 효과 안의 용도(반짝임)에만 쓰고 글자에는 절대 쓰지 않습니다. 어떤 유형에도 글라스나
  젖빛 느낌은 쓰지 않습니다. 메뉴 커튼은 평평한 40% 어둠입니다.
- system.js가 배경(`ui.grounds`)을 올리며, 페이지 스크립트에서 `fx.mountAll`을 호출하지 않습니다.
  셰이더를 바꾼 뒤에는 `assets/objects/_print-core`와 `_scenes`에서 `lint-glsl.mjs`를 돌립니다.
  이름에 GLSL ES 예약어(`flat`, `smooth`, `sample`, `filter`, `input`, `output`…)를 쓰지 않으며,
  모든 WebGL 부품은 셰이더가 실패하면 정지 대체물을 보여 줍니다. 속도는 `perf.md`에 있습니다.

## 금지

- other 유형 페이지의 효과, 프린트, 그레인, 그라디언트, WebGL. 사진이 있어야 할 자리의 효과.
- 어떤 유형에서든 사진 위의 프린트, 디더, 보정, 필터.
- 카드 안의 라이브 효과나 움직이는 캔버스. 스크롤에 따라 움직이는 카드.
- 시각물을 설명하는 캡션(출처는 푸터 한 줄에 적음). 깜박이거나 무작위인 효과. 보라색이나 라벤더.
- 다른 사이트의 코드, 에셋, 시그니처 장치를 복사하는 일. 일반적인 발상만 가져와 스킬 자신의 장면과
  모먼트로 고객의 콘텐츠를 넣어 만듭니다.
