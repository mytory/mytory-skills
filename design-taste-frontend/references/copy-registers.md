# 문구 어조

고를 수 있는 목소리이며, 언어 모델 이전(2014~2021)의 전문 사이트들이 쓴 방식에서 가져왔습니다. 고객마다 하나를 고르고, 두 번째
어조에서는 기법 하나만 빌립니다. 모든 예시 문장은 이 파일을 위해 가상의 고객을 상정해 쓴 것입니다. 어조는 부제, 본문, 이야기,
마이크로카피의 모양을 정할 뿐 `copy.md` 의 규칙(h1의 범주, 제목의 명사, 버튼의 동사)을 구부리지 않습니다.

**기본값은 없습니다.** 구매자, 가격, 고객의 실제 성격에 따라 고릅니다. 브리프로 정해지지 않으면 이번 세션에서 마지막으로 쓴
페이지와 가장 다른 어조를 택합니다.

## 0. 모델의 기본값(피해야 할 것)

따뜻하고, 익살스럽고, 겸손하고, 약간 문학적이며, 대기업에 살짝 반감이 있습니다. 문단은 무표정한 반전으로 끝나고, 진정성은
honest, calm, quiet, actually에서 나오며, 수치 띠, 다듬은 인용 셋, 푸터의 말장난이 따라붙습니다. 고객이 원할 때만 쓰고, 그때도
장치 예산 안에서 씁니다.

## 1. 사실만

- **들리는 모습:** "Kessler Partners advises family firms on succession. Founded 1994, nine partners,
  offices in Basel and Freiburg."
- **기법:** 이름, 날짜, 수치가 든 평이한 서술문. 3인칭이나 간결한 1인칭. 배타성은 형용사가 아니라 규칙이나 사실로
  보여 줍니다.
- **어울림:** 탄탄한 실적, 전문 서비스, B2B 인프라, 클럽, 컨설턴트.
- **실패하는 경우:** 사실이 약할 때. 그러면 속 빈 이력서처럼 읽힙니다.

## 2. 기술적이고 건조하며 근거가 있는 어조

- **들리는 모습:** "Every pull request gets its own database, seeded from last night's backup. Branch
  in 4 seconds; delete it on merge."
- **기법:** 라벨과 구체적 수치의 짝. 동사로 시작하는 단계로 쓴 메커니즘. 페이지에 실제 명령, UI 문자열, 파일 이름. 적은
  범주("most preview setups"). 전문가를 위해 일부러 남기거나 한 번 풀어 쓴 전문 용어. 문장의 주어로서의 제품.
- **어울림:** 개발자 도구, 인프라, API, 기술 소프트웨어.
- **실패하는 경우:** 불편은 이름 붙이지 않은 채 사양 나열로 흐르거나, 추상어("power and alignment")로 흐를 때.

## 3. 창업자의 편지

- **들리는 모습:** "We ran a print shop for eleven years and lost a day a week to quotes. So we built
  the quoting tool we wanted, and now 300 shops use it."
- **기법:** 1인칭. 이름 붙인 습관이나 범주를 적으로 삼음. 독자의 불편을 독자 자신의 말로. 일부러 쓰는 후렴. 섹션들을 가로질러
  이어지는 논지이며, 각 문단은 `copy.md` 의 길이 안에서. 본문 안의 평이하고 인간적인 맺음(푸터에는 안 둠).
- **어울림:** 입장이 있는 제품, 작은 소프트웨어 회사, 창업자가 이끌며 세상의 관행에 반대하는 모든 것.
- **실패하는 경우:** 입장이 꾸민 것이거나 창업자에게 실제 논지가 없을 때.

## 4. 자의식이 있고 장난스러운 어조

- **들리는 모습:** "Hot sauce from one farm in Kent. Medium is hot. Hot is a mistake you make once."
- **기법:** 작은 제품에 대해 정색하고 말함. 농담은 부제나 카드에 두고 그 바로 아래에 사실. 브리프가 주는 사내 용어.
  마이크로카피는 목소리를 다 실음. 실패를 드러냄. 과대 광고 단어는 농담으로도 쓰지 않습니다. copy-lint는 반어든 아니든
  FAIL로 처리합니다.
- **어울림:** 음료, 간식, 작은 소비재, 작은 스튜디오, 장난기 있는 앱.
- **실패하는 경우:** 농담이 뜬금없거나, 고객을 겨누거나, 진지한 구매(돈, 건강)에 얹힐 때.

## 5. 문학적이고 격식 있는 어조

- **들리는 모습:** "A balm for hands worn by cold water and rope. Citrus, cedar, a little smoke. 75 ml,
  34 euro."
- **기법:** 정확하고 약간 격조 있는 어휘. "customers"가 아니라 "clients". 촘촘한 목록으로 쓴 감각 노트. 재료와 식물은
  이름으로. 느낌표는 절대 쓰지 않음. 가격은 버튼에 평이하게.
- **어울림:** 스킨케어, 향수, 디자인 오브제, 고급 소매.
- **실패하는 경우:** 정확하지 않은 채 장식적이 될 때("a luxurious ritual of the senses").

## 6. 고유명사와 절제

- **들리는 모습:** "The old customs house above the harbour, built 1871. Eight rooms face the strait;
  the ferry to the island leaves below the terrace at 7:40."
- **기법:** 장소, 역사, 건물, 지리가 일을 함. 서두르지 않는 신체 동사(overlook, stroll, reside). 히어로에 가격 없음, 인용
  없음. 세 문장과 날짜 하나로 쓴 이야기. "luxury"라는 단어는 절대 나오지 않음.
- **어울림:** 럭셔리 호텔, 유서 깊은 저택, 건축 사무소, 갤러리.
- **실패하는 경우:** 브리프에 이름 붙일 실제 장소나 역사가 없을 때.

## 7. 감각적인 사실, 2인칭, 현재형

- **들리는 모습:** "You order at the counter beside the roaster. The cardamom buns come out at 8:00
  and again at 11:00."
- **기법:** 독자가 보고, 냄새 맡고, 듣고, 들게 될 것이며 각각 그 장소의 글자 그대로의 사실(오븐, 시각, 바닥, 무게). 공예는
  반복되는 단계와 제약으로 보여 줌. 규정하는 부재 하나("no mirrors in the studio"). 사람다운 고르지 않은 수. 은유나 분위기
  문단은 절대 안 됨. `copy.md` 의 하한이 유지됩니다.
- **어울림:** 카페, 음식, 바, 피트니스, 요가, 스파, 몸으로 소비하는 모든 것.
- **실패하는 경우:** 모든 섹션이 감각적으로 변할 때. 가격과 예약은 평이하게 둡니다.

## 8. 역사적 장면

- **들리는 모습:** "In 1958 the tram stopped outside, and the bakery opened at five for the drivers. It
  still does."
- **기법:** 브랜드가 아니라 날짜가 있는 순간으로 엶. 거리, 가구, 사람을 이름으로. 옛 사진은 증거로 쓰되 페이지에서
  캡션을 달지 않음(`copy.md`).
- **어울림:** 식당, 가족 기업, 브리프에 실제 계보가 있는 모든 것.
- **실패하는 경우:** 역사를 지어냈거나 평범할 때("rooted in tradition").

## 9. 꾸밈없이 말하는 활동가

- **들리는 모습:** "Every jacket we sell, we take back. In 2025 that was 3,140 jackets, and 2,200 went
  back on sale."
- **기법:** 측정 가능한 한 문장으로 쓴 사명. 어려운 주제를 평이하게 말함. 자기 쪽의 해악을 인정. 사명에 따라 움직이는
  버튼. 수치와 보고서로 하는 근거.
- **어울림:** 사명 중심의 소비자 브랜드, 비영리 단체, 브리프에 실제 영향 수치가 있는 기업.
- **실패하는 경우:** 사명이 추상 명사의 문단일 때("inspiring healthier communities").

## 10. 거절과 좁은 범위

- **들리는 모습:** "We repair bicycles. Not e-bikes, not scooters. Bicycles, in two days, at the bench
  you can see from the street."
- **기법:** 하지 않을 것으로 자리매김. 희소성은 솔직한 한계로 진술. 브리프가 이름을 주면 만든 사람을 이름으로. 공동체로서의
  의식.
- **어울림:** 장인, 소량 생산, 전문가, 단일 제품 회사.
- **실패하는 경우:** 거절을 집중하는 듯 들리려고 지어냈을 때. (페이지의 부정 연속 예산을 씁니다.)

## 11. 제품이 주인공

- **들리는 모습:** "The X2 runs 140 minutes on a charge and climbs a 2 cm sill. It maps the flat on the
  first run."
- **기법:** "we"는 거의 없음. 모든 문장의 주어는 제품. 말의 멋을 부린 뒤에는 곧바로 사양이 따라옴. 삶의 한 순간
  ("crumbs under the sofa at 22:00").
- **어울림:** 하드웨어, 물리적 제품, 강력한 기능 하나를 가진 앱.
- **실패하는 경우:** 말장난 아래에 사실이 없을 때.

## 12. 서두르는 대화체

- **들리는 모습:** "Packaging for small food brands, by three people in one studio in Bristol (the one
  who answers the phone also draws the box)."
- **기법:** 바쁜 한 사람에게 말함. 괄호 안의 곁말. 자기 비하. 그래도 사물을 이름 붙이는 격의 없는 섹션 라벨. 떠나도 좋다는
  허락.
- **어울림:** 작은 스튜디오, 프리랜서, 포트폴리오, 창업자가 있는 D2C 브랜드.
- **실패하는 경우:** 허물없어질 때("We get it.") 또는 농담이 정보를 대신할 때.

## 업종에 목소리 맞추기(출발점일 뿐)

| 업종 | 먼저 시도 | 피할 것 |
| --- | --- | --- |
| 카페, 로스터리, 빵집 | 7 감각, 8 역사 장면, 4 장난기 | 0 기본값 |
| 개발자 도구, 인프라 | 2 기술적·건조, 3 창업자의 편지 | 히어로의 4 장난기 |
| 소기업용 소프트웨어 | 3 창업자의 편지, 11 제품이 주인공 | 추상어 "power and alignment" |
| AI 제품 | 2 기술적·건조, 11 제품이 주인공 | "magic", "superpowers" |
| 에이전시, 스튜디오 | 1 사실만, 12 서두름, 4 장난기 | 범주 명사 쌓기("digital brand experience company") |
| 포트폴리오 | 12 서두름, 1 사실만 | 사람이 없는 작업 목록 |
| 럭셔리 호텔 | 6 절제 | "luxury"라는 단어 |
| 게스트하우스, 소형 호텔 | 12 서두름, 7 감각, 6 절제 | "boutique", "curated experiences" |
| 피트니스, 요가 | 7 감각, 10 거절 | "the best version of yourself" |
| 건축 | 6 절제, 1 사실만 | "spaces that inspire" |
| 강좌, 교육 | 3 교사의 편지, 신체 기술이면 7 감각 | "transform your life" |
| 스킨케어, 뷰티 | 5 문학적, 10 거절 | 성분 없는 "clean", "glow" |
| 금융 | 1 사실만, 3 창업자의 편지 | 돈 걱정에 대한 농담, 출처 없는 절감액 |
| 하드웨어, 가전 | 11 제품이 주인공, 2 기술적·건조 | 사양이 들어갈 자리의 형용사 |
| 게임 | 게임 자체의 세계와 어조, 스튜디오는 12 | 스토어 페이지의 기본 어조 |
| 음료, 간식 | 4 장난기, 9 활동가 | 0 기본값 |
| 수리점, 기술직 | 10 거절, 1 사실만 | "passion", "quality you can trust" |
| 웨딩, 행사, 사진 | 7 감각, 12 서두름 | "capturing your special day" |
