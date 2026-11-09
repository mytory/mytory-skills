# 큰 장면

기술 페이지에서 화면 전체가 스크롤에 따라 하나의 장면이 되는 단 한 구간입니다. 각 장면은
`assets/scenes/<id>/` 폴더(`scene.js`, `scene.css`, `meta.json`, `demo.html`)이고, `index.json`이
이를 나열하며, `lib.js`는 장면들이 함께 쓰는 고정 무대이고, `scenes.js`가 장면을 불러오며,
`print.js`는 오브젝트 장면 둘을 위해 오브젝트 렌더를 올립니다.

## 누가 쓰는가

- **기술 페이지만:** 소프트웨어(앱, AI, 개발자 도구, 핀테크), 기술(기술 제품, 하드웨어, 네트워크),
  게임입니다. 장소, 서비스, 평범한 제품(site-kind other: 카페, 게스트하우스, 가게, 스튜디오)에는
  장면을 쓰지 않고 사진을 씁니다. `index.json`의 `types`는 정확히 `software`, `tech`, `gaming`입니다.
- **한 페이지에 최대 하나이며,** 브리프에 장면의 `needs`(고객 자신의 사진, 화면, 문구. 게임의
  키아트와 인게임 샷이 그 게임의 사진입니다)가 있을 때만 씁니다. 필요한 것이 없으면 장면도
  없습니다. 고객의 그림을 대신하는 대체물로 쓰지 않습니다. 아트 파일이 없는 게임은 배경 세계의
  대체 사진 위에 이름을 크게 얹고(`photo` 히어로와 그 세계 섹션. 브리프가 3D를 요청할 때만
  렌더), 그 자리에 효과를 넣지 않습니다(`sections.md` 3절 게임).
- **무작위로 뽑습니다.** `fits`에 그 섹션이 있고, `types`에 페이지의 유형이 있고, 브리프가 `needs`를
  충족하는 장면 가운데 `weight`로 가중해 뽑되, `.taste-skill/scenes-history.json`의 최근 셋은
  피합니다(명령은 `effects-usage.md`에 있습니다). 계획에 장면과 그 섹션을 적습니다. 큰 장면은
  페이지의 유일한 효과입니다. 셰이더 배경도, 옆의 WebGL 부품도 두지 않습니다.
- **히어로는 정지 상태에서 한 화면을 차지하므로,** `restH`가 1인 장면만 히어로로 뽑습니다.
  `restH`가 2인 장면(지금은 히어로용 장면 셋 모두)은 히어로 아래에만 두는 두 화면 섹션(`--h: 2`)으로
  들어가며 그 제목은 h2입니다. 이때 히어로는 평소대로 뽑습니다.
- **오브젝트 장면 둘**(`fixed-hero-object`, `object-through-giant-type`)은 고객 자신의 업종에 속한
  오브젝트(카드 게임 엔진이면 카드 한 벌, 엣지 네트워크면 지구본)를 WebGL 렌더로 그립니다.
  다른 업종의 오브젝트는 안 되고, 카페에 컵을 올리는 일도 안 됩니다.
- **페이지의 나머지는 차분하게 둡니다.** 페이지가 스크롤됐다는 이유로 카드, 행, 타일이 움직이지
  않습니다. 장면 옆에서도 섹션 모먼트를 하나나 둘 더 쓸 수 있습니다(하우스 오버라이드: 큰 장면
  하나와 스크롤 모먼트 하나나 둘). `moments.md`의 방식대로 뽑되(짧은 페이지는 하나, 여덟 섹션 이상은
  둘), 장면의 섹션이나 그 옆 섹션에는 두지 않고, 장면의 `avoidMoments`나 그 쌍둥이에 있는 것도
  쓰지 않습니다(`effects-usage.md`, 큰 장면).

| id | fits | types | needs | WebGL | restH | phone |
| --- | --- | --- | --- | --- | --- | --- |
| `descend-through-weather` | 히어로(아래에만) | tech, gaming | 고객 세계의 사진 두 장, 높은 곳과 낮은 곳 | - | 2 | 정지 |
| `shaped-window-over-fixed-world` | 히어로(아래에만) | tech, gaming | 고객 세계의 와이드 사진 한 장 | - | 2 | 정지 |
| `fixed-hero-object` | 히어로(아래에만) | tech, gaming | 오브젝트 렌더나 누끼 한 장, 챕터 1~4개 | 1 | 2 | 정지 |
| `powers-of-ten-pullback` | 제품 | software, tech | 실제 크기의 제품 UI | - | 1 | 정지 |
| `product-assembles-into-its-action` | 제품 | software, tech | HTML로 된 화면, 4~6단계 | - | 1 | 정지 |
| `parts-lock-into-the-whole` | 제품 | software, tech | 패널 경계로 자른 화면 | - | 1 | 정지 |
| `fly-into-the-shape` | 사이, 제품 | software, tech, gaming | 하나의 패스로 된 마크, 어두운 사진 한 장 | - | 1 | 정지 |
| `letter-physics` | 선언 | software, tech, gaming | 주장과 그 답 | - | 1 | 가벼움 |
| `object-through-giant-type` | 선언 | software, tech, gaming | 짧은 줄 3~5개의 인용문, 오브젝트 하나 | 1 | 1 | 정지 |
| `dot-becomes-the-full-stop` | 선언 | software, tech, gaming | 4~6단어의 주장 하나 | - | 1 | 가벼움 |
| `letter-bar-floods-the-ground` | 사이, 선언 | software, tech, gaming | 선언 둘, 뒤따르는 반전 섹션 | - | 1 | 정지 |

`powers-of-ten-pullback`은 절대 히어로가 되지 않습니다. 첫 화면에 제목도 행동 유도도 없기
때문입니다. 각 장면의 `scene.js` 머리 주석에 그 장면의 마크업과 옵션이 있고, `meta.json`에
`look`, `needs`, `never`, `avoidWith`가 있습니다.

## 페이지에 하나 올리기

장면 폴더와 공유 파일(`scenes.js`, `lib.js`, `scenes.css`, 오브젝트 장면이면 `print.js`도)을
`assets/scenes`로 복사합니다. 장면의 머리 주석을 보고 고객 자신의 문구와 그림으로 마크업을
씁니다. `<head>`에는 스크립트가 있음을 일찍 표시하는 한 줄과 스타일시트 둘을 넣어, 완성된
구성이 스크립트 없이도 스타일을 받고 장면이 올라갈 때 아무것도 튀지 않게 합니다. `<body>`
끝에는 런타임을 한 번 넣습니다.

```html
<head>
  …
  <script>document.documentElement.classList.add('sc-js');setTimeout(()=>document.documentElement.classList.add('sc-safe'),2500)</script>
  <link rel="stylesheet" href="assets/scenes/scenes.css">
  <link rel="stylesheet" href="assets/scenes/<id>/scene.css">
</head>
…
<section class="sc" data-big-scene="<id>" data-big-scene-opts='{"hold": 1}' style="--h: <the scene's restH>" aria-labelledby="…">
  <div class="sc__stage">…</div>
</section>
…
<script type="module" src="assets/scenes/scenes.js"></script>
```

섹션은 `main`의 직계 자식입니다. `<html data-scenes-ready>`는 장면이 올라갔다는 뜻이고,
`data-scenes-over`는 오류입니다. 장면은 페이지의 토큰, 서체, 반경, 버튼을 그대로 씁니다.

### 높이(규칙 3)

장면의 섹션도 다른 섹션처럼 페이지 리듬 안에 머뭅니다. 정확히 한 화면이나 두 화면이며, 문구는
내비게이션 아래에 있습니다. 실제 동작 중에는 (hold + 1) 화면입니다. `lib.js`와 모든 장면의
`hold` 기본값이 1이므로 동작 중의 섹션은 두 화면(1440x900에서 1800px)입니다. 정지 상태(폰,
모션 축소, 스크립트 없음)에서는 `scenes.css`가 섹션의 `--h`와 패딩을 최소 높이로 유지하므로,
`--h`에 장면의 `restH`(위 표)를 주고 그 섹션에 페이지 CSS는 쓰지 않습니다. 고정 높이를 주면
구성이 잘려 다음 섹션을 덮습니다. 검사를 피하려고 `data-screen="free"`로 장면을 숨기지 마세요.
390 샷을 봅니다. 정지 구성이 자기 화면의 절반도 채우지 못하면 비어 보입니다(규칙 2).

## 규칙

- **데모는 자리표시자입니다.** 출고되는 장면의 모든 그림, 문구, 오브젝트는 고객의 것입니다.
  사진 출처는 푸터 한 줄에 적고, 프레임 밖까지 잘라 쓴 사진에는 "adapted"를 붙입니다.
- **장면 없이도 읽힙니다.** 장면의 문구는 마크업 안의 진짜 텍스트이며 읽는 순서대로 있고,
  완성된 구성이 장면이 하는 말을 모두 전합니다.
- **네이티브 스크롤만:** 무대는 `hold` 화면 동안 붙어 있고, 어떤 것도 휠을 가로채지 않습니다.
- **폰에는 정지 구성이나 가벼운 버전을 줍니다.** 전체 장면은 주지 않습니다. 768px 미만에서는 모든
  장면이 완성된 구성을 보여 주며, 가벼움으로 표시한 타입 장면 둘만 예외입니다(깊이 없음, 겹침 없음).
- **모션 축소, 스크립트 없음, 모듈 로딩 실패:** 완성된 구성을 보여 주며, 이는 hold의 끝 상태이기도
  합니다. 오브젝트 장면은 이때 오브젝트의 정지 사진을 보여 주고 WebGL을 올리지 않습니다.
- **WebGL:** 장면당 컨텍스트는 최대 하나이며 페이지의 공유 예산(`lib.glBudget`,
  `window.__tpGl`, 페이지당 넷)에서 가져옵니다. 섹션이 활성 상태이고 뷰포트에서 한 화면 이내일
  때만 올리고, 벗어나면 파괴하며, WebGL이나 셰이더가 실패하면 그 밑에 정지 사진을 둡니다.
  이름에 GLSL ES 예약어를 쓰지 않습니다.
- **움직이는 것이 읽는 글자를 가로지르지 않습니다.** 선언은 모든 정지 상태에서 통째로 읽힙니다.
  사진 위 글자는 페이지 바탕색의 평평한 띠나 사진의 차분하고 어두운 부분 위에서 4.5:1(디스플레이
  글자는 3:1)로 서고, 사진 위에 스크림이나 그라디언트를 두지 않습니다(`system.md`).
- **비용:** 고정 크기 레이어에서 transform, opacity, clip-path만 씁니다. 프레임마다 다시 그리는
  width, height, SVG clip은 쓰지 않습니다.
- **장면을 설명하는 캡션은 두지 않습니다.** 장면 아래에도 옆에도 두지 않으며, 스크롤과 함께 날아다니는
  카드 크롬, 칩, 라벨도 두지 않습니다.

## 검사하기

```bash
node <skill>/assets/scenes/_demo/shoot.mjs shoot --out <dir> --profile <your own Chrome profile dir> [--only <id>] [--page <url>] [--reduced] [--port 5836]
node <skill>/assets/scenes/_demo/shoot.mjs index [--out <file|dir>]   # from the project folder: its own index.json
```

`index`는 `assets/scenes`가 있는 프로젝트 폴더에서 실행하면(또는 `--out <file|dir>`를 주면) 그
프로젝트의 `assets/scenes/index.json`을 씁니다. 설치된 스킬 안에서는 거부하고 아무것도 쓰지 않으며,
`--in-skill`은 스킬 자신의 인덱스를 일부러 다시 쓰는 옵션이라 페이지 작업이 아닙니다. 페이지에서
이것이 필요한 때는 장면의 `meta.json`이 바뀐 뒤뿐이므로, 보통의 페이지에서는 건너뜁니다.

CPU에서 WebGL을 쓰는 헤드리스 Chrome 하나가 자기 PID로 닫히며, 1440과 390에서 시작, 중간, 끝을
찍고 장면마다 콘택트 시트 한 장을 만듭니다. 모든 시트를 읽고, `--reduced`로 한 번 찍습니다.
