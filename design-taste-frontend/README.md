# tasteskill v2 (`design-taste-frontend`)

2026년 10월 One Page Love와 Awwwards Sites of the Day의 선정 사이트 247개를 조사해 만든 코딩 에이전트용 디자인 스킬입니다. 평균적인 랜딩페이지 대신 아트 디렉션을 제공하고 장식 없는 공통 스타일을 검사하며, 완료 전에 렌더링 결과를 직접 보게 합니다.

## 작동 방식

1. **고유 요소 목록.** 이름과 뜻, 거리, 수치, 제약, 재료, 영업시간처럼 이 고객만 가진 것을 적습니다.
2. **추첨.** `scripts/draw.mjs`가 우수 사이트에서 찾은 아이디어 장치 20개 중 방향 3개를 제시합니다. 목록의 특징을 담을 방향을 고르면 히어로·섹션 구도, 실제 무료 서체, 팔레트, 사진, 모션, 참고 사이트, 각 설계와 공통 규칙의 충돌을 받습니다. 최근 추첨을 기억해 프로젝트 사이의 반복을 줄입니다.
3. **아이디어와 살아 있는 요소.** 고객의 재료를 방향의 장치와 연결하는 문장을 쓰고 가까운 경쟁사에 대입해 검사합니다. 방문자가 할 수 있는 행동 하나를 만듭니다.
4. **구현.** 시트에 따라 문구부터 충분한 콘텐츠로 만듭니다. 자체 사진이 없으면 `scripts/assets.mjs`로 공개 컬렉션에서 거리의 옛 엽서·지도·재료·업종 판화·박물관 물체를 찾아 다운로드하고 출처를 기록합니다. 정직한 사진이 없을 때만 코드로 그립니다.
5. **관문.** `scripts/lint.mjs`로 소스를, `scripts/inspect.mjs`로 실제 브라우저의 1440·768·390px 화면을 검사합니다. 두 줄 제목, 작은 상단 라벨·고정폭·장식 번호·가는 선·그라디언트·정지 그림자·크림+테라코타·보라 금지와 함께 초점 없음·빈 화면·가린 글·긴 고정 구간·가로 행·옅은 글자를 측정합니다.
6. **보기.** 저장된 스크린샷을 Awwwards 가중 평가표로 평가하고 큰 문제 3개를 수정합니다. 최대 3회 반복합니다.

스킬 없는 기준과 다른 디자인 스킬을 비교한 블라인드 테스트 5회의 기록은 `references/research.md` §11에 있습니다.

## 구성

| 경로 | 역할 |
| --- | --- |
| `SKILL.md` | 실행 절차·공통 규칙·제작 원칙 |
| `references/` | 문구·서체·색·레이아웃·이미지·모션·평가·상투적 특징·조사 |
| `scripts/draw.mjs` | 후보·방향 추첨, 재출력·재추첨, `--alternatives`, `--photos`, `--site` |
| `scripts/assets.mjs` | 공개 이미지 검색(Openverse, Wikimedia Commons, Art Institute of Chicago, Met), `--video` 영상 검색(Wikimedia Commons, Internet Archive, NASA), `--get` 출처 포함 다운로드, `--credits` 출처 출력 |
| `scripts/lint.mjs` | 금지 패턴·상투적인 문구의 정적 검사 |
| `scripts/inspect.mjs` | 렌더링·측정·촬영 |
| `scripts/lib/` | 의존성 없는 Chrome DevTools 클라이언트·페이지 프로브·규칙 |
| `library/` | 방향 20개·히어로·섹션·서체·팔레트·사진·조사 사이트·모션 |
| `assets/base.css`, `assets/base.js` | 선택 가능한 중립 기반 |
| `evals/evals.json` | 스킬 없는 기준과 비교할 브리프 6개 |

## 요구 사항

`inspect.mjs`에는 Node 22+와 Chrome·Edge·Chromium이 필요합니다. Node 내장 WebSocket으로 DevTools 프로토콜을 사용하며 패키지를 설치하지 않습니다. `draw.mjs`, `lint.mjs`, `assets.mjs`는 Node 18+에서 실행됩니다. `assets.mjs`에는 네트워크가 필요하고 API 키는 필요하지 않습니다. 브라우저가 일반적인 위치에 없으면 `CHROME_PATH`를 지정하세요.

## 설치

이 폴더를 `~/.claude/skills/design-taste-frontend/` 같은 스킬 디렉터리나 저장소의 `.claude/skills/` 아래에 복사합니다.

## 참고

- 라이브러리 사진은 Unsplash 라이선스의 Unsplash 자료를 Lorem Picsum으로 제공합니다. 분위기를 위한 임시 사진이므로 프로젝트 자체 사진으로 교체하세요.
- `assets.mjs`로 찾은 사진에는 각자의 라이선스가 적용됩니다. 기본적으로 CC0·퍼블릭 도메인·CC BY·CC BY-SA만 제공하며 `--get`은 제목·제작자·라이선스·출처를 `assets/credits.json`에 기록합니다. 페이지에도 출처를 표시하세요(`--credits`).
- `assets.mjs --video`는 대상 세계의 짧은 영상을 찾아 720p 이하 버전을 받습니다. `--max-mb`가 없으면 25MB 초과 파일은 거부하고 각 영상에 포스터 프레임을 저장합니다. 무음 반복·포스터·모션 축소 시 정지는 `references/imagery.md` §11을 따릅니다.
- 서체는 Google Fonts와 Fontshare에서 로드합니다. 용도에 맞는 개별 라이선스를 확인하세요.
- `references/research.md`의 점수는 스크린샷에 대한 모델 평가이며 Awwwards의 점수가 아닙니다.
- 추첨 기록은 `~/.taste-skill/history.json`에 저장됩니다. `TASTE_SKILL_HISTORY`로 바꾸고 파일을 삭제해 초기화할 수 있습니다.
- 전체 보기·수정 과정을 포함하면 에이전트 작업은 약 30–45분, 수십만 토큰이 들 수 있습니다. 자체 사진이 없는 프로젝트에서는 이미지 검색·그리기가 대부분을 차지합니다.
