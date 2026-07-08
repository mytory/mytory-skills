---
name: scaffold-exercises
description: 섹션, 문제, 해답, 설명이 포함된 연습문제 디렉터리 구조를 생성하고 린트를 통과하도록 합니다. "연습문제 뼈대 만들어줘", "코스 섹션 설정해줘", "연습문제 스텁 생성해줘", "강의 구조 잡아줘"라고 할 때 사용합니다.
---

# 연습문제 스캐폴딩

`pnpm ai-hero-cli internal lint`를 통과하는 연습문제 디렉터리 구조를 만든 후, `git commit`으로 커밋하세요.

## 디렉터리 네이밍

- **섹션**: `exercises/` 안에 `XX-section-name/` (예: `01-retrieval-skill-building`)
- **연습문제**: 섹션 안에 `XX.YY-exercise-name/` (예: `01.03-retrieval-with-bm25`)
- 섹션 번호 = `XX`, 연습문제 번호 = `XX.YY`
- 이름은 dash-case (소문자, 하이픈)

## 연습문제 변형

각 연습문제는 최소한 다음 하위 폴더 중 하나가 필요합니다:

- `problem/` - 학생 워크스페이스, TODO 포함
- `solution/` - 참조 구현
- `explainer/` - 개념 자료, TODO 없음

뼈대 생성 시, 계획에서 별도 지정이 없으면 기본값은 `explainer/`입니다.

## 필수 파일

각 하위 폴더(`problem/`, `solution/`, `explainer/`)에는 `readme.md`가 필요하며:

- **비어 있지 않아야** 함 (실제 내용이 있어야 하며, 제목 한 줄만 있어도 됨)
- 깨진 링크가 없어야 함

뼈대 생성 시, 제목과 설명이 있는 최소한의 readme를 만드세요:

```md
# 연습문제 제목

설명을 여기에 작성
```

하위 폴더에 코드가 있으면 `main.ts`(>1줄)도 필요합니다. 하지만 뼈대의 경우 readme만 있는 연습문제도 괜찮습니다.

## 작업 흐름

1. **계획 파싱** - 섹션명, 연습문제명, 변형 유형 추출
2. **디렉터리 생성** - 각 경로에 `mkdir -p`
3. **뼈대 readme 생성** - 변형 폴더마다 제목이 포함된 `readme.md` 하나씩
4. **린트 실행** - `pnpm ai-hero-cli internal lint`로 검증
5. **오류 수정** - 린트가 통과할 때까지 반복

## 린트 규칙 요약

린터(`pnpm ai-hero-cli internal lint`)가 확인하는 것:

- 각 연습문제에 하위 폴더(`problem/`, `solution/`, `explainer/`)가 있음
- `problem/`, `explainer/`, `explainer.1/` 중 최소 하나 존재
- 기본 하위 폴더에 `readme.md`가 있고 비어 있지 않음
- `.gitkeep` 파일 없음
- `speaker-notes.md` 파일 없음
- readme에 깨진 링크 없음
- readme에 `pnpm run exercise` 명령어 없음
- readme 전용이 아닌 경우 하위 폴더당 `main.ts` 필수

## 연습문제 이동/이름 변경

번호를 다시 매기거나 연습문제를 이동할 때:

1. `mv` 대신 `git mv`로 디렉터리 이름 변경 — git 히스토리 보존
2. 숫자 접두사를 업데이트하여 순서 유지
3. 이동 후 린트 재실행

예시:

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## 예시: 계획에서 뼈대 생성

다음과 같은 계획이 주어졌을 때:

```
Section 05: Memory Skill Building
- 05.01 Introduction to Memory
- 05.02 Short-term Memory (explainer + problem + solution)
- 05.03 Long-term Memory
```

생성:

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

그런 다음 readme 뼈대 생성:

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# Introduction to Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# Long-term Memory"
```
