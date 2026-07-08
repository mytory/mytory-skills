---
name: open-code-review
description: >
  `ocr` CLI(alibaba/open-code-review)를 사용하여 Git 변경사항에 대해 AI 기반 코드
  리뷰를 수행합니다. 사용자가 코드 리뷰, 풀 리퀘스트 리뷰, 스테이징/언스테이징 변경사항
  리뷰, 특정 커밋 리뷰, 또는 브랜치 간 비교를 요청할 때 사용합니다. 라인 단위 리뷰
  코멘트를 생성하고 요청 시 자동 수정을 적용할 수 있습니다. 적절한 리뷰 규칙과 함께
  버그, 보안 취약점, 성능 문제, 코드 품질 우려 등 다양한 유형의 이슈를 탐지할 수 있습니다.
license: Apache-2.0
compatibility: >
  `ocr` CLI 설치 필요(`npm install -g @alibaba-group/open-code-review` 또는 GitHub
  릴리스 바이너리). 첫 실행 전에 LLM(Anthropic 또는 OpenAI 호환) 설정이 필요합니다.
metadata:
  author: alibaba
  homepage: https://github.com/alibaba/open-code-review
  version: "1.0.0"
---

# Open Code Review

[open-code-review](https://github.com/alibaba/open-code-review)(`ocr`)를 호출하는 스킬입니다.
오픈소스 AI 코드 리뷰 CLI로, Git diff를 읽고 구조화된 라인 단위 리뷰 코멘트를 생성합니다.

## 사전 준비 확인

리뷰를 시작하기 전에 환경을 확인하세요:

```bash
# 1. CLI 설치 확인
which ocr || echo "설치되지 않음"

# 2. LLM 연결 확인
ocr llm test
```

`ocr`이 설치되지 않았다면 먼저 설치합니다:

```bash
npm install -g @alibaba-group/open-code-review
```

`ocr llm test`가 실패하면 사용자가 LLM을 설정해야 합니다. 다음 옵션 중 하나를 안내하세요:

**옵션 A — 환경 변수 (최우선 순위, CI에 권장):**

```bash
export OCR_LLM_URL=https://api.anthropic.com/v1/messages
export OCR_LLM_TOKEN=<api-key>
export OCR_LLM_MODEL=claude-opus-4-6
export OCR_USE_ANTHROPIC=true
```

**옵션 B — 영구 설정:**

```bash
ocr config set llm.url https://api.anthropic.com/v1/messages
ocr config set llm.auth_token <api-key>
ocr config set llm.model claude-opus-4-6
ocr config set llm.use_anthropic true
```

여기서 멈추고 사용자에게 자격 증명을 입력하도록 요청하세요. 절대 API 키를 임의로 생성하거나 하드코딩하지 마세요.

## 워크플로우

### 1단계: 비즈니스 컨텍스트 수집

리뷰 대상(커밋, 브랜치 또는 변경사항)을 분석하여 간결한 비즈니스 컨텍스트를 추출합니다.
이 컨텍스트를 `--background`로 전달하면 리뷰 품질이 향상됩니다.

### 2단계: 코드 리뷰 실행

적절한 플래그와 함께 OCR 명령을 실행합니다. **가능하면 항상 `--background`로 비즈니스 컨텍스트를 전달**하세요:

```bash
ocr review --audience agent --background "비즈니스 컨텍스트" [사용자-인자]
```

**인자 처리:**

- **배경 컨텍스트** (권장): `--background "컨텍스트"` 또는 `-b "컨텍스트"`로 비즈니스 컨텍스트 제공
- **기본값** (사용자 인자 없음): 스테이징, 언스테이징, 추적되지 않은 변경사항 모두 리뷰 (워크스페이스 모드)
- **특정 커밋**: `--commit` 또는 `-c`로 특정 커밋을 부모와 비교하여 리뷰
- **브랜치 비교**: `--from <ref>`와 `--to <ref>`로 두 ref 간 diff 리뷰
- **타임아웃**: 기본 타임아웃은 파일당 10분; `--timeout <분>`으로 조정
- **동시성**: 기본 동시성은 8개 파일 워커; rate limit에 걸리면 `--concurrency <n>`으로 감소
- **미리보기 모드**: `--preview` 또는 `-p`로 LLM 실행 없이 리뷰할 파일 목록 미리보기
- **설치**: `ocr` 명령어를 찾을 수 없으면 `npm i -g @alibaba-group/open-code-review`로 설치

**자주 사용되는 호출 패턴:**

| 사용자 요청 | 실행할 명령어 |
|------------|--------------|
| "내 변경사항 리뷰해줘" / "작업 중인 코드 리뷰" | `ocr review --audience agent -b "컨텍스트"` |
| "이 PR 리뷰해줘" / "feature 브랜치 리뷰" | `ocr review --audience agent -b "컨텍스트" --from main --to <브랜치>` |
| "커밋 abc123 리뷰해줘" | `ocr review --audience agent -b "컨텍스트" --commit abc123` |
| "뭐가 리뷰될지 미리보기" (dry-run) | `ocr review --preview` |

**출력 모드:**

- 항상 `--audience agent`를 사용하여 진행 UI를 숨기고 최종 요약만 출력

### 3단계: 분류 및 보고

리뷰 출력의 각 코멘트를 우선순위별로 분류하여 모든 이슈를 사용자에게 보고합니다:

- **높음(High)**: 명백한 버그, 보안 이슈, 확실한 실수, 또는 정확한 수정 제안이 있는 근거 있는 제안
- **중간(Medium)**: 합리적인 우려사항이지만 컨텍스트에 따라 다름, 스타일/성능 제안, 또는 수동 구현이 필요한 수정사항
- **낮음(Low)**: 오탐 가능성 높음, 컨텍스트 부족, 사소한 지적, 또는 의미 없는 제안

모든 코멘트를 우선순위 레벨별로 그룹화하여 보고합니다.

### 4단계: 수정

수정을 적용하기 전에 사용자가 자동 수정을 요청했는지 확인하세요:

- 사용자가 명시적으로 "리뷰하고 수정해줘" 등으로 요청한 경우 자동 수정 진행
- 사용자가 수정 의도 없이 "리뷰"만 요청한 경우 변경 적용 전에 허가 요청

이슈 및 제안 수정 시:

- 높음(High) 및 중간(Medium) 우선순위 항목에 집중
- 안전하고 명확하게 정의된 경우 코드에 직접 수정 적용
- 수동 개입이 필요한 복잡한 수정사항은 수행할 작업을 명확히 설명
- 항상 사용자에게 수정사항을 확인한 후 커밋

## 출력 형식

각 코멘트는 다음을 포함합니다:

- `path`: 파일 경로
- `content`: 리뷰 코멘트 텍스트
- `start_line` / `end_line`: 라인 범위 (둘 다 0이면 위치 찾기 실패)
- `suggestion_code`: 선택적 수정 제안 코드
- `existing_code`: 선택적 원본 코드 스니펫
- `thinking`: 선택적 LLM 추론 과정

코멘트를 우선순위별로 필터링한 후, 다음 템플릿을 사용하여 결과를 표시합니다:

```markdown
## 코드 리뷰 결과

**리뷰한 파일**: N개
**발견된 이슈**: 높음 X개 / 중간 Y개

### 높음 우선순위

- **`path/to/file.java:42`** — 간단한 설명
  > 권장사항: 수정 방법

### 중간 우선순위

- **`path/to/file.ts:88`** — 간단한 설명
  > 권장사항: 수정 방법 (해당 시)
```

필터링 후 이슈가 없으면 다음과 같이 표시합니다: "리뷰 완료 — N개 파일에서 이슈 없음."

**우선순위 분류 기준:**

- **높음(High)**: 명백한 버그, 보안 이슈, 확실한 실수, 또는 정확한 수정 제안이 있는 근거 있는 제안
- **중간(Medium)**: 합리적인 우려사항이지만 컨텍스트에 따라 다름, 스타일/성능 제안, 또는 수동 구현이 필요한 수정사항
- **낮음(Low)**: 자동 폐기 (오탐 가능성, 컨텍스트 부족, 사소한 지적, 의미 없는 제안)

**위치 미지정 코멘트 처리:**

`start_line`과 `end_line`이 모두 `0`이면 파일 내 정확한 위치를 찾지 못한 것입니다.
이 경우:

1. 코멘트 내용을 읽어 이슈 파악
2. 코멘트에 언급된 대상 파일 검토
3. 코멘트 컨텍스트를 기반으로 관련 코드 섹션 식별
4. 올바른 위치에 수정 또는 제안 적용

## 사용자 정의 리뷰 규칙

프로젝트별 규칙이 필요한 경우, OCR은 다음 우선순위로 규칙을 적용합니다:

1. `--rule <path>` 플래그 (최우선)
2. `<repo>/.opencodereview/rule.json`
3. `~/.opencodereview/rule.json`
4. 내장 시스템 기본값 (최하위)

기본적으로 첫 번째로 일치하는 사용자 규칙이 내장 시스템 규칙을 대체합니다.
규칙 항목에 `merge_system_rule: true`를 설정하면 일치하는 시스템 규칙과 사용자 규칙이 모두 포함됩니다.

규칙 파일 형식:

```json
{
  "rules": [
    {
      "path": "**/*.java",
      "rule": "모든 새 메서드는 필수 파라미터에 대해 null 검증을 수행해야 합니다",
      "merge_system_rule": true
    },
    {
      "path": "**/*mapper*.xml",
      "rule": "SQL 인젝션 위험 및 누락된 닫는 태그 확인"
    }
  ]
}
```

리뷰 전에 파일에 적용되는 규칙을 미리 확인하려면:

```bash
ocr rules check src/main/java/com/example/Foo.java
```

## 주의사항

- **LLM을 먼저 설정해야 함** — `ocr review`는 연결 가능한 LLM이 없으면 오류와 함께 실패합니다. 첫 리뷰 전에 항상 `ocr llm test`를 실행하세요.
- **작업 디렉토리가 중요** — `ocr review`는 현재 디렉토리의 Git 저장소에서 작동합니다. 다른 위치에서 실행하려면 `--repo /path/to/repo`를 사용하세요.
- **워크스페이스 모드에서 추적되지 않은 파일도 리뷰** — 기본 `ocr review`는 스테이징, 언스테이징, *그리고* 추적되지 않은 변경사항을 모두 포함합니다. 범위를 좁히려면 선택적으로 스테이징하세요.
- **큰 diff는 토큰 제한에 걸릴 수 있음** — 매우 큰 diff가 있는 파일은 잘릴 수 있습니다. 기본 `MAX_TOKENS`는 요청당 58888입니다.
- **50라인에서 계획 단계(plan phase) 트리거** — 50라인을 초과하는 변경 라인 수의 diff는 본 리뷰 전에 추가 위험 분석 단계를 실행합니다. 지연 시간이 추가되지만 품질이 향상됩니다.
- **`--audience human`을 사용하지 마세요** — 진행 UI가 스트리밍되어 출력을 오염시킵니다. 항상 `--audience agent`를 사용하세요.
- **코멘트 언어는 설정을 따름** — `language` 설정을 `English` 또는 `Chinese`(기본값: Chinese)로 설정하여 리뷰 코멘트 언어를 제어합니다.

## 검증

리뷰 완료 후 성공 여부를 다음으로 확인하세요:

1. 명령어가 종료 코드 0으로 종료되었는지
2. 코멘트가 생성되었는지 (또는 "No comments generated" 메시지가 표시되는지)
3. 경고(있는 경우)가 stderr에 표시되는지

오류가 발생한 경우, stderr 경고에서 어떤 파일이 실패했는지와 그 이유를 확인하세요.

## 참고 자료

- 전체 문서: https://github.com/alibaba/open-code-review
- NPM 패키지: https://www.npmjs.com/package/@alibaba-group/open-code-review
- 이슈 트래커: https://github.com/alibaba/open-code-review/issues
