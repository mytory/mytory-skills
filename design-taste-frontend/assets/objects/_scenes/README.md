# 장면 오브젝트 (`assets/objects/<id>`, 런타임은 `_scenes`)

프린트 효과를 거쳐 보여 주는 실제 사물로, 포인터 아래에서 살아 움직입니다. 넷은 클라이언트 자신의 사진(`src`)을
받고, 하나는 일반적인 사물을 코드로 모델링합니다. 각각 카드 하나나 히어로 프레임 하나의 그림이며, 정지
상태에서는 정지하거나 거의 정지해 있고, 포인터 아래에서 움직이며, 스크롤로는 절대 움직이지 않습니다.

| id | 보여 주는 것 | 스스로 움직임 | 호버 / 터치 |
|---|---|---|---|
| `split-reveal` | 사진 한 장, 절반은 하프톤으로 인쇄되어 있고 그 사이에 선이 있음 | 아니오 | 선이 포인터를 따라감. 터치에서는 드래그. 키보드용 슬라이더 |
| `dither-sequence` | 서로 어울리는 사진 2~6장을 디더링하여 하나씩 넘김 | 예: 멈췄다가 와이프함(일시정지 원판) | 포인터로 프레임을 훑음. 터치에서는 드래그 |
| `dot-object` | 사진에서 오려 낸 사물 하나를 점으로 표현 | 아니오 | 포인터 아래에서 점이 돋보기처럼 사진의 실제 색을 띰 |
| `exploded-layers` | 사진 한 장(또는 최대 네 장)을 원근감 있는 인쇄된 시트 넷으로 | 아니오 | 시트들이 벌어짐. `names`가 있으면 각각에 라벨이 붙음. 터치에서는 탭 |
| `product-turntable` | 턴테이블 위의 일반적인 카메라, 의자, 스피커, 컵을 디더링 | 예: 1.7초마다 한 스텝(일시정지 원판) | 가로로 움직이면 한 스텝씩 돎. 터치에서는 드래그 |

`index.json`이 목록을 보여 주고, 각 폴더의 `meta.json`에 모든 파라미터(와 그 `for`, `never`)가 있으며,
`demo.html`(디스크에서가 아니라 서빙해서)은 히어로 하나와 카드 둘에 팔레트 전환기와 함께 오브젝트를 보여
줍니다.

## 어디에 쓰는가: 소프트웨어 페이지에만

**장면은 프린트(하프톤, 디더, 점)이고, 프린트는 소프트웨어, 기술, AI, 개발자 도구, 게임 페이지의 것**이며,
그 페이지의 한 모먼트로 히어로 프레임 하나나 피처 카드 하나에 씁니다. 하우스 규칙: 효과는 기술이나 게임
사이트에 어울리고, 동네 커피숍에는 절대 어울리지 않습니다.

- **장소, 서비스, 지역 업체 페이지**(카페, 바, 가게, 호텔, 병원, 사람들이 찾아가는 스튜디오): 장면을
  쓰지 않습니다. 사진은 하프톤, 디더, 점으로 인쇄하지 않고 그대로 보여 줍니다(`references/photos.md`).
- **제품 페이지**(자전거, 가구, 램프, 기기 제조사): 장면을 쓰지 않습니다. 제품 자체의 사진은 그대로
  보여 주고, 사진이 없으면 그 오브젝트 렌더(`assets/objects/print-*`, `_print-core/README.md`)를 쓰며, 장면이나
  다른 것의 스톡은 절대 쓰지 않습니다.
- **소프트웨어 페이지**에서 장면은 제품이 다루거나 함께 쓰는 실제 사물을 보여 줍니다.
  - `split-reveal`, `exploded-layers`: 사진·디자인·인쇄 도구가 다루는 사진, 기술 회사가 만드는 기기, 게임의
    키 아트. `exploded-layers`는 클라이언트의 용어로 쓴 `names`(그 소프트웨어가 다루는 레이어)가 있을 때만
    라벨을 붙이며, 이름이 없으면 라벨 없이 열리고 시트에 기법의 이름(하프톤, 디더)을 붙이지 않습니다.
  - `dither-sequence`: 서로 어울리는 사진 2~6장(여러 면에서 본 기기, 소프트웨어가 만드는 결과물의 단계,
    게임의 장면)이며, 무작위나 분위기용 세트는 절대 쓰지 않습니다.
  - `dot-object`: 이음매 없는 단색 배경(사물보다 밝거나 어둡거나 다른 색)에서 찍은 사물이나, 배경이 분명한
    오려 낸 PNG에만 씁니다. 복잡하거나 햇빛이 드는 배경은 오려 낼 수 없으므로 `split-reveal`을 씁니다.
  - `product-turntable`은 일반적인 사물을 그리며 클라이언트의 제품은 절대 그리지 않습니다. 소프트웨어가
    다루는 종류의 사물에 관한 카드에 씁니다(대여 플랫폼 재고 속의 카메라, 가구 마켓플레이스의 의자, 오디오
    앱이 제어하는 스피커).
- 한 화면에 장면 하나, 한 페이지에 최대 둘이며, 페이지의 다른 WebGL도 함께 셉니다.
- 장면 아래에는 그것을 설명하거나 변명하는 캡션을 붙이지 않습니다("made in code", "a print of", "a
  stand-in"). 카드의 제목과 본문이 그것이 무엇인지 말합니다.
- 데모 사진은 테스트용 그림입니다. 클라이언트의 것으로 출하하지 않습니다.

## 페이지에 하나 두기

```html
<article class="card">
  <h3>Every edit on its own layer</h3>
  <p>Turn any adjustment off later without touching the rest.</p>
  <div class="panel">
    <div data-scene="exploded-layers" data-scene-src="assets/img/sample-edit.jpg"
         data-scene-params='{"names":["Photo","Colour","Shade","Masks"]}'
         aria-label="A portrait taken apart into its four edit layers"></div>
  </div>
</article>
<!-- once, after system.js -->
<script type="module" src="assets/objects/_scenes/auto.js"></script>
```

오브젝트마다 하나씩, 복사해서 `src`와 문구를 바꿉니다.

```html
<div data-scene="split-reveal" data-scene-src='{"src":"assets/img/raw-scan.jpg","alt":"A scanned print, half of it screened","focus":[0.5,0.4]}' data-scene-params='{"split":0.6}'></div>
<div data-scene="dither-sequence" data-scene-src='[{"src":"assets/img/a.jpg","alt":"Front"},{"src":"assets/img/b.jpg","alt":"Side"},{"src":"assets/img/c.jpg","alt":"Back"}]'></div>
<div data-scene="dot-object" data-scene-src="assets/img/sensor-on-white.jpg" aria-label="The sensor the app reads"></div>
<div data-scene="exploded-layers" data-scene-src="assets/img/map-tile.png" data-scene-params='{"names":["Imagery","Roads","Labels","Terrain"]}'></div>
<div data-scene="product-turntable" data-scene-params='{"form":"chair"}' aria-label="A side chair from the catalogue"></div>
```

- 호스트는 빈 `div`입니다. `.panel`, `.panel__screen`, `.frame` 안에서는 상자를 채우며(상자에 크기를
  줍니다: 종횡비나 높이), 그 밖에서는 직접 크기를 줍니다.
- `data-scene-src`: 페이지 기준 상대 경로나 URL, 또는 JSON `{ src, alt, focus: [x, y], by, page,
  licence, licenceUrl }`이나 그 배열입니다. 사진은 사이트 자체에서 서빙합니다(CORS 헤더를 보내지 않는
  호스트는 프린트할 수 없으며, 그 경우 일반 사진이 대신 보입니다).
- `data-scene-params`: JSON, `meta.json`의 모든 파라미터. `data-scene-palette`: JSON `{ bg, ink,
  muted, accent }`. `aria-label`: 그림이 보여 주는 것(없으면 사진의 alt).
- **색**: 팔레트가 없으면 장면은 자기가 놓인 상자의 배경 위에 페이지 토큰(`--bg`, `--surface`, `--ink`,
  `--muted`, `--accent`)으로 인쇄합니다(`--surface` 위의 `.panel`은 `--surface` 위에 인쇄하고, 어두운 띠는
  밝은 잉크로 인쇄합니다). 자기 배경을 직접 칠하므로 일반 패널에 두며, 뽑은 효과 배경 위에는 절대
  두지 않습니다.
- **그룹당 움직이는 장면 하나**: 섹션(또는 `[data-scene-group]`)에서 첫 번째 `product-turntable`이나
  `dither-sequence`만, 또는 `data-scene-loop`이 있는 것만 스스로 움직이고, 나머지는 포인터가 닿을 때까지
  정지합니다. 움직이는 장면은 공용 32px 일시정지 원판(`.loop-pause`)을 상자의 오른쪽 아래 모서리에
  둡니다. 그 모서리는 비워 둡니다.
- 글은 패널 위나 옆에 두고 장면 위에는 절대 두지 않습니다. 효과를 설명하는 캡션도, 칩도 없습니다.
  사진의 크레딧은 페이지의 크레딧 한 줄에 넣습니다.
- **크레딧**: `import { credits } from 'assets/objects/_scenes/kit.js'`. `credits([entry, ...])`는
  장면이 인쇄하는 모든 사진의 푸터용 작은 글씨 한 줄을 돌려주며, 각 사진은 한 번씩만 이름을 댑니다
  ("Photographs: A on Unsplash, adapted; B, CC BY-SA 4.0, via Wikimedia Commons, adapted."). 그림 아래에
  크레딧을 두거나 사진마다 한 줄씩 두지 않습니다. 클라이언트 자신의 사진에는 필요 없습니다.
- **스크립트**: `import obj from 'assets/objects/split-reveal/object.js'; const ctrl = obj.mount(el,
  { src, params, palette })`. 컨트롤러에는 `pause()`, `resume()`, `setPalette(p | null)`,
  `destroy()`, `ready`(사진이 들어오면 완료되는 프로미스)가 있습니다. `auto.js`는 요소에서 컨트롤러로 가는
  Map인 `scenes`를 내보냅니다. 테마가 바뀐 뒤에는 각각에 `setPalette(null)`을 호출합니다.

## 동작

- **정지 상태에서는 정지**: `split-reveal`, `dot-object`, `exploded-layers`는 한 번 그리고, 포인터가
  움직일 때만 다시 그립니다. `product-turntable`과 `dither-sequence`는 스텝이나 와이프를 하는 동안에만
  그리며(초당 최대 30프레임) 멈춰 있는 동안에는 아무것도 그리지 않습니다.
- **스크롤로는 절대 움직이지 않음**: 화면에 들어올 때 움직이는 것은 없으며, 완성된 상태로 그려집니다.
- **모션 감소**: 정지 프레임 하나이며 일시정지 원판은 없습니다. 포인터는 여전히 선, 프레임, 돋보기,
  턴테이블을 즉시 움직입니다.
- **WebGL이 없거나, 셰이더가 실패하거나, 사진이 실패할 때**: 일반 사진(초점에 맞춰 cover로 잘림)이 패널을
  차지하고 오버레이는 사라집니다. 턴테이블은 해당 형태의 스틸을 보여 줍니다(`make-fallbacks.html`이 만드는
  `fallback-<form>-light|dark.png`). 시퀀스는 실패한 사진을 루프에서 뺍니다. 패널은 절대 비어 있지 않습니다.
  셰이더가 GLSL ES 1.00이나 3.00의 규칙을 어기거나(`kit.js`의 `glslLint`가 컴파일 전에 모든 셰이더를
  읽습니다), 컴파일이나 링크에 실패하거나, 프레임이 예외를 던지거나, 첫 프레임이 단색으로 나올 때도 스틸이
  들어갑니다. 사진이 아예 로드되지 않을 때(호스트가 내려갔거나 막힘)만 패널 자신의 배경이 남으며, 이때 호스트에
  `data-scene-empty`가 붙고 콘솔에 오류가 찍힙니다. 사진은 사이트 자체에서 서빙합니다.
- **셰이더**: 테스트용 Chrome은 WebGL을 CPU(SwiftShader)로 렌더링하므로 노트북 GPU가 거부하는 단어를
  컴파일합니다(`flat`이라는 이름의 구조체 필드가 한때 히어로를 비워 두었습니다). 셰이더를 바꾼 뒤에는
  `node assets/objects/_scenes/lint-glsl.mjs`를 실행합니다. 모든 장면 셰이더를 컴파일된 상태로 검사하며,
  예약어, 이름이나 필드로 쓰인 키워드나 타입, 밑줄 두 개, 알 수 없는 `gl_` 이름, 내장 함수를 가리는 이름이
  있으면 종료 코드 1로 끝납니다.

## 노트북 GPU에서 가볍게

- 장면마다 캔버스 하나와 WebGL 컨텍스트 하나를 가지며, 화면 밖이거나 탭이 숨겨지면 멈추고, 화면을 벗어난 지
  1.5초 뒤에 해제되며, 돌아오기 전에 다시 만들어집니다.
- 장면 컨텍스트는 동시에 최대 2개만 살아 있을 수 있으며(`kit.js`의 `config.live`) 이는 하드 상한입니다.
  화면 밖의 것이 먼저, 그다음 한가한 것, 그다음 정지한 것이 자기 것을 내놓습니다(각각 마지막 프레임을
  그림으로 유지). 페이지의 배경과 다른 효과까지 함께 세어 한 페이지에 라이브 컨텍스트 4개를 지킵니다.
- 부드러운 캔버스는 CSS 픽셀당 캔버스 픽셀 1개 이하로 렌더링하고(레이어는 1 MP를 넘는 프레임에서 0.75),
  1.5 MP를 넘지 않습니다. 디더링한 캔버스는 디더 셀당 캔버스 픽셀 1개를 가집니다. MSAA는 없습니다. 점과
  레이어는 정적 버퍼에서 그리며, 프레임마다 CPU에서 도는 것은 없습니다.
