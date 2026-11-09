# 아이콘

도구를 이름으로 언급하는 페이지는 그 도구의 실제 로고를 자기 색으로 보여 줍니다. Google Docs라고 쓴 파일
카드에는 Google Docs 아이콘이, Word 파일에는 Word 파일 아이콘이 붙습니다. 닮은 것을 그려 내지 않고,
실제 아이콘이 있는 곳에 동그라미 속 글자나 일반 문서 글리프를 넣지 않습니다. 가상 고객 자신의 마크는
설계하며 빌려 오지 않습니다.

`scripts/icons.mjs`가 유일한 리졸버입니다. 페이지, `diagram.js`, 그 밖의 모든 부품은 그것이 쓴 SVG 파일을
읽으며, 런타임에 아이콘을 가져오거나, 색을 입히거나, 판단하는 일은 없고, 어떤 페이지도 아이콘을 위해 CDN을
부르지 않습니다.

## 출처

| 세트 | 출처(고정) | 담고 있는 것 | 그림의 라이선스 |
|---|---|---|---|
| `logos` | `cdn.jsdelivr.net/gh/gilbarbara/logos`의 커밋 `d6960edc1b73`(2026년 10월 26일. 저장소에 태그가 없음) | 풀컬러 브랜드 약 1,500개: 첫 번째 선택 | CC0(그 커밋의 LICENSE.txt) |
| `si` | `simple-icons` 16.30.0 | 브랜드 hex로 칠한 단색 마크: 컬러 마크가 없는 곳에서만 쓰는 대체 | CC0 |
| `file` | `@iconify-json/vscode-icons` 1.2.30 | 컬러 파일 유형(pdf, markdown, zip, Word, Excel, PowerPoint): 브랜드가 아닌 문서 유형 | MIT |
| `ui` | `@iconify-json/lucide` 1.2.100 | 인터페이스 글리프, 한 가지 선 세트 | ISC |

`si`는 Google Docs, Sheets, Slides, Forms, Chat, Tasks, Calendly, Evernote, QuickBooks, Revolut, 콘솔과 게임
스토어 마크(PlayStation, Epic Games, Riot, Battle.net, itch.io, Roblox, EA, Ubisoft, Rockstar, Valve,
CurseForge, Modrinth, GOG)에 씁니다. Xbox와 Nintendo는 허용된 어떤 세트에도 없으므로, 콘솔은 글자로
이름을 쓰고 그린 마크는 절대 쓰지 않습니다. 게임의 스토어 행은 Steam, PlayStation, Epic Games입니다
(`apps --tag gaming`). Google 편집기는 브랜드의 파랑, 초록, 노랑으로 나오고, Microsoft Office 마크는
허용된 어떤 출처에도 없으므로 Word, Excel, PowerPoint 파일 카드는 파일 유형 아이콘(`docx`, `xlsx`,
`pptx`)을 씁니다.

**theSVG(`brands` 세트)는 뺐습니다.** 그 패키지는 MIT인데 이는 모음집에만 해당하고, 마크마다 기록한
라이선스는 그쪽의 자체 표기일 뿐 소유자가 준 허락이 아니며, Microsoft 마크 37개가 "no express
redistribution licence supplied"라고 합니다. 프레스 키트 다운로드는 이 스킬이 택하는 경로가 아닙니다.
`brands:` id는 이제 그렇다고 말하는 메시지와 함께 실패합니다.

모든 마크는 여전히 소유자의 상표입니다. 지명적 사용에 한합니다. 제품이 실제로 연동하는 도구의 이름만
쓰고, 보증을 암시하지 않습니다. 푸터에 "Product names and logos are trademarks of their owners"를 쓰고,
사이트는 `icons-credits.json`(파일, 세트, 커밋이 있는 출처, 라이선스, 상표 표시, 그 브랜드의 사이트)을
함께 담습니다.

## 명령

사이트 루트에서 `node <skill>/scripts/icons.mjs ...`를 실행합니다.

- `find google docs`: 모든 세트에서 맞는 것과 라이선스.
- `apps --tag gaming`: 엄선한 목록. 앱 458개와 파일 유형 38개를 짧은 이름(`google-docs`, `steam`, `pdf`)으로
  보여 줍니다. `list --tags`는 태그를 보여 줍니다(dev, ai, gaming, engine, hardware, chips, cloud, db,
  monitoring, payments, social ...). 인터페이스 글리프: `list --set ui --tag gaming`(435개: gamepad-2,
  swords, microchip, circuit-board ...).
- `fetch google-docs slack file:pdf2 ui:arrow-right --out assets/icons`: 파일을 쓰고 붙여 넣을 태그를
  출력합니다.
- `scan index.html --out assets/icons`: 페이지가 이름 붙인 모든 아이콘(다이어그램 스펙, `data-diagram`
  프리셋 이름, `data-icon`)을 가져옵니다. 완성된 페이지에 빠진 아이콘이 없도록 마지막에 실행합니다.
- `check`: 모든 항목이 해결되는지 봅니다. 워드마크, 단색 대체, 검정과 보라 마크를 나열합니다.
- `measure`: 유지보수. 헤드리스 Chrome(CPU 플래그, 자기 PID로 닫음)에서 모든 컬러 마크의 그려진 박스를
  측정해 `index.json`의 `boxes`에 넣고, `fetch`가 그 박스로 크롭합니다. 엄선한 목록이 바뀔 때 실행합니다
  (`--profile <dir>`이 Chrome 프로필을 정합니다).
- 코드에서: `import { resolveIcon } from './icons.mjs'`.

쓰인 각 파일은 판단을 담고 있습니다. 루트의 `data-ic="violet"`, `"ink"`, `"paper"`이며, `diagram.js`와 모든
페이지는 `icons.mjs`가 출력한 그대로 다룹니다.

## 어느 것을 쓰는가

- 브랜드나 파일 유형: 컬러 아이콘이며, 엄선한 목록(`logos`)에서 먼저 고르고, `si` 마크는 목록이 그렇다고 한 곳에서만 씁니다.
- 인터페이스 글리프(검색, 화살표, 체크, 기능 포인트): `ui:`만 쓰며 두 번째 선 세트는 쓰지 않습니다. 글리프는 인라인 svg이고 글자 색을 따릅니다.
- 단색(`--mono`)은 고객 로고 행, 푸터의 소셜 링크, 브랜드에 컬러 버전이 없는 곳에서 더 낫습니다.
  여러 톤의 마크는 단색으로 세부를 유지합니다. 종이색 부분은 단색으로 채우지 않고 실루엣에서 도려냅니다.
- 검정 마크(GitHub, Apple, X)는 `ic-ink`를 달며, icon.css가 어두운 바탕에서 이를 흰색으로 바꿉니다. 워드마크만 있는 로고(Stripe, NVIDIA, Go)는
  `ic-wide`를 달고, `--tile`로 출력하면 넓은 타일을 줍니다.
- 밝은 타일에서 사라지는 밝은 마크는 목록에 없습니다(그래서 Wise, Klarna를 뺐습니다).

### 보라색 규칙(판단이며 그렇다고 밝힙니다)

"보라색이나 라벤더색은 절대 쓰지 않는다"는 페이지 자신의 디자인에 대한 규칙입니다. 제3자 로고는 그
소유자의 마크이므로 색을 바꾸지 않지만, 보라색 덩어리는 팔레트를 깹니다. 채워진 색 가운데 보라색의 비율로
판단합니다(`check`가 출력하며, 짙은 남색은 보라색이 아닙니다).

- 절반 이상(Stripe, Twitch, Google Forms, Terraform, Datadog, ClickUp, Loom, Kotlin, C#, .NET, Bootstrap, ESLint ...): `[violet]`로
  표시합니다. 제품이 실제로 연동하는 도구는 자기 색을 유지합니다. `--colour`를 붙여 `fetch`나 `scan`하세요(없으면 마크가
  글자 색으로 출력되며, 알려진 로고의 회색 대체물은 결함입니다). 보라색 금지는 페이지의 팔레트에 해당하며 제3자 로고에는
  절대 해당하지 않습니다. `--mono`는 고객 로고 행에만 씁니다.
- 절반 미만(Figma 20%, Google Drive 14%): 그려진 그대로 출력합니다. 실제 로고가 페이지를 공식처럼 보이게 합니다. `--mono`는 단색으로 출력합니다.

## 놓는 법

system.css 뒤에 `assets/icons/icon.css`를 연결합니다. `.ic-tile`은 로고 뒤의 부드러운 타일(어두운 바탕에서는
밝은 타일이라 모든 색이 읽힘), `.ic-row`는 목록 행, `.ic-chip`은 아이콘이 붙은 이름, `.ic-stack`은 겹친 타일,
`.ic-cell`을 가진 `.ic-grid--mosaic`은 연동 그리드, `.ic-file`과 `.ic-file--tile`은 파일 카드,
`.ic-point`는 짧은 글이 붙은 글리프입니다. 크기는 16, 20, 24, 28, 32, 36, 40, 48, 56입니다. 아무것도
움직이지 않습니다. `assets/icons/demo.html`은 모자이크, 파일 카드, 종류별 458개 도구 전부, 다크 페이지,
글리프를 보여 줍니다(모든 아이콘은 `assets/icons/demo/`에 있습니다).

모양: `fetch`는 마크를 측정된 그림(여백 2%)으로 크롭하고 크롭한 비율로 모양 클래스를 붙입니다. `ic-wide`(1.8:1 초과),
`ic-land`(1.25:1 초과), `ic-tall`(0.8:1 미만: Google Docs, Figma)입니다. 타일은 가로형 마크를 너비의 70%로,
세로형은 높이의 68%로 맞춥니다. `file` 세트는 일부러 크롭하지 않습니다.

파일 카드, 연동 그리드, "reads from" 목록은 회색 상자가 아니라 20에서 40px의 실제 아이콘을 씁니다. 로고는 자기
비율과 색을 유지합니다.
