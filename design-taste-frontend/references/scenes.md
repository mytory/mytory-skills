# 스크롤 장면

페이지의 큰 순간입니다. 섹션 열이 스크롤 구간에서 하나의 장면으로 바뀝니다. 이미지 사이를 나는 카메라, 창에서 화면 전체로 커지는 사진, 스크롤에 휘는 단어, 궤도를 돌다 그리드에 착지하는 사진들입니다. 방문자가 수상 사이트에서 기억하는 것은 이런 순간이며, 단정한 섹션만 조립한 페이지에는 없습니다.

장면 라이브러리는 최근 Awwwards Sites of the Day를 분석하고(2026년 10월: 43개 사이트의 스크롤을 프레임별 기록, 장면 261개 설명, 유형 30개), 자체 코드로 처음부터 재구현했습니다. 데스크톱·휴대폰·동작 줄이기에서 프레임별 테스트하고 출처 장면과 비교 검토했습니다. 사이트 소유 자산은 포함하지 않습니다. `library/scenes.json`이 배포되기 전에는 추첨하지 않습니다. 필요한 페이지는 8절의 stage에서 이 문서의 모든 규칙을 지켜 직접 만드세요.

## 목차

1. 장면이란
2. 페이지에 장면 넣기
3. 콘텐츠 채우기
4. 페이지에 맞추기
5. 휴대폰·동작 줄이기·스크립트 없음
6. 확인
7. 장면 규칙
8. 맞는 라이브러리 장면이 없을 때
9. 목록

## 1. 장면이란

페이지가 지나가는 동안 stage는 멈추는 높은 섹션입니다. stage는 `position: sticky`, 섹션 높이는 (hold + 1)화면이므로 `hold`화면 동안 고정됩니다. 그 스크롤이 GSAP 타임라인을 0에서 1까지 스크럽합니다. 휠을 가로채지 않으며 스크롤바는 실제 위치를 반영하고 키보드·트랙패드도 평소처럼 작동합니다. 장면은 끝이 있습니다.

페이드 상승·작은 패럴랙스·고정 푸터·마키는 장면이 아닌 조용한 층입니다(`references/motion.md`). 장면은 화면 전체를 바꿉니다.

방향 시트 9절은 서로 다른 계열의 두세 장면을 각자 전달할 논지의 섹션에 배치합니다. 6단계에서 해당 섹션과 함께 구현하세요. 장면은 마지막에 더하는 장식이 아닌 구성입니다.

## 2. 페이지에 장면 넣기

공통 stage와 제공 장면 파일을 프로젝트로 복사하세요(`assets/scenes/stage.css`, `stage.js`, `<id>.css`, `<id>.js`). 각 장면 파일의 헤더 주석에 필요한 마크업과 옵션이 있으며, `assets/scenes/demo/<id>.html`은 함께 볼 완전한 작동 예시입니다.

```html
<head>
  <script>document.documentElement.classList.add('js')</script>
  <link rel="stylesheet" href="scenes/stage.css">
  <link rel="stylesheet" href="scenes/<id>.css">
</head>
<body>
  …
  <section class="scene" data-scene="<id>" data-options='{"hold": 3}' aria-label="…">
    <div class="scene-stage">
      <!-- the markup from the scene file's header, filled with this page's content -->
    </div>
  </section>
  …
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrollTrigger.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.min.js"></script>
  <script src="scenes/stage.js"></script>
  <script src="scenes/<id>.js"></script>
  <script>Stage.smooth(); Stage.init();</script>
</body>
```

- 장면 파일이 요구할 때만 SplitText(`gsap@3.15.0/dist/SplitText.min.js`)를 불러오세요.
- `Stage.smooth()`는 가중 휠 스크롤(Lenis, lerp 0.12)을 추가합니다. 터치와 동작 줄이기에서는 꺼집니다. 조용한 페이지에서는 생략하세요. 장면은 어느 쪽에서도 작동합니다.
- `Stage.init()`는 페이지의 모든 `[data-scene]`을 시작합니다. 장면이 두 개면 파일도 둘 다 불러옵니다.
- 버전은 고정돼 있습니다. `@latest`나 고정하지 않은 주 버전으로 바꾸지 마세요.

## 3. 콘텐츠 채우기

장면의 힘은 콘텐츠에 달렸습니다. 헤더와 시트의 “Content” 줄에 필요한 이미지·단어 수가 있습니다. 공통 규칙:

- **같은 계열 이미지.** 빛·색보정·대상 종류가 같아야 합니다. 서로 다른 스톡 사진은 타이밍 오류보다 빨리 한 공간의 환상을 깹니다. 대상 세계의 실제 이미지(`assets.mjs`), 프로젝트 자체 자산, 제공 사진 순으로 고르세요(`references/imagery.md`). 최대 표시 크기에 맞추고 `width`·`height`를 지정하세요.
- **한 호흡에 읽는 말.** 고정 진술은 4–12단어, 캡션은 본문 서체와 문장식 표기로 1–4단어입니다. 한 화면에 진술 하나입니다.
- **대상에 관해 말하는 장면.** 스튜디오 작업 사이를 비행하거나 실제 배송 경로·집의 네 방·제품 상태 변화를 보여주세요. 무관한 사진을 채우면 속임수처럼 보입니다.
- **실제 콘텐츠만.** 사진 여덟 장이 필요한데 세 장뿐이면 대용품 대신 `--redraw scenes`를 쓰세요.

## 4. 페이지에 맞추기

- 장면은 페이지 토큰 `--ground`, `--ink`, `--muted`, `--accent`, `--font-display`, `--font-text`를 대체값과 함께 읽습니다. 시트대로 `:root`에 설정하면 장면도 색상·서체를 따릅니다. 페이지를 데모에 맞추지 말고 데모를 페이지 기준으로 확인하세요.
- 장면 큰 제목도 제공 서체와 두 줄 규칙을 지키며, 진술은 진술 크기를 지킵니다.
- 두 장면 사이에 조용한 섹션(본문·목록·단순 이미지)을 두세요. 연속 장면은 긴 놀이기구 하나처럼 보여 뒤 장면이 약해집니다.
- 첫 화면의 장면은 진행률 0에서 제목·문장·행동이 첫 프레임에 보여야 합니다(모션 규칙 1). 방문자가 스크롤해야 움직이기 시작합니다.
- 섹션에 제목을 주세요. 장면에 눈에 보이는 제목이 없어도 섹션 `aria-label`과 완성 구성의 실제 제목은 있어야 합니다.

## 5. 휴대폰·동작 줄이기·스크립트 없음

- **휴대폰.** 각 파일의 계획은 수치 조정·단순화·완성 구성을 보여주는 `phone: 'rest'` 중 하나입니다. 터치 스크롤에는 부드러운 보정을 쓰지 않습니다. 휴대폰 시트도 데스크톱만큼 꼼꼼히 보세요.
- **동작 줄이기와 스크립트 없음.** 같은 콘텐츠를 움직임 없이 읽는 완성 구성을 일반 섹션으로 표시합니다. 스크립트를 기다리며 숨기지 않습니다. 검사기의 `reduced-hidden`과 `scenes.mjs`의 reduced 시트로 확인하세요.
- **CDN 실패**도 완성 구성으로 돌아갑니다(stage가 `.is-rest` 추가). 검사기는 데스크톱에서 정지 상태인 장면을 `scene-not-live`로 실패 처리하므로 고장난 스크립트가 통과하지 못합니다.

## 6. 확인

```bash
node <skill>/scripts/scenes.mjs <page>        # every scene at 0, 10 … 100%, desktop and phone, and reduced motion
node <skill>/scripts/inspect.mjs <page>       # the gate; with scenes on the sheet it also films the scroll
```

`scenes.mjs`는 장면·폭마다 `.taste-skill/scenes/`에 콘택트 시트를 만듭니다. 전부 읽으세요. 매 프레임에서 볼 것이 하나로 명확한지, 진술이 읽히는지, 튀거나 비거나 잘리거나 글자를 가리는 것이 없는지, 충분히 대담한지 물으세요. 검사기의 `desktop-film-NN.jpg`는 페이지 전체를 3분의 1화면 간격으로 보여줍니다. 장면과 조용한 섹션이 리듬을 만들며 사이가 비지 않았는지 확인하세요.

## 7. 장면 규칙

1. **페이지당 서로 다른 계열 두세 개**, 사이에는 조용한 섹션. 검사기는 네 개 초과(`many-scenes`)나 페이지의 60% 초과 고정(`scene-heavy`)을 경고합니다.
2. **각각 1–4화면 고정.** 이야기 한 박자당 약 한 화면. 새로 보여줄 것이 없으면 늘리지 말고 줄이세요.
3. **네이티브 스크롤만.** 휠 가로채기·페이지 잠금·클릭해야 실행되는 장면은 쓰지 않습니다. 부드러운 보정은 `Stage.smooth()`만 씁니다.
4. **멈추는 지점에서 읽혀야 합니다.** 문장이 온전히 보이고 읽는 중 글자 위로 다른 것이 지나가지 않으며 사진 위 글자에는 단색 스크림이나 차분한 영역이 있어야 합니다.
5. **장면 안에서는 장면의 수치가 우선**합니다(모션 규칙 7). 사진이 창에서 화면 전체로 커지고 글자가 stage를 가로지르며 카메라가 사진 사이를 날 수 있습니다. 바깥은 `references/motion.md`의 조용한 제한을 따릅니다.
6. **transform·opacity·clip-path.** 매 프레임 레이아웃을 강제하지 마세요. 사진은 움직이기 전에 디코딩합니다.
7. **장면 안에서도 자체 규칙 유지.** 고정폭 캡션·01/07 카운터(필요하면 평범한 “3 of 7”)·그라데이션(단색 스크림 사용)·그림자·광채·가는 선 장식·장식 입자·보라색을 쓰지 않습니다.
8. **완성 구성을 먼저 설계**하세요. 부차적 결과물이 아닙니다. 동작 줄이기·스크립트 실패·일부 휴대폰이 그것을 봅니다.

## 8. 맞는 라이브러리 장면이 없을 때

먼저 `--redraw scenes`로 다시 뽑으세요. 브리프에 정말 라이브러리에 없는 장면이 필요하면 같은 stage에서 만들어 안전장치를 이어받으세요.

```js
Scenes['my-scene'] = (root, opts = {}) => Stage.scene(root, {
  hold: opts.hold ?? 2,          // screens the stage is held for
  scrub: opts.scrub ?? true,     // true when Lenis runs; 0.4-0.8 without it reads as weight
  phone: 'same',                 // or 'rest', or { hold, build } for a phone plan
  build(tl, { q, phone }) {      // positions are fractions of the scene, 0-1
    tl.fromTo(q('.picture'), { clipPath: 'inset(30% 30% 30% 30%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.6 }, 0)
      .to(q('.title'), { yPercent: -40, autoAlpha: 0, duration: 0.25 }, 0.7);
  },
});
```

CSS의 완성 구성을 먼저 쓰고 `.scene.is-live` 아래에 실행 레이아웃을 쓰세요. 다른 장면처럼 `scenes.mjs`로 확인합니다.

## 9. 목록

`library/scenes.json`에서 생성하며 추첨도 이 목록을 씁니다. `node <skill>/scripts/draw.mjs --list scenes`로 출력합니다.
