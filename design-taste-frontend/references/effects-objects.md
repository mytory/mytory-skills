# 오브젝트와 프린트(`assets/objects`)

세 계열의 오브젝트 열세 개와 빌더 하나입니다. 각 계열의 README가 계약이고 각 `meta.json`이 파라미터입니다.
`assets/objects/index.html`은 오브젝트를 보여 주고, `product-render/views.html`은 빌더의 작동 예시 스펙 셋을 모든 뷰에서 기준 크기로 보여 줍니다.

| 계열 | 오브젝트 | 무엇인가 |
|---|---|---|
| 프린트 오브젝트 | `print-cup`, `print-wheel`, `print-lamp`, `print-globe`, `print-cards` | 코드로 모델링한 물건입니다. 스튜디오 렌더(기본값) 또는 그것을 프린트한 것(하프톤, 판화, 디더). `_print-core/README.md` |
| 사진 프린트 | `photo-halftone`, `photo-engraving`, `photo-dither` | 진짜 사진 한 장을 셰이더로 프린트하며 포인터 아래에서는 사진이 보입니다. `photo-kit/README.md` |
| 장면 | `split-reveal`, `dither-sequence`, `dot-object`, `exploded-layers`, `product-turntable` | 프린트를 거친 사진(턴테이블은 일반 형태)이 포인터 아래에서 살아 움직입니다. `_scenes/README.md` |
| 제품 렌더 | `product-render`(빌더이며 고정된 오브젝트는 없음) | 부품의 JSON 스펙으로 구성한 모든 물리적 제품을 진짜 소재로 스튜디오 정지 이미지로 렌더합니다(요청이 있을 때만 라이브). `product-render/README.md` |

## 언제 쓰는가

- **한 페이지에 강한 오브젝트 모먼트 하나.** 두 번째 효과 옆이나 움직이는 배경 위에는 절대 두지
  않습니다.
- **장소, 서비스, site-kind other의 모든 페이지**(카페, 게스트하우스, 가게, 스튜디오, 의원, 제품
  브랜드)에는 오브젝트, 프린트, 장면이 없고 평범한 사진이 이끕니다. 하우스 규칙: 셰이더 효과는 그
  업종에 기술적 주제가 있을 때만 씁니다. 유일한 예외는 아래에 있습니다. 브리프가 3D를 요청한 제품은
  자기 렌더를 보여 줍니다.
- **사진이 있는 제품:** 사진이 이끕니다.
- **사진이 없는 모든 물리적 제품**(램프, 의자, 자전거, 유모차, 로봇 팔)은 site-kind other든 tech든
  **사진이 먼저이며, 기본값으로 렌더는 쓰지 않습니다.** 고객 자신의 사진, 브리프가 주는 누끼나 CAD
  뷰를 쓰고, 없으면 `photos.mjs search`로 찾은 같은 종류의 대체 사진을 쓰며 보고서에 나열합니다
  (`photos.md`, 사진이 없는 제품. `sections.md` 3절 제품). 테스트에서 자전거를 한 번도 보여 주지 않은
  카고 바이크 페이지는 10점 중 3점이었고, 렌더와 고정된 소품 세트로 끌고 간 페이지는 무작위 3D
  오브젝트처럼 읽혔습니다. 깔끔하게, 그 종류의 진짜 모습을 보여 주세요.
- **브리프가 3D나 렌더를 요청할 때만 렌더를 씁니다**(컨피규레이터, "3D로 보여 줘", 모델로만 존재하는
  제품). `assets/objects/product-render`가 이 제품을 자기 부품, 크기, 소재의 JSON 스펙으로
  구성하며(아래 제품 렌더) 히어로를 이끌고(`deal.mjs --type product --has object`, 하드웨어는
  `--kind tech`를 더함), 이어서 통으로 최대 두 섹션에 더 나오되 섹션마다 다른 뷰로, 프레임 안에서
  크게, 회색 패널 안에는 절대 넣지 않으며, 부품의 클로즈업이 나머지를 맡습니다(아래 뷰.
  `sections.md` 1절 물체 하나가 페이지를 혼자 끌고 가지 않습니다, 3절 제품). 이것은 제품의 그림이지 효과가 아닙니다. 페이지의 평평한
  바탕 위나 tech의 조명 배경 위에, 기본은 정지 이미지이고 요청이 있을 때만 라이브
  (`data-product-mode="live"`)이며 라이브 컨텍스트는 최대 하나이고, site-kind other에서는 프린트도,
  그 옆의 셰이더 배경이나 모먼트도 없으며, 헤드라인의 약속이 필요로 하지 않는 한 소품도 없습니다.
  다른 종류의 오브젝트(바퀴는 자전거가 아님), 그린 SVG, 헬퍼가 구성하지 않은 낱개 프리미티브의 모델,
  분위기용 스톡, 다른 제작자의 제품은 쓰지 않습니다. 굽은 껍데기는 실제 치수의 둥근 박스, 원기둥,
  필릿으로 구성합니다. 주문 폼만 담은 `split` 히어로도, 그 자리에 놓는 효과도 안 됩니다.
- **아트 파일이 없는 게임:** 히어로는 배경 세계의 대체 사진 위에 크게 얹은 게임 이름이며
  (`deal.mjs --type software --kind gaming --has setting`, `photo` 히어로), 세계 섹션은 그 사진들
  가운데 가장 넓은 것을 전폭으로 씁니다. 효과는 자기 섹션에 둘 수 있으나 키아트를 대신하지 않습니다
  (`sections.md` 3절 게임). 히어로 오브젝트나 세계의 렌더는 브리프가 3D를 요청할 때만 씁니다.
- **소프트웨어, AI, 아트가 있는 게임:** 프린트 오브젝트는 그 카드가 다루는 대상에 프린트로 씁니다(지역에
  지구본). 게임 자신의 세계 오브젝트는 `fixed-hero-object`에 씁니다(`scenes.md`).
- **사진 프린트와 사진 장면**은 사진을 프린트하는데, 어떤 페이지도 사진을 프린트, 디더, 보정하지
  않습니다(`photos.md`, `effects-usage.md`). 이들은 키트의 갤러리에만 두고 페이지에는 절대 쓰지
  않습니다. `product-turntable`(일반 형태, 사진 없음)은 그 형태가 자기 것일 때에 한해 기술 제품의
  오브젝트입니다.

## 마운트

```html
<div class="panel"><div data-print="print-globe" data-print-place="card"
  data-print-params='{"effect":"engrave"}'></div></div>
<script type="module" src="assets/objects/_print-core/auto.js"></script>
```

(키트의 사진 장면도 같은 방식으로 `data-scene`과 `_scenes/auto.js`로 마운트하지만 갤러리 전용입니다.
여기서의 `data-scene`은 큰 장면이 아니며, 큰 장면은 `data-big-scene`입니다, `scenes.md`.)

- **스크립트:** `<id>/object.js`의 `obj.mount(el, opts)`. 프린트 오브젝트는 `{ place, params,
  palette }`를, 사진 프린트와 장면은 `{ src, params, palette }`를 받습니다. 컨트롤러에는 `pause()`,
  `resume()`, `setPalette()`, `destroy()`가 있습니다.
- **배치**(프린트 오브젝트): `card`는 크게 두고 왼쪽 아래 가장자리로 잘리고, `tile`은 통으로
  정사각 타일의 아래쪽에 두며, `hero`는 넓은 프레임의 중심 오른쪽에 둡니다. 정중앙에 놓지 않습니다.
  사진 프린트와 장면은 자기 박스를 채우므로 종횡비를 줍니다.
- **팔레트:** 토큰 `--bg`, `--surface`, `--ink`, `--muted`, `--accent`, 또는 그 오브젝트의 것. 테마를
  바꾼 뒤에는 `setPalette(null)`을 호출합니다(사진 프린트는 `setPalette(fx.readPalette(el))`).
  지구본의 바다는 강조색이므로 파랑이나 청록을 줍니다.
- **일시정지:** 돌거나 반복하는 오브젝트는 한 번 그려지면 패널의 오른쪽 아래 모서리에 둥근 일시정지
  버튼을 둡니다. 그 모서리를 비워 두고, 그룹당 움직이는 것은 하나입니다.
- **출처:** 프린트나 장면이 보여 주는 사진은 푸터의 출처 한 줄에 적습니다(`photos.mjs
  credits --adapted`, `photo.js`의 `creditsLine()`, `kit.js`의 `credits()`). 렌더에는 필요 없습니다.

## 제품 렌더

`assets/objects/product-render`: 브리프가 3D나 렌더를 요청할 때 물리적 물건을 그리는 그림입니다.
site-kind other의 제품(자전거, 램프, 의자), 하드웨어(로봇 팔, 드론, 기기), 게임의 히어로 오브젝트나
세계에 쓰입니다. 그 요청이 없으면 사진이 없는 물건은 고객의 사진이나 대체 사진으로 보여 줍니다
(`photos.md`, `sections.md` 3절 제품과 게임). `build.js`는 물건 자신의 부품을 담은 JSON 스펙을
레이마칭 스튜디오 렌더로 바꿉니다(진짜 소재, 부드러운 빛과 그림자, 광택 부품의 소프트박스, 바닥
그림자, 요청하는 부품에는 페이지의 강조색). `auto.js`가 마운트하고, `make-posters.mjs`가 스펙을
검사하고 포스터와 정지 이미지를 찍습니다. 옆의 README가 전체 계약이며, `views.html`은
`specs/`의 작동 예시 스펙 셋(`city-bike` 부품 64개, `desk-lamp` 19개, `robot-arm` 28개)을 모든 뷰,
스펙마다 장면 하나, 색 전환 둘과 함께 보여 줍니다(`?only=bike|lamp|arm`, `?mode=still|live`).
`demo.html`은 턴테이블입니다. 형식은 복사하되 그 스펙을 고객의 제품으로 출고하지 않습니다.

### 마운트

```html
<div class="frame" data-product="assets/objects/product-render/specs/<id>.json"
     data-product-place="stage"></div>
<script type="module" src="assets/objects/product-render/auto.js"></script>
```

- `data-product`: 페이지에서 본 스펙의 URL이며, 포스터는 그 옆에 있습니다. 스펙은 `assets/objects`
  아래에 둡니다(`make-posters.mjs`는 그 밖의 것을 거부합니다). 예: `product-render/specs/<id>.json`.
- `data-product-place`: 제품 자신의 경계가 채우는 프레임의 비율만 정하며(더 타이트한 쪽), 항상 프레임
  중앙에 둡니다(`build.js`). `stage` 0.86, `hero` 0.88, `tile` 0.84, `card` 0.9이고, `legacy`는 한
  장의 넓은 프레임 안에서 글 오른쪽에 두던 옛 턴테이블입니다. 지정하지 않으면 `.frame`에서는 `hero`,
  `.panel`에서는 `card`, 정사각이나 세로 프레임에서는 `tile`입니다. 어떤 place도 글자를 제품 위에
  얹거나 옆에 놓지 않습니다. 프레임의 크기와 위치는 페이지의 CSS가 주고 글은 프레임 밖에 둡니다.
  `product` 히어로의 `.hero__stage`(`layout.css` 3b: 무대는 랩 전체에 걸치고 프레임은 위아래로 7%
  넘게 뻗으므로 제품이 무대만큼 큽니다)와 `split`이나 전폭 프레임에는 `stage`를, 정사각이나 세로
  타일에는 `tile`을 씁니다. 모든 place는 프레임의 바탕 위에서 투명하며 바닥 그림자도 그렇고,
  `layout.css`는 `[data-product]` 프레임에서 `.frame`의 채움, 테두리, 패딩을 걷어 내므로 패널 없이
  페이지의 바탕 위에 섭니다.
- `data-product-view`(`three-quarter` 기본, `side`, `front`, `top`, 클로즈업), `data-product-scene`,
  `data-product-color`(컬러웨이 id), `data-product-mode`(`auto`는 정지 이미지이며 기본값. `live`는
  요청이 있을 때만. `image`, `still`), `data-product-fill`(0.3-1.2): 아래 뷰를 보세요. 마운트된
  프레임에서 `-color`, `-view`, `-scene`을 바꾸면 그 변형이 보입니다.
- `data-product-params`(place 프리셋 위에 얹는 JSON): `{"angle":-20}`, 램프를 끄는 `{"step":0}`,
  `{"size":0.7,"x":0.1,"y":-0.05}`.
- `data-product-palette`: `{ bg, surface, ink, accent }`. 없으면 페이지의 `--bg`, `--ink`,
  `--accent`를 씁니다. `aria-label`은 스펙의 `label`을 덮어쓰며, 렌더는 이를 담아 `role="img"`를
  설정하고(클릭으로 바뀌면 버튼) `product-shown`이 이를 읽습니다.
- 스크립트: `import { loadProduct, checkSpec } from '…/product-render/build.js'`;
  `(await loadProduct(url)).mount(el, { place, params, palette })`. 컨트롤러: `pause()`, `resume()`,
  `step(on)`, `set(params)`, `setPalette(p | null)`(테마를 바꾼 뒤 `setPalette(null)` 호출),
  `destroy()`. `auto.js`는 `products`(요소에서 컨트롤러로), `ready`, `mountAll(root)`를 내보냅니다.
  로딩에 실패한 스펙은 그 요소에 `data-product-error`를 설정합니다.

### 뷰(섹션마다 다른 것. 제품 전체는 최대 세 곳)

모두 하나의 스펙에서 나오며 키트 자신의 이름을 씁니다(`build.js`, 작동 예시 스펙 셋이 각각 보여
줍니다). 각 섹션의 뷰를 그 계획 줄에 적고 둘이 같지 않게 합니다(히어로에는 `side`, 그다음 `three-quarter`,
`detail:<part>` 클로즈업이나 `exploded` 장면, 스펙 자신의 `rear-quarter`. 전체 뷰는 최대 세 섹션.
`sections.md` 3절 제품).

| 스펙 키 | 주는 것 |
|---|---|
| (필요 없음) | 표준 뷰 `three-quarter`(스펙의 `angle`), `side`(긴 제품의 가장 넓은 면: 그 히어로), `side-left`, `front`, `rear`, `top`, `low`(스펙의 `supports`가 나열한 것만). `detail:<part>[,<part>]`(또는 `detail-<part>`)는 지명한 부품을 프레임에 담고 나머지는 프레임 밖으로 흘려보내는 클로즈업 |
| `views` | 스펙 자신의 뷰, `{ "detail-saddle": { "part": ["saddle*", "seat post"], "angle": -42, "elev": 16, "margin": 1.3 } }`(`from`은 표준 뷰, 부품 이름은 그 이름으로 시작하는 부품을 받고 `*`는 무엇이든) |
| `scenes` | 사용 중이거나 짐을 실은 제품: `{ "loaded": { "label", "hide": [parts], "props": [{ "prop", "at", "size", … }], "parts", "lit", "pool", "click" } }`. 헬퍼가 그릴 수 있는 소품: `crate`, `bag`, `child-seat`, `bench`, `parcel`, `desk`, `book`, `mug`, `sheet`, `tray`. `lit`은 램프 주위의 그것들을 밝힙니다. 기본값으로는 장면도 소품도 없습니다. 헤드라인의 약속이 필요로 하는 곳에만(“takes four crates”에는 상자 넷) 섹션이 읽을 수 있는 크기로 두며, 사용 사진이 더 낫습니다 |
| `colors` | 제공하는 컬러웨이, `[{ "id", "name", "accent", "materials"? }]`: 강조색은 `"color": "accent"`로 칠한 부품을 다시 밝히고, `materials`는 다른 것들을 바꿉니다 |
| `make` | `make-posters.mjs`가 찍는 것: `{ "variants": ["three-quarter", "side", "front", "detail-saddle", "three-quarter+loaded"], "grounds": ["light", "dark"] }`(`view+scene`) |
| 램프의 빛 | 스펙의 `click: "light"`와 `pool`. `{"step":0}`은 끔 |

**뷰 마운트.** `<div class="frame" data-product="…/specs/<id>.json" data-product-place="stage"
data-product-view="side" data-product-color="blue">`. `make-posters.mjs`를 돌리고 나면 모든 뷰는 기본으로
그 정지 이미지입니다. 그것이 쓴 `<img class="product-render__img">`, 즉
`specs/stills/<poster>-<variant>-<colour>.webp`(`srcset`에는 `-half.webp`, 어두운 바탕에는 `-dark`.
`<poster>.stills.json`이 그것들과 제품이 채우는 박스를 나열합니다)를 제품이 place의 비율을 채우도록
배치하므로 페이지에는 캔버스도 WebGL도 없습니다. **기본은 정지 이미지이고, 요청이 있을 때만 라이브
(`data-product-mode="live"`)이며, 라이브 컨텍스트는 최대 하나입니다.** `auto`(기본값)는 정지 이미지를
보여 줍니다(먼저 `make-posters.mjs`를 돌립니다. 만든 정지 이미지가 없으면 도는 쪽으로 갑니다).
`image`는 정지 이미지만, `still`은 프레임 크기로 한 번 렌더해 `<img>`로 두고 컨텍스트를 해제하며,
`live`는 도는 것입니다. 클로즈업(`detail-*`, `detail:<part>`)은 제품의 나머지가 잘려 나가는 쪽을 프레임
가장자리에 맞추거나 그 너머로 둡니다(프레임이 잘라 냅니다). 안쪽에서 딱딱하게 잘리는 일은 없습니다.
스크립트로는 `(await loadProduct(url)).mount(el, { place, view, scene, color, mode })`이며 컨트롤러에
`setView(v)`, `setScene(s)`, `setColor(id)`(페이지의 스워치는 아래의 `data-product-swatch`를 쓰고 이것은
쓰지 않습니다), `ready()`가 더해집니다. **프레임이 검사기와 테스트에 알려 주는 것:** `data-product-mode`,
`data-product-state`(`image` | `still` | `live` | `poster`), `data-product-view`,
`data-product-color-shown`, 그리고 `window.__tpProduct` `{ stills, images, live, freed }`입니다. `live`만
`window.__tpGl`에 세어지며, `[data-product]` 프레임 안의 캔버스는 제품 자신의 렌더이지 효과가
아닙니다.

**크게:** 렌더는 투명하므로 섹션의 바탕 위에 기준 크기로 서며 회색 `.panel` 안에는 절대 넣지 않습니다.
place의 채움은 프레임의 0.84~0.9입니다(`size` 0.3~1.2가 이를 덮어씁니다). 히어로와 한 섹션 더에서는
제품의 긴 쪽이 프레임의 80~100%이거나 `detail:` 뷰가 가장자리 밖으로 흘려보내며, `product`
히어로에서는 가장 넓은 뷰가 1440에서 랩의 80% 이상에 걸칩니다(`layout.css` 3b. 시티 바이크의 `side`는
1280 중 1046, `three-quarter`는 818). **색 스워치:** 주문 카드의 색 버튼이나 라디오는
`data-product-swatch="#hero-bike, #loaded-bike"`(그것이 구동하는 프레임. 비우면 그 색이 있는 스펙의 모든
프레임)와 `value="<colour id>"`를 달며, 클릭이나 변경 때 프레임이 그 색의 정지 이미지로 바뀌고 버튼
그룹은 `aria-pressed`를 하나만 유지합니다. 페이지 자체 스크립트는 없습니다. 아니면
`frame.dispatchEvent(new CustomEvent('product:set', { detail: { color } }))`를 쓰거나
`data-product-color`를 설정합니다. 제공하는 모든 색은 페이지에서 한 번씩 보입니다. 정지 이미지는
렌더로 칩니다. 뷰와 색마다 그림 하나이며(그 `-half` 파일은 그 그림의 `srcset`에만), 같은 뷰를 두 크기로
한 페이지에 두 번 두지 않습니다.

### 스펙

```json
{
  "id": "city-bike", "name": "City bicycle", "label": "A city bicycle with a front basket",
  "units": "m", "angle": -34, "turn": { "mode": "sway", "amp": 22, "period": 24 },
  "materials": { "frame": { "kind": "paint", "color": "accent", "finish": "gloss" } },
  "parts": [
    { "type": "wheel", "at": [-0.53, 0.35, 0], "r": 0.35, "spokes": 36, "wall": "#c7a57a" },
    { "type": "tube", "from": [-0.07, 0.29, 0], "to": [-0.23, 0.81, 0], "r": 0.017, "mat": "frame", "blend": 0.01 }
  ]
}
```

- **축:** x는 제품의 앞, y는 위, z는 가로(각도 0에서 보는 사람 쪽)입니다. 단위는 아무거나 되며,
  모델은 가장 큰 변이 1 단위가 되도록 크기를 맞추고 가장 낮은 점이 바닥에 놓입니다. 실제 치수로
  모델링하세요. 그것으로 읽히게 하는 것은 대부분 비례입니다.
- **키:** `id`, `name`, `label`(스크린 리더가 읽는 것), `poster`(포스터의 파일 이름, 기본값은 id),
  `angle`(정지 상태와 정지 이미지의 회전, 기본값 -32, 쓰리쿼터 뷰), `turn`(`{"mode":"sway","amp":26,"period":22}`가
  기본값, `{"mode":"spin","speed":10}`, `{"mode":"still"}`), `camera`(`{"elev":12}`), `click: "light"`(클릭하면
  모든 `light` 소재와 `glow`가 전환되며 켜진 채로 시작), `pool`(`{"at":[x,0,z],"r":0.2}`: 바닥 위의
  그 빛), `materials`, `motion`, `parts`.
- **모든 부품**은 `mat`(이름이나 인라인 소재), `blend`(앞선 부품과 만나는 곳의 필릿, 단위 기준: 용접된
  튜브, 주조 몸체), `in`(모션 그룹), `name`을 받습니다. 부품은 `from` + `to`(둘 사이의 선형 부품. `up`이
  그 단면을 돌림) 또는 `axis`(`"x"`, `"y"`, `"z"` 또는 벡터)가 붙은 `at`과 `rot`([x, y, z] 도)로
  놓습니다. 튜브, 빔, 박스, 원기둥의 `seams`(반 길이를 따라 -1..1의 높이, `seamWidth`, `seamDepth`)는
  패널 선을 팝니다. 로봇의 껍데기나 받침의 홈이 그 예입니다.

| type | 크기 | 용도 |
|---|---|---|
| `tube` | `r`, `r2`(테이퍼), `cap` `flat`/`round`, `round` | 프레임 튜브, 기둥, 막대, 테이퍼진 로봇 링크 |
| `beam` | `w`, `d`, `round` | 납작한 바, 크랭크, 레일, 드론의 팔 |
| `box` | `size` [x,y,z], `round` | 하우징, 몸체, 페달, 그리퍼, 상자 |
| `panel` | `size`(얇음) | 판, 뚜껑, 화면의 뒷면, 선체의 갑판 |
| `cylinder` / `disc` | `r`, `h`, `round` | 받침, 허브, 모터, 렌즈, 로터 |
| `sphere`, `ellipsoid` | `r` / `size` | 전구, 종, 손잡이, 부표 |
| `torus` | `R`, `r` | 링, 체인링, 상태 표시등 |
| `joint` | `r`, `w`, `capMat` | `axis`(기본값 z)를 중심으로 한 캡이 있는 경첩 마디 |
| `wheel` | `r`, `tyre`, `rim`, `hub`, `spokes`, `spokeR`, `style` `spoked`/`disc`/`solid`, `wall`, `rimMat`, `hubMat`, `spin` | 자전거, 유모차, 카트, 캐스터 |
| `shade` | `from`(닫힘) `to`(열림), `r1`, `r2`, `t`, `bulge`, `innerMat` | 램프 갓, 종, 나팔, 스피커 콘 |
| `seat` | `size` [length,height,width], `style` `saddle`/`cushion` | 안장, 좌석, 쿠션 |
| `basket` | `size`, `style` `wire`/`slats`/`solid`, `pitch`, `wire`, `rimMat` | 바구니, 상자, 통, 쟁반 |
| `arc` | `R`, `a0`, `a1`, `r` 또는 `size` | 흙받이, 손잡이, 후프, 휜 프레임 |
| `spring` | `from`, `to`, `R`, `r`, `turns` | 스프링, 말린 코드 |
| `path` | `points`(2개 이상), `r`, `smooth` | 핸들바, 케이블, 휜 튜브, 크레인의 밧줄 |

- **소재:** `materials`에 있는 이름, 내장 이름, 또는 `{ "kind", "color": "#hex" |
  "accent", "finish": "gloss" | "satin" | "matte" }`입니다. 종류: `paint`(`color: "accent"`는 페이지의
  강조색을 받음), `metal`(헤어라인 합금), `chrome`, `steel`(어두운 스테인리스: 스포크, 와이어),
  `rubber`, `plastic`, `wood`(나이테. `grain`, `scale`), `fabric`(`weave`), `leather`, `light`(빛을 냄.
  `click`으로 전환). 어떤 소재든 `glow` 0..1(밝은 안쪽 면)을 받습니다. 내장 이름: `accent`, `paint`,
  `white`, `black`, `graphite`, `alloy`, `aluminium`, `chrome`, `steel`, `rubber`, `plastic`, `wood`, `oak`,
  `walnut`, `fabric`, `leather`, `light`.
- **모션:** 최대 네 그룹, `{ "id", "parent", "pivot": [x,y,z], "axis", "amp", "period",
  "phase", "rest" }`이며, 부품은 `"in"`으로 합류합니다. 각 그룹은 피벗(정지 상태, 스펙 단위로 지정)을
  중심으로 `rest` + `amp` x `period`초 사인만큼 부모 그룹 다음에 돕니다(로봇의 요, 어깨, 팔꿈치,
  손목). 관절은 제품이 도는 동안에만 움직입니다.

### 포스터

스펙을 바꿀 때마다 빈 포트(기본값 5905와 그 뒤 4개)에서 돌립니다.

```bash
node assets/objects/product-render/make-posters.mjs <spec.json> --profile <own chrome dir> --port <port> [--variants side,detail-saddle,three-quarter+loaded] [--grounds light,dark] [--px 1100] [--legacy]
node assets/objects/product-render/make-posters.mjs --check <spec.json>     # spec, views, scenes and shader, no browser
```

결함이 있으면(알 수 없는 부품 type, 소품, 소재, 없는 부품을 지명한 뷰나 장면, 그룹을 지명하지 않은
`in`, 90개를 넘는 부품, 노트북 GPU가 거부하는 셰이더 단어) 1로 종료하고, 없으면 소프트웨어 렌더링하는
헤드리스 Chrome 하나에서 변형(`make.variants` 또는 `--variants`)과 바탕마다
`<poster>-<variant>.fallback-render[-dark].png`(그 포스터)를, 컬러웨이마다 `stills/`에 투명한 정지
이미지 하나와 `<poster>.stills.json`을 씁니다. `--legacy`는 옛 턴테이블 포스터를 더합니다. 포스터는
즉시 보이며 WebGL2가 없거나 셰이더가 실패하거나 프레임이 비어 나오면 계속 남습니다. 포스터가 없는
스펙은 WebGL이 그릴 때까지 아무것도 보여 주지 않습니다. CPU 렌더러에서 부품 60-90개는 변형마다
1~4분입니다(부품 20-30개는 1분 미만). 각 변형은 만들어지는 대로 바로 써지므로 `--timeout <minutes>`는
끝난 것을 잃지 않고 실행을 끊고, `--variants`에 목록의 일부만 주면 실행이 짧게 유지됩니다(매니페스트는
병합됩니다). `--quiet`는 파일 줄을 뺍니다.

### 한계

- **기본은 정지 이미지이고, 요청이 있을 때만 라이브(`data-product-mode="live"`)이며, 라이브 컨텍스트는
  최대 하나입니다.** 모든 뷰에 정지 이미지가 있도록 `make-posters.mjs`를 돌립니다(만든 것이 없으면
  `auto`는 도는 쪽으로 갑니다). 요청받은 라이브 렌더 하나는 페이지의 컨텍스트 넷에 들어갑니다
  (`window.__tpGl`). 폰(최대 폭 700px 또는 coarse 포인터)과 모션 축소는 선명한 정지 프레임 하나를 받고
  컨텍스트를 해제합니다. 도는 제품은 프레임의 오른쪽 아래 모서리에 일시정지 버튼을 둡니다.
- **비용:** 모든 부품은 레이 스텝마다 평가됩니다(경계 구가 가장 가까운 적중 너머에 있으면 건너뜀).
  약 20개 부품은 프린트 오브젝트와 비슷한 비용이고, 60-70개는 노트북 GPU에서는 괜찮고 CPU에서는
  느립니다. 스펙은 90개 아래로 유지합니다.
- **할 수 없는 것:** 제품 위의 글자나 로고, 투명 유리, 드레이프되는 천, 자유로운 유기적 껍데기(신발,
  자동차 차체, 얼굴, 생물), 텍셀 하나보다 얇은 것(두껍게 만들어집니다). 그런 것은 고객의 사진이나
  렌더가 필요합니다. 게임은 기계, 건물, 소품을 구성하며 캐릭터는 구성하지 않습니다. 딱딱한 기기
  껍데기(드론, 카메라, 센서)는 실제 치수의 둥근 박스, 원기둥, 필릿이며, 주문 폼만 둔 `split` 히어로의
  이유가 되지 못합니다.
- **공들이기:** 그 물건을 알아보게 하는 디테일을 넣습니다(자전거의 스포크, 체인, 흙받이, 안장 스프링.
  램프의 스프링, 손잡이, 코드. 로봇의 캡, 이음매, 그리퍼 패드. 바지선의 볼라드, 케이블, 램프).
  강조색은 제작자가 칠할 부분에 두고, 금속과 고무는 자기 모습 그대로 둡니다. 출고하기 전에 1440과
  390에서 확인합니다.
- **금지:** 다른 종류의 제품, 장소 페이지, 캡션을 붙이거나 페이지에서 렌더, 모델, 일러스트레이션이라고
  부르는 것. 이것은 그 물건의 그림이지 효과가 아닙니다(tech에서는 효과가 그 뒤에 놓일 수 있되, 두
  번째 비트로 그 옆에 놓이지는 않습니다).

## GPU 비용

| 계열 | 등급 | 컨텍스트 |
|---|---|---|
| 프린트 오브젝트 | 프레임당 높음(레이마칭), 화면 가까이에서 움직이는 동안만. 쉬는 동안에는 선명한 프레임 하나를 보관 | 2를 공유 |
| 사진 프린트 | 낮음, 쉬는 동안 정지 | 각 1, 최대 3 |
| 장면 | 낮음, 움직이거나 단계가 넘어가는 동안만 그림 | 최대 2 |
| 제품 렌더 | 정지 이미지(`<img>`)는 없음. `still` 모드는 렌더 한 번 뒤 해제. `live`: 프레임당 높음(레이마칭, 부품이 늘수록 비용 증가), 화면 가까이에서 도는 동안만 | 0(`live`: 1) |

페이지의 배경과 효과를 합쳐 **라이브 WebGL 컨텍스트는 최대 4개**입니다. 화면 밖과 숨겨진 탭에서는
해제하고, 모션 축소에서는 정지 프레임 하나입니다.

## 금지

- **캡션.** 렌더나 프린트 아래에 설명하거나 사과하는 줄을 두지 않습니다("made in code", "a
  stand-in"). 그것이 무엇인지는 제목이 말하고, 출처는 푸터에 적습니다.
- **스크롤에 따른 애니메이션.** 뽑은 큰 장면(`fixed-hero-object`, `object-through-giant-type`) 안은
  예외입니다. 그 밖에서는 자기 느린 회전, 포인터, 클릭만 있습니다.
- **히어로 사진 위에 얹기,** 또는 고객의 사진을 대신하기.
- **비어 있기.** 셰이더가 실패하거나 WebGL이 없으면 그 포스터가 남습니다. 셰이더를 바꾼 뒤에는
  `_print-core/lint-glsl.mjs`와 `_scenes/lint-glsl.mjs`를 돌립니다. 이름에 GLSL ES 예약어는 쓰지
  않습니다. 제품 스펙은 `product-render/make-posters.mjs`(검사와 포스터를 한 번에)를 돌립니다.
