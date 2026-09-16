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
  릴리스 바이너리). 첫 실행 전에 지원되는 LLM 제공자 설정이 필요합니다
  (프로토콜: Anthropic, OpenAI Chat Completions, OpenAI Responses, AWS Bedrock).
metadata:
  author: alibaba
  homepage: https://github.com/alibaba/open-code-review
  version: "1.0.0"
---

# Open Code Review

[open-code-review](https://github.com/alibaba/open-code-review)(`ocr`)를 호출하는 스킬입니다.
오픈소스 AI 코드 리뷰 CLI로, Git diff를 읽고 구조화된 라인 단위 리뷰 코멘트를 생성합니다.

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

- **배경 컨텍스트** (권장): `--background "컨텍스트"` 또는 `-b "컨텍스트"`로 비즈니스 컨텍스트를 제공하여 리뷰 품질 향상
- **기본값** (사용자 인자 없음): 스테이징, 언스테이징, 추적되지 않은 변경사항 모두 리뷰 (워크스페이스 모드)
- **특정 커밋**: `--commit` 또는 `-c`로 특정 커밋을 부모와 비교하여 리뷰
- **브랜치 비교**: `--from <ref>`와 `--to <ref>`로 두 ref 간 diff 리뷰
- **타임아웃**: 리뷰 그룹당 실효 타임아웃 = `--timeout` × 리뷰 라운드. 기본 `--timeout 15`에 기본 effort `medium`(2라운드)이면 30분, `low`/`high`는 각각 15/45분입니다.
- **동시성**: 기본 동시성은 8개 파일 워커; rate limit에 걸리면 `--concurrency <n>`으로 감소
- **미리보기 모드**: `--preview` 또는 `-p`로 LLM 실행 없이 리뷰할 파일 목록 미리보기
- **출력 파일**: `--output <path>`로 전체 결과를 stdout 대신 파일에 기록합니다. 명령이 `unknown flag: --output`으로 실패하면 stdout으로 리뷰를 계속하지 마세요. 사용자에게 업그레이드(`npm i -g @alibaba-group/open-code-review@latest`) 여부를 묻고 답변을 기다린 뒤 진행하세요. 사용자가 확인하고 업그레이드가 성공하면 `--output`과 함께 다시 실행하세요.
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
- **출력 잘림 방지**: 대규모 리뷰나 도구 환경이 제한적인 경우 `--output /tmp/ocr_out.txt`를 전달하고 파일 읽기 도구로 전체를 확인하세요. `tail`이나 `head`로 stdout을 파이프하면 앞부분의 리뷰 코멘트가 유실됩니다.

**실패 시:** `ocr review`가 0이 아닌 코드로 종료되면(예: LLM 연결 오류) 무작정 재시도하지 말고, 아래 문제 해결(Troubleshooting) 섹션에서 해당하는 해결책을 확인한 후 다시 실행하세요.

### 3단계: 보고

OCR 출력에는 각 코멘트마다 구조화된 `severity`(critical / high / medium / low)와 `category`(bug / security / performance / maintainability / test / style / documentation / other)가 포함됩니다. 결과를 심각도별로 그룹화하여 제시하고, 오탐 가능성이 높거나 사소한 `low` 심각도 항목은 버립니다.

### 4단계: 수정

수정을 적용하기 전에 사용자가 자동 수정을 요청했는지 확인하세요:

- 사용자가 명시적으로 "리뷰하고 수정해줘" 등으로 요청한 경우 자동 수정 진행
- 사용자가 수정 의도 없이 "리뷰"만 요청한 경우 변경 적용 전에 허가 요청

이슈 및 제안 수정 시:

- critical, high, medium 심각도 항목에 집중
- 안전하고 명확하게 정의된 경우 코드에 직접 수정 적용
- 수동 개입이 필요한 복잡한 수정사항은 수행할 작업을 명확히 설명
- 항상 사용자에게 수정사항을 확인한 후 커밋

## 출력 형식

OCR 출력의 각 코멘트는 다음을 포함합니다:

- `path`: 파일 경로
- `content`: 리뷰 코멘트 텍스트
- `start_line` / `end_line`: 라인 범위 (둘 다 0이면 위치 찾기 실패)
- `category`: 이슈 카테고리 (bug, security, performance, maintainability, test, style, documentation, other)
- `severity`: 이슈 심각도 (critical, high, medium, low)
- `suggestion_code`: 선택적 수정 제안
- `existing_code`: 선택적 원본 코드 스니펫
- `thinking`: 선택적 LLM 추론 과정

다음 템플릿을 사용하여 결과를 심각도별로 그룹화하여 제시합니다:

```markdown
## 코드 리뷰 결과

**리뷰한 파일**: N개
**발견된 이슈**: critical X개, high Y개, medium Z개

### Critical

- **`path/to/file.java:42`** [bug] — 간단한 설명
  > 권장사항: 수정 방법

### High

- **`path/to/file.java:26`** [bug] — 간단한 설명
  > 권장사항: 수정 방법

### Medium

- **`path/to/file.ts:88`** [performance] — 간단한 설명
  > 권장사항: 수정 방법 (해당 시)
```

필터링 후 critical, high, medium 심각도 이슈가 남지 않으면 다음과 같이 표시합니다: "리뷰 완료 — N개 파일에서 critical, high, medium 이슈 없음."

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

## 고급 리뷰 옵션

위의 일반적인 플래그 외에도 `ocr review`는 몇 가지 제어 그룹을 제공합니다. 전체 목록은 `ocr review --help`로 확인하세요.

**범위 지정(Scoping)**

- `--exclude '<patterns>'` — 콤마로 구분된 gitignore 스타일 패턴(예: `--exclude '**/generated/*,**/testdata/*'`). `rule.json`의 exclude와 병합됩니다.
- `--background-file <path>` — Markdown 파일에서 리뷰 컨텍스트를 읽습니다. `--background`보다 우선합니다.

**출력(Output)**

- `--format text|json|sarif` — `text`(기본값)는 사람이 읽기용, `json`은 기계 판독 가능한 결과, `sarif`는 GitHub Code Scanning 같은 코드 스캐닝 연동용입니다.

**모델(Model)**

- `--provider <name>` / `--model <name>` — 이번 실행에 한해 설정된 제공자/모델을 재정의합니다(예: 다른 모델로 diff를 재검토; 사용자가 모델명을 지정하며, `ocr llm providers`가 내장 목록을 출력합니다).

**예산(Budget)**

- `--max-tokens <n>` — 그룹당 프롬프트 상한. 설정값 또는 템플릿 기본값(`200000`)이 기본입니다.
- `--max-tokens-budget <n>` — 실행 전체의 입력 + 출력 토큰을 제한합니다. 초과하면 디스패치가 중단되고, 부분 결과는 그대로 게시되며, 건너뛴 파일은 `failed(budget)`으로 보고됩니다.
- `--no-filter` — 모든 리뷰 코멘트를 유지하고 LLM 사후 필터링 호출을 건너뜁니다.

## 주의사항

- **LLM을 먼저 설정해야 함** — 연결 가능한 LLM이 없으면 `ocr review`는 명확히 실패합니다. 이 경우 아래 문제 해결 섹션을 참고하세요.
- **작업 디렉토리가 중요** — `ocr review`는 현재 디렉토리의 Git 저장소에서 작동합니다. 다른 위치에서 실행하려면 `--repo /path/to/repo`를 사용하세요.
- **워크스페이스 모드에서 추적되지 않은 파일도 리뷰** — 기본 `ocr review`는 스테이징, 언스테이징, *그리고* 추적되지 않은 변경사항을 모두 포함합니다. 범위를 좁히려면 선택적으로 스테이징하세요.
- **큰 diff는 토큰 제한에 걸릴 수 있음** — `MAX_TOKENS`가 프롬프트 예산을 설정합니다(리뷰 템플릿은 `200000`, `ocr scan`은 `58888`). 대화 컨텍스트는 이 프롬프트 예산 안에 머물도록 압축됩니다. 모델 출력은 `MAX_COMPLETION_TOKENS`(`16384`)로 별도 제한됩니다. diff 자체가 `MAX_TOKENS`의 약 80%를 초과하는 파일은 LLM 호출 전에 건너뜁니다.
- **계획 단계(plan phase)는 두 임계값 중 하나로 트리거됨** — 그룹 내 가장 큰 변경 파일이 `PLAN_MODE_LINE_THRESHOLD`(기본 `50`)에 도달하거나, 결합 변경 라인 수가 `PLAN_MODE_GROUP_LINE_THRESHOLD`(기본 `100`)에 도달하는 파일을 2개 이상 보유하면, 본 리뷰 전에 추가 위험 분석 단계를 실행합니다. 지연 시간이 추가되지만 품질이 향상됩니다.
- **`--audience human`을 사용하지 마세요** — 진행 UI가 스트리밍되어 출력을 오염시킵니다. 항상 `--audience agent`를 사용하세요.
- **코멘트 언어는 설정을 따름** — `language` 설정이 리뷰 코멘트 언어를 제어하며 기본값은 `English`이고, 임의의 언어 이름(예: `English`, `中文`)을 사용할 수 있습니다.
- **출력 잘림 방지** — 대규모 리뷰는 출력이 장황합니다. 명령 출력을 `tail`이나 `head`로 파이프하지 마세요. 앞부분의 리뷰 코멘트가 유실됩니다. `--output <path>`를 사용해 전체를 읽고, 구버전 CLI라면 위의 **출력 파일** 안내를 따르세요.
- **중단된 리뷰 재개** — 실패하거나 중단된 range/commit 리뷰는 동일한 `--from`/`--to` 또는 `--commit` 대상으로 `ocr review --resume <id>`를 사용해 이어갈 수 있습니다(실패 시 `retry with: --resume <id>`로 id가 출력되며, `ocr session list`로 찾을 수도 있습니다). 워크스페이스 재개는 지원되지 않습니다.

## 검증

리뷰 완료 후 성공 여부를 다음으로 확인하세요:

1. 명령어가 종료 코드 0으로 종료되었는지
2. 코멘트가 생성되었는지 (또는 "No comments generated" 메시지가 표시되는지)
3. 경고(있는 경우)가 stderr에 표시되는지

오류가 발생한 경우, stderr 경고에서 어떤 파일이 실패했는지와 그 이유를 확인하세요.

## 문제 해결

**`ocr: command not found`**

CLI를 설치하세요:

```bash
npm install -g @alibaba-group/open-code-review
```

**`unknown flag: --output`**

CLI가 v1.10.0보다 오래된 버전입니다. stdout으로 리뷰를 계속하지 마세요. 사용자에게 업그레이드(`npm i -g @alibaba-group/open-code-review@latest`) 여부를 묻고 답변을 기다린 뒤 진행하세요. 사용자가 확인하고 업그레이드가 성공하면 `--output`과 함께 다시 실행하세요.

**`ocr review`가 LLM 연결 오류로 실패**

사용자에게 LLM 제공자 설정을 요청하세요.

대화형 설정(권장):

```bash
ocr config provider
```

수동 설정(대안):

```bash
ocr config set llm.url https://api.anthropic.com/v1/messages
ocr config set llm.auth_token <api-key>
ocr config set llm.model claude-opus-4-6
ocr config set llm.use_anthropic true
```

`ocr llm test`로 연결을 확인하세요. 여기서 멈추고 사용자에게 자격 증명을 입력하도록 요청하세요 — 절대 API 키를 임의로 생성하거나 하드코딩하지 마세요.

## 참고 자료

- 전체 문서: https://github.com/alibaba/open-code-review
- NPM 패키지: https://www.npmjs.com/package/@alibaba-group/open-code-review
- 이슈 트래커: https://github.com/alibaba/open-code-review/issues
