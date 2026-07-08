---
name: find-skills
description: 사용자가 "X 어떻게 해", "X 관련 스킬 찾아줘", "이런 기능 가능해?", "스킬 설치하고 싶어" 같은 질문을 할 때 에이전트 스킬을 검색하고 설치할 수 있도록 도와줍니다. 설치 가능한 스킬 형태로 존재할 수 있는 기능을 사용자가 찾고 있을 때 사용합니다.
---

# 스킬 찾기

이 스킬은 오픈 에이전트 스킬 생태계에서 스킬을 검색하고 설치할 수 있도록 도와줍니다.

## 언제 이 스킬을 사용하나요

다음과 같은 경우에 사용하세요:

- 사용자가 "X 어떻게 해"라고 물었는데 X에 기존 스킬이 있을 수 있는 경우
- "X 관련 스킬 찾아줘" 또는 "X 할 수 있는 스킬 있어?"라고 말하는 경우
- "너 X 할 수 있어?"라고 물었는데 X가 특화된 기능인 경우
- 에이전트 기능 확장에 관심을 보이는 경우
- 도구, 템플릿, 워크플로우를 검색하고 싶어 하는 경우
- 특정 도메인(디자인, 테스트, 배포 등)에 도움이 필요하다고 말하는 경우

## Skills CLI란?

Skills CLI(`npx skills`)는 오픈 에이전트 스킬 생태계의 패키지 관리자입니다. 스킬은 특화된 지식, 워크플로우, 도구로 에이전트 기능을 확장하는 모듈형 패키지입니다.

**주요 명령어:**

- `npx skills find [검색어]` - 대화형 또는 키워드로 스킬 검색
- `npx skills add <패키지>` - GitHub 등에서 스킬 설치
- `npx skills check` - 스킬 업데이트 확인
- `npx skills update` - 설치된 모든 스킬 업데이트

**스킬 둘러보기:** https://skills.sh/

## 사용자의 스킬 검색을 돕는 방법

### 1단계: 필요한 것 이해하기

사용자가 도움을 요청할 때 파악하세요:

1. 도메인 (예: React, 테스트, 디자인, 배포)
2. 구체적 작업 (예: 테스트 작성, 애니메이션 생성, PR 리뷰)
3. 스킬이 존재할 만큼 흔한 작업인지

### 2단계: 리더보드 먼저 확인

CLI 검색을 실행하기 전에 [skills.sh 리더보드](https://skills.sh/)를 확인하여 해당 도메인에 잘 알려진 스킬이 있는지 보세요. 리더보드는 총 설치 수로 스킬 순위를 매겨 가장 인기 있고 검증된 옵션을 보여줍니다.

예를 들어, 웹 개발 관련 최상위 스킬:
- `vercel-labs/agent-skills` — React, Next.js, 웹 디자인 (각 10만+ 설치)
- `anthropics/skills` — 프론트엔드 디자인, 문서 처리 (10만+ 설치)

### 3단계: 스킬 검색

리더보드에 사용자 요구를 충족하는 항목이 없으면 find 명령어 실행:

```bash
npx skills find [검색어]
```

예시:

- "React 앱을 더 빠르게 만드는 방법?" → `npx skills find react performance`
- "PR 리뷰 도와줄 수 있어?" → `npx skills find pr review`
- "체인지로그 만들어야 해" → `npx skills find changelog`

### 4단계: 추천 전 품질 검증

**검색 결과만으로 스킬을 추천하지 마세요.** 항상 다음을 검증하세요:

1. **설치 수** — 1K+ 설치 스킬을 선호. 100 미만은 주의.
2. **출처 평판** — 공식 출처(`vercel-labs`, `anthropics`, `microsoft`)가 무명 저자보다 신뢰할 수 있음.
3. **GitHub 스타** — 소스 저장소 확인. 100 스타 미만 저장소의 스킬은 의심.

### 5단계: 사용자에게 옵션 제시

관련 스킬을 찾으면 사용자에게 제시하세요:

1. 스킬명과 하는 일
2. 설치 수와 출처
3. 실행할 수 있는 설치 명령어
4. skills.sh에서 자세히 알아볼 수 있는 링크

예시 응답:

```
도움이 될 만한 스킬을 찾았어요! "react-best-practices" 스킬은
Vercel Engineering의 React 및 Next.js 성능 최적화 가이드라인을 제공합니다.
(18.5만 설치)

설치하려면:
npx skills add vercel-labs/agent-skills@react-best-practices

자세히 보기: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### 6단계: 설치 제안

사용자가 진행을 원하면 스킬을 대신 설치할 수 있습니다:

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 플래그는 전역(사용자 수준) 설치, `-y`는 확인 프롬프트 건너뛰기.

## 일반적인 스킬 카테고리

검색 시 고려할 일반 카테고리:

| 카테고리     | 예시 검색어                                |
| ------------ | ------------------------------------------ |
| 웹 개발      | react, nextjs, typescript, css, tailwind  |
| 테스트       | testing, jest, playwright, e2e            |
| 데브옵스     | deploy, docker, kubernetes, ci-cd         |
| 문서화       | docs, readme, changelog, api-docs         |
| 코드 품질    | review, lint, refactor, best-practices    |
| 디자인       | ui, ux, design-system, accessibility      |
| 생산성       | workflow, automation, git                 |

## 효과적인 검색 팁

1. **구체적 키워드 사용**: "testing"보다 "react testing"이 더 좋음
2. **대체 용어 시도**: "deploy"가 안 되면 "deployment"나 "ci-cd" 시도
3. **인기 출처 확인**: 많은 스킬이 `vercel-labs/agent-skills`나 `ComposioHQ/awesome-claude-skills`에서 나옴

## 관련 스킬이 없을 때

관련 스킬이 없으면:

1. 기존 스킬을 찾지 못했음을 인정
2. 일반 기능으로 직접 도움을 제공하겠다고 제안
3. `npx skills init`으로 자신만의 스킬을 만들 수 있다고 제안

예시:

```
"xyz" 관련 스킬을 검색했지만 일치하는 항목을 찾지 못했어요.
그래도 직접 도와드릴 수 있어요! 진행할까요?

자주 하는 작업이라면 직접 스킬을 만들 수도 있어요:
npx skills init my-xyz-skill
```
