# 문구의 티

웹사이트 문구가 모델이 쓴 것처럼 읽히게 만드는 것들과 각각의 해결법입니다. 2026년 11월 기준입니다. 티는 모델 세대마다
바뀌므로, 목록을 외우지 말고 각각이 왜 모델처럼 읽히는지를 익힙니다. 티 하나가 증명하는 것은 적고, 신호는 뭉침과 반복입니다.
`scripts/copy-lint.mjs` 가 셀 수 있는 것을 셉니다. 그 id를 대괄호 안에 적었습니다.

심각도: **ban**(하나만 있어도 티), **cap**(한 번은 괜찮고 반복되면 티), **context**(다른 티 옆에 있을 때만 계산).

## 왜 생기는가

모델은 가장 많은 페이지에 들어맞는 표현을 고르고, 튜닝은 그것을 안전하고 긍정적이며 밀도 높은 문장 쪽으로 매끄럽게 다듬습니다.
고르지 않은 사실은 어떤 사업에도 들어맞는 주장으로 대체됩니다. 그러므로 구체성은 스타일 규칙이 아니라 입력(브리프, 고객의
말)에서 와야 합니다. 그리고 습관을 금지하는 모든 규칙에는 그 옆에 긍정적인 기법이 있어야 하고, 그러지 않으면 모델은 가장
가까운 대체물을 집습니다.

## 1세대: 옛 티(지금은 대부분 피하지만 여전히 점검)

- **금지 단어** [copy-slop-word]: delve, tapestry, testament to, realm, embark, beacon, multifaceted,
  paradigm, myriad, plethora, meticulous, intricate, interplay, garner, boasts (for "has"); elevate,
  unlock, unleash, empower, harness, supercharge, turbocharge, seamless, effortless, cutting-edge,
  revolutionary, transformative, holistic, next-level, next-generation, world-class, best-in-class,
  game-changer, game-changing, state-of-the-art, bespoke, synergy, leverage, reimagine, powerful,
  robust, nestled, unparalleled, unrivalled. 각 단어는 사실 하나를 대신합니다. "seamless"는 설정 단계, "robust"는 실패
  사례, "powerful"은 수치를 대신합니다. 업종에서 글자 그대로의 뜻인 단어는 남깁니다. 클라이밍 harness, bespoke tailoring,
  seamless knit, elevated terrace, 게임의 realm. 로고, ":" 앞의 title, `og:site_name` 이 적는 곳에서의 고객 자신의 이름
  (Elevate Pilates)도 마찬가지입니다. WARN 하나가 나오며 [copy-brand-word], 브리프가 그 이름을 주면 그대로 둡니다.
- **판에 박힌 문장** [copy-stock-phrase]: "In today's fast-paced world", "Unlock the power of", "The
  future of X is here", "Say goodbye to", "Whether you're A or B", "Join thousands of", "Trusted by teams
  worldwide", "Imagine a world where", "Ready to transform your X?", "Look no further", "one-stop shop",
  "X made simple", "at your fingertips", "in just a few clicks", "It's not just a X, it's a Y", "Not
  only X but also Y", "Here's the thing", "Let that sink in".
- **잔여물** [copy-residue]: "Certainly!", "I hope this helps", "[Company Name]", lorem ipsum,
  `{{tokens}}`, 렌더된 페이지의 마크다운 별표나 `##`, 남아 있는 `[NEED]`. 가장 강력한 단일 티입니다. 대화나 템플릿이 페이지에
  붙여 넣어진 것입니다.
- **모양:** 사실에 덧붙은 -ing 꼬리(", ensuring a smooth start") [copy-ing-rider]. 곧바로 답하는 질문("The
  result? Three hours back.")과 콜론으로 드러내기("One thing changed: X") [copy-reveal]. "is"나 "has"로 충분한 곳의 "serves
  as", "stands as", "plays a key role" [copy-puffery].
- **문장부호:** 여기저기의 엠 대시 [copy-em-dash]. 본문의 느낌표 [copy-exclaim]. 글머리표로 쓴 이모지. 어떤
  링크든 그 말 뒤에 붙인 화살표.
- **죽은 은유:** landscape, ecosystem, journey (여행이 아닌 한), "in the X space", hub, "the world of",
  "where X meets Y", "in the heart of" [copy-puffery]. 거리나 사물의 이름을 씁니다.

## 2세대: 지금의 티

이것들은 좋은 문구처럼 보이기 때문에 검토를 통과해 살아남습니다.

- **하우스 목소리**(메타 티). 모든 고객에게 따뜻하고, 익살스럽고, 겸손하고, 약간 문학적. 해결: 고객마다
  `copy-registers.md` 에서 어조를 고릅니다.
- **지어낸 구체성**(ban). "6:12 a.m., from the window of Room 9", "Batch No. 047", "38% fewer
  re-runs". 세부가 설득하기 때문에 장식으로 만들어 낸 세부입니다. 해결: 브리프의 세부만 쓰고, 없으면 더 평이한 문장.
- **수치 띠** [copy-stat-strip]. 한 단어 라벨 위에 놓인 수치 서너 개의 행이 히어로나 이야기 아래에 있으며
  거의 모든 모델 페이지에 있습니다. 해결: 각 숫자는 그것이 입증하는 문장 안에. 띠는 브리프가 주는 평이한 사실(가격, 영업시간,
  개수)만으로. 메뉴의 가격, 시간표, 한 단위로 된 열은 띠가 아닙니다.
- **두 조각 제목 "X. Y."** (cap 1) [copy-two-fragment]. "Twelve rooms. Three ways to stay." 해결: `copy-moves.md`
  의 다른 제목 모양, 즉 그 아래에 주장이 있는 이름, 동사와 대상, 평이한 문장.
- **숫자 짝 제목** (cap 0 to 1) [copy-number-pair]. "Four projects, four very different
  problems." 관련 없는 두 모델 페이지가 거의 똑같이 썼습니다. 해결: 섹션이 담은 것을 말합니다.
- **대조 틀과 그 대체물** (cap 2 in all) [copy-contrast]. "Freshness isn't a
  slogan here." "not X but Y"를 억제하면 "rather than", "instead of", "without the"로 돌아옵니다. 해결: 긍정적 사실만
  말합니다. FAQ의 구매자 질문은 이 장치가 아닙니다.
- **부정 연속** (cap 1) [copy-negation]. "No forms, no back-and-forth." 각 항목이 구매자가 확인할 수 있는
  거절일 때만 하나를 둡니다.
- **미덕 단어** (ban about ourselves) [copy-virtue]. honest, calm, quiet, actually, genuinely,
  truly, simply, thoughtful, carefully, intentional, steady, dependable. 해결: 인정이나 사실로 보여 줍니다. 페이지는 자신을
  honest라고 부르지 않습니다.
- **건조한 끝맺음.** 대부분의 문단 끝에 붙는 "They hold spoons now." 관련 없는 두 사이트에서 같은 농담.
  해결: 정보로 끝맺고 유머는 마이크로카피로 옮깁니다.
- **푸터 맺음말** [copy-footer-signoff]. "Made in Rotterdam, fired at 1,260 degrees."
  "Every Tuesday since 2019." 해결: `copy.md` 의 법적 행, 그 밖에는 아무것도 없음.
- **이름의 은유를 끝까지 우려먹기.** 모든 섹션을 "fires"하는 Kiln이라는 브랜드.
  해결: 한 번만, 또는 아예 쓰지 않음.
- **기원 템플릿.** "In [year], [two first names] found [an old hardware store] and kept [one
  original detail]." 해결: 브리프의 실제 이야기. 없으면 이야기 섹션을 두지 않습니다.
- **다듬은 후기** [copy-quotes]. 항상 셋이며, 각각 수치와 한 방이 있는 작은 이야기입니다.
  tasteskill 페이지에는 브리프가 글자 그대로 주지 않는 한 없습니다.
- **기본 배역** [copy-cast, copy-cast-company]. 사람: Priya (Raman, Shah, Nair), Daniel or
  Amara Okafor, Marcus, Dana, Aisha, Lena M., Tomas, Nora, Maya, Mara and Theo, Isla, Ines, Jess, Sarah J.,
  Elara. 회사: Fieldnote, Kestrel, Halcyon, Brightloop, Acme, Northwind, Lumen, Nimbus, Apex, Zenith,
  Vertex. 해결: 사람 이름은 브리프에서만. 목업의 이름은 그 도시와 세대에 맞춤. 지어낸 브랜드는 이 중 어느 것도 아님
  (`copy.md`, names.json).
- **섹션 템플릿.** 모든 섹션에 아이브로우, 주장 제목, 짧은 리드, 카드 서넛. 인용 위의 "Kind words".
  나란한 기능에 단 단계 번호 [copy-numbered]. 각 섹션 제목 위에 놓은 작은 라벨 [copy-eyebrows]. 가운데 요금제의 "Most
  popular". 해결: 독자의 질문에서 모양을 정함(`copy-voice.md` 3절).
- **응답 시간 약속** [copy-response-time]. 사이트마다 "Within two working days". 해결: 브리프에서 가져온
  하나를, 반복되는 곳마다 같은 말로.
- **"Since [year]"** [copy-since]: 중요한 곳에 한 번, 브리프에서.
- **근거 수치** [copy-proof-figure]. "3x faster", "10,000+ teams", "98% satisfied". 둥글고, 깔끔하고, 출처가
  없습니다. 해결: 브리프가 주는 수치만, 단위와 함께 문장 안에.
- **완벽한 균일함.** 모든 카드가 같은 길이, 모든 문단이 같은 곡선 [copy-rhythm]. 해결: 브리프가 가장 잘
  아는 곳에 글을 씁니다. 한 섹션은 길 수 있고 한 섹션은 두 줄일 수 있습니다.
- **쓰지 않고 둔 마이크로카피.** 기성 폼 오류와 기성 감사 문구 위의 손으로 다듬은 히어로. 해결:
  어조에 맞춰 씁니다(`copy-moves.md`).
- **과정 이야기** [copy-reveal]. "This section shows", "Below, you'll find", "Here are 3 reasons",
  "We've added". 페이지는 자기 자신이나 만들어진 방식에 대해 이야기하지 않습니다.
- **오래된 연도** [copy-stale-year]. 올해보다 오래된 저작권 줄.

## 과잉 교정: 규칙 자체가 만드는 것

| 적용한 규칙 | 그것이 낳는 습관 | 대응 |
| --- | --- | --- |
| No em dashes | 쉼표 이어붙이기, 마침표만 사용 | 자연스러운 곳에 콜론, 괄호, 세미콜론 |
| No "not X but Y" | "rather than", "instead of", "without the" | 합쳐서 세고, 긍정적 사실을 말함 |
| No hype words | 차분한 어휘: quietly, steady, honest, practical | 어떤 형용사든 사실로 대체 |
| Avoid threes | 모든 것이 쌍 | 있는 만큼 나열 |
| Be specific | 지어낸 숫자와 일화 | 팩트 시트, 아니면 더 평이한 문장 |
| Short, punchy sentences | 조각들의 북소리 | 섹션마다 한 문장은 길어도 됨 |
| End strong | 모든 문단에 교훈이나 재담 | 정보로 끝맺음 |
| Add personality | 모든 섹션에 농담 | 유머 예산을 마이크로카피에 씀 |
| Vary section length | 모든 페이지에 거대한 섹션 하나와 아주 작은 섹션 하나 | 길이는 소재를 따름 |
| One rule pack on every page | 새로운 획일적 하우스 스타일 | 페이지 간 동질성 점검 |

## 티가 아닌 것(건드리지 않음)

완벽한 문법. 평이한 "is"와 "has". "In order to". 단독으로 쓴 전환어. 고객의 하우스 스타일일 때의 제목 대문자 표기. 사실일 때의
"no card needed" 하나. 브리프가 입증할 수 있는 좁은 최상급. 의도적으로 반복한 후렴. 셋이 있을 때의 세 항목 목록. 고객이 직접 쓴
문구(copy-lint가 그 문구의 단어를 FAIL로 처리하면, 게이트는 브리프를 이유로 그 한 건에 대해 면제를 받습니다: `gate.md`).
판매 페이지에서의 판매: 설득이 그 장르이며, 시험은 그것이 사실 위에 서 있는가입니다.
