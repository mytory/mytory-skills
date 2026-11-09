# 사진 프린트

셰이더가 사진 한 장을 통째로 페이지의 잉크로 자기 종이 위에 인쇄합니다. 하프톤, 판화, 디더가 있습니다.
호버(휴대폰에서는 탭)하면 프린트 아래의 사진 자체가 보입니다. 프린트는 페이지의 공들인 한 모먼트이며,
페이지가 사진을 보여 주는 방식이 되어서는 안 됩니다.

| 오브젝트 | 모양 | 호버 |
|---|---|---|
| `photo-halftone` | 한 가지 잉크의 하프톤: 45° 스크린 위의 둥근 점, 밝은 곳은 깨끗한 종이, 가장 깊은 그림자는 꽉 찬 잉크 | 돋보기(둥근 렌즈, 가는 테두리, 부드러운 그림자)가 사진을 원래 색으로 보여 줌 |
| `photo-engraving` | 판화 동판: 그림자에서 굵어지고 형태를 따라 휘어지는 대각선 선들이 사진 색의 옅은 워시 위에 놓임 | 커서 주위로 선이 갈라지며 사진이 비쳐 보임 |
| `photo-dither` | 세 가지 색의 그레인: 사진에서 가장 깊고 가장 선명한 색들이 종이 위에 놓임 | 사진이 부드러운 원 안에서 그레인을 통해 현상됨 |

각 폴더의 `demo.html`(http로 서빙)이 라이트, 다크, 컬러 팔레트에서의 모습을 보여 줍니다. `meta.json`에
파라미터, 터치 동작, 대체 동작, 비용이 있습니다.

## 프린트를 쓸 곳과 쓰지 않을 곳

- **쓸 곳:** 소프트웨어, AI, 디자인 도구, 게임 페이지의 한 모먼트: 페이지의 유일한 사진 띠나, 사진이
  주제인 피처 타일(그림을 인쇄하는 이미징이나 디자인 도구, 브랜드의 잉크를 위한 `tint: 1`). 페이지당
  프린트 하나이며, 세 개의 행은 프린트에 관한 페이지에서만 씁니다.
- **절대 쓰지 않을 곳:** 히어로 사진이나 섹션의 주 사진 위(`references/photos.md`). 거기서는 프린트가
  깨졌거나 해상도가 낮은 것처럼 읽힙니다. 카페, 게스트하우스, 가게 같은 지역 업체 페이지에도 쓰지 않습니다.
  그런 페이지는 사진을 그대로 보여 줍니다.
- **절대** 효과를 설명하는 캡션을 아래에 붙이지 않으며, 그것이 프린트라는 안내도 붙이지 않습니다.

## 사진

클라이언트 자신의 사진이 먼저입니다. 없으면 잘 인쇄되는(분명한 피사체 하나, 단순한 배경, 분명한 빛) 검증된
라이브러리의 사진을 씁니다.

```bash
node <skill>/scripts/photos.mjs list --trade office --json     # entries with "prints": true
node <skill>/scripts/photos.mjs fetch <id> --out .             # the files, credits.json and the <img>
```

어두운 페이지에서는 더 어두운 사진(`"tone": "dark"` 또는 `"mid"`)을 고릅니다. 밝은 사진은 거기서 큰 밝은
판으로 인쇄됩니다.

## 마운트

`photos.mjs fetch`가 출력하는 `<img>`를 프레임에 붙여 넣습니다. 프린트는 그 그림(`srcset` 중 가장 큰
크기)을 읽고, 그 `alt`를 유지하며, 그 `object-position`을 피사체의 위치로 받습니다.

```html
<div class="print-frame" style="aspect-ratio: 4 / 5; border-radius: var(--radius-card)">
  <img src="assets/img/photo-d88.jpg" srcset="..." sizes="(max-width: 1023px) 100vw, 50vw"
       width="1280" height="1757" alt="Cream ceramic table lamp in low sun" loading="lazy" decoding="async"
       style="object-position: 50% 40%">
</div>
<script type="module">
  import fx from './assets/effects/fx.js';
  import halftone from './assets/objects/photo-halftone/object.js';
  const el = document.querySelector('.print-frame');
  halftone.mount(el, { palette: fx.readPalette(el) });
</script>
```

- 프레임에는 크기가 필요합니다(`aspect-ratio`나 높이). 프린트가 그것을 채우고, 프레임이 한 장의 종이처럼
  읽히도록 페이지의 `--surface` 위에 인쇄하며(`ground: 0`은 `--bg` 위에 인쇄), 페이지의 팔레트를 따릅니다(팔레트
  전환 뒤에는 `ctrl.setPalette(fx.readPalette(el))`).
- `focusX`/`focusY`(0..1)는 `<img>`의 `object-position`을 덮어씁니다.
- 프린트는 첫 프레임부터 거기 있습니다. 등장 효과도, 디졸브도 없으며, 정지 상태에서는 아무것도 움직이지
  않습니다.
- 작은 UI 카드는 프레임의 모서리에 걸칠 수 있지만(`cards.md`) 피사체 위에는 절대 두지 않으며, 프린트 위에
  글은 절대 두지 않습니다.

## 크레딧

크레딧은 푸터의 크레딧 한 줄에 넣으며 프린트 아래에는 절대 두지 않습니다. 인쇄한 사진은 각색한 것으로
셉니다.

```bash
node <skill>/scripts/photos.mjs credits --out . --adapted <id>
```

`photos.mjs`를 거치지 않은 사진은 `photo.js`의 `creditsBlock(entries, { adapted: [id] })`가 `{ id, by,
page, licence, licenceUrl, source }`로 같은 푸터 블록을 씁니다(목록을 여는 한 줄, "Photographs via
..."). 클라이언트 자신의 사진에는 필요 없습니다.

## 그릴 수 없을 때

첫 프레임 전, 캔버스가 화면 밖에서 해제되어 있는 동안, 그리고 WebGL이 없거나, 셰이더가 컴파일이나 링크에
실패하거나, 사진의 호스트가 CORS 헤더를 보내지 않을 때마다 사진 자체가 팔레트에 맞춰 회색조로 보입니다.
정지한 그림이며 빈 프레임은 절대 아닙니다. 런타임은 GLSL ES 예약어(`flat`, `smooth`, `sample`, `filter`,
`input`...)를 쓰는 셰이더도 거부하고 스틸을 보여 줍니다. 노트북 GPU는 CPU WebGL(SwiftShader)이 컴파일하는
것을 거부하기 때문입니다. `photo.js`의 `glslLint(src)`와 `photoShader(object)`가 Node에서 셰이더를
검사합니다.

## 비용

프린트마다 캔버스 하나와 WebGL 컨텍스트 하나이며, 화면 밖이거나 탭이 숨겨지면 멈추고, 화면을 벗어난 지
1.5초 뒤에 해제됩니다. 컨텍스트를 쥘 수 있는 프린트는 최대 3개이며, 네 번째는 하나가 떠날 때까지 자기 스틸을
보여 주며 기다리고, 스크롤로 사라지는 프레임은 들어오는 프레임에 자리를 내줍니다. 페이지의 다른 WebGL
효과와 함께 세어 한 페이지에 라이브 컨텍스트 3개를 지킵니다. 하프톤과 판화는 점과 선이 선명하도록 CSS
픽셀당 캔버스 픽셀을 최대 2개까지 렌더링하며, 모든 프린트는 캔버스 1.5 MP 아래로 유지됩니다. 각 픽셀은
밉맵에서 사진을 2~5번 읽으며 루프는 없습니다.
