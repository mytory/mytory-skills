# 스킬 최신화 최근 수행

- 마지막 처리일: 2026-10-19
- 결과: 외부 출처 8곳(이동한 imagegen-skills 포함)을 확인했습니다. design-taste-frontend를 tasteskill v2로 갱신하고 한국어 본문·참고 문서 11개와 스크립트·자산·라이브러리·라이선스를 반영했습니다. image-to-code는 새 원본으로 출처를 옮기고 MIT 라이선스를 추가했습니다. 이동 전후 본문은 동일해 기존 번역을 유지했습니다. 다른 스킬 본문과 원본에서 사라진 기존 스킬은 보존했습니다. README 출처·설치 예시를 정리했습니다.
- 로컬 조정: 원본에 없는 장면 카탈로그·구현·데모의 기능 제한을 명시했습니다. 평가 예시의 이메일 3개는 예약 도메인 `.example`로 변경했습니다.
- 검증: 스킬 37개와 README 목록 37개 일치, YAML 53개 파싱, JavaScript 12개와 Python 구문 검사, JSON 10개 파싱, 페이지·앱 방향 생성 및 후보 생성, 코드 예제 보존, 상대 링크와 git diff --check 확인. 실제 브라우저의 렌더링·외부 이미지 검색은 실행하지 않았습니다.
- 공개 파일 점검: 추적 파일과 새 지원 파일에서 인증 정보·개인 홈 경로·내부 주소 후보를 검색했습니다. 검사 스크립트의 임시 로컬 서버 주소는 정상 용도로 확인했습니다. 기존 Git 작성자 설정·이력은 수정하지 않았습니다.

## 확인한 원본 기준

| 원본 | 커밋 |
| --- | --- |
| mattpocock/skills | `49dd158d1076134a641b33efb035946536778336` |
| leonxlnx/taste-skill | `b9ca2fd8047f4c72d7da90ebc1c1203e57c72cd2` |
| Leonxlnx/imagegen-skills | `beb16b0d0f4dae9a6f5cb04ea41e97b93a54ab8e` |
| vercel-labs/agent-browser | `dac13bb87468fe9d74a040d862720f6cc17a9565` |
| anthropics/skills | `dbd4588f9e1033efb41dad4bef2f7947c8993d44` |
| ctxrs/ctx | `56aaf35233ce7f8aa739c207525a3d67e6ddddbd` |
| alibaba/open-code-review | `27def8684b3f5c5f235871fac2957be58262f43d` |
| deusyu/translate-book | `a663b1b4f1e625b286cd2a81dffd16571e6f2aa2` |
