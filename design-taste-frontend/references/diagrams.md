# 다이어그램

`assets/diagrams/diagram.js`는 작은 JSON 스펙으로 카드 패널(약 560x340)이나 섹션(1200x560)용 노드와 선
시각 요소를 그립니다. `presets.json`에 바로 쓸 스펙 27개가 있고 각각 어울리는 페이지 kind(`types`:
software, tech, gaming, product, service)가 태그로 붙어 있습니다. `demo.html`은 이를 기능 카드에서 밝게와
어둡게 보여 주고(`?type=gaming`), `lab.html`은 하나를 만드는 도구입니다(아래).

## 다이어그램을 쓸 때, UI 조각을 쓸 때

- 다이어그램은 요점이 사물이 어떻게 연결되는가일 때 씁니다. 읽어 오는 도구, 병렬 작업으로 나뉘는 입력
  하나, 한곳으로 모이는 여러 출처, 동기화되는 두 시스템, 순서대로 놓인 단계, 지역입니다.
- UI 조각(`assets/ui`)은 요점이 사용자가 보거나 하는 것일 때 씁니다. 작성된 답장, 캘린더, 대시보드입니다.
  화면을 그린 다이어그램은 절대 쓰지 않습니다.
- 섹션당 다이어그램 하나, 페이지에는 많아야 둘입니다(tech. product나 service 페이지는 하나이고 정지 상태).
  place 페이지에는 없습니다. 게임 페이지에서 다이어그램은 게임의 시스템(매치메이킹, 저장, 스토어)을
  보여 주며, 게임 자신의 사진을 대신하지 않습니다.

## 레이아웃과 프리셋 고르기

| 레이아웃 | 보여 주는 것 | 프리셋 |
|---|---|---|
| `hub` | 중심과 그 도구. `children`이 있으면 마인드맵, `"shape": "radial"`이면 웹 | hub-tools, hub-branches, hub-web, hub-stack (tech), hub-stores (gaming) |
| `ring` | 궤도 위의 로고나 지역 | ring-apps, ring-regions, ring-edge (tech), ring-servers (gaming) |
| `tree` | 뻗어 나가는 하나 | tree-orders, tree-release (tech) |
| `lanes` | 입력 하나, 코어, 병렬 레인(스레드 셋) | lanes-agent, lanes-media, lanes-deploy, lanes-render (tech), lanes-matchmaking (gaming) |
| `fanin`, `bowtie` | 여럿이 하나로. 그리고 여럿으로 | fanin-warehouse, fanin-telemetry (tech), bowtie-events, bowtie-model (tech) |
| `sync` | 두 시스템, 오가는 레코드 | sync-crm, sync-saves (gaming) |
| `timeline` | 차례로 하는 단계 | timeline-onboarding, timeline-season (gaming) |
| `grid` | 파이프라인으로 들어가는 파일 | grid-documents, grid-assets (gaming) |
| `free` | 직접 정한 노드와 엣지 | free-approval |

kind로 거릅니다. `dg.presets()`가 객체를 주며, `types`에 페이지의 kind가 있는 것만 둡니다. 게임과 tech 페이지는
펄스가 있는 tech와 gaming 프리셋을 쓰고, product나 service 페이지는 많아야 하나를 정지 상태로 씁니다.

```html
<link rel="stylesheet" href="assets/diagrams/diagram.css">
<div class="panel"><div class="dg" data-diagram="lanes-agent"></div></div>
<script type="module" src="assets/diagrams/mount.js"></script>
```

프리셋을 `data-diagram='{...}'`에 복사한 뒤 모든 라벨, 아이콘, 숫자를 고객의 것으로 바꿉니다. 아포스트로피나
따옴표(`it's`)가 든 라벨은 작은따옴표 속성을 끝내 버리므로, 그럴 때는 스펙을 요소 안의 스크립트에 넣습니다.

```html
<div class="panel"><div class="dg" data-diagram><script type="application/json">{"layout": "hub", ...}</script></div></div>
```

파싱되지 않는 스펙은 `console.error`를 남기고 읽을 수 있었던 이름만 남깁니다.

## 빌더 페이지(빠르게 하나 만드는 도구)

`assets/diagrams/lab.html`을 http로 엽니다. 페이지 kind와 프리셋을 고르고, JSON을 고치거나(입력하는 동안
다시 그려짐) 컨트롤(바탕, 빛, 선 모양, 사이클 2.5에서 4초)을 쓰고, 카드, 섹션, 폰과 밝게, 어둡게를
전환하고, 루프를 다시 시작하고, 마크업과 아이콘 줄을 복사합니다. 카드 안에서는 목업이 아니라 실물을 보여
줍니다. 새 다이어그램은 프리셋에 고객의 말을 더한 것입니다. `free`는 상자의 비율로 정한 노드와 나열한
엣지를 받습니다.

## 아이콘: 리졸버 하나, 마지막에 실행

`diagram.js`는 아이콘 파일만 읽습니다. CDN도, 색 입히기도, 런타임의 Simple Icons 호출도 없습니다. 사이트
루트에서:

`node <skill>/scripts/icons.mjs scan index.html --out assets/icons`

이 명령이 페이지의 다이어그램이 이름 붙인 모든 id를 가져옵니다(`gmail`, `steam`, `google-docs` 같은 엄선한
짧은 이름, `logos:`, `file:`, `si:` id, `ui:` 글리프). 컬러 마크는 logos 세트의 풀컬러에서 오고, 없는
곳(Google Docs, Sheets, Slides)은 `icons.mjs`가 칠한 브랜드 hex의 Simple Icons 마크가 옵니다. 없는 아이콘은 이름의
첫 글자를 보여 주고, 콘솔이 가져오는 줄과 함께 `diagram.js: N icons are not in .../assets/icons ...`라고
말합니다. 그 줄을 실행하세요. 완성된 페이지에는 그런 줄이 없습니다. 대부분 보라색인 마크(Stripe, Twitch)는
글자 색으로 그려지고, 검정 마크는 잉크를 받고, 워드마크는 2:1 슬롯을 받으며 그 타일은 필이 됩니다. 이는 모두
`icons.mjs`가 정해 파일에 구워 넣습니다(`data-ic`). `data-icon-base`는 요소나 그 둘레에 두어 폴더를
옮깁니다.

## 모션: 2.5에서 4초의 한 사이클

- 다이어그램 카드의 펄스는 자기만의 루프입니다(카드 그룹당 하나가 아님). 프로그램은 물결처럼 배치됩니다.
  각 스포크, 가지, 경로가 앞의 것보다 한 박자 뒤에 시작하고(0.24에서 0.5초, 스태거), 전체 프로그램은 3.2초의
  사이클 하나(`"motion": {"cycle": 2.5..4}`)에 맞춰지며 나머지 동안 선이 사라집니다. `d.T`는 항상 2.5에서
  4초입니다. 반복합니다.
  히어로 아래에서는 두 루프가 한 화면을 공유하지 않습니다. 루프하는 조각 옆에서는 둘 중 하나가 멈춥니다
  (`motion.md`).
- 포인터가 카드에 들어가거나(마우스와 펜) 키보드로 포커스가 들어가면 첫 박자부터 다시 시작합니다.
- 화면에 있을 때만 돕니다. 폰(640px 미만)과 동작 줄이기 설정에서는 가장 바쁜 순간 하나로 멈춰 있습니다.
  `"pulse": "none"`도 멈춥니다. `data-dg-still`은 손으로 멈추고 포인터가 카드 위에 있는 동안 재생합니다.
  `data-ui-still`은 다이어그램을 멈추지 않습니다. 도는 루프에는 일시정지 디스크가 붙습니다.
- 빛은 광채와 밝은 머리가 있는 그라데이션 혜성입니다(`"pulse": "dot"`은 머리만). 강조색은 빛과 그것이 닿는 곳에만
  씁니다. 선은 헤어라인이고, 코어는 잉크 타일입니다. 카드는 움직이지 않고, 스크롤로 시작하는 것은 없습니다.
- 바탕은 기본적으로 다양합니다(허브 둘레에는 `rings`, 궤도, 타임라인, 싱크 아래에는 `none`, 흐름에는 `dots`.
  섹션을 이끄는 다이어그램은 `glow`를 더합니다). `ground`가 정합니다. kind other(product나 service 페이지의 정지 다이어그램 하나)에서는
  `"ground": "none"`과 `"motion": {"pulse": "none"}`을 설정합니다. 패턴, 광채, 펄스는 tech 전용입니다. 크기: 평평한 그림은 맞으면 한 단계 큰
  크기를 받고, `"size": "band"`나 `"card"`가 강제합니다.
- 선: 허브의 스포크는 코어 테두리에서 나가는 직선 광선입니다(`"curve": "curve"`, `"elbow"`, `"swirl"`로 바꿈). 흐름은 둥근 엘보로
  꺾입니다.

## 쉬운 라벨

- 도구는 이름으로(Gmail, Zendesk), 단계는 결과로(Reply drafted, Label printed), 장소는 도시로 씁니다. 한 단어에서 세 단어.
- `meta`에는 진짜 같은 숫자(2,481, 14 ms).
- 전문 용어 노드("Orchestration layer", "AI engine")는 쓰지 않습니다. 코어는 제품이 부르는 이름으로 부릅니다.
- 스포크는 최대 8개, 카드 안의 노드는 최대 12개입니다. 빽빽하면 목록이어야 합니다.
- 다이어그램 아래에 캡션은 없습니다. 카드 제목이 보여 주는 것을 말하고, 스펙의 `alt`가 스크린 리더용으로 말합니다.
- 도구 마크는 자기 색으로, 동그라미 속 글자는 절대 안 됩니다. 아이콘이 없는 코어는 이름이 적힌 필입니다.
