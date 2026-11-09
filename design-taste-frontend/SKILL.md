---
name: design-taste-frontend
description: >-
  tasteskill 2.5.1. AI가 만든 티가 나는 프런트엔드를 걸러 내는 스킬로, figma.com과 x.ai 수준의
  전문 기업 웹사이트를 만듭니다. 쉬운 문구와 고유한 목소리, 하나의 시스템, 화면당 섹션 하나,
  같은 좌우 가장자리, 실제 사진과 실제 제품 UI(고객에게 사진이 없으면 사용권이 있는 대체 사진,
  제품 렌더는 브리프가 3D를 요구할 때만), 모든 페이지의 히어로 등장 효과와 뽑은 모먼트 한두 개,
  기술·게임·소프트웨어 페이지에만 쓰는 셰이더 효과와 장면, 조용한 마이크로 인터랙션을 갖추고,
  이를 실제 브라우저에서 강제하는 검사기와 마무리 게이트를 씁니다. 랜딩페이지,
  회사·제품·쇼핑몰·카페·호텔·스튜디오·SaaS·AI·개발자 도구·게임 사이트를 만들거나
  디자인·리디자인·스타일 변경·다듬기·품질 검토를 할 때 사용합니다. 정적 HTML/CSS로 만들 때도,
  기존 React·Next.js·Vue·Svelte·Astro·Tailwind 프로젝트 안에서 만들 때도 적용합니다. "AI가 만든 것 같다", "템플릿 같다",
  "밋밋하다", "고급스럽게", "디자인을 다듬어줘"라는 말에도 사용합니다.
hooks:
  Stop:
    - hooks:
        - type: command
          command: 'for f in ${CLAUDE_SKILL_DIR:+"$CLAUDE_SKILL_DIR/scripts/gate.mjs"} ${CLAUDE_PLUGIN_ROOT:+"$CLAUDE_PLUGIN_ROOT/scripts/gate.mjs" "$CLAUDE_PLUGIN_ROOT/skills/taste-skill/scripts/gate.mjs"} ${CLAUDE_PROJECT_DIR:+"$CLAUDE_PROJECT_DIR/.claude/skills/design-taste-frontend/scripts/gate.mjs" "$CLAUDE_PROJECT_DIR/.agents/skills/design-taste-frontend/scripts/gate.mjs"} ${HOME:+"$HOME/.claude/skills/design-taste-frontend/scripts/gate.mjs" "$HOME/.agents/skills/design-taste-frontend/scripts/gate.mjs"}; do if [ -f "$f" ]; then exec node "$f" --hook claude; fi; done; if [ -d .taste-skill ]; then printf "%s gate.mjs not found; CLAUDE_PLUGIN_ROOT=%s CLAUDE_PROJECT_DIR=%s HOME=%s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${CLAUDE_PLUGIN_ROOT-}" "${CLAUDE_PROJECT_DIR-}" "${HOME-}" > .taste-skill/gate-hook-missing.txt 2>/dev/null; fi; for d in .taste-skill */.taste-skill; do if [ -f "$d/build.json" ]; then echo "tasteskill gate: gate.mjs not found (CLAUDE_PLUGIN_ROOT=${CLAUDE_PLUGIN_ROOT-}); the build in $d is not checked" >&2; break; fi; done; exit 0'
          timeout: 600
---

# tasteskill 2.5

좋은 회사가 내놓을 법한 웹사이트를 만듭니다. 무엇을 파는지 쉬운 말로 밝히고, 모든 화면에 실제
대상을 보여 주며, 템플릿에서 나온 것도 예술 작품 같은 것도 아니고 이 고객을 위해 만든 것으로
보여야 합니다. 기준은 figma.com과 x.ai입니다(말로 풀어 쓴 기준은 `layout-v4.md` 1절).

`<skill>`은 이 폴더입니다. Node 22+와 Chrome, Edge 또는 Chromium이 필요합니다(ffmpeg는 선택).

## 하우스 규칙

이 아홉 가지는 이 스킬의 다른 모든 내용보다 우선합니다.

1. **이미지, 렌더, 시각 요소 아래에 캡션이나 설명을 달지 않습니다.** 라이선스 크레딧은 푸터의 한 줄에
   모읍니다.
2. **모든 시각 요소는 1440, 1024, 768, 390에서 빈 바탕이 아니라 실제로 그려져야 합니다.**
3. **화면당 섹션 하나:** 첫 화면에는 히어로만 있고, 모든 섹션은 1440x900에서 정확히 한 화면 또는 두
   화면 높이이며, 다음 섹션의 제목이 비집고 들어오지 않습니다. 유일한 예외는 모먼트로 정해지는
   `photo-chapters` 섹션이며, 세 화면 또는 네 화면입니다.
4. **콘텐츠의 좌우 가장자리가 같습니다.**
5. **호버 마이크로 애니메이션:** 링크 카드는 2px 떠오르고, 사진은 프레임 안에서 1.02-1.03배로 확대되고,
   버튼은 호버에서 한 단계 변하고 클릭에서 눌리고, 밑줄은 그려지고, 카드 루프는 2.5-4초에 한 바퀴
   돌며 반복하고 호버하면 다시 시작합니다. 이는 모션 레이어가 처리하며, 제거하거나 덮어쓰지 않습니다.
   기울임, 캐러셀, 자동 전환 탭은 쓰지 않습니다. 모든 히어로는 로드할 때 한 번 등장하고(`data-enter`),
   모든 페이지는 뽑은 모먼트를 하나, 긴 페이지는 둘 갖습니다(게이트가 둘 다 확인합니다).
6. **어울리는 곳에는 더 많고 더 나은 실제 사진을 씁니다.** 더 나은 배경, 더 나은 히어로, 레이아웃,
   서체도 마찬가지입니다.
7. **실제 풀컬러 아이콘**(이미 알려진 제품의 실제 아이콘이며 그려 낸 아이콘은 쓰지 않습니다). 카드 안에는
   작은 다이어그램 시각 요소를 넣습니다(가지가 뻗은 허브, 입력 하나와 메인 프로세서와 세 개의 병렬
   레인, 선을 따라 달리는 펄스).
8. **큰 어워드 사이트식 장면과 창의적 모먼트는 이 스킬의 일부입니다.** 모든 페이지가 모먼트를
   뽑지만(기술이 아닌 페이지는 사진 중심과 글자 중심), 셰이더 효과와 장면은 업종에 기술적 주제가
   있을 때(기술, AI, 개발자 도구, 게임, 핀테크, 하드웨어)만 쓰고, 동네 카페·빵집·게스트하우스·가게에는
   절대 쓰지 않습니다. 그런 곳에는 사진을 씁니다.
9. **주소:** 도로명과 구·동까지만(도로명이 없으면 구·동), 번지수·우편번호·좌표 없이, 사업자등록번호나
   부가세 번호 없이, 실제 형식의 전화번호 없이, 연락처는 `.example`로 씁니다.

## 1. 업종이 모든 것을 결정합니다

계획의 첫 줄에 업종을 적고 페이지에 선언합니다. 페이지 유형은 `<html data-type>`과
`<meta name="page-type">`에(같은 값), 그리고 `<meta name="site-kind">`에 넣고, 장소형은
`<meta name="page-kind" content="place">`를 더합니다. 뽑기 명령은 마지막 열을 받고
(`start.mjs --page`, `moments.mjs --page`), 히어로 뽑기는 페이지 유형을 받으며, `consistency.mjs`가
메타를 읽습니다.

| 브리프 | page type | site-kind | kind |
|---|---|---|---|
| 앱, SaaS, AI, 개발자 도구, 핀테크·뱅킹 앱, 자체 소프트웨어를 파는 스튜디오 | software | software | software |
| 게임, 자기 게임을 출시하는 스튜디오 | software | gaming | gaming |
| 하드웨어나 기술 기기(드론, 로봇 팔, 키보드) | product | tech | tech |
| 그 밖의 물리적 제품이나 브랜드(의자, 자전거, 온라인으로 파는 원두) | product | other | product |
| 사람을 고용하는 곳: 병원, 법률 사무소, 에이전시, 크리에이티브 스튜디오, 기능 업종 | service | other | service |
| 사람이 찾아오는 곳: 카페, 바, 빵집, 레스토랑, 게스트하우스, 작은 호텔, 가게, 꽃집, 자전거 가게, 체육관, 동네 스튜디오 | place | other | place |

문을 열거나 수업을 하는 제작자(도자기 스튜디오, 웹 숍이 있는 빵집)는 **place**이며, 웹 숍은 상품
섹션이 됩니다. 문 앞에서 일어나는 일이 전혀 없을 때만 product입니다.

아래에서 "tech"는 site-kind가 software, gaming, tech인 경우를 뜻하고, "other"는 나머지 모두입니다.
효과, 장면, 루프, 카운트, CSS 바탕, 다크 페이지, 다크 히어로는 tech 전용입니다. other 페이지는 사진,
단색 바탕, 글자, 실제 아이콘, 히어로의 등장 효과, 뽑은 모먼트 하나(사진 중심 또는 글자 중심,
`moments.md`), 호버 레이어로 만듭니다.

## 2. 업종별 페이지 계획

전체 계획, 뽑기 목록, 섹션 순서는 `references/sections.md`에 있습니다.

- **Place**(카페, 빵집, 게스트하우스, 가게). 사진이 이끕니다. 전체 페이지는 12-20장, 간결한 페이지는
  8-12장이고, 8장 미만이면 3화면짜리 짧은 페이지로 만듭니다(업종과 무관). 고객 사진이 없으면 초안
  경로와 실시간 검색(`photos.md`)을 거친 뒤 장수를 셉니다. 팔레트는 업종에 맞춰 뽑습니다. 프레임이
  맞는 한 히어로는 사진이고(외진 장소는 그 지역의 풍경), 방문 블록은 두 번째 화면에, 이어서 메뉴·상품,
  장소, 주문이나 예약이 옵니다.
  **효과 없는 변주**(`sections.md` 4절): 메뉴·상품 섹션과 장소 섹션은 서로 다른 구도를 뽑으며, 사진 한
  장을 두 섹션이 돌려 쓰지 않습니다. 글자 모먼트는 하나(큰 글자로 놓은 주소나 이름), 한 화면에 주요
  행동 하나, 목록 글자는 16px입니다. 단색 바탕, 정사각형 사진, 한 가지 버튼 스타일, 전화 바, 뽑은
  모먼트를 쓰고, 효과·바탕·루프·조각·다이어그램·탭은 쓰지 않습니다.
- **Product와 service**(site-kind other). 사진이 이끕니다. 제품, 사람, 공간, 작업을 product 페이지에서는
  한 화면에 두 장 이상 보여 줍니다. 스튜디오가 쓰는 도구는 실제 아이콘으로, 정지 다이어그램은 많아야
  하나, 단색 바탕과 브랜드 띠 하나로 만듭니다. 셰이더 효과, 프린트, 그레인, 그라데이션, 장면, 루프는
  쓰지 않습니다(뽑은 모먼트만). WebGL은 브리프가 요구한 제품 렌더에만 씁니다. **사진이 없는 물리적
  제품은 사진으로 보여 줍니다.** 전체 제품 페이지에서는 `photos.mjs search`로 찾은 같은 종류의 대상
  대체 사진을 쓰고 보고서에 각각 올립니다. 렌더(`assets/objects/product-render`, 정지 이미지)는 브리프가
  3D나 렌더를 요구할 때만 쓰고, 그림이나 분위기용 스톡 사진이나 소품 모음은 절대 쓰지 않습니다
  (`sections.md` 3절 제품).
- **모든 product 페이지**(사진으로, 대체 사진으로, 또는 3D 요구에 따른 렌더로 보여 주며 하드웨어도
  마찬가지입니다. 기준은 Figure와 1X이며 `sections.md` 3절 제품): 제품이 통째로 서 있는 곳에서는
  제품을 **크게** 보여 줍니다(프레임 대부분을 채우거나 바탕 위에 앵커 크기로). 회색 바탕 위 회색
  둥근 패널 안에 중간 크기로 놓지 않습니다. **섹션마다 다른 사진**을 쓰며 같은 각도를 두 번 쓰지
  않습니다. **헤드라인의 모든 약속을 사진으로 보여 줍니다**(가족용 자전거라면 아이용 좌석). 뽑은 구도를
  쓰고, 같은 구조를 두 번 쓰지 않으며, 대비되는 바탕을 하나 둡니다. **색상 견본이 사진을 바꾸고**
  색마다 한 번씩 보여 줍니다. **같은 사실을 두 번 쓰지 않으며**, 버튼은 한 단계 변하고 눌립니다(규칙 5).
- **Tech**(소프트웨어, 게임, 하드웨어). 고객 자신의 주제가 실제 크기로 이끕니다. 소프트웨어는 자체
  UI를, 그것이 다루는 대상을 보여 주는 라이브 HTML로(코드 리뷰 도구라면 Accept 동작이 있는 빨강·초록
  diff) 하나의 `app-frame` 안에 넣으며, 일반적인 대시보드나 패널 위의 조각들만 놓지 않습니다. 카드는
  밝힌 패널 위의 조각, 펄스가 도는 다이어그램, 실제 아이콘입니다. 하드웨어는 자체 사진을 쓰고, 없으면
  같은 종류의 대체 사진을 쓰며(렌더는 브리프가 3D를 요구할 때만), 주문 양식뿐이거나 그려 낸 SVG뿐인
  분할 히어로는 쓰지 않습니다. 게임은 h1에 이름, 출시 문구 한 줄, 풀블리드 키 아트로 보여 주는 세계관
  (없으면 배경이 되는 곳의 대체 사진 위에 크게 놓은 이름)을 쓰며, 효과가 그 자리를 대신하지 않습니다
  (`sections.md` 3절 게임). UI 목업 밖에서는 **한 화면에 60-80단어**입니다(`copy.md`). 뽑기에 따라
  **효과 하나**(히어로의 셰이더 바탕이나 `[data-visual]` 프레임 하나, WebGL 부품, 오브젝트, 큰 장면
  하나)와 각자의 섹션에 **모먼트 한두 개**를 쓰며, 라이브 WebGL 컨텍스트는 네 개까지이고, 스크롤에
  따라 움직이는 카드는 없습니다(`effects-usage.md`).
- **하나의 오브젝트가 페이지를 혼자 끌고 가지 않습니다.** 제품이나 히어로 오브젝트가 통째로 나오는
  곳은 히어로와 **많아야 두 섹션 더**이고, 나머지는 브리프가 뒷받침하는 다른 종류의 시각 요소가
  맡습니다(`sections.md` 1절의 표). 게임의 세계와 등장인물, 하드웨어를 작업대에서 쓰는 모습과
  부품 클로즈업, 정지 다이어그램 카드, 글자 모먼트, 업종이 허용하는 맥락 사진이 그것입니다.
- **고객 자신의 자산에는 슬롯이 있습니다.** 브리프가 말한 트레일러, 키 아트, 스크린샷, CAD 렌더,
  모션 영상은 각각 지금 당장 완성돼 보이는 프레임을 갖습니다(대체 포스터가 있는 실제 `<video>`,
  재생할 페이지나 파일이 있을 때만 재생 컨트롤, 세계관의 대체 사진 세 장에서 다섯 장, CAD 프레임).
  고객이 파일을 넣을 수 있게 주석으로 이름을 적어 두며, 절대 비워 두지 않습니다
  (`sections-library.md`, client-slots).

## 3. 어떤 페이지에 무엇을 쓰는가

페이지가 쓰는 모든 자산군의 레퍼런스를 먼저 엽니다. 대시(-)는 절대 쓰지 않는다는 뜻입니다.

| 필요 | 자산 | 소프트웨어, 게임 | 하드웨어 | 제품, 서비스 | 장소 | 레퍼런스 |
|---|---|---|---|---|---|---|
| 높이, 가장자리, 히어로, 글자 | `system.css`, `assets/layout` | 뽑은 히어로 | 뽑은 히어로 | 뽑은 히어로 | 장소 히어로 | `layout-v4.md` |
| 섹션과 레시피 | `starter.html` | 해당 계획 | 제품 계획 | 해당 계획 | 장소 계획 | `sections.md`, `sections-library.md` |
| 토큰, 그리드, 버튼, 내비게이션, 푸터, 색 | `system.css`, `system.js` | 예 | 예 | 예 | 장소 토큰 | `system.md` |
| 양식, 키보드, head와 공유 태그 | `starter.html`, `system.css`, `system.js` | 예 | 예 | 예 | 예 | `system.md` |
| 문구, 연락처, 크레딧 | `scripts/copy-lint.mjs` | 예 | 예 | 예 | 예 | `copy.md`, `copy-voice.md` |
| 히어로 등장 효과, 호버, 눌림, 포커스, 내비게이션, 탭 | `assets/motion` | 예 | 예 | 예 | 예 | `motion.md` |
| 카드 루프, 카운트 | `assets/motion`, `assets/ui` | 예 | 예 | - | - | `motion.md`, `cards.md` |
| 사진 | `scripts/photos.mjs` | 사람, 고객. 게임은 아트, 없으면 그 배경의 대체 사진 | 중심 | 중심 | 중심, 12-20장 | `photos.md` |
| 실제 도구·앱·파일 아이콘 | `scripts/icons.mjs` | 예 | 예 | 실제로 쓰는 도구 | - | `icons.md` |
| 기능 카드, UI 조각 | `assets/ui` | 중심(게임은 없음) | 그 앱 | 고객이 운영하는 앱 | - | `cards.md` |
| 다이어그램 카드(허브, 레인, 펄스) | `assets/diagrams` | 0-2개, 펄스 | 0-2개, 펄스 | 0-1개, 정지 | - | `diagrams.md` |
| CSS 바탕 | `assets/backgrounds` | 0-2개 뽑기 | 0-2개 뽑기 | 단색 토큰 | 단색 토큰 | `backgrounds.md` |
| 셰이더 바탕 | `assets/effects` | 효과 하나 | 효과 하나 | - | - | `effects-usage.md` |
| 창의적 부품(`fx-*`) | `assets/components` | 예 | 예 | `fx-photo`는 일반, `fx-map`은 정지 | `fx-map` 정지 | `effects-creative.md` |
| 오브젝트와 프린트 | `assets/objects` | 효과로서 하나. 브리프가 3D를 요구하면 렌더 | 브리프가 3D를 요구하면 그 렌더 | 브리프가 3D를 요구하면 그 렌더 | - | `effects-objects.md` |
| 어워드 사이트식 모먼트 | `assets/moments` | 1-2개 | 1-2개 | 1-2개(사진, 글자) | 1-2개(사진, 글자) | `moments.md` |
| 큰 장면 | `assets/scenes` | 0-1개 | 0-1개 | - | - | `scenes.md` |
| 속도와 무게 | `scripts/perf.mjs` | 예 | 예 | 예 | 예 | `perf.md` |

첫 페이지를 만들기 전에 `copy.md`, `copy-voice.md`, `system.md`, `layout-v4.md`, `sections.md`를 전부
읽습니다.

## 4. 진행 순서

0. **스택.** 빈 폴더는 정적 페이지로 만듭니다. `<skill>/assets`를 `assets`로 복사하고
   `assets/starter.html`에서 시작합니다. 기존 프로젝트는 자기 스택으로 만들고, 컴포넌트가 스타터의
   마크업과 클래스를 가져오며, 키트는 공개 폴더(`public/assets`)에 복사해 일반 파일로 불러옵니다.
   Next.js를 요구하는 브리프는 정적 내보내기(`output: 'export'`)로 만들고, 빌드된 페이지로 검사합니다
   (`--root out`).

1. **브리프를 읽습니다.** 업종(1절), 파는 것, 사는 사람, 주요 행동 하나(거래를 일으키는 행동: Book a
   room, Order a cake, Start a free trial. 둘 다 없는 장소는 Get directions), 실제 재료(로고, 화면,
   사진, 가격, 주소, 영업시간)를 적어 둡니다. 그런 다음 페이지가 생기기 전에 마무리 게이트를 켭니다.

   ```bash
   node <skill>/scripts/gate.mjs --start index.html --kind <kind> --category "<what is sold>" --primary "<main action>"
   ```

   프레임워크 빌드는 `index.html` 대신 개발 서버 URL(`--start http://localhost:5173/`)이나 빌드된
   페이지(`--start dist/index.html --root dist`. Next.js 내보내기는 `out`)를 지정하고, 게이트를 돌리기
   전마다 다시 빌드합니다.

2. **문구를 먼저 전부 씁니다.** 문구 레이어(`copy-voice.md`: 팩트 시트, 계획에 적는 목소리 카드, 페이지의
   모양, 장치 예산. `copy-registers.md`의 어조, `copy-moves.md`의 기법)를 `copy.md`의 규칙 안에서
   씁니다. h1은 업종과 사는 사람이나 장소를 말하고(게임은 이름과 장르), 첫 화면에 확실한 사실 하나, 모든
   제목에 명사, 버튼은 동사와 목적어입니다. 지어낸 브랜드 이름(먼저 검색하고 결과는 페이지 옆
   `names.json`에 보관)과, 장소의 경우 그럴듯한 영업시간과 가격(각각 `data-assumed`로 표시, `copy.md`, 가정해도 되는 것) 외에는 아무것도 지어내지 않습니다. `.md` 파일에 둔 초안도 페이지와 같은
   방식으로 린트됩니다(목소리 카드와 파트 라벨은 건너뜁니다).

3. **페이지를 화면 단위로 계획합니다.** 1행: 업종. 2행: 뽑기 결과(4단계)와 팔레트가 업종에 맞는 이유
   한 문장. 이어서 섹션마다 한 줄씩 적습니다. id, 하나의 아이디어, 사진과 그 종류(object, use, parts,
   world, slot, diagram, type. object 줄은 세 개까지), 화면 수(콘텐츠 높이에 따라 1 또는 2,
   `layout-v4.md` 2절), 모먼트가 있는 섹션과 그것이 움직이는 이유(tech는 효과나 장면도)를 적습니다.
   지금 사진을 고릅니다(`photos.md`). 대체 사진을 포함한 사진 장수가 장소 페이지의 길이를 정합니다(2절).
   그런 다음 `cards.md`와 사용하는 모든 id의 레시피(`sections-library.md`)를 읽습니다.

4. **취향으로 고르지 말고 뽑습니다.** 각 명령은 이력을 남기므로 페이지마다 달라집니다.

   ```bash
   node <skill>/assets/layout/deal.mjs --type <page type> --has <photo,ui,film,object,setting> --history .taste-skill/layout-history.json   # the hero; a game adds --kind gaming, hardware --kind tech
   node <skill>/scripts/start.mjs deal --page <kind> --trade <trade> --history .taste-skill/history.json    # three palettes made for the trade, three pairings: take the first; add --axis after a word or editorial hero
   node <skill>/scripts/start.mjs css --page <kind> --palette <id> --type <id> --radius soft --history .taste-skill/history.json
   node <skill>/scripts/start.mjs brand --page place --bg "#.." --ink "#.." --accent "#.." [--surface "#.."] [--muted "#.."] --type <id> --radius soft   # the client's own colours (a logo, a painted shopfront), in place of css
   node <skill>/scripts/moments.mjs pick --page <kind> --count 1|2 --fits section,statement --photo --history .taste-skill/history.json   # every kind
   node -e "for(const l of process.argv.slice(1)){const o=l.split('|');console.log(o[Math.floor(Math.random()*o.length)])}" <the kind's lists, below>
   ```

   모든 명령은 프로젝트 폴더에서 실행합니다(뽑기는 실행한 폴더에서 게이트를 켜거나, 한두 단계 위에
   이미 열려 있는 빌드에 합류합니다). 목록은 내비게이션, 푸터, 마무리, 리듬, 버튼, 마크 순서입니다
   (`sections.md` 2절과 3절).
   - software: `"nav-mega|nav-cards|nav-centre" "footer-dark|footer-statement|footer-columns" "close-type|close-word" "dark-band|surface-pairs|space" "solid|pill|tonal|arrow" "wordmark|initial|arc|ring|stack|dots"`
   - gaming: `"nav-mega|nav-centre|nav-cards" "footer-dark|footer-statement" "close-word|close-type" "dark-band|media-band|space" "solid|pill|block" "wordmark|initial|arc|ring|stack|dots"`
   - product and hardware: `"nav-cards|nav-split|nav-mega" "footer-columns|footer-dark" "close-photo|close-type|close-word" "dark-band|brand-band" "arrow|solid|block|pill" "wordmark|initial|arc|ring|stack|dots"`
   - service: `"nav-mega|nav-split|nav-centre" "footer-visit|footer-dark|footer-columns" "close-type|close-photo" "surface-pairs|dark-band|space" "solid|tonal|block|arrow" "wordmark|initial|arc|ring|stack|dots"`
   - place: `sections.md` 4절 장소(뽑기)의 한 줄 전체를 그 순서대로 읽습니다.

   사진이 없는 product나 hardware는 대체 사진을 쓰기 위해 `--has photo`로 뽑습니다. `--has object`는
   브리프가 요구한 누끼나 렌더가 있을 때만 쓰며(항상 `product` 히어로, 박스 없이 래퍼 전체에 걸친 가장
   넓은 각도), 아트 파일이 없는 게임은 `--has setting`을 넘기고(`photo` 히어로, 배경이 되는 곳의 대체
   사진 위에 이름을 놓음. 게임은 항상 `--has`를 넘깁니다). product 페이지는 product, photo, film
   히어로만 뽑습니다. 장소 히어로는 뽑지 않고 출력합니다(`--type place`). 페이지에 없는 사진이 필요한
   부품이 뽑히면 다시 뽑습니다(`sections.md` 2절). 처음 출력된 팔레트와 짝짓기를 씁니다(첫 번째가
   고객의 로고나 사진과 충돌하거나, 짝짓기가 `hero-lines`를 통과하지 못할 때만 다음 것을 쓰며, 이유는
   계획 2행에 적습니다). 고객 자신의 색은 대신 `start.mjs brand`로 처리합니다(`sections.md` 4절 룩). 보라색은 쓰지 않으며 다시 뽑습니다. `:root` 블록은 출력된 그대로 둡니다. 반경은 핀테크와
   개발자 도구에는 `sharp`, 기본은 `soft`, 소비자 앱에는 `round`, 장소는 사각입니다. tech에서만 밝힌
   바탕(`<html data-ground>`: 한 줄짜리 명령으로 `sand|sky|sage`), CSS 바탕(`backgrounds.md`), 효과 하나
   (`effects-usage.md`)를 씁니다. 모든 결과를 계획 2행과 `<body>` 맨 위 주석에 적고 정확히 그대로
   만듭니다(짧은 페이지는 섹션이 없는 부분을 뺍니다: `sections.md` 4절).

5. **만듭니다.** `starter.html`에서 `<html lang data-type data-radius data-buttons data-motion>`을
   설정하고(lang은 브리프의 언어), 메타 세 개, head 블록(title, description, og, icon, theme-color:
   `system.md`, Head), 내비게이션 클래스를 넣습니다. 건너뛰기 링크와 `m-enter` head 줄은 둡니다.
   `assets/layout/hero-<id>.html`에서는 `<section class="hero …" data-enter>`만 복사하고(그 내비게이션,
   다른 섹션, 푸터, 크레딧 줄은 절대 가져오지 않으며, 모든 단어와 사진은 고객의 것으로 바꿉니다), 뽑은
   마무리와 푸터는 `<template>` 밖으로 옮기고 나머지는 지웁니다. 모든 섹션은 `main > section`이고
   `.wrap` 하나, h2가 먼저, `--h: 1` 또는 `2`입니다. 각 섹션은 시스템의 클래스와 토큰으로 레시피대로
   만듭니다. 페이지 CSS는 레퍼런스가 페이지 CSS라고 한 곳에서만 씁니다(시각 요소 안, `--p-h`, `.wall`,
   `.rail`, `.device`). UI는 `assets/ui/<name>/fragment.html`에서 붙여 넣고 모든 이름, 숫자, 로고를
   고객의 것으로 다시 씁니다(키트 아이콘은 `data-icon`이 됩니다, `cards.md`). 다이어그램 카드는 고객의
   라벨을 넣은 `data-diagram="<preset>"`입니다. 마지막으로 `icons.mjs scan index.html --out assets/icons
   --colour`를 실행해 페이지가 언급하는 모든 아이콘이 로컬 파일이 되게 합니다. 효과, 오브젝트, 모먼트,
   장면은 해당 레퍼런스가 말하는 그대로 장착하며, 직접 만든 스크립트로 하지 않습니다. 모먼트의 섹션은
   `assets/moments/_demo/in-page.html`(장소: photo-chapters, word-highlight)이나
   `in-page-service.html`(pinned-chapters, picture-develops 필름)에서 복사하고, 모먼트 자신의
   `demo.html`은 그것만 보여 주는 것이며 페이지 모델이 아닙니다. 양식은 스타터의 `booking-form`입니다
   (`system.md`의 양식). 크레딧: 마크업이 사진을 쓰고 난 뒤 `photos.mjs credits`가 만드는 푸터 한 줄입니다
   (페이지를 읽습니다). 히어로의 타일은 `shoot.mjs`에서 `share.jpg`로 페이지 옆에 복사합니다.

6. **검사하고 봅니다.** 이 스킬의 스크립트만 씁니다. 각 스크립트는 CPU의 WebGL을 켠 헤드리스 Chrome 하나를
   돌리고 자기 PID로 닫으며, 한 번에 하나씩 10분 타임아웃으로 포그라운드에서 실행합니다. 백그라운드,
   창이 뜨는 브라우저, 브라우저 도구로는 절대 돌리지 않습니다.
   각 스크립트는 페이지 파일을 127.0.0.1의 http로 직접 서빙하므로(`file://`은 절대 쓰지 않음) 서버가
   필요 없습니다. 링크가 사이트 루트에서 시작하는 빌드된 페이지(`/_astro/page.css`)는 `--root`에 빌드
   폴더(`dist`)를 넘깁니다.
   `--profile <dir>`은 Chrome 프로필입니다. OS 임시 폴더나 프로젝트의 `.taste-skill` 폴더
   (`.taste-skill/chrome-check`)에 자기 폴더를 두고, 프로젝트 밖은 절대 안 됩니다(`../` 금지). 밖으로
   나가는 상대 경로는 `.taste-skill/chrome-<script>`로 대체됩니다. 그런 다음 실행합니다.

   ```bash
   node <skill>/scripts/copy-lint.mjs index.html --kind <kind>
   node <skill>/scripts/consistency.mjs index.html --widths 1440,1024,820,768,390 --rhythm-widths 1440,820,768,390 --profile <dir> --page <kind> --category "<what is sold>" --primary "<main action>"
   node <skill>/assets/layout/check.mjs --url index.html --profile <dir> --sizes 1440x900,1024x768,820x1180,768x1024,390x844 --shots shots/layout
   node <skill>/scripts/shoot.mjs --url index.html --w 1440 --out shots/1440.png --profile <dir>
   node <skill>/scripts/perf.mjs index.html --profile <dir>
   ```

   1024, 820x1180, 768x1024, 390도 촬영합니다. `check.mjs`의 모든 발견은 페이지를 실패시킵니다
   (`--no-stress` 금지). copy-lint는 브라우저를 열지 않고 1초 안에 끝납니다. 모든 FAIL을 고치고
   (copy-lint WARN도 고치거나 남기는 이유를 밝힙니다) 문구를 소리 내어 읽고(`copy-voice.md` 6절), 다시
   촬영해 모든 스크린샷을 체크리스트와 대조해 읽습니다. 수정 라운드에서는 `consistency.mjs --quick
   --widths 1440,390`을 돌립니다. 그런 다음 게이트를 돌립니다. 게이트는 매번 1440과 390에서 검사기를
   돌리고, 320에서 페이지를 훑으며 넘침, 겹침, 탭 크기를 보고, copy-lint를 실행하며 그 FAIL은 검사기의
   FAIL처럼 막습니다.

   ```bash
   node <skill>/scripts/gate.mjs index.html
   ```

   게이트가 나열한 것을 고치고 마지막 줄이 `GATE: PASS` 또는 `GATE: OPEN`이 될 때까지 다시 돌리며,
   최대 세 라운드입니다(Claude Code에서는 끝낼 때도 자동으로 돌며, 첫 게이트 실행 전의 중단은
   라운드가 아니고, 막힌 뒤 사용자에게 무언가 물으려면 다시 한 번 멈추기만 하면 됩니다). 사용자가
   멈추라고 하거나 페이지를 있는 그대로 내보내라고 하면 `gate.mjs --done "<what they said>"`를
   실행하고(`GATE: DONE`) 열려 있는 FAIL을 보고합니다.
   `GATE: SETUP`(페이지가 아직 없음, 프레임워크의 소스 셸, 로컬이 아닌 페이지)은 브라우저가 열 수 있는
   것을 켜고(1단계) 다시 돌립니다. `GATE: ERROR`(검사를 돌리지 못함)나 `GATE: OFF`는 그 줄을 보고서에
   넣고 끝내며 다시 돌리지 않습니다. 키트의 파일을 고치거나 검사기에서 무언가를 숨기는 일은 절대
   하지 않습니다. 오탐이라고 판단한 FAIL은 이유와 함께 `.taste-skill/waivers.json`에서 면제하며, 검사를
   속여서 고치지 않습니다(`references/gate.md`). 고객 자신의 문구 가운데 copy-lint가 FAIL로 잡은
   단어는 건별로 면제하며 브리프를 이유로 씁니다(로고나 제목에 적힌 고객 이름 안의 단어는 세지 않고
   WARN 하나로 처리합니다).

7. **보고합니다.** `GATE:` 줄을 먼저 쓰고, 이어서 모든 면제와 그 이유, 열려 있는 모든 FAIL을 씁니다.
   업종, 뽑기 결과(팔레트와 그것이 맞는 이유, 짝짓기, 히어로, 바탕, 효과, 모먼트, 장면), 한 줄로 쓴
   목소리 카드와 남긴 모든 copy-lint WARN과 그 이유, 검사기·레이아웃·성능 결과, 확인하지 못한 것,
   가정한 모든 사실(검사기의 `assumed` 목록)과 지어낸 이름의 검색 결과, 양식의 `.example` 대체 값과
   앞으로 정해질 정식 도메인, 고객이 제공해야 하는 사진과 아트(대체 사진 프레임 전부 포함, 라이브러리와
   실시간 검색), 고객 슬롯마다 그 파일과 대체물을 적습니다.

## 5. 체크리스트

각 줄에 해당 검사를 적습니다. `consistency.mjs` id는 대괄호, `check.mjs` 발견은 중괄호, `perf.mjs`
행은 그대로 씁니다. 마지막 줄은 눈으로 보는 것입니다.

- **첫 화면:** 무엇을 파는지, 누구에게 또는 어디서 파는지를 확실한 사실 하나와 함께 말합니다
  [copy-headline, copy-fact]. 히어로가 모든 너비에서 첫 화면을 혼자 채우고 주요 버튼이 그 안에 있습니다
  [hero-screen, hero-fill, fold-action, fold-cut] {hero-fold}.
- **화면당 섹션 하나:** 모든 섹션이 1화면 또는 2화면이고, h2가 먼저이며 위쪽에 정렬되고, 이웃 섹션의
  제목이나 사진이 자기 타일에 들어오지 않으며, 휑한 곳이 없고, 반쯤 빈 섹션이 없습니다
  [section-height, one-section, one-heading, section-air, one-screen, section-gaps, empty-area]
  {screen-short, screen-height, sparse, neighbour, neighbour-ground}.
- **같은 가장자리:** 모든 블록이 `.wrap` 선이나 그리드 열에 맞고, 한쪽으로 삐져나간 것이 없으며, 가로
  스크롤이 없습니다 [container-edges, row-lines, split-pair, off-grid, right-edge, col-edge, spill,
  off-viewport, stagger, top-stagger] {edge-left, edge-right, spill, bleed-one-side, one-sided, lines}.
- **모든 시각 요소가 그려집니다.** 1440, 1024, 768, 390에서 그렇고, 거부된 효과는 정지 대체 이미지를
  보여 줍니다 [visual-empty, empty-visual, gl-fallback, shader-lint, no-visual, photo-weight].
- **캡션이 없습니다.** 사진을 설명하거나 변명하거나 이름 붙이는 캡션이 없고, 크레딧은 푸터 한 줄에
  있습니다 [visual-caption, caption, credit-wall, photo-credit]. 자리 표시자, 샘플 안내, 출력된
  `.example` 주소가 없습니다 [placeholder, sample-label].
- **업종에 맞는 것들:** tech가 아니면 효과 바탕, 프린트, 장면이 없고 뽑은 사진 중심·글자 중심
  모먼트만 있습니다(WebGL은 브리프가 요구한 제품 렌더에만) [effect-kind, effects-fit, photo-print].
  대상 자체가 보입니다. 제품은 크게, 통째로, 많아야 세 섹션에서, 매번 새 사진으로 [product-shown,
  same-object, photo-repeat]. 브리프가 말한 각 자산은 자기 슬롯에 있고, 게임은 이름과 키 아트로 보이는
  세계관, 코드 리뷰 도구는 diff, 소프트웨어는 `app-frame`이 있습니다. 어울리는 곳에는 실제 사진을
  쓰고 같은 사진을 두 번 쓰지 않으며 [photo-set, photo-repeat, photo-upscale], 실제 아이콘은 자기
  색으로, other에는 단색 바탕 [grounds], 장소는 서로 다른 구도 두 개와 글자 모먼트 하나를 뽑습니다.
- **모션:** 모든 버튼, 링크, 링크 카드, 링크 사진이 포인터에 눈에 띄게 반응하고 기울어지는 것은
  없습니다 [motion-layer, hover, hover-move, tilt]. 히어로는 로드할 때 한 번 등장합니다 [hero-enter].
  뽑은 모먼트는 한두 개입니다 [moment-none]. 카드 루프는 2.5-4초에 한 바퀴 돕니다 [loop-cycle].
  스크롤했다고 움직이는 것은 자기 섹션 안의 뽑은 모먼트(모든 업종)와 큰 장면(tech)뿐입니다
  [scroll-linked, scroll-reveal, pinned: 그곳에서만 나와야 함]. 5초를 넘게 움직이는 것에는 일시정지
  버튼이 있습니다 [loop-pause]. 동작 줄이기 설정에서는 모두 멈추고 숨겨진 것이 없습니다
  [reduced-motion, hidden-content]. 라이브 컨텍스트는 네 개까지입니다 [webgl].
- **연락처**는 규칙 9를 따릅니다 [street-number, postcode, coordinates, company-number,
  phone-number]. Get directions는 도로명이 있을 때만, "See the area"는 구·동이 있을 때만 쓰고, 도시만
  있으면 지도 링크가 없습니다 [map-link].
- **키보드와 head:** 모든 컨트롤에 이름이 있고, 사진에 alt가 있고, 눈에 보이는 레이블이 있고, 제목은
  한 단계씩 내려가고, 0보다 큰 tabindex가 없습니다. Tab은 건너뛰기 링크에 가장 먼저 닿고, 그 링이 즉시
  보이며 헤더 밑에 가려지지 않습니다. 메뉴 버튼이 자기 상태를 말하고, lang, title, description, 공유
  태그가 있습니다 [a11y-name, img-alt, field-label, heading-order, tabindex, skip-link, focus-ring,
  focus-visible, focus-hidden, menu-toggle, lang, page-meta, share-meta].
- **하나의 시스템:** 버튼 한 쌍, 카드 스타일 하나, 반경 스케일 하나, 링크 모양 하나
  [button-styles, button-shape, card-family, card-layout, link-styles]. 상자 중첩은 두 겹까지
  [nesting]. 제목 스케일 하나와 불러온 서체 [heading-scale, font-load]. 글자 대비 [text-contrast,
  contrast].
- **문구와 링크:** 제목은 사물의 이름을 말하고, 버튼은 동사와 목적어이며, 히어로 행동은 많아야 둘
  [copy-headings, copy-buttons, copy-actions, action-count]. 같은 행동은 한 화면에 많아야 두 번
  [action-repeat]. 제목의 회색 뒷부분은 별개의 문장 [run-on]. 사실 하나에 표현 하나 [fact-agree].
  가정한 사실은 표시하고, 그것으로 영업 중이라는 줄을 쓰지 않습니다 [assumed, open-now]. 모든 링크가
  연결되고, 양식이 전송되고, 확인 메시지는 실제로 전송된 뒤에만 나오며, 각 오류는 자기 필드 아래에
  있습니다 [links, forms, form-send, form-fields]. 슬롭 단어, 상투 문구, 남은 흔적, 습관처럼 쓴 장치가
  없고 고유한 목소리가 있습니다(copy-lint의 id: copy-residue, copy-slop-word, copy-stock-phrase,
  copy-two-fragment, copy-virtue, ...; `copy-voice.md`).
- **빠름:** `perf.mjs`에 FAIL 행이 없습니다(이미지 무게, 컨텍스트, 레이아웃 이동).
- **820, 768, 390, 320:** 섹션이 자기 화면 수를 지킵니다 [section-height]. 폰에서는 섹션이 최소한 자기
  화면 수만큼이고 담은 내용에 따라 늘어나므로, 아무것도 다른 것 위에 눕거나 고정 바 밑에 깔리지
  않습니다 [collide]. 본문 밖의 모든 링크와 컨트롤은 높이가 44px입니다 [tap-size] (다른 대상이 8px
  미만 거리에 있으면 FAIL). 320에서 화면 밖으로 나가는 것이 없고 [off-viewport], 거기서도 아무것도
  다른 것 위에 눕지 않습니다 [collide]. 첫 화면은 온전히 끝나거나 분명한 블리드로 끝납니다
  [fold-card] (`layout-v4.md`). 분할 레이아웃은 글이 먼저 쌓이고 반쯤 빈 행이 없습니다. 390에서는 한
  열, 버튼은 전체 너비, 전체 화면 메뉴, 장소의 액션 바가 있습니다.
- **눈으로 보기:** figma.com과 x.ai 프레임 옆에 놓아도 전문 기업 사이트로 읽힙니다. 기울거나, 어긋나거나,
  잘리거나, 겹친 것이 없습니다. 히어로는 분위기가 아니라 본업입니다.

## 6. 하지 않는 것

- 스크롤하면 페이드인되는 카드, 행, 타일. 모든 섹션의 페이드인. 글자 패럴랙스. 스크롤 잭킹. 무작위
  깜빡임.
- 고객의 제품, 사람, 장소인 것처럼 내놓은 스톡 사진(대체 사진은 보고서에 대체 사진으로 올리며, 다른
  제작자의 이름이나 로고와 함께 보여 주지 않습니다). 제품을 한 번도 보여 주지 않는 제품 페이지.
- 실제 로고를 닮게 그린 그림. 지어낸 후기, 인용, 고객, 수치.
- 페이지 자체 디자인의 보라색이나 라벤더색: 강조색, 바탕, 그라데이션, 효과 색, 틴트(실제 제3자
  로고는 자기 색을 유지합니다, `icons.md`).
- 레퍼런스 사이트의 코드, 문구, 사진, 시그니처 효과를 베끼는 것.
- 검사를 통과시키려고 키트의 파일(`assets/`, `scripts/`)을 지우거나 고치는 것. 키트 파일을 지적하는
  검사는 보고하고, 무엇이든 바꾼 뒤에는 페이지를 다시 검사합니다.

## 레퍼런스

모두 `references/`에 있습니다. 3절이 각 자산에 필요한 레퍼런스를 알려 줍니다.
