# 도메인 문서

엔지니어링 스킬이 코드베이스를 탐색할 때 이 저장소의 도메인 문서를 읽는 방법입니다.

## 탐색 전에 읽을 문서

- 저장소 루트의 **`GLOSSARY.md`**, 또는
- 루트에 **`GLOSSARY-MAP.md`**가 있으면 이를 읽으세요. 컨텍스트별 `GLOSSARY.md`를 가리킵니다. 주제와 관련된 용어집을 각각 읽으세요.
- **`docs/adr/`**: 작업할 영역에 관한 ADR을 읽으세요. 다중 컨텍스트 저장소에서는 `src/<context>/docs/adr/`의 결정도 확인하세요.

파일이 없으면 **조용히 진행하세요**. 없다는 점을 지적하거나 미리 만들자고 제안하지 마세요. `/domain-modeling` 스킬(`/grill-with-docs`와 `/improve-codebase-architecture`를 통해 접근)은 용어나 결정이 실제로 확정될 때 해당 파일을 만듭니다.

## 파일 구조

단일 컨텍스트 저장소 (대부분):

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

다중 컨텍스트 저장소 (루트에 `GLOSSARY-MAP.md`가 있음):

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← 시스템 전체에 관한 결정
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← 컨텍스트별 결정
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## 용어집의 어휘 사용

이슈 제목, 리팩터링 제안, 가설, 테스트 이름 등에서 도메인 개념을 언급할 때는 `GLOSSARY.md`에 정의된 용어를 사용하세요. 용어집에서 명시적으로 피하는 동의어로 바꾸지 마세요.

필요한 개념이 용어집에 없다면 프로젝트에서 쓰지 않는 표현을 만들었을 수도 있으니 재고하세요. 실제로 빠진 개념이라면 `/domain-modeling`을 위해 기록하세요.

## ADR과의 충돌 표시

결과물이 기존 ADR과 충돌한다면 조용히 덮어쓰지 말고 명시적으로 알리세요.

> _ADR-0007(이벤트 소싱 주문)과 충돌하지만, … 때문에 결정을 다시 검토할 만합니다._
