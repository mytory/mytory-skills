# 모션

애니메이션을 추가하기 전에 이 파일을 읽으세요. 정적인 페이지를 완성하고 `inspect.mjs`를 통과한 상태여야 합니다. 모션은 마지막 작업이며 약한 레이아웃을 구제하는 수단이 아닙니다.

## 목차

1. 모션 예산
2. 훌륭한 페이지의 모션 사용법
3. 애니메이션 전 네 가지 질문
4. 토큰
5. 스크롤 동작 순위
6. 구현법 (복사한 뒤 조정)
7. 대표 동작
8. 모션 줄이기와 성능
9. 생성형 모션의 흔적
10. 모션 규칙

## 1. 모션 예산

움직이지 않는 페이지는 시안처럼 보입니다. 검사기는 로드와 스크롤 중 움직이는 요소를 세며 8개 미만이면 실패로 판정합니다. 모션 계층은 다섯 부분입니다.

- **스크롤 장면 두세 개:** 수상 사이트를 기억하게 하는 큼직한 스크롤 연출입니다. 이미지 들판을 가로지르는 카메라, 작은 창에서 전체 화면으로 커지는 사진, 고정된 무대를 가로지르는 글자, 펼쳐지고 쌓이는 카드가 해당합니다. 라이브러리에 브리프에 맞는 장면이 있으면 방향 시트가 `library/scenes.json`에서 뽑습니다. 채우고 조정하는 방법은 `references/scenes.md`에 있습니다. 이 부분에서 대담하게 표현하고 나머지는 차분하게 유지해 장면을 돋보이게 합니다.
- **대표 순간 하나:** 방문자가 한 시간 뒤에도 설명할 장면입니다. 마스크 뒤에서 떠오르는 제목, 셔터처럼 열리는 이미지, 스크롤에 따라 크기가 달라지는 워드마크입니다. `draw.mjs`의 방향 시트가 하나를 지정합니다. 그것을 잘 구현하세요. 강하게 드러나도 되는 동작은 이것뿐입니다.
- **섹션마다 안무를 정한 등장:** 제목, 본문, 사진, 세부 정보가 읽는 순서로 나타납니다. 60–90ms 간격으로 엇갈리고 불투명도가 변하며 16–32px 올라오되 한 번만 실행합니다. 같은 프리셋을 찍어 내지 말고 콘텐츠에 맞춥니다. 목록은 행마다, 사진은 마스크가 열리거나 약간 큰 상태에서 제자리로, 수치는 한 번의 카운트업으로, 문장은 줄마다 나타냅니다.
- **조작에 대한 피드백:** 누르면 반응하는 버튼, 포인터에 응답하는 링크, 호버에 반응하는 카드와 사진, 클릭한 곳에서 열리는 메뉴입니다.
- **움직이는 사진 하나:** 포스터 프레임을 갖춘 무음 반복 클립, 큰 사진의 느린 이동·확대, 히어로 사진의 스크롤 연동 동작 중 하나입니다.

모든 블록에 같은 시간의 페이드업을 적용하는 일은 여전히 금지합니다. 생성형 페이지에서 가장 자주 지적되는 모션 흔적입니다. 대체 수단 없이 스크립트 실행까지 콘텐츠를 숨기거나, 바운스·탄성 이징을 쓰거나, 레이아웃 속성을 애니메이션하지 마세요. 획일적 동작은 아무 결정도 내리지 않았다는 인상을 줍니다. 하나의 특별한 순간을 보호한 안무는 의도를 보여 줍니다.

## 2. 훌륭한 페이지의 모션 사용법

최신 Awwwards Sites of the Day 99개(2026년 7~10월)를 1440과 390에서 측정했습니다. 로드와 스크롤 중 전환, 트윈, 스크롤 트리거를 기록했습니다. 갤러리 사례가 이 스킬의 규칙을 어기면 아래에 스킬의 대안을 적었습니다.

- **기술 구성.** 3분의 2는 부드러운 스크롤 라이브러리, 5분의 3은 Three.js를 사용하며 56개에서 GSAP이 확인됩니다. 아래의 조용한 계층(등장, 줄 상승, 글자색 채우기)에는 필요 없습니다. CSS 스크롤 타임라인과 뷰 전환이면 되지만 실제 사용 사이트는 각각 3개와 6개뿐입니다. 큰 스크롤 장면은 수상 사이트처럼 GSAP ScrollTrigger로 만들되 `assets/scenes/`의 공통 무대를 사용합니다(`references/scenes.md`).
- **곡선.** 실제 실행된 곡선은 강한 ease-out입니다. expo out(`.16,1,.3,1`, `.19,1,.22,1`)은 14개 사이트, cubic out은 13개, quint out은 7개에서 실행되었습니다. 전환 횟수로도 quint와 expo out이 선택 곡선 중 선두입니다. in-out은 와이프와 위치 이동에 사용합니다(cubic·quart in-out 각각 약 15개 사이트). ease-in은 느린 등장 전에 짧게 퇴장할 때만 보입니다. 색상은 기본 `ease`를 씁니다(46개). 오버슈트는 스타일시트 19개에 있지만 실행된 곳은 2개입니다.
- **시간.** 호버 색상 200~300ms, 작은 인터페이스 이동 300~450ms, 등장·줄 상승 600~1,000ms, 사진 열기·와이프 1,100~1,600ms입니다. 사이트에서 실행된 모든 모션 시간의 중앙값은 420ms입니다.
- **엇갈림.** 글자 간 20~40ms, 줄 간 75~120ms, 목록 항목 간 50~100ms입니다.
- **스크롤 연동은 스크롤바에 고정합니다.** 스크럽 사이트 18개 중 14개는 보간 없이 고정하며 나머지 4개는 0.1~3초로 보간합니다. 등장은 요소 상단이 뷰포트 아래쪽 80~95%에 왔을 때 한 번 실행합니다.
- **움직이는 양.** 스크립트로 움직이는 요소는 페이지당 중앙값 130개지만 몇 가지 동작에서 나옵니다. 나눈 제목 하나가 20~60개 요소입니다. 검사기 하한(8개, 16개 미만 경고)은 목표가 아니라 최저 기준입니다.
- **가장 흔한 비용은 기다림입니다.** 99개 중 60개가 로딩 화면으로 시작하고 그중 26개는 카운터를 띄웁니다. 사용 가능한 페이지의 절반은 브라우저 로드 완료 후 2.5초에도 읽을 수 없었고 3분의 1은 4.5초에도 그랬습니다. 프리로더는 느린 페이지를 가리는 장치가 아니었습니다. 문서는 오히려 다른 페이지보다 빨랐고 독자의 디자인 점수도 대기 시간과 무관했으며 사용성만 떨어졌습니다. 이 스킬에서는 프리로더 없이 첫 프레임부터 메시지를 읽게 하고 로드 연출을 1.2초 안에 끝냅니다.
- **고정에는 길이 비용이 듭니다.** 스크롤 페이지 3분의 2가 sticky 또는 pinned 요소를 사용합니다. 페이지는 두 배 길지만(중앙값 16.6화면 대 7.5화면) 화면당 단어는 적습니다(27 대 46). 이 스킬에서는 고정 무대 최대 두 개, 단계당 약 한 화면, 무대당 세 화면을 사용합니다.
- **모션 줄이기가 대부분 빠져 있습니다.** 99개 중 35개만 `prefers-reduced-motion` 규칙이 있고 16개는 세 개 이상입니다. 스크롤 스크럽 장면 26개 중 5개만 지원합니다. 이 파일의 모든 구현법은 모션을 줄인 상태에서 최종 상태를 보여 줍니다.

## 3. 애니메이션 전 네 가지 질문

1. **얼마나 자주 보나요?** 방문당 한 번(히어로 로드, 섹션 등장)은 천천히 해도 됩니다. 방문당 여러 번(호버, 메뉴, 아코디언)은 빠르고 작게 합니다. 수백 번(키보드 조작, 입력)은 애니메이션하지 않습니다.
2. **목적이 무엇인가요?** 어디서 왔는지 보여 주기, 동작 확인, 갑작스러운 변화 완화, 제품 작동 설명, 대표 순간이 타당한 답입니다. “보기 좋아서”는 대표 순간에만 허용됩니다.
3. **어떤 이징인가요?** 등장·퇴장은 눈이 닿는 즉시 시작하도록 ease-out, 화면의 두 위치 간 이동은 ease-in-out, 호버의 색상·불투명도는 `ease`, 일정한 이동(마키, 진행)은 `linear`입니다. `ease-in`은 첫 프레임이 거의 움직이지 않아 인터페이스를 느리게 만드니 쓰지 마세요. CSS 키워드 곡선은 약하므로 아래 토큰을 사용합니다.
4. **얼마나 오래 걸리나요?** 누름 피드백 100–160ms, 호버 150–200ms, 메뉴·팝오버 150–250ms, 대화상자·서랍 250–450ms, 섹션·히어로 등장 500–900ms입니다. 퇴장은 등장보다 빠르게, 약 70%로 합니다.

## 4. 토큰

```css
:root {
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);        /* entrances, moving hovers, UI under 600ms */
  --ease-expo: cubic-bezier(0.16, 1, 0.3, 1);        /* new: reveals of 800ms and longer, line rises, openings */
  --ease-in-out: cubic-bezier(0.76, 0, 0.24, 1);     /* wipes, panels, things that travel while visible */
  --ease-soft: cubic-bezier(0.33, 1, 0.68, 1);       /* slow scale and drift on photographs */
  --ease-exit: cubic-bezier(0.55, 0.055, 0.675, 0.19); /* new: something leaving for good, short */
  --t-press: 140ms;
  --t-hover: 180ms;
  --t-ui: 240ms;
  --t-reveal: 800ms;
  --t-open: 1200ms;                                  /* new: picture openings and clip wipes */
  --stagger-line: 90ms;                              /* new */
  --stagger-item: 70ms;                              /* new */
}
```

연구 결과와 각 토큰의 관계입니다.

- `--ease-out`(quint out)은 유사 곡선까지 포함해 스타일시트 28개에 있으며 실행된 전환에서 가장 많이 선택된 단일 곡선입니다. 유지합니다.
- `--ease-expo`는 새 토큰입니다. expo out(`.16,1,.3,1`, `.19,1,.22,1`)은 스타일시트 28개, 실행 사이트 14개로 선택 곡선 계열 중 가장 많습니다. 줄 상승, 사진 열기, 0.9~1.6초 카드 등장 같은 긴 연출에 쓰입니다. `--t-reveal` 이상에 사용하며 마스크 제목과 스크롤 등장 구현법의 `--ease-out`을 대체합니다.
- `--ease-in-out`(quart in-out)은 해당 계열(스타일시트 14개, 실행 7개)과 맞습니다. 와이프, 셔터, 메뉴, 페이지 전환에 유지합니다.
- `--ease-soft`(cubic out)은 cubic-out 계열(스타일시트 21개, 실행 13개)과 맞지만 연구에서는 이미 `--ease-out`이 담당하는 0.3~0.8초 인터페이스 이동에도 씁니다. 사진의 느린 확대·이동으로 범위를 좁힙니다.
- `--ease-exit`은 새 토큰입니다. ease-in에 맞는 일은 완전히 사라지는 요소(퇴장 캡션, 교체 슬라이드, 닫히는 패널)뿐입니다. 해당 등장의 60~70%로 짧게 합니다. 방문자가 기다리는 콘텐츠에는 쓰지 않습니다.
- 채택하지 않은 것: `.4,0,.2,1`(스타일시트 38개)은 프레임워크 기본값이며 오버슈트 곡선(19개)은 인터페이스 요소에서 계속 금지합니다.
- `--t-hover`는 180ms로 유지합니다. 연구의 색상 호버는 200~300ms지만 조금 빠른 편이 정밀하게 보입니다. 라벨 롤이나 화살표처럼 무언가 움직이는 호버는 `--t-ui`에서 400ms까지 씁니다.

## 5. 스크롤 동작 순위

| 동작 | 99개 중 페이지 수 | 목적 | 이 스킬의 방식 |
| --- | --- | --- | --- |
| 부드러운 스크롤 라이브러리 | 67 | 무게감, 스크럽 장면 구현 편의 | 선택 사항. `Stage.smooth()`로 Lenis lerp 0.1~0.14를 사용하며 터치·모션 줄이기에서는 끔 |
| 고정(sticky 또는 pinned) 무대 | 44 | 하나의 사진·사물로 여러 주장과 장 구성 | 스크롤 장면(`references/scenes.md`)으로 페이지당 두세 개, 각각 1~4화면. 그 밖의 sticky 무대는 최대 세 화면 |
| 텍스트 분할 | 40 | 읽는 순서대로 줄·단어 등장, 호버 롤 | 제목·문장은 줄 단위, 단어는 글자색 채우기에만, 글자 단위는 1~3단어 제목에만 |
| 장별 색상 | 34 | 여백 띠 없이 장 구분 | 섹션 경계에서 즉시 전환. 헤더 글자색은 300ms로 따라감 |
| 스크롤 스크럽 장면(카메라, 사물, 이미지 시퀀스) | 26 | 움직임으로 제품 설명 | 장면 라이브러리와 공통 무대 사용. 모션 줄이기용 완성된 구도 제공 |
| 패럴랙스 깊이 | 24 | 콜라주의 깊이, 큰 프레임 안 사진 이동 | 이동은 요소의 8% 미만, 사진은 프레임의 106~110% |
| 마키 | 21 | 정적인 띠에 생동감 | 기존 “화면 끝에서 끝까지 마키”. 페이지당 하나, 일시 정지 가능 |
| 마스크 줄·단어 상승 | 18 | 조판처럼 들어오는 제목 | 로드 시 “마스크 줄 등장”, 첫 화면 아래는 “스크롤하며 떠오르는 줄” |
| 휠로 장면만 조작하고 페이지 스크롤 없음 | 16 | 사물 하나 탐색 | 사용 안 함(2.6 참고) |
| 흐림 등장 | 15 | 부드러운 등장 | 최대 8px, 600ms, 안정 후 완전 제거. 본문에는 금지 |
| 안쪽 프레임에서 전체 화면으로 사진 확장 | 14 | 글자 화면에서 큰 사진으로 전환 | “열리는 창”, 약 한 화면의 스크롤 |
| 회색에서 본색으로 텍스트 채우기 | 14 | 한 문장의 속도 조절 | 페이지당 한 번, 글자색 45%에서 시작. “글자색 채우기” |
| 고정 계층 위로 시트 이동 | 11 | 장 사이 페이지 넘김 리듬 | 새 동작 “고정 사진 위의 시트” |
| 글자 뒤섞기·해독 | 11 | “코드” 분위기 | 사용 안 함(2.6 참고) |
| 장에 따른 헤더 글자색 | 10 | 고정 헤더 가독성 | 장별 색상과 함께 사용 |
| 세로 스크롤에 고정한 가로 트랙 | 8 | 방·컬렉션을 거닐기 | 기본은 네이티브 드래그 행. 3화면 미만 행만 키보드 지원을 갖춰 고정. “가로 갤러리” |
| 커튼 푸터 | 8 | 장면으로 페이지 마무리 | 기존 동작 |
| 굴러가는 숫자 | 6 | 등장하는 수치 | 몇 개의 수치가 핵심인 페이지에 사용. “굴러가는 수치” |
| 호버 미리보기가 있는 색인 | 5 | 이름으로 작품 탐색 | 기존 동작, 구현법 개선 |

텍스트 분할 단위는 글자 약 20페이지, 줄 약 14페이지, 단어 약 11페이지입니다. 글자 분할은 짧은 제목과 버튼 롤에 쓰며 긴 문장에 쓰면 스크롤 도중 파편만 남습니다.

## 6. 구현법

모든 구현법은 JavaScript가 꺼져도 콘텐츠를 보여 주고 숨김 상태를 `prefers-reduced-motion: no-preference` 안에 두며 위 토큰을 사용합니다. 여러 구현법에 해당하는 주의사항 두 가지입니다.

- **스크롤 타임라인에는 관찰할 스크롤 컨테이너가 필요합니다.** `animation-timeline: view()`는 가장 가까운 스크롤 컨테이너를 선택하며 `overflow: hidden`도 컨테이너를 만듭니다. 따라서 `overflow: hidden` 프레임 안 사진은 애니메이션되지 않습니다. 프레임에는 `overflow: clip`을 쓰거나 섹션에 타임라인 이름(`view-timeline-name: --hero`)을 주고 자식에서 그 이름을 참조하세요. 기존 “JavaScript 없는 스크롤 연동 진행”에도 적용됩니다.
- **스크롤 연동은 선형입니다.** 스크롤 자체가 이징입니다. 연구의 스크럽 사이트 18개 중 14개는 스크롤바에 고정하며 CSS 스크롤 타임라인도 같은 방식입니다.

JavaScript가 꺼져 있거나 느려도 콘텐츠는 보여야 합니다. 한 줄 인라인 스크립트가 설정하는 `html.js`에서만 숨김 상태를 적용합니다.

```html
<script>document.documentElement.classList.add('js')</script>
```

### 1.2초 로드 시퀀스

모든 요소는 HTML에 있고 첫 프레임에 그려집니다. 시퀀스는 등장 효과만 더합니다. load 이벤트를 기다리지 않으며 내비게이션은 움직이지 않습니다.

```html
<header class="hero">
  <h1 class="display lines">
    <span class="line"><span data-line style="--i:0">Stools for</span></span>
    <span class="line"><span data-line style="--i:1">small kitchens</span></span>
  </h1>
  <p class="lead" data-load style="--d:420ms">…</p>
  <a class="button" data-load style="--d:480ms" href="#stools">See the stools</a>
  <figure class="hero__picture" data-open><img src="stool.jpg" alt="…" fetchpriority="high"></figure>
</header>
```

```css
.hero__picture { overflow: clip; margin: 0; }
@media (prefers-reduced-motion: no-preference) {
  .js .hero [data-line] { transform: translateY(105%); animation: load-line 800ms var(--ease-expo) forwards; animation-delay: calc(100ms + var(--i) * var(--stagger-line)); }
  .js .hero [data-load] { opacity: 0; transform: translateY(12px); animation: load-rise 500ms var(--ease-out) forwards; animation-delay: var(--d); }
  .js .hero [data-open] { clip-path: inset(0 0 100% 0); animation: load-open 1000ms var(--ease-in-out) 150ms forwards; }
  .js .hero [data-open] img { transform: scale(1.08); animation: load-settle 1100ms var(--ease-expo) 100ms forwards; }
}
@keyframes load-line { to { transform: none; } }
@keyframes load-rise { to { opacity: 1; transform: none; } }
@keyframes load-open { to { clip-path: inset(0); } }
@keyframes load-settle { to { transform: none; } }
```

제목 줄은 100~990ms, 사진 열기는 150~1,150ms, 문장과 버튼은 420~980ms에 실행됩니다. 최대 네 요소이며 모두 1.2초 안에 안정됩니다. 디스플레이 서체를 미리 로드해(`<link rel="preload" as="font" type="font/woff2" crossorigin>`) 실제 서체로 줄이 올라오게 합니다. 사진에는 `fetchpriority="high"`와 사진에서 추출한 배경색을 지정해 느리게 로드되어도 빈 상자 대신 사진의 색으로 열리게 합니다. 연구에서 91페이지 중 22개는 첫 도입 프레임부터, 추가 11개는 1.2초 안에 읽을 수 있었습니다. 독자가 배려한다고 평가한 도입은 약 1~1.2초에 끝났으며 페이지 3분의 1은 4.5초에도 읽을 수 없었습니다.

### 마스크 줄 등장 (전형적인 갤러리 제목)

각 줄이 자기 기준선 뒤에서 올라옵니다. 제목은 최대 두 줄이므로 줄바꿈을 직접 정하고 각 줄을 감쌉니다.

```html
<h1 class="lines">
  <span class="line"><span data-line style="--i:0">Stools for</span></span>
  <span class="line"><span data-line style="--i:1">small kitchens</span></span>
</h1>
```

```css
.lines .line { display: block; overflow: hidden; padding-bottom: 0.08em; margin-bottom: -0.08em; }
.lines [data-line] { display: block; }
@media (prefers-reduced-motion: no-preference) {
  .js .lines [data-line] {
    transform: translateY(105%);
    animation: line-up 900ms var(--ease-out) forwards;
    animation-delay: calc(var(--i) * 110ms + 150ms);
  }
}
@keyframes line-up { to { transform: none; } }
```

`padding-bottom`과 음수 마진을 함께 써서 디센더(g, y, p)가 마스크에 잘리지 않게 합니다. 좁은 휴대폰에서는 지정한 두 줄이 각각 다시 줄바꿈될 수 있습니다. 모바일 스크린샷을 확인하고 필요하면 `<br class="only-wide">` 패턴으로 모바일 줄을 짧게 정하거나 크기를 줄입니다.

### 스크롤 등장 (한 번)

모든 블록이 아니라 등장 효과가 필요한 두세 섹션에 사용합니다.

```css
@media (prefers-reduced-motion: no-preference) {
  .js [data-reveal] { opacity: 0; transform: translateY(24px); transition: opacity 700ms var(--ease-out), transform 900ms var(--ease-out); }
  .js [data-reveal].is-in { opacity: 1; transform: none; }
}
```

```js
const io = new IntersectionObserver((entries) => {
  for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
}, { rootMargin: '0px 0px -12% 0px', threshold: 0.1 });
document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));
```

등장을 스크롤 리스너에 연결하거나 요소 재진입 때 다시 실행하지 마세요. 관찰자가 작동하지 않아도 `opacity: 0`에 남겨 두지 마세요(`html.js` 조건이 JS 미사용을, `unobserve`가 재실행을 처리합니다).

### 이미지 셔터

프레임 안에서 크기가 조금 줄어들며 한쪽 끝부터 열리는 이미지입니다. 갤러리의 기본 연출이며 히어로 또는 쇼케이스 이미지 하나에 사용합니다.

```css
.shutter { overflow: hidden; }
@media (prefers-reduced-motion: no-preference) {
  .js .shutter { clip-path: inset(0 0 100% 0); transition: clip-path 1100ms var(--ease-in-out); }
  .js .shutter img { transform: scale(1.12); transition: transform 1500ms var(--ease-soft); }
  .js .shutter.is-in { clip-path: inset(0); }
  .js .shutter.is-in img { transform: none; }
}
```

### 누름과 호버

```css
.button { transition: transform var(--t-press) var(--ease-out), background-color var(--t-hover) ease, color var(--t-hover) ease; }
.button:active { transform: scale(0.97); }
.link { text-decoration: underline; text-decoration-color: transparent; text-underline-offset: 0.2em; text-decoration-thickness: 0.07em; transition: text-decoration-color var(--t-hover) ease; }
@media (hover: hover) and (pointer: fine) {
  .button:hover { background-color: var(--accent-strong); }
  .link:hover { text-decoration-color: currentColor; }
}
```

터치 기기는 탭으로 호버를 발생시키고 유지하므로 호버 스타일은 `(hover: hover)` 안에 둡니다. 호버는 대비를 높여야 합니다. 호버 시 글자 굵기를 바꾸면 텍스트가 다시 배치되니 바꾸지 마세요. 모든 카드가 들리거나 커지게 하지 말고 작고 일관된 반응 하나면 충분합니다.

### JavaScript 없는 스크롤 연동 진행

히어로가 사라질 때 크기가 바뀌는 워드마크, 몇 퍼센트 움직이는 이미지, 진행 막대에 사용합니다. 스크롤 타임라인 미지원 브라우저에는 정적인 상태를 제공하도록 `@supports`로 감쌉니다.

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .drift { animation: drift linear both; animation-timeline: view(); animation-range: entry 0% exit 100%; }
    @keyframes drift { from { transform: translateY(-4%); } to { transform: translateY(4%); } }
  }
}
```

이동은 요소의 8% 미만으로 작게 유지합니다. 큰 패럴랙스는 글자를 읽기 어렵게 하고 낡아 보입니다.

### 고정 이야기

항목이 지나가는 동안 제목이 머무르는 섹션입니다. `position: sticky`를 사용하고 스크롤을 가로채지 마세요.

```css
.story { display: grid; grid-template-columns: 5fr 7fr; gap: var(--gutter); align-items: start; }
.story__title { position: sticky; top: 18vh; }
@media (max-width: 800px) { .story { grid-template-columns: 1fr; } .story__title { position: static; } }
```

### 행에 붙어 있는 미리보기 색인

이름 행을 가리키거나 탭으로 이동하면 그 행 높이에 프레임 하나가 열립니다. 프레임은 포인터 대신 행을 따라갑니다.

```html
<section class="index">
  <ul class="index__list">
    <li><a class="index__row" href="/work/harbour-house" data-preview="/img/harbour-house.jpg">
      <span class="index__name">Harbour House</span><span class="index__year">2025</span>
      <img class="index__thumb" src="/img/harbour-house-small.jpg" alt="" loading="lazy" width="640" height="400">
    </a></li>
    <!-- … -->
  </ul>
  <div class="index__frame" aria-hidden="true"><img alt=""></div>
</section>
```

```css
.index { position: relative; }
.index__list { list-style: none; margin: 0; padding: 0; }
.index__row { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 0 var(--gutter); padding-block: 0.3em; font-size: var(--step-head); color: inherit; text-decoration: none; transition: opacity var(--t-hover) ease; }
.index__thumb { order: -1; flex-basis: 100%; width: 100%; height: auto; margin-bottom: 0.4rem; }
.index__frame { display: none; }
@media (hover: hover) and (pointer: fine) {
  .index__list { max-width: 62%; }
  .index__thumb { display: none; }
  .index__list:has(.index__row:hover, .index__row:focus-visible) .index__row:not(:hover, :focus-visible) { opacity: 0.4; }
  .index__frame { display: block; position: absolute; top: 0; right: var(--margin); width: 30%; aspect-ratio: 4 / 3; z-index: 1; pointer-events: none; clip-path: inset(100% 0 0 0); transition: clip-path 320ms var(--ease-out), transform 360ms var(--ease-out); }
  .index__frame.is-open { clip-path: inset(0); }
  .index__frame img { width: 100%; height: 100%; object-fit: cover; }
}
@media (prefers-reduced-motion: reduce) { .index__frame { transition: none; } }
```

```js
(() => {
  const root = document.querySelector('.index');
  if (!root) return;
  const frame = root.querySelector('.index__frame');
  const picture = frame.querySelector('img');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  let warmed = false;
  const show = (row) => {
    if (!fine.matches) return;
    if (!warmed) { warmed = true; root.querySelectorAll('[data-preview]').forEach((a) => { new Image().src = a.dataset.preview; }); }
    picture.src = row.dataset.preview;
    const y = row.offsetTop + row.offsetHeight / 2 - frame.offsetHeight / 2;
    const max = root.offsetHeight - frame.offsetHeight;
    const opening = !frame.classList.contains('is-open');
    if (opening) frame.style.transitionProperty = 'clip-path';   // open in place, do not slide in from the top
    frame.style.transform = `translateY(${Math.min(max, Math.max(0, y))}px)`;
    if (opening) { frame.getBoundingClientRect(); frame.style.transitionProperty = ''; }
    frame.classList.add('is-open');
  };
  const hide = () => frame.classList.remove('is-open');
  root.querySelectorAll('.index__row').forEach((row) => {
    row.addEventListener('pointerenter', () => show(row));
    row.addEventListener('focus', () => show(row));
  });
  root.addEventListener('pointerleave', hide);
  root.addEventListener('focusout', (e) => { if (!root.contains(e.relatedTarget)) hide(); });
})();
```

터치 화면에서는 각 행의 이름 위에 해당 사진을 보여 줍니다. 연구의 5개 페이지가 이 방식으로 작품을 탐색합니다. 프레임은 약 470×270부터 목록 뒤 큰 판까지 다양하며 다른 행은 약 0.3으로 흐려집니다(여기서는 흐린 텍스트의 하한인 0.4). 연구의 다른 사례에서 보인 이미지 꼬리와 커서 부착 미리보기는 눈요기 버전입니다.

### 스크롤하며 떠오르는 줄

줄바꿈을 통제할 수 없는 섹션 제목이나 문장에 사용합니다. 서체 로드 후 나누고 한 번 등장한 뒤 일반 텍스트로 되돌려 자연스럽게 다시 줄바꿈되게 합니다. 일반 텍스트만 사용합니다(내부 링크·강조 없음).

```html
<h2 class="head" data-lines>Turned by hand in one small workshop</h2>
```

```css
[data-lines] .line { display: block; overflow: clip; padding-bottom: 0.12em; margin-bottom: -0.12em; }
[data-lines] .line > span { display: block; }
@media (prefers-reduced-motion: no-preference) {
  .is-split .line > span { transform: translateY(110%); }
  .is-split.is-in .line > span { transform: none; transition: transform 900ms var(--ease-expo) calc(var(--i) * var(--stagger-line)); }
}
```

```js
(() => {
  const els = [...document.querySelectorAll('[data-lines]')];
  if (!els.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const restore = (el) => { el.textContent = el.dataset.text; el.classList.remove('is-split', 'is-in'); };
  const split = (el) => {
    const text = el.textContent.trim().replace(/\s+/g, ' ');
    el.dataset.text = text;
    el.textContent = '';
    const words = text.split(' ').map((word) => {
      const s = document.createElement('span');
      s.style.display = 'inline-block';
      s.textContent = word;
      el.append(s, ' ');
      return s;
    });
    const lines = [];                                   // group the words by the line they landed on
    for (const w of words) {
      const last = lines.at(-1);
      if (last && Math.abs(last.top - w.offsetTop) < 4) last.words.push(w.textContent);
      else lines.push({ top: w.offsetTop, words: [w.textContent] });
    }
    el.textContent = '';
    lines.forEach((line, i) => {
      const mask = document.createElement('span');
      const inner = document.createElement('span');
      mask.className = 'line';
      inner.style.setProperty('--i', i);
      inner.textContent = line.words.join(' ');
      mask.append(inner);
      el.append(mask, ' ');
    });
    el.classList.add('is-split');
  };
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      io.unobserve(e.target);
      e.target.classList.add('is-in');
      e.target.querySelector('.line:last-of-type > span')
        .addEventListener('transitionend', () => restore(e.target), { once: true });
    }
  }, { rootMargin: '0px 0px -12% 0px' });
  document.fonts.ready.then(() => els.forEach((el) => { split(el); io.observe(el); }));
  let width = innerWidth;                               // a width change before the reveal: give the text back
  addEventListener('resize', () => {
    if (innerWidth === width) return;
    width = innerWidth;
    els.filter((el) => el.matches('.is-split:not(.is-in)')).forEach((el) => { io.unobserve(el); restore(el); });
  });
})();
```

연구에서는 줄 아래 100~120%에서 마스크 상승, 0.6~1.2초, 줄 사이 75~120ms를 사용하며 블록 상단이 뷰포트 아래 80~95%에 오면 시작합니다. 모션 줄이기에서는 스크립트를 실행하지 않고 일반 텍스트를 보여 줍니다.

### 열리는 창

글자 화면에서 큰 사진 하나로 이어집니다. 고정 무대 중앙의 창으로 시작한 사진이 약 한 화면의 스크롤에 걸쳐 전체 화면으로 열립니다.

```html
<section class="opening">
  <div class="opening__stage">
    <img src="workshop-wide.jpg" alt="The workshop at first light, benches cleared" width="2400" height="1500">
  </div>
</section>
```

```css
.opening__stage { height: 100svh; overflow: clip; }
.opening__stage img { display: block; width: 100%; height: 100%; object-fit: cover; }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .opening { height: 200svh; view-timeline-name: --opening; --inset-y: 20%; --inset-x: 28%; }
    .opening__stage { position: sticky; top: 0; animation: opening-window linear both; animation-timeline: --opening; animation-range: contain 0% contain 75%; }
    .opening__stage img { animation: opening-settle linear both; animation-timeline: --opening; animation-range: contain 0% contain 75%; }
  }
}
@media (max-width: 700px) { .opening { --inset-y: 18%; --inset-x: 8%; } }
@keyframes opening-window { from { clip-path: inset(var(--inset-y) var(--inset-x)); } to { clip-path: inset(0); } }
@keyframes opening-settle { from { transform: scale(1.15); } to { transform: none; } }
```

섹션 높이는 두 화면, 무대 고정은 한 화면입니다. 고정 구간 4분의 3에서 창이 완전히 열리므로 페이지가 넘어가기 전 전체 화면 사진이 잠시 머뭅니다. 연구의 14페이지에서 시작 창은 너비 38~60%, 이동 구간은 600~1,800px였으며 독자는 1~2화면을 원했습니다. 스크롤 타임라인이 없거나 모션 줄이기이면 사진을 전체 화면으로 보여 줍니다.

### 고정 사진, 지나가는 캡션

사진용 고정 이야기입니다. 한쪽 사진은 머무르고 다른 쪽의 짧은 캡션이 지나갑니다. 화면 가운데 캡션이 강조되며 그 사진이 나타납니다.

```html
<section class="steps">
  <figure class="steps__media">
    <div class="steps__pictures">
      <img src="seasoning.jpg" alt="Ash boards stacked to season" class="is-on">
      <img src="turning.jpg" alt="A leg being turned on the lathe">
      <img src="finish.jpg" alt="Oil rubbed into a finished seat">
    </div>
    <figcaption class="steps__count" aria-hidden="true"></figcaption>
  </figure>
  <ol class="steps__list">
    <li class="steps__item"><h3>Seasoned for a year</h3><p>…</p></li>
    <li class="steps__item"><h3>Turned by hand</h3><p>…</p></li>
    <li class="steps__item"><h3>Finished with oil</h3><p>…</p></li>
  </ol>
</section>
```

```css
.steps { display: grid; grid-template-columns: 7fr 5fr; column-gap: var(--gutter); }
.steps__media { margin: 0; align-self: start; }           /* a stretched grid item cannot stick */
.steps__pictures img { display: block; width: 100%; height: auto; }
.steps__list { list-style: none; margin: 0; padding: 0; }
.steps__item { min-height: 80svh; display: flex; flex-direction: column; justify-content: center; }
.js .steps__media { position: sticky; top: 0; height: 100svh; display: flex; flex-direction: column; justify-content: center; gap: 0.75rem; }
.js .steps__pictures { position: relative; aspect-ratio: 4 / 5; max-height: 80svh; }
.js .steps__pictures img { position: absolute; inset: 0; height: 100%; object-fit: cover; opacity: 0; transition: opacity 500ms ease; }
.js .steps__pictures img.is-on { opacity: 1; }
.js .steps__item { opacity: 0.4; transition: opacity var(--t-ui) ease; }
.js .steps__item.is-active { opacity: 1; }
@media (max-width: 800px) {
  .steps { display: block; }                               /* the section, not a grid area, contains the sticky picture */
  .js .steps__media { height: auto; z-index: 1; background: var(--bg); padding-block: 0.5rem; }
  .js .steps__pictures { aspect-ratio: 3 / 2; max-height: 42svh; }
  .steps__item { min-height: 60svh; }
}
@media (prefers-reduced-motion: reduce) { .js .steps__pictures img, .js .steps__item { transition: none; } }
```

```js
(() => {
  const root = document.querySelector('.steps');
  if (!root || !('IntersectionObserver' in window)) return;
  const items = [...root.querySelectorAll('.steps__item')];
  const pictures = [...root.querySelectorAll('.steps__pictures img')];
  const count = root.querySelector('.steps__count');
  const show = (i) => {
    items.forEach((el, k) => el.classList.toggle('is-active', k === i));
    pictures.forEach((el, k) => el.classList.toggle('is-on', k === i));
    if (count) count.textContent = `${i + 1} of ${items.length}`;
  };
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) show(items.indexOf(e.target));
  }, { rootMargin: '-45% 0px -45% 0px' });                 // a band across the middle of the screen
  items.forEach((el) => io.observe(el));
  show(0);
})();
```

JavaScript가 없으면 사진과 캡션은 일반적인 두 열이 됩니다. 연구에서 비활성 항목은 20~40%(10~15%는 글자가 사라진 것처럼 보여 여기서는 하한 40%), 교차 페이드는 400~600ms, 단계당 약 한 화면이었습니다. 독자는 두 단계를 넘는 고정 시퀀스에 보이는 개수를 요구했습니다. 개수는 본문 서체의 평범한 문장으로 적으며 앞에 0을 붙인 숫자는 쓰지 않습니다.

### 가로 갤러리

짧은 컬렉션(8항목 이하)의 사진 행이 고정 무대에서 세로 스크롤에 따라 가로로 움직입니다. 기본은 네이티브 드래그 행입니다. 모션이 허용된 넓은 화면에서 행 길이가 세 화면 미만일 때만 고정 버전을 추가합니다.

```html
<section class="gallery">
  <div class="gallery__stage">
    <h2 class="head">Eight kitchens, one stool</h2>
    <ul class="gallery__track">
      <li class="gallery__item"><a href="/kitchens/leith"><img src="leith.jpg" alt="A narrow galley kitchen in Leith" width="1200" height="1500"><span>Leith</span></a></li>
      <!-- … -->
    </ul>
  </div>
</section>
```

```css
.gallery__track { display: flex; gap: var(--gutter); list-style: none; margin: 0; padding: 0 var(--margin); overflow-x: auto; scroll-snap-type: x mandatory; scroll-padding-inline: var(--margin); }
.gallery__item { flex: 0 0 min(72vw, 28rem); scroll-snap-align: start; }
.gallery__item img { display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; }
.gallery.is-pinned .gallery__stage { position: sticky; top: 0; height: 100svh; display: flex; flex-direction: column; justify-content: center; gap: 2rem; overflow: clip; }
.gallery.is-pinned .gallery__track { overflow: visible; scroll-snap-type: none; }
.gallery.is-pinned .gallery__item { flex-basis: calc(62svh * 0.8); }
```

```js
(() => {
  const root = document.querySelector('.gallery');
  if (!root) return;
  const track = root.querySelector('.gallery__track');
  const wide = matchMedia('(min-width: 900px) and (prefers-reduced-motion: no-preference)');
  let dx = 0, queued = false;
  const place = () => {
    queued = false;
    if (!root.classList.contains('is-pinned')) return;
    const p = Math.min(1, Math.max(0, -root.getBoundingClientRect().top / dx));
    track.style.transform = `translate3d(${(-p * dx).toFixed(1)}px, 0, 0)`;
  };
  const measure = () => {
    root.classList.add('is-pinned');                     // measure the row as it would be when pinned
    track.style.transform = '';
    dx = track.scrollWidth - track.clientWidth;
    const pin = wide.matches && dx > 0 && dx < innerHeight * 3;
    root.classList.toggle('is-pinned', pin);
    root.style.height = pin ? `${innerHeight + dx}px` : ''; // one pixel of scroll moves the row one pixel
    place();
  };
  track.addEventListener('focusin', (e) => {             // keyboard: bring the focused item into view
    if (!root.classList.contains('is-pinned')) return;
    const item = e.target.closest('.gallery__item');
    const x = Math.min(dx, Math.max(0, item.offsetLeft - parseFloat(getComputedStyle(track).paddingLeft)));
    scrollTo({ top: root.getBoundingClientRect().top + scrollY + x, behavior: 'instant' });
  });
  addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(place); } }, { passive: true });
  addEventListener('resize', measure);
  addEventListener('load', measure);
  wide.addEventListener('change', measure);
  measure();
})();
```

연구의 8개 페이지가 가로 트랙을 고정했습니다. 페이지 길이는 중앙값 25화면이었고 최악의 사례는 카드 세 개에 9화면, 트랙 하나에 휠 이동 10,000~23,000px가 들었습니다. 여기서는 속도를 1:1로 하고 마지막 사진이 여백에 닿으면 고정을 끝냅니다. 휴대폰, 좁은 창, 모션 줄이기, 긴 행은 터치·트랙패드·키보드를 지원하는 네이티브 스냅 행을 사용합니다. CTA의 유일한 사본을 움직이는 행 안에 넣지 마세요.

### 물러나는 히어로

첫 화면이 떠날 때 사진은 조금 가라앉고 어두워지며 글자는 조금 더 빠르게 떠오릅니다. 히어로가 단순히 스크롤 밖으로 사라지는 대신 뒤로 물러납니다.

```html
<header class="hero">
  <img class="hero__picture" src="kitchen.jpg" alt="…" width="2400" height="1600" fetchpriority="high">
  <div class="hero__copy"><h1 class="display">…</h1><p class="lead">…</p></div>
</header>
```

```css
.hero { position: relative; min-height: 100svh; overflow: clip; display: grid; align-items: end; view-timeline-name: --hero; }
.hero__picture { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero::after { content: ''; position: absolute; inset: 0; background: var(--ink); opacity: 0; pointer-events: none; }
.hero__copy { position: relative; z-index: 1; padding: var(--margin); }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .hero__picture { animation: hero-sink linear both; animation-timeline: --hero; animation-range: exit 0% exit 100%; }
    .hero::after { animation: hero-dim linear both; animation-timeline: --hero; animation-range: exit 0% exit 100%; }
    .hero__copy { animation: hero-lift linear both; animation-timeline: --hero; animation-range: exit 0% exit 70%; }
  }
}
@keyframes hero-sink { to { transform: translateY(8%) scale(1.06); } }
@keyframes hero-dim { to { opacity: 0.35; } }
@keyframes hero-lift { to { transform: translateY(-6%); opacity: 0; } }
```

`exit` 범위는 히어로 상단이 화면 상단에 닿을 때부터 하단이 닿을 때까지이며 첫 화면에서는 첫 한 화면의 스크롤입니다. 연구에서는 퇴장하며 가라앉고 어두워지는 사진, 140px에서 60px로 스크럽되는 제목, 휴대폰에서 축소되는 제목 카드가 있었습니다. 독자는 조용하며 페이지가 “한 장” 같다고 했습니다. 이동은 8% 미만, 덮개는 그러데이션 대신 최대 35%의 단색입니다. 미지원 또는 모션 줄이기에서는 정적입니다.

### 페이지 사이 전환

브라우저 자체 뷰 전환으로 사이트 페이지를 탐색합니다. 이전 페이지가 빠르게 사라지고 새 페이지가 올라오며 클릭한 사진이 다음 페이지 히어로 자리로 이동합니다. 라이브러리나 전체 화면 커튼은 쓰지 않습니다.

```css
/* on every page */
@view-transition { navigation: auto; }
@media (prefers-reduced-motion: reduce) { @view-transition { navigation: none; } }
::view-transition-old(root) { animation: vt-leave 200ms var(--ease-exit) both; }
::view-transition-new(root) { animation: vt-arrive 380ms var(--ease-out) 60ms both; }
::view-transition-group(*) { animation-duration: 480ms; animation-timing-function: var(--ease-in-out); }
::view-transition-image-pair(*.picture) { overflow: clip; }
::view-transition-old(*.picture), ::view-transition-new(*.picture) { height: 100%; object-fit: cover; }
@keyframes vt-leave { to { opacity: 0; } }
@keyframes vt-arrive { from { opacity: 0; transform: translateY(16px); } }
```

```html
<!-- on the index: the card picture of one project -->
<img src="/img/leith.jpg" alt="…" style="view-transition-name: kitchen-leith; view-transition-class: picture">
<!-- on that project's page: its hero picture -->
<img src="/img/leith-wide.jpg" alt="…" style="view-transition-name: kitchen-leith; view-transition-class: picture">
```

각 이름은 페이지당 한 번만 나올 수 있습니다. 문서 간 뷰 전환을 지원하지 않는 브라우저는 그대로 이동합니다. 연구의 16페이지는 페이지 전환 라이브러리를 로드해 0.7~2.4초 전체 화면 커튼을 실행했고 6페이지는 뷰 전환을 썼습니다. 새 페이지는 0.5초 안에 읽을 수 있어야 합니다.

### 글자색 채우기

한 문장이 화면을 올라가며 줄마다 옅은 글자색에서 완전한 글자색으로 채워집니다. 채워지기 전부터 읽을 수 있으며 채움은 속도만 정합니다.

```html
<p class="statement head" data-fill>Nine people, one workshop, no catalogue: every stool is made for the kitchen it goes to.</p>
```

```css
[data-fill] { --fill: var(--ink); color: var(--fill); }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .is-filling > span { display: inline-block; color: color-mix(in oklab, var(--fill) 45%, transparent); animation: ink-fill linear both; animation-timeline: view(); animation-range: cover 20% cover 45%; }
  }
}
@keyframes ink-fill { to { color: var(--fill); } }
```

```js
(() => {
  if (!CSS.supports('animation-timeline: view()') || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('[data-fill]').forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach((word, i) => {
      const s = document.createElement('span');
      s.textContent = word;
      el.append(s, i < words.length - 1 ? ' ' : '');
    });
    el.classList.add('is-filling');
  });
})();
```

각 단어가 자기 위치를 관찰하므로 줄이 화면 아래 4분의 3에서 중앙을 조금 지나는 동안 같은 줄의 단어가 함께 채워집니다. 어두운 장에서는 `--fill`을 해당 글자색으로 설정합니다. 연구의 14페이지가 문장을 회색에서 글자색으로 스크럽했습니다. 읽지 않은 단어는 약 25~30%에서 시작했고 멈춘 프레임에도 반쯤 흐린 문장이 남아 비활성 텍스트처럼 보였습니다. 여기서는 페이지당 문장 하나, 3~5줄, 32px 이상, 45%에서 시작합니다(배경 대비 약 3:1로 큰 글자에 충분). 스크롤 타임라인이 없거나 모션 줄이기이면 완전한 글자색입니다.

### 굴러가는 수치

몇 개의 숫자가 핵심인 페이지에서 각 자리 숫자가 한 번 제 값으로 굴러가며 열마다 한 박자씩 차이를 둡니다. 스크린 리더와 검색을 위해 실제 숫자는 텍스트에 남깁니다.

```html
<p class="figure"><span class="display" data-roll>1987</span> the year the first stool was sold</p>
```

```css
.roll__digits { display: inline-flex; font-variant-numeric: tabular-nums; line-height: 1; }
.roll__col { display: inline-block; height: 1em; overflow: clip; }
.roll__strip { display: flex; flex-direction: column; transform: translateY(calc(var(--d) * -1em)); }
.roll__strip > span { height: 1em; }
@media (prefers-reduced-motion: no-preference) {
  .roll:not(.is-in) .roll__strip { transform: none; }
  .roll.is-in .roll__strip { transition: transform 1100ms var(--ease-expo) calc(var(--i) * var(--stagger-item)); }
}
```

```js
(() => {
  const els = [...document.querySelectorAll('[data-roll]')];
  if (!els.length) return;
  els.forEach((el) => {
    const value = el.textContent.trim();
    const said = Object.assign(document.createElement('span'), { className: 'sr-only', textContent: value });
    const shown = Object.assign(document.createElement('span'), { className: 'roll__digits' });
    shown.setAttribute('aria-hidden', 'true');
    let i = 0;
    for (const ch of value) {
      if (!/\d/.test(ch)) { shown.append(ch); continue; }
      const col = Object.assign(document.createElement('span'), { className: 'roll__col' });
      const strip = Object.assign(document.createElement('span'), { className: 'roll__strip' });
      strip.style.setProperty('--d', ch);
      strip.style.setProperty('--i', i++);
      for (let n = 0; n < 10; n++) strip.append(Object.assign(document.createElement('span'), { textContent: n }));
      col.append(strip);
      shown.append(col);
    }
    el.classList.add('roll');
    el.replaceChildren(said, shown);
  });
  if (!('IntersectionObserver' in window)) { els.forEach((el) => el.classList.add('is-in')); return; }
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -15% 0px' });
  els.forEach((el) => io.observe(el));
})();
```

연구의 6페이지가 통계·연도·좌표의 숫자 열을 굴립니다. 열당 약 0.9~1.1초 expo-out이며 열마다 엇갈립니다. 디스플레이 크기 수치 3~4개에 사용하며 본문이나 로드 후 바뀌는 값에는 쓰지 않습니다. 모션 줄이기에서는 수치를 최종 값으로 둡니다.

### 아코디언

```css
.acc__panel { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 320ms var(--ease-out); }
.acc__panel > div { overflow: hidden; }
.acc[open] .acc__panel, .acc__item.is-open .acc__panel { grid-template-rows: 1fr; }
```

`grid-template-rows`를 `0fr`에서 `1fr`로 애니메이션하면 JavaScript로 측정하지 않아도 콘텐츠의 실제 높이로 열립니다.

### 메뉴 또는 대화상자

```css
.menu { transform-origin: top right; transition: opacity var(--t-ui) var(--ease-out), transform var(--t-ui) var(--ease-out); }
.menu[hidden], .menu.is-closed { opacity: 0; transform: scale(0.97) translateY(-6px); pointer-events: none; }
```

요소는 실행한 위치에서 열립니다(`transform-origin`을 트리거에 둠). `scale(0)`에서 등장하지 말고 0.95–0.98에서 시작합니다. 중앙 대화상자만 가운데를 기준으로 확대합니다.

## 7. 대표 동작

방향 시트가 하나를 지정합니다. 다음은 조사한 갤러리 사이트에서 반복해서 보인 동작입니다.

| 동작 | 일어나는 일 | 구현 방법 |
| --- | --- | --- |
| 마스크 제목 | 로드 때 기준선 뒤에서 줄이 떠오름 | 마스크 줄 등장 구현법 |
| 셔터 이미지 | 히어로·쇼케이스가 가장자리부터 열리며 1.12배에서 안정됨 | 이미지 셔터 구현법 |
| 크기가 변하는 워드마크 | 히어로가 스크롤 밖으로 나갈 때 거대한 워드마크가 몇 퍼센트 축소·확대 | `scale`의 스크롤 연동 구현법 |
| 고정 이야기 | 항목이 지나가는 동안 제목 고정 | sticky 구현법 |
| 미리보기 색인 | 호버한 텍스트 행의 이미지 표시 | 행에 붙어 있는 미리보기 색인 |
| 커튼 푸터 | 끝에 닿으면 페이지 밑에서 마지막 섹션 등장 | 배경과 `z-index`를 가진 main 아래 `position: sticky; bottom: 0` 푸터 |
| 느린 교차 페이드 | 히어로에서 3~4장 사진이 각각 5~6초 교차 전환 | 겹친 이미지와 opacity 키프레임, 탭이 숨겨지면 정지 |
| 화면 끝에서 끝까지 마키 | 매우 큰 글자 한 줄이 천천히 가로 이동 | 콘텐츠 복제, `translateX(-50%)` 선형 반복, 호버·모션 줄이기에서 정지 |
| 드래그 행 | 큰 이미지의 가로 스크롤과 스냅 | `overflow-x: auto; scroll-snap-type: x mandatory`, 라이브러리 없음 |
| 장별 색상 | 각 장의 전체 배경색이 섹션 경계에서 바뀌며 고정 헤더는 아래 장의 글자색을 따름 | CSS 섹션 배경. `base.js`가 `data-ink`에서 `--header-ink` 설정. observer로 전체 페이지를 다시 칠하지 않음 |
| 열리는 창 | 고정 무대 중앙 창이 약 한 화면에 걸쳐 전체 사진으로 열림 | 열리는 창 구현법 |
| 글자색을 채우는 문장 | 화면을 올라가며 45%에서 완전한 글자색으로 채움 | 글자색 채우기 구현법 |
| 고정 사진 위의 시트 | 전체 화면 사진을 한 화면 고정한 뒤 다음 장이 불투명 시트처럼 덮음 | 100svh `position: sticky; top: 0` figure 다음에 자체 배경과 더 높은 `z-index`를 가진 섹션. 스크립트 없음 |
| 가로 갤러리 | 세로 스크롤로 무대를 고정한 동안 짧은 사진 행이 가로 이동 | 가로 갤러리 구현법 |
| 밀리는 줄 | 큰 글자 한 줄이 스크롤로 가로 이동하며 중간에 전체가 읽힘 | 줄에 `animation-timeline: view()`, `translateX` 12%에서 -12%, 선형. 미지원은 정적 |
| 굴러가는 수치 | 핵심 수치 몇 개가 한 번 최종 값으로 굴러감 | 굴러가는 수치 구현법 |
| 이어지는 사진 | 목록에서 클릭한 사진이 다음 페이지 히어로 자리로 이동 | 페이지 사이 전환 구현법 |

주제에 맞춰 고르세요. 포트폴리오는 미리보기 색인, 식당은 느린 교차 페이드, 제품은 히어로 사물의 셔터가 어울립니다. 주제를 설명하지 않는 동작은 장식이므로 빼는 편이 낫습니다.

마찬가지로 좋은 사진 하나가 있는 제품·장소는 열리는 창, 장마다 자체 사진이 있으면 시트, 짧은 방·주방·작품 묶음은 가로 갤러리, 한 단어로 주장하는 브랜드는 밀리는 줄, 숫자를 앞세우는 보고서·펀드·사무소는 굴러가는 수치, 색인과 사례 페이지를 모두 만드는 포트폴리오는 이어지는 사진을 고릅니다.

## 8. 모션 줄이기와 성능

- `prefers-reduced-motion: reduce`는 모션을 없애기보다 적고 부드럽게 하라는 뜻입니다. 불투명도·색상은 유지하고 이동·확대·패럴랙스·자동 재생은 뺍니다. 위 구현법은 모두 `no-preference` 안에 있으므로 모션 줄이기 상태는 곧 완성 상태입니다.
- `transform`, `opacity`, `clip-path`를 애니메이션합니다. `width`, `height`, `top`, `left`, `margin`, `padding`은 매 프레임 레이아웃을 다시 계산합니다. 아코디언의 `grid-template-rows`는 짧고 드물게 쓰므로 허용하는 예외입니다.
- 부모의 CSS 변수 하나를 바꿔 여러 자식을 움직이지 말고 움직이는 요소에 transform을 설정합니다.
- `will-change`는 곧 움직일 요소에만 적용하고 끝나면 제거합니다.
- 화면 밖이거나 탭이 숨겨지면 반복을 멈춥니다.
- 스크롤 가로채기와 사용자 지정 커서는 금지합니다. 사용성은 Awwwards 점수의 30%이며 수상작 점수가 가장 낮은 경우가 많은 항목입니다. 부드러운 스크롤은 터치·모션 줄이기에서 꺼지는 `Stage.smooth()`만 사용합니다.

## 9. 생성형 모션의 흔적

- 모든 블록에 같은 페이드업.
- 히어로에 십여 개의 엇갈린 등장.
- 모든 카드와 이미지의 호버 상승·확대.
- 인터페이스의 바운스·탄성 이징.
- 의미 없는 무한 반복: 맥박치는 점, 떠다니는 도형, 반짝이는 글자, 회전 배지.
- 실행되지 않아 빈 띠를 남기는 등장 효과. 모션 작업 후 `inspect.mjs`를 실행하고 모든 스크린샷에서 빠진 콘텐츠를 확인합니다.

### 최신 Sites of the Day의 사례

연구에서 본 빈도와 이 스킬의 대안입니다.

- **프리로더와 카운터(99개 중 60개, 카운터 26개).** 사용 가능한 페이지 절반은 로드 2.5초 후에도, 3분의 1은 4.5초 후에도 읽을 수 없었습니다. 프리로더는 대부분 이미 로드된 페이지에 남았고 3초 이내 로드된 29개 중 25개도 4.5초에 읽을 내용이 없었습니다. 카운터는 멈추거나 로드보다 오래 지속되거나 실제 진행과 무관한 트윈이었습니다. 이 스킬은 프리로더를 쓰지 않습니다. 장면 로드가 필요하면 HTML 첫 화면(제목·사진·행동)을 즉시 보여 주고 준비된 장면을 뒤에서 페이드인합니다.
- **진입·소리·나이·제스처 관문(99개 중 10개).** 사용하지 않습니다. 소리는 페이지의 컨트롤로 제공하며 기본은 꺼짐입니다.
- **스크롤 가로채기(휠 장면 16개, 무한 장면 9개, 휠이 작동하지 않는 단일 화면 14개).** 방문자는 현재 위치·남은 양·탈출 방법을 모르며 키보드와 스크린 리더에도 정보가 없습니다. 사용성은 6.01로 스크롤 페이지의 6.50보다 낮습니다. 네이티브 스크롤을 사용하고 모든 장면은 끝이 있으며 개수가 보이는 sticky 무대의 스크롤 위치로 구동합니다.
- **부드러운 스크롤 라이브러리(99개 중 67개).** 스크럽 장면에 무게감을 주지만 손과 페이지 사이에 지연을 만듭니다. 긴 이징은 휠이 멈춰도 페이지를 계속 움직입니다.
- **사용자 지정 커서(99개 중 28개).** 따라오는 요소, 이미지 꼬리, 제목을 뭉개는 렌즈, 호버해야 보이는 라벨입니다. 28개 중 10개만 모션 줄이기 규칙이 있습니다. 시스템 커서를 쓰고 라벨은 페이지에 둡니다.
- **글자 뒤섞기와 타자 효과(각각 11개, 5개).** 4초 동안 읽히지 않는 제목, 스크롤 도중 깨지는 본문, 타이핑 종료까지 보류되는 행동입니다. 사용하지 않습니다. 실제 단어가 온전하게 등장합니다.
- **긴 고정 이동 구간.** 고정 페이지는 평균 두 배 길고 화면당 단어는 적습니다. 17페이지가 20화면 이상이며 느린 회전만 있는 화면도 있습니다. 단계당 약 한 화면, 무대당 세 화면, 모든 고정 화면에 글 한 줄을 둡니다.
- **불투명도 0에 묶인 콘텐츠.** 스크롤이 멎을 때까지 글을 숨기는 등장, 10~15%로 흐린 비활성 항목, 반쯤 흐리게 남은 문장입니다. 첫 화면 아래에서 한 번만 등장하고 화면 안 숨김은 최대 900ms, 흐림은 40% 이상, 채움은 45%에서 시작합니다.
- **글을 가로지르는 모션.** 문장 위를 지나는 마키·사물, 자기 단어를 잘라내는 이동 줄, 동작 도중 남아 있는 글자 흐림입니다. 읽는 글 위로 무언가 지나가지 않게 하고 이동 줄은 이동 구간 중 한 번 전체가 읽히게 합니다.
- **오버슈트와 바운스(스타일시트 19개).** 인터페이스에서 계속 금지합니다.
- **끄기 없는 무한 반복.** 대부분 모션 줄이기 규칙 없이 실행되는 그레인, 맥박 점, 이퀄라이저, 회전 배지입니다. 화면 밖이면 일시 정지하고 모션 줄이기에서는 중지합니다.

연구 사례가 금지 동작을 쓴 경우 이 스킬의 대안은 다음과 같습니다. 고정 무대의 가는 진행 막대·눈금은 본문 서체의 단순 개수(“4개 중 2개”)로, 앞에 0을 붙인 카운터(“01/08”)는 단순 개수 또는 생략으로, 교차 페이드 그러데이션 바닥은 장별 단색의 즉시 전환으로, 고정폭 HUD 라벨은 본문 서체의 작은 글자로 바꿉니다.

## 10. 모션 규칙

1. **첫 프레임.** 제목·문장·사진은 HTML에 있으며 첫 프레임에 그려집니다. load 이벤트를 기다리지 않고 최대 네 요소의 로드 연출을 1.2초 안에 끝냅니다.
2. **프리로더·카운터·관문·사용자 지정 커서·휠 가로채기는 없습니다.** 부드러운 스크롤은 `Stage.smooth()`만 씁니다(Lenis lerp 0.1~0.14, 터치·모션 줄이기에서 끔). 손이 멈춘 뒤 계속 미끄러지는 페이지 대신 무게감만 줍니다.
3. **곡선.** 600ms 미만은 `--ease-out`, 800ms 이상 등장은 `--ease-expo`, 와이프·이동은 `--ease-in-out`, 완전 퇴장은 `--ease-exit`, 스크롤 연동·반복은 `linear`, 색상은 기본 `ease`입니다. 오버슈트는 없습니다.
4. **시간.** 누름 140ms, 호버 색상 180~200ms, 이동 호버 300~400ms, 메뉴 240ms, 등장 700~900ms, 사진 열기 1,100~1,300ms, 퇴장은 해당 등장의 60~70%입니다.
5. **엇갈림.** 줄 80~110ms, 목록 50~90ms, 글자 20~40ms이며 글자는 1~3단어 제목에만 씁니다. 시퀀스 하나는 최대 네 단계입니다.
6. **등장.** 요소 상단이 뷰포트 아래 85~90%에 올 때 한 번 실행합니다. 12~32px 상승 또는 줄 마스크를 사용합니다. 보이는 콘텐츠를 900ms 넘게 숨기지 않으며 첫 화면의 요소는 스크롤을 기다리지 않습니다.
7. **스크롤 장면에서 대담하게 표현합니다.** 큰 동작은 장면 라이브러리(`references/scenes.md`)에서 가져옵니다. 방향 시트가 페이지당 두세 개를 뽑으며 각각 `assets/scenes/stage.js` 기반, 1~4화면 고정, 휴대폰 버전과 완성 구도를 갖춥니다. 장면 내부에서는 장면의 수치를 따릅니다. 사진은 창에서 전체 화면으로 커지고 글자는 무대를 가로지르며 카메라는 사진 들판을 날 수 있습니다. 읽는 글에는 규칙 8과 10이 여전히 적용됩니다.
8. **장면 밖 스크롤 연동은 조용하게 합니다.** 선형으로 스크롤바에 고정하고 패럴랙스는 요소의 8% 미만, 확대는 0.94~1.15입니다. `@supports` 안 스크롤 타임라인으로 만들고 미지원은 정적으로 둡니다. 그 밖의 고정 무대는 sticky, 단계당 약 한 화면, 최대 세 화면이며 모든 고정 화면에 글 한 줄이 있습니다.
9. **각각 하나.** 대표 동작 하나(뽑힌 장면이어도 됨), 움직이는 사진 하나, 마키 최대 하나입니다. 두 장면 사이에는 조용한 섹션을 두어 각 장면을 돋보이게 합니다.
10. **글자는 계속 읽힙니다.** 채움은 글자색 45%에서 시작하고 흐림은 40% 아래로 내리지 않습니다. 블러는 최대 8px이며 안정되면 사라집니다. 읽는 글을 가로지르는 이동은 없습니다.
11. **장별 색상**은 섹션 경계에서 즉시 전환하고 고정 헤더 글자색은 300ms로 따라갑니다.
12. **가로 이동.** 네이티브 드래그 행이 우선입니다. 고정 가로 갤러리는 세 화면 미만 행에만 사용하고 키보드를 지원합니다.
13. **페이지 전환.** 뷰 전환은 최대 480ms이며 모션 줄이기에서 끕니다.
14. **모션 줄이기.** 모든 숨김 상태는 `prefers-reduced-motion: no-preference` 안에 둡니다. 모션을 줄인 페이지는 완성된 페이지이며 반복은 멈춥니다. 수상 페이지 3분의 2가 생략한다는 사실은 실천할 이유이지 생략할 이유가 아닙니다.

