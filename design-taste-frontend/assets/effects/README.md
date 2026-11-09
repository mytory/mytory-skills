# 효과

코드로 그린 효과 배경 25개로, 히어로 프레임·기능 카드·띠 영역에 씁니다. 모든 효과는 색을 전부 페이지
팔레트에서 가져옵니다. 여기서는 동영상이나 다른 라이브러리를 불러오지 않습니다. 사진 보정(photo grade)만
이미지를 받으며, 그 이미지는 해당 섹션의 사진입니다.

- `gallery.html`은 모든 효과를 실시간으로 보여 주며, 팔레트 전환기, 무작위 뽑기, UI 키트의 기능 카드가
  들어 있습니다. `lab.html`에는 모든 파라미터와 카드, 넓은 레이아웃과 히어로 레이아웃용 슬라이더가
  있습니다.
- 두 페이지 모두 `file://`가 아니라 http가 필요합니다. `node scripts/effects.mjs serve --port 5230`을
  실행한 뒤 `/assets/effects/gallery.html`을 엽니다.

## 마운트

요소에 크기와 `data-fx` id를 주고, 페이지의 모든 요소를 마운트합니다.

```html
<div class="panel" data-fx="caustics" data-fx-seed="21"></div>

<script type="module">
  import fx from './assets/effects/fx.js';
  fx.mountAll(document);
</script>
```

- **팔레트.** 각 요소는 `--bg`, `--surface`, `--ink`, `--muted`, `--accent`, `--accent-ink`를 읽거나,
  `--fx-bg`와 나머지 `--fx-*` 이름을 읽으며 후자가 우선합니다. 직접 넘길 수도 있습니다.
  `fx.mountAll(document, { bg, surface, ink, muted, accent, accentInk })`. 한 요소에서 색 하나만 바꾸려면
  `data-fx-palette='{"accent":"#..."}'`를 씁니다.
- **시드.** `data-fx-seed`는 구도를 고정합니다. 시드가 없으면 로드할 때마다 새로운 그림이 나옵니다.
- **파라미터.** `data-fx-params='{"speed":0.3}'`. `index.json`에 각 파라미터와 범위가 나와 있습니다.
  효과 위의 텍스트는 `calmX`와 `calmY`(프레임의 0~1)를 텍스트가 놓인 위치로 설정합니다. 효과는 그
  영역을 조용하게 유지합니다.
- **요소 하나.** `const c = await fx.mount(el, 'caustics', { palette, seed, params })`. 결과 `c`에는
  `pause()`, `resume()`, `set(params)`, `setPalette(p)`, `destroy()`가 있습니다.
- **내장 동작.** 효과는 화면을 벗어나거나 탭이 숨겨지면 그리기를 멈춥니다. `prefers-reduced-motion`에서는
  정지 프레임 하나를 보여 줍니다. WebGL이 없으면 같은 색의 CSS 그림을 보여 줍니다. 기기 픽셀 비율에는
  상한이 있습니다(효과가 선명한 픽셀을 필요로 하지 않는 한 1.75). 페이지에 살아 있는 WebGL 컨텍스트가
  14개를 넘으면 화면 밖에서 놀고 있는 것부터 해제합니다.
- 텍스트와 UI 조각은 요소 안에 넣습니다. 캔버스는 그 아래에 놓입니다(격리된 요소 안에서
  `z-index: -1`).

## 무작위 뽑기

페이지의 효과는 취향으로 고르지 않고 뽑습니다. 슬롯 하나에 효과 하나이며, `hero`는 히어로 또는 큰 분할
프레임, `card`는 카드 그룹, `band`는 넓은 띠 또는 마무리 행동 유도, `footer`는 푸터입니다. 페이지의 팔레트
종류(meta.json의 `palettes`)와 해당 슬롯에 맞게 만든 효과만 뽑으며, 한 페이지에서 같은 id를 두 번 뽑지
않습니다(슬롯에 맞는 효과가 모두 이미 페이지에 있으면 하나가 자기 시드로 반복되고 pick이 안내를
출력합니다). 이 명령에는 `--palette`가 필요하며, 브라우저에서는 팔레트 없이 호출하면 세 종류 모두에 맞게
만든 효과만 뽑습니다. 최근 페이지에서 쓴 id와, 이미 뽑은 계열에서의 두 번째 뽑기는 확률이 낮아집니다.
서로를 `avoidWith`에 적은 두 효과는 한 페이지에 함께 나오지 않습니다.

**초점(focal)** 배경(`"focal": true`)은 구, 빔, 봉우리, 빛웅덩이 같은 자기만의 주제가 있습니다. 작은 UI
조각 하나만 올릴 수 있고, 큰 창이나 스크린샷이나 텍스트는 올리지 않습니다. `--quiet`(브라우저에서는
`quiet: true`)는 고르고 **조용한** 배경만 뽑으며, 큰 창이 올라가는 슬롯에 씁니다.

효과 넷은 절대 뽑지 않습니다(meta.json의 `"random": false`). `dotted-globe`(글자 그대로의 주제로,
결제·인프라·물류·네트워크처럼 도달 범위가 전 세계인 제품에만), `duotone-grade`(섹션 자체의 사진을 보정),
`edge-glow`(핵심 오브젝트 하나인 프롬프트 상자나 추천 요금제의 빛나는 테두리), `ridgeline`
(`assets/components/fx-band`의 구분 띠)입니다. 내용이 필요로 할 때 해당 슬롯에 이름으로 지정합니다. 그래도
맞지 않는 팔레트 종류나 슬롯, 같은 id를 두 번 지정한 경우, 피하는 효과 옆(지정했거나 `--exclude`로
넘긴 경우)에는 거부됩니다.

```bash
node scripts/effects.mjs pick --palette dark --slots hero,card,band --seed 4821 --history .taste-skill/effects-history.json
node scripts/effects.mjs pick --palette dark --slots hero:dotted-globe,card,band --seed 4821 --history .taste-skill/effects-history.json
```

브라우저에서는 같은 코드를 씁니다.

```js
import { pick } from './assets/effects/pick.js';
const index = await fetch('./assets/effects/index.json').then(r => r.json());
const { picks } = pick(index.effects, { palette: fx.paletteKind(palette), slots: ['hero', 'card', 'card'], history });
// picks: [{ slot: 'hero', id: 'god-rays' }, ...]; history: the ids of earlier picks, oldest first
// a named slot: slots: ['hero:dotted-globe', 'card'] (or { slot: 'hero', id: 'dotted-globe' })
```

`fx.paletteKind(palette)`는 배경색으로 `light`, `dark`, `colour` 중 하나를 돌려줍니다.

## 목록

| id | 이름 | 계열 | 슬롯 | 팔레트 | 배경 | 움직임 |
|---|---|---|---|---|---|---|
| `film-light-leak` | 필름 빛 샘 | Grain | hero, card, band | dark, colour | focal | slow |
| `grain-gradient` | 그레인 그라디언트 | Grain | hero, card, band, footer | light, dark, colour | quiet | slow |
| `ascii-shade` | ASCII 음영 | Dither | hero, card, footer | light, dark, colour | focal | slow |
| `bayer-dither` | 바이어 디더 | Dither | hero, card, band, footer | light, dark, colour | quiet | slow |
| `halftone-screen` | 하프톤 스크린 | Dither | hero, band | light, dark, colour | quiet | slow |
| `line-engraving` | 선 판화 | Dither | hero, card, band | light, dark, colour | quiet | still |
| `aurora-curtains` | 오로라 커튼 | Mesh | hero, band, footer | dark, colour | focal | slow |
| `gradient-mesh` | 그라디언트 메시 | Mesh | hero, card, band | light, dark, colour | quiet | slow |
| `painterly-landscape` | 회화풍 풍경 | Mesh | hero, card | light, dark, colour | quiet | slow |
| `god-rays` | 신의 광선 | Light | hero, band | dark, colour | focal | slow |
| `orb-sphere` | 빛의 구 | Light | hero, card, band | light, dark, colour | focal | slow |
| `prism-dispersion` | 프리즘 빛 | Light | hero, card, band | dark | focal | slow |
| `soft-light-bars` | 부드러운 빛줄기 | Light | hero, card, band, footer | light, dark, colour | focal | slow |
| `spotlight-cone` | 무대 스포트라이트 | Light | hero, card | dark, colour | focal | slow |
| `caustics` | 물의 코스틱 | Light | hero, card, band | light, dark, colour | focal | slow |
| `edge-glow` | 가장자리 글로우(지정 전용) | Light | card | light, dark, colour | border | slow |
| `dot-terrain` | 점 지형 | Pattern | hero, card, band | light, dark, colour | quiet | slow |
| `grid-pulse` | 격자 펄스 | Pattern | hero, card, band | light, dark, colour | quiet | slow |
| `ruled-grounds` | 줄 친 점 배경 | Pattern | card, band | light, dark, colour | quiet | slow |
| `contour-lines` | 지형 등고선 | Pattern | hero, card, band, footer | light, dark, colour | quiet | slow |
| `dotted-globe` | 점으로 된 지구본(지정 전용) | Pattern | hero, card, band | light, dark, colour | focal | slow |
| `ridgeline` | 능선(지정 전용) | Pattern | band | light, dark, colour | focal | slow |
| `fluted-glass` | 플루티드 유리 | Material | hero, card, band | light, dark, colour | quiet | slow |
| `silk-folds` | 실크 주름 | Material | hero, card, band | light, dark, colour | quiet | slow |
| `duotone-grade` | 듀오톤 보정(지정 전용) | Photo | hero, card, band | light, dark, colour | quiet | still |

각 효과의 한 줄 설명은 `index.json`의 `look` 필드입니다. `node scripts/effects.mjs list`는 이 표를
출력하며, `--family`, `--on`, `--palette`, `--motion`, `--quiet`로 걸러 낼 수 있습니다. 존재하지 않는
필터 값은 빈 목록이 아니라 오류입니다.

10월 31일에 보기 흉하거나 싸 보여서 퇴출한 것: `riso-print`, `ink-bloom`, `liquid-chrome`, `metaballs`,
`brushed-metal`, `paper-texture`, 이어서 `terrazzo-speckle`(주방 바닥), `marble-warp`(얼룩말 줄무늬),
`pixel-mosaic`(깨진 JPEG 블록), `truchet-arcs`(굵은 회색 벌레), `soft-particles`(스톡 보케)입니다.
이들은 색인에 없습니다. `ridgeline`은 혼자 뽑히면 음반 표지처럼 보여서 지정 전용입니다.

## 명령

```bash
node scripts/effects.mjs index      # rebuild index.json from every <id>/meta.json and effect.js
node scripts/effects.mjs gallery    # write gallery.html and lab.html from scripts/*.template.html
node scripts/effects.mjs publish    # the gallery as one folder: publish/index.html, effects/, ui/, files.json
```

`gallery.html`이나 `lab.html`이 아니라 `scripts/`의 템플릿을 수정합니다. `publish`는 두 페이지를 다시
만든 뒤 갤러리가 불러오는 파일만 복사합니다. `files.json`은 그 파일을 모두 상대 경로로 나열합니다.

## 효과 추가

`<id>/` 폴더에 파일 두 개를 둡니다.

- `meta.json`: `id`, `name`, `family`(grain, dither, mesh, light, pattern, material, photo), `look`(한
  문장), `bestOn`, `palettes`, `motion`(`still`, `slow`, `interactive`), `cost`. 선택 항목: 글자 그대로의
  주제라 지정만 하고 뽑지 않는 `"random": false`, 자기만의 주제가 있는 배경의 `"focal": true`,
  `avoidWith`(자기 페이지에 함께 나오지 않는 id), `subjects`(지정 전용 효과가 쓰이는 대상).
- `effect.js`: `export default { id, name, family, params, mount(el, { palette, params, seed }) }`.
  `mount`는 `{ destroy, pause, resume }`을 돌려줍니다.
  - 프래그먼트 셰이더에는 `fx.shader(el, { frag, schema, params, palette, seed, fallback })`를 씁니다.
    캔버스, 수명 주기, DPR 상한, 컨텍스트 예산, CSS 대체 그림을 처리합니다.
  - 캔버스 2D에는 `fx.lifecycle(el, { draw })`를 씁니다.
  - 자기 WebGL 컨텍스트를 만드는 효과는 직전에 `fx.glBudget(holder)`를 호출해, 그 컨텍스트가 페이지의
    예산에 계산되게 합니다(`dotted-globe` 참고).

모든 색은 팔레트에서 가져와 OKLab(`fx.color`)으로 섞습니다. 고정 색상을 쓰지 말고, 기본값을 보라나
라벤더로 두지 않습니다. 효과 위의 텍스트는 4.5:1로 읽혀야 합니다. 셰이더 코드는 빨리 컴파일될 만큼
작게 유지합니다. Windows의 Chrome 뒤에 있는 D3D 컴파일러는 모든 함수 호출을 인라인으로 풀어 넣습니다.
16번 호출한 헬퍼 하나가 컴파일에 40초 걸린 적이 있습니다. 유니폼으로 횟수를 세는 루프는 이를
피합니다(`halftone-screen` 참고). `index`를 실행한 뒤 갤러리에서 라이트·다크·컬러로 효과를 확인합니다.
