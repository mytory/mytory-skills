# 스킬 최신화 최근 수행

- 마지막 처리일: 2026-11-10
- 결과: 성공. 외부 출처 9곳을 확인했고 4곳에서 스킬 경로가 바뀌어 반영했습니다. design-taste-frontend를 tasteskill 2.5.1로 갱신했습니다. 스크립트·에셋(약 39MB)·라이브러리·라이선스를 원본대로 교체하고, SKILL.md와 참고 문서 22개, 에셋 README 5개를 한국어로 번역했습니다. mattpocock 스킬 5개(code-review, codebase-design, improve-codebase-architecture, grilling, setup-matt-pocock-skills)와 agent-browser에는 바뀐 문장만 반영했습니다. translate-long-text에는 원본의 Markdown 입력·각주 검증·페이지 번호 옵션·빌드 후 부분 수정 단계를 합쳤습니다. frontend-design, ctx-agent-history-search, open-code-review, image-to-code, web-design-guidelines는 스킬 경로에 변경이 없었습니다. README 출처 커밋을 갱신했습니다.
- 원본에서 빠진 기능: tasteskill 2.5.0부터 앱 화면(대시보드·관리 화면) 경로, 방향 추첨(`draw.mjs`), v2 평가 예시(`evals/`)가 없어져 함께 제거했습니다. 새 SKILL.md frontmatter에는 마무리 게이트를 실행하는 Claude Code `Stop` 훅이 들어 있습니다.
- 로컬 조정: 에셋 예시 이메일 `northwind.co` 3곳을 예약 도메인 `.example`로 바꿨습니다. translate-long-text의 TXT 처리 확장은 보존했습니다. 원본의 `assets/poster/style.md`와 `tests/`는 가져오지 않았습니다.
- 검증: 스킬 53개 frontmatter 파싱과 name·폴더명 일치, README 목록 38개와 총계 일치, design-taste-frontend JavaScript 153개 `node --check`, 번역 문서별 원문 대비 코드 블록·제목·표 행 수 일치, 상대 링크, `git diff --check`를 확인했습니다. translate-long-text는 원본 테스트 287개 중 284개 통과, 3개 건너뜀, 실패 0개였고 TXT 스모크 테스트도 통과했습니다. 실제 브라우저에서 tasteskill 검사기·게이트는 실행하지 않았습니다.
- 공개 파일 점검: 변경 파일에서 인증 정보·개인 홈 경로·사설 주소·실제 도메인 이메일 후보를 검색했고 해당 없음을 확인했습니다. 파일 내용과 별개로 Git 작성자 메타데이터는 기존 설정을 그대로 썼고 수정하지 않았습니다.

## 확인한 원본 기준

| 원본 | 커밋 |
| --- | --- |
| mattpocock/skills | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` |
| leonxlnx/taste-skill | `f6b76575f949707b4e3c37cd86cb44b0b98643e8` |
| Leonxlnx/imagegen-skills | `beb16b0d0f4dae9a6f5cb04ea41e97b93a54ab8e` |
| vercel-labs/agent-browser | `edc992b1a3ded1433558c8931d5d5f484ae89846` |
| vercel-labs/agent-skills | `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` |
| anthropics/skills | `2c5958ecac7cee2b583967a2c4981d0f4a75c579` |
| ctxrs/ctx | `33ba4645b620fd89d138c6db1fabf33096a0ee16` |
| alibaba/open-code-review | `04deca6721ec4fe2f74a6a0eb069d2a01b3d31cb` |
| deusyu/translate-book | `cf3862d46e79dc89abe3de13f3839039f1d8a637` |
