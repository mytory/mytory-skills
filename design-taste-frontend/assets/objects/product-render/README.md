# 제품 렌더 (`assets/objects/product-render`)

**어떤 물리적 제품이든** 짧은 JSON 스펙으로 구성하는 스튜디오 렌더입니다. 스펙은 제품 자체의 단위로 된
크기와 위치를 가진 부품 목록입니다. `build.js`가 스펙을 모델로 바꾸고 `_print-core/print3d.js`가
렌더링합니다. 실제 재질(도장한 금속, 합금, 크롬, 고무, 나무, 직물, 가죽, 플라스틱, 광원), 부드러운
그림자가 있는 부드러운 스튜디오 조명, 광택 부품에 비치는 소프트박스, 바닥 그림자, 액센트를 요구하는
부품에 입히는 페이지의 액센트를 다룹니다. 턴테이블처럼 천천히 흔들리거나 가만히 서 있고, 램프는 클릭하면
켜졌다 꺼지며, 로봇의 관절은 움직입니다.

**브리프가 3D나 렌더를 요구할 때**(구성기, 모델로만 존재하는 제품) 씁니다. 이때 렌더가 히어로와
설명 섹션에서 제품의 그림이 됩니다. 사진이 없고 그런 요구도 없는 제품은 자기 사진이나 대체 사진으로
보여 줍니다(`references/photos.md`). 사진이 있는 제품에는 절대 쓰지 않고, 장소 페이지에도, 캡션을 붙이는
용도로도, 다른 종류의 제품에도 쓰지 않습니다. 페이지당 제품 렌더는 하나입니다.

## 마운트: 앵커 크기의 제품

```html
<div class="frame" id="bike" data-product="assets/objects/product-render/specs/my-bike.json"
     data-product-place="stage" data-product-view="side" data-product-color="blue"></div>
<script type="module" src="assets/objects/product-render/auto.js"></script>
```

프레임이 곧 그림입니다. 제품 자체의 경계가 프레임의 일정 비율(너비와 높이 중 빡빡한 쪽)을 채우고,
페이지의 바닥 위에 바닥 그림자와 함께 서며, 주변은 투명합니다. **패널도 회색 상자도 없습니다.** 프레임에
크기를 주면(화면 높이만큼 큰 히어로 열, 전체 너비의 무대, 타일) 제품이 그것을 채웁니다.

| 속성 | |
|---|---|
| `data-product-place` | 프레임의 `hero` 0.88, `stage` 0.86, `tile` 0.84, `card` 0.9 (`legacy`: 글 오른쪽의 옛 턴테이블) |
| `data-product-view` | `three-quarter`(기본값), 그다음 스펙이 `supports`에 나열한 뷰만(`side`, `front`, `top`, `detail-saddle` 같은 자체 클로즈업). `product.views`가 목록을 보여 주며, 그 밖의 뷰(자전거의 `top`)는 예외를 던지고 프레임에 `data-product-error`가 붙습니다. 또는 `detail:<부품 이름>` |
| `data-product-scene` | 스펙의 장면, 짐을 싣거나 쓰이는 중인 제품(`loaded`, `desk`, `work`) |
| `data-product-color` | 스펙의 컬러웨이 id(`spec.colors`). 기본값은 첫 번째 |
| `data-product-mode` | `auto`(기본값): make-posters가 만든 스틸, 없으면 턴, 없으면 여기서 한 프레임 렌더. `image`, `still`, `live`는 하나를 강제 |
| `data-product-fill` | 0.3~1.2, place의 비율에 곱함 |
| `data-product-params` | `{"turn":1}`은 실시간 턴을 요청, `{"x":0.1,"y":-0.05}`는 위치를 옮김, `{"step":0}`은 램프 끄기 |
| `data-product-palette` | `{ bg, surface, ink, accent }`. 없으면 페이지 토큰 `--bg`, `--ink`, `--accent` |

**섹션마다 다른 뷰.** 제품 페이지는 제품을 크게, 전체가 보이게 최대 세 섹션에 보여 주며 같은 뷰를
두 번 쓰지 않습니다. 히어로에는 가장 넓은 뷰(자전거의 `side`, 램프나 로봇 팔의 `three-quarter`), 스펙
옆에는 다른 각도, 섹션이 말하는 부품에는 클로즈업, 카피가 무엇을 실을 수 있는지 약속하는 곳에는 짐을 실은
장면을 둡니다. 헤드라인의 모든 약속은 그림으로 보여 줍니다(벨트가 달린 아이 시트, 상자들, 책상 위 램프의
빛).

**클로즈업**(`detail-*`, `detail:<부품>`)은 이름 붙은 부품을 프레임에 맞춰 가운데에 둡니다(그 상자,
매니페스트의 `focus`가 place의 비율을 채웁니다). 제품의 나머지는 프레임 가장자리 밖으로 흘러 나가며(프레임이
잘라 냅니다), 그 안에서 딱딱하게 잘리는 곳은 없습니다. 넓은 타일에서도 그렇게 되도록 클로즈업의 샷은
충분히 넓게 만들고(`cover`, 기본값 2: 높이의 최대 두 배 너비의 프레임, 1 : 1.25는 세로로 긴 프레임)
제품이 부품 너머로 갈 수 있는 데까지 이어지게 하며, 스틸은 제품 자체의 상자가 아니라 부품들의 중심을
기준으로 고르게 잘라 냅니다.

**주문 카드의 색상.** 스와치는 스크립트 없이 자신이 지정한 프레임을 조작합니다.

```html
<button type="button" data-product-swatch="#bike, #bike-loaded" value="red" aria-pressed="false">Signal red</button>
<input type="radio" name="colour" value="red" data-product-swatch="#bike">
```

클릭(버튼이면 `aria-pressed`가 유지되고 그룹당 하나만 눌림)이나 change(input)가 일어나면 지정한 프레임(기본값:
해당 컬러웨이가 스펙에 있는 모든 프레임)이 `data-product-color`를 설정하고 그 색의 스틸로 바뀝니다.
마운트된 프레임에 `data-product-color`, `-view`, `-scene`을 설정해도 같고, 이벤트도 같습니다.
`el.dispatchEvent(new CustomEvent('product:set', { detail: { color: 'red', view: 'side' } }))`, 또는
`document`에서 `detail.target`에 선택자를 줍니다.

**프레임이 알려 주는 것**(검사기와 테스트용): `data-product-mode`, `data-product-state`(`image` |
`still` | `live` | `poster`), `data-product-view`, `data-product-color-shown`. 그림은
`img.product-render__img`이고, `window.__tpProduct` = `{ stills, images, live, freed }`입니다. `image`
모드에서는 페이지에 캔버스도 WebGL 컨텍스트도 없습니다. `still`은 한 번 렌더링하고 `<img>`를 유지하며
컨텍스트를 해제하고 캔버스를 제거합니다. `live`만 컨텍스트를 유지합니다(`window.__tpGl`에도 계산됩니다).
제품 페이지는 스틸을 씁니다(make-posters를 한 번 돌린 뒤의 기본값). `still`은 측정되어(불투명 픽셀과
클로즈업의 부품) 포스터 스틸과 같은 레이아웃으로 배치되므로 place의 비율(타일 .84)을 정확히 채우고
가운데에 놓입니다.

스크립트: `import { loadProduct } from '.../product-render/build.js'; const p = await loadProduct(url);
const ctrl = p.mount(el, { place: 'stage', view: 'side', scene, color, mode });` 컨트롤러에는
`setColor(id)`, `setView(v)`, `setScene(s)`, `ready()`, `pause()`, `resume()`, `step(on)`,
`set(params)`, `setPalette(p | null)`, `destroy()`가 있습니다. `auto.js`는 `products`(프레임과 컨트롤러의
대응)와 `ready`를 내보냅니다. 이 파일 옆의 `views.html`이 실제 예시입니다(모든 뷰, 스펙마다 장면 하나, 색상
전환 둘, `still` 마운트 하나).

## 스틸과 포스터: 스펙을 바꿀 때마다 실행합니다

```
node assets/objects/product-render/make-posters.mjs path/to/spec.json --profile <own chrome dir> [--port 5905]
     [--variants side,detail-saddle,three-quarter+loaded] [--grounds light,dark] [--px 1100] [--timeout 9] [--quiet] [--legacy]
node assets/objects/product-render/make-posters.mjs --check path/to/spec.json      (spec, views, scenes and shaders only)
```

스펙을 검사하고(알 수 없는 부품·프롭·재질, 뷰나 장면이 이름을 댔는데 없는 부품, 너무 많은 부품, 노트북
GPU가 거부하는 셰이더 단어) 헤드리스에 소프트웨어 렌더링되는 Chrome(자기 프로필을 쓰고 자기 PID로
닫으며 포트 3000은 절대 쓰지 않음)에서 `spec.make.variants`의 모든 변형(`view` 또는 `view+scene`)을
`spec.make.grounds`의 각 배경 위에 렌더링한 뒤, 스펙 옆에 다음을 씁니다.
`stills/<id>-<variant>-<colour>[-dark].webp`와 `-half.webp`(컬러웨이마다 스틸 하나, 투명, 제품과 그
그림자에 맞춰 잘림), `<id>-<variant>.fallback-render[-dark].png`(실시간 렌더의 포스터), 그리고
`<id>.stills.json`(무엇을 만들었는지, 제품과 클로즈업의 프레이밍된 부품이 어디에 놓이는지, 클로즈업이 어느
쪽을 자르는지)입니다. 컬러웨이는 렌더 비용이 없습니다. 액센트 부품에 각 색으로 조명을 다시 줍니다. 각
변형은 만들어지는 대로 바로 기록됩니다. 부품 60~90개면 CPU로 변형당 1~4분이 걸리므로 `--variants`에는
몇 개씩만 넘깁니다. `--legacy`는 턴테이블의 포스터 네 장도 씁니다. 스틸이 없는 뷰는 페이지에서 한 번
스스로 렌더링하고(`still` 모드) 컨텍스트를 해제합니다.

## 스펙

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

축: **x는 앞쪽**(제품의 전면), **y는 위**, **z는 가로**(각도 0일 때 보는 사람 쪽). 단위는 자유이며,
모델은 가장 큰 변이 1 단위가 되도록 스케일되고 가장 낮은 지점이 바닥에 놓입니다. 제품은 실제 치수로
모델링합니다. 렌더처럼 읽히는 데는 비율이 대부분을 차지합니다.

| 키 | 내용 |
|---|---|
| `id`, `name`, `label` | label은 스크린 리더가 읽는 문장입니다("A desk lamp, switched on") |
| `poster` | 포스터의 파일 이름(기본값은 id) |
| `angle` | 정지 상태와 스틸에서의 회전 각도, 도 단위(기본값 -32: 쓰리쿼터 뷰) |
| `turn` | `{ "mode": "sway", "amp": 26, "period": 22 }`(기본값), `{ "mode": "spin", "speed": 10 }`, `{ "mode": "still" }` |
| `camera` | `{ "elev": 12 }` 바닥 위 각도, 도 단위 |
| `click` | `"light"`: 클릭하면 모든 `light` 재질(과 `glow`)이 켜졌다 꺼집니다. 켜진 상태로 시작 |
| `pool` | `{ "at": [x, 0, z], "r": 0.2 }`: 켜져 있을 때 바닥에 드리우는 빛 |
| `materials` | 부품에 쓰는 이름 붙은 재질 |
| `motion` | 움직이는 그룹(관절), 아래 참고 |
| `colors` | 컬러웨이: `[{ "id": "blue", "name": "Deep blue", "accent": "#2c4f7c" }]`(액센트 부품이 이 색을 받음. `materials`는 재질도 바꾸며 렌더 한 번씩 듦) |
| `views` | 클로즈업과 자체 뷰: `{ "detail-saddle": { "part": ["saddle*", "seat post"], "angle": -42, "elev": 16, "margin": 1.3, "cover": 2 } }`(`*`로 끝나는 이름은 그 이름으로 시작하는 모든 부품을 가리킴. `cover`는 샷이 채우는 가장 넓은 프레임이고 1이면 여백만. 2~3 MP 클로즈업 렌더는 CPU로 2~9분 걸림) |
| `scenes` | 짐을 싣거나 쓰이는 중인 제품, 아래 참고 |
| `supports` | 제품이 잘 그려지는 뷰, `["three-quarter", "side", "front", "detail-saddle"]`: 이 뷰만 제공되고(`product.views`), 만들어지고(밖에 있는 `make.variants`는 `--check`에서 실패), 마운트됩니다. 뷰는 스틸을 보고 나서야 목록에 올립니다(위에서 본 자전거는 옆으로 누운 것처럼 읽혀서 city bike는 `top`을 뺍니다). `three-quarter`(기본 뷰)는 유지합니다 |
| `make` | `{ "variants": ["three-quarter", "side", "detail-saddle", "three-quarter+loaded"], "grounds": ["light", "dark"], "px": 1100 }`: make-posters가 만드는 것 |
| `parts` | 부품, 아래 참고(약 90개 아래로 유지) |

### 부품

모든 부품은 `mat`(재질 이름 또는 인라인 재질), `blend`(앞에 나열한 부품과 만나는 곳의 필릿, 단위는 스펙
단위: 용접한 튜브, 주조 몸체), `in`(모션 그룹), `name`(자신을 위한 이름)을 받습니다. 배치는 `from` + `to`(선형
부품은 그 사이로 뻗음. `up`은 단면을 돌림), 또는 `at`에 `axis`(`"x"`, `"y"`, `"z"` 또는 벡터)와/또는
`rot`([x, y, z] 도 단위)로 합니다.

| 타입 | 크기 | 용도 |
|---|---|---|
| `tube` | `r`, `r2`(테이퍼), `cap` `flat`/`round`, `round`, `seams` | 프레임 튜브, 기둥, 막대, 손잡이, 테이퍼진 로봇 링크 |
| `beam` | `w`, `d`(단면), `round`, `seams` | 납작한 바, 크랭크, 레일 |
| `box` | `size` [x, y, z], `round`, `seams` | 하우징, 몸체, 페달, 그리퍼 |
| `panel` | `size`(얇음), 더 둥글게 | 판, 뚜껑, 화면의 뒷면 |
| `cylinder` / `disc` | `r`, `h`, `round`, `seams` | 베이스, 허브, 모터 하우징, 캡 |
| `sphere`, `ellipsoid` | `r` / `size` | 전구, 종, 노브 |
| `torus` | `R`, `r` | 링, 체인링, 상태 표시등 |
| `joint` | `r`, `w`, `capMat` | 힌지: `axis`(기본값 z)를 중심으로 한 너클과 양면의 캡 |
| `wheel` | `r`, `tyre` [너비, 높이], `rim` [깊이, 너비], `hub` [r, 길이], `spokes`, `spokeR`, `style` `spoked`/`disc`/`solid`, `wall`(옆면 색), `rimMat`, `hubMat`, `spin`(도/초) | 자전거, 유모차, 카트, 캐스터. 축은 `axis`(기본값 z)를 따라감 |
| `shade` | `from`(닫힌 끝) `to`(열린 끝), `r1`, `r2`, `t`, `bulge` 0..1, `innerMat` | 램프 갓, 종, 나팔, 스피커 콘 |
| `seat` | `size` [길이, 높이, 너비], `style` `saddle`/`cushion` | 안장, 좌석, 쿠션(로컬 x가 앞) |
| `basket` | `size`, `style` `wire`/`slats`/`solid`, `pitch`, `wire`, `rimMat` | 바구니, 상자, 통, 트레이(위가 열림) |
| `arc` | `R`, `a0`, `a1`(도), `r` 또는 `size` [반경, 축 방향] | 흙받이, 손잡이, 휜 프레임, 고리 |
| `spring` | `from`, `to`, `R`, `r`, `turns` | 스프링, 꼬인 코드 |
| `path` | `points` [[x,y,z]...], `r`, `smooth`(3개 이상이면 켜짐) | 핸들바, 케이블, 구부러진 튜브 |

`seams`: 부품의 길이 방향 높이마다 둘레로 파는 패널 선(반 길이의 -1..1): 로봇 외피의 이음매, 베이스의
홈. `seamWidth`, `seamDepth`는 스펙 단위입니다.

### 재질

`materials`의 이름, 내장 이름, 또는 `{ "kind": ..., "color": "#hex" | "accent", "finish": "gloss" | "satin" | "matte" }`입니다.

| kind | | 내장 이름 |
|---|---|---|
| `paint` | 에나멜 또는 분체 도장. `color: "accent"`는 페이지의 액센트를 받음 | `accent`, `paint`, `white`, `black`, `graphite` |
| `metal` | 브러시드 합금 | `alloy`, `aluminium` |
| `chrome` | 광택 | `chrome` |
| `steel` | 어두운 스테인리스(스포크, 와이어) | `steel` |
| `rubber` | 타이어, 패드, 그립 | `rubber` |
| `plastic` | 새틴 플라스틱 | `plastic` |
| `wood` | 나이테가 있는 오일 마감 나무. `grain` x/y/z, `scale` | `wood`, `oak`, `walnut` |
| `fabric` | 고운 직조. `weave` | `fabric` |
| `leather` | | `leather` |
| `light` | 빛을 냄. `click: "light"`가 있으면 켜고 끔 | `light` |

모든 재질은 `glow`(0..1)를 받습니다. 안쪽 면이 빛나게 합니다(램프가 켜졌을 때 갓의 안쪽).

### 모션

```json
"motion": [
  { "id": "yaw", "pivot": [0, 0.14, 0], "axis": "y", "amp": 26, "period": 13 },
  { "id": "shoulder", "parent": "yaw", "pivot": [0, 0.32, 0], "axis": "z", "amp": 9, "period": 11, "phase": 0.2 }
]
```

그룹은 자기 부품(`"in": "shoulder"`)을 `pivot`과 `axis`를 기준으로 `rest` + `amp` x `period`초의
사인만큼 돌리며, 부모의 움직임 뒤에 적용됩니다. 피벗은 정지 상태에서 스펙 단위로 줍니다. 그룹은 최대
넷입니다. 관절은 제품이 돌 때만 움직입니다. 스틸, 휴대폰, 모션 감소 환경에서는 정지 자세를 보여 줍니다.

### 장면과 프롭: 짐을 싣거나 쓰이는 중인 제품

```json
"scenes": {
  "loaded": { "label": "A city bicycle with a child seat on the rack, a crate of fruit and a pannier",
    "hide": ["basket"],
    "props": [ { "prop": "child-seat", "at": [-0.578, 0.796, 0] },
               { "prop": "crate", "at": [0.6, 0.76, 0], "size": [0.3, 0.2, 0.32], "contents": "fruit" },
               { "prop": "bag", "at": [-0.62, 0.42, 0.152], "hooks": true } ] },
  "desk": { "lit": { "at": [0.53, 0.11], "r": 0.19, "k": 3.6 }, "pool": null,
    "props": [ { "prop": "desk", "at": [0.2, -0.032, 0.02] }, { "prop": "book", "at": [0.3, 0, -0.15], "count": 2 } ] }
}
```

장면은 프롭(그리고 일반 `parts`)을 더하고, 이름으로 부품을 숨기며, `label`, `pool`, `click`,
`materials`를 바꿀 수 있습니다. `lit`는 램프의 따뜻한 빛웅덩이를 프롭의 위쪽 면에 던집니다. 프롭은 실물
크기의 일반 부품으로 만들며 y = 0에 서서 x를 향하고 단위는 미터입니다(`scale`이 변환합니다. 밀리미터 단위
스펙이면 1000). 각 프롭은 `at`, `yaw`, `scale`, `size`, `color`, `mats` { 역할: 재질 }, `in`(모션 그룹:
그리퍼가 잡은 소포), `name`을 받습니다.

| 프롭 | 내용 | 옵션 |
|---|---|---|
| `child-seat` | 랙 시트: 높은 등받이, 날개, 쿠션, 빨간 버클로 이어지는 어깨·허리 벨트, 발 받침 | `color`. 역할 shell, pad, belt, buckle |
| `bench` | 어린이나 승객 1~3명이 한 줄로 앉는 패딩 벤치(카고 박스): 좌석마다 벨트 둘과 버클 하나 | `seats`, `width`, `color`. 역할 frame, pad, belt, buckle |
| `crate` | 위가 열린 널빤지 나무 상자 | `size`, `contents` fruit / bottles / loaves / parcels / none |
| `bag` | 패니어(덮개, 끈, 손잡이, 랙용 `hooks`) 또는 `style: "tote"` | `size`, `color` |
| `parcel` | 테이프와 라벨이 붙은 골판지 상자 | `size`, `color` |
| `tray` | 소포가 서 있는 낮고 열린 통 | `size`, `parcels` 0-4 |
| `desk` | 탁자 상판 | `size`, `color` |
| `book` | 쌓인 책 1~3권 | `count`, `colors` |
| `mug` | 커피가 담긴 머그 | `r`, `h`, `color` |
| `sheet` | 종이 한 장 | `size` |

장면은 약 110개 부품 아래로 유지합니다. 프롭은 페이지가 보여 주는 크기에서 읽혀야 하며(벨트, 버클, 상자의
널빤지, 가방의 덮개), 장면은 카피가 약속하는 곳에 둡니다.

## 동작과 한계

- **항상 그림을 보여 줍니다**: 그 뷰의 스틸(WebGL 없음). 스틸이 없으면 포스터를 바로 보여 주고 그 위에
  렌더를 얹으며, WebGL이 실패하면 포스터가 남습니다. `prefers-reduced-motion`이나 휴대폰(max-width 700px
  또는 coarse 포인터)에서는 선명하게 그린 정지 프레임 하나를 보여 주고 컨텍스트를 해제합니다. 돌아가는
  제품에는 프레임의 오른쪽 아래 모서리에 일시정지 버튼이 있습니다.
- **제품에 라이브 컨텍스트는 최대 하나**: 마운트된 첫 번째 제품 렌더만 돌며(페이지가 턴을 요청하거나 스틸이
  만들어지지 않은 경우), 두 번째는 정지합니다. 페이지의 컨텍스트 상한 4개(`window.__tpGl`)에 이것도
  계산됩니다.
- **비용**: 모든 부품은 레이 스텝마다 평가되며, 경계 구가 지금까지 가장 가까운 부품보다 멀면 건너뜁니다.
  부품 약 20개는 프린트 오브젝트처럼 렌더링되고, 60~70개(스포크가 있는 자전거)는 노트북 GPU에서는
  괜찮지만 CPU 렌더러에서는 느립니다(포스터: 약 90초). 90개 아래로 유지합니다.
- **할 수 없는 것**: 제품 위의 글자나 로고, 투명한 유리, 늘어지는 천, 자유로운 유기적 외피(신발, 얼굴, 자동차
  차체), 텍셀 하나보다 얇은 모든 것(두껍게 만들어 버림). 이런 것은 클라이언트의 사진이나 렌더를 쓰고,
  이것으로 만들지 않습니다.
- **절대** 다른 종류의 제품에 쓰지 않고, 장소 페이지에 쓰지 않으며, 아래에 캡션을 붙이지 않습니다.

`specs/`의 스펙 셋(시티 자전거, 데스크 램프, 로봇 팔)은 각각 뷰, 장면, 컬러웨이를 갖춘 실제 예시입니다
(스펙에 `make-posters.mjs`를 돌려 스틸을 만들 수 있으며, 그 전에는 각 프레임이 스스로 한 번 렌더링합니다).
`views.html`은 앵커 크기에서 색상 전환과 함께 이들을 보여 주고(`?only=bike|lamp|arm`,
`?mode=still|live`), `demo.html`은 턴테이블을 보여 줍니다(`?turn=0`, `?fallback=1`).
