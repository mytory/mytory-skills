---
name: open-code-review-delegate
description: >
  open-code-review(OCR)의 위임(delegation) 모드입니다. OCR이 LLM 엔드포인트를 호출하는
  대신, 호스트 에이전트가 자체 LLM 능력을 사용해 코드 리뷰를 직접 수행하도록 지시합니다.
  OCR은 파일 선택과 규칙 해석 같은 결정적(deterministic) 엔지니어링에만 사용합니다.
  호스트 에이전트가 자체 LLM 기능으로 리뷰를 주도해야 할 때 사용합니다.
license: Apache-2.0
compatibility: >
  `ocr` CLI 설치 필요(`npm install -g @alibaba-group/open-code-review` 또는 GitHub
  릴리스 바이너리). LLM 엔드포인트 설정은 필요하지 않습니다 — 위임 모드에서 OCR 측은
  LLM을 사용하지 않습니다.
metadata:
  author: alibaba
  homepage: https://github.com/alibaba/open-code-review
  version: "1.0.0"
---

# Open Code Review — 위임 모드

OCR이 결정적 엔지니어링(파일 필터링, 규칙 해석)을 제공하고, 호스트 에이전트가 자체 지능과 도구로 실제 리뷰를 수행하는 AI 코드 리뷰 스킬입니다.

## 워크플로우

### 1단계: Preview — 무엇을 리뷰할지 결정

```bash
ocr delegate preview --format json [--from <ref> --to <ref>] [--commit <hash>] [--exclude <patterns>]
```

출력 내용:
- **mode** (workspace / range / commit)
- **from / to / commit / merge_base** — git 명령 구성에 사용할 ref 메타데이터
- **리뷰 가능한 파일 목록** — 경로, 상태, 추가/삭제 라인 수
- **제외된 파일** — 제외 사유 포함

**자주 쓰는 호출:**

| 시나리오 | 명령어 |
|----------|---------|
| 워크스페이스 변경사항 | `ocr delegate preview` |
| 브랜치 비교 | `ocr delegate preview --from main --to feature` |
| 단일 커밋 | `ocr delegate preview -c abc123` |

### 2단계: 파일별 규칙 가져오기

```bash
ocr delegate rule --format json <path1> <path2> ...
```

1단계에서 얻은 리뷰 가능한 파일 경로를 전달합니다. 출력은 규칙 내용별로 그룹화되므로, 같은 규칙을 공유하는 파일은 하나의 그룹 아래에 모여 중복이 사라집니다.

### 3단계: diff 가져오기

1단계의 mode와 ref에 따라 diff 명령을 선택합니다. 리뷰 중 모든 Git 호출에는 `git --no-pager`를 사용합니다.

diff 명령은 외부 diff 프로그램, 텍스트 변환, 색상을 비활성화하여 일반 텍스트 패치를 출력합니다.

**Range 모드** (preview 출력에 merge_base가 제공됨):
```bash
git --no-pager diff --no-ext-diff --no-textconv --no-color <merge_base>..<to> -- "<path>"
```

**Commit 모드**:
```bash
git --no-pager show --no-ext-diff --no-textconv --no-color <commit> -- "<path>"
```

**Workspace 모드**:
```bash
# 추적 중인 파일
git --no-pager diff --no-ext-diff --no-textconv --no-color HEAD -- "<path>"
# 추적되지 않은 새 파일 — 직접 읽기 (파일 전체가 새 코드)
cat "<path>"
```

컨텍스트를 읽을 때는 다음 명령을 사용합니다:

```bash
git --no-pager log --no-color --oneline -- "<path>"
git --no-pager blame --no-textconv -- "<path>"
git --no-pager show --no-ext-diff --no-textconv --no-color "<ref>:<path>"
```

큰 diff는 선택한 모드의 명령에 `--output="<absolute-diff-file>"`을 추가합니다. 저장소 밖의 고유한 절대 경로를 선택하고 상위 디렉터리를 만듭니다. 파일 읽기 도구에서도 같은 경로를 사용합니다:

```bash
git --no-pager diff --no-ext-diff --no-textconv --no-color --output="<absolute-diff-file>" <merge_base>..<to> -- "<path>"
```

Git이 종료 코드 0으로 끝나면 파일 전체를 나누어 읽고 리뷰한 뒤 삭제합니다. Git이 실패하거나 시간 초과되면 재시도하거나 오류와 함께 `skipped`로 기록합니다. 예상과 달리 출력이 비어 있으면 preview를 다시 실행해 확인합니다.

### 4단계: 파일별 리뷰

`reviewable_files`의 모든 항목을 담은 체크리스트를 만듭니다. 각 리뷰 대상 파일에 대해:

체크리스트 식별자로 `(path, status)`를 사용합니다. 워크스페이스 모드에서는 스테이징된 삭제 뒤에 추적되지 않은 파일이 다시 생성된 경우 같은 경로가 두 번 보고될 수 있습니다.

1. 해당 파일의 diff 가져오기 (3단계)
2. 리뷰 체크리스트를 위해 해당 파일의 Rule Group 확인 (2단계)
3. 필요에 따라 적절한 컨텍스트 도구를 사용해 철저히 리뷰
4. 파일을 `reviewed`로 표시하거나, 구체적인 사유와 함께 `skipped`로 표시

변경 규모가 크면 공유 규칙과 diff 크기를 기준으로 묶어 제한된 배치 단위로 리뷰합니다. 첫 번째 고심각도 이슈를 발견했다고 멈추지 마세요.

### 5단계: 출력 형식

각 코멘트는 다음 구조를 따라야 합니다:

| 필드 | 타입 | 필수 | 설명 |
|-------|------|----------|-------------|
| path | string | 예 | 상대 파일 경로 |
| content | string | 예 | 이슈를 설명하는 리뷰 코멘트 |
| start_line | integer | 아니오 | 새 파일에서의 시작 라인 |
| end_line | integer | 아니오 | 새 파일에서의 종료 라인 |
| category | enum | 아니오 | bug, security, performance, maintainability, test, style, documentation, other |
| severity | enum | 아니오 | critical, high, medium, low |

### 6단계: 분류 및 보고

보고하기 전에 preview한 모든 파일이 처리되었는지 확인합니다. 요약에 `total_files`, `reviewed_files`, `skipped_files`, `coverage_rate`를 포함하세요. 건너뛴 파일은 반드시 사유를 포함해야 합니다.

발견 사항을 심각도별로 그룹화합니다:

- **Critical/High**: 버그, 보안 이슈, 데이터 손실 위험 — 항상 보고
- **Medium**: 성능 우려, 오류 처리 누락, 유지보수성 문제 — 컨텍스트와 함께 보고
- **Low**: 스타일 지적, 사소한 제안 — 명확히 가치가 있을 때만 보고

오탐 가능성이 높은 항목은 조용히 버립니다.

### 7단계: 수정 (선택)

사용자가 "리뷰 및 수정"을 요청한 경우:
- High/Critical 수정은 직접 적용
- 수동 개입이 필요한 Medium 수정은 설명
- Low 우선순위 항목은 사소한 경우가 아니면 건너뜀

## 하위 명령 참조

| 명령어 | 목적 |
|---------|---------|
| `ocr delegate preview` | 리뷰할 파일 + mode/ref 메타데이터 |
| `ocr delegate rule <path...>` | 내용별로 그룹화된 리뷰 규칙 |

## 공통 플래그

| 플래그 | 설명 |
|------|-------------|
| `--from <ref>` | range 모드의 소스 ref |
| `--to <ref>` | range 모드의 대상 ref |
| `-c, --commit <hash>` | 단일 커밋 모드 |
| `--repo <path>` | 저장소 루트 (기본값: 현재 디렉토리) |
| `--rule <path>` | 사용자 정의 rule.json 경로 |
| `--exclude <patterns>` | 콤마로 구분된 제외 패턴 |
| `-b, --background <text>` | 비즈니스 컨텍스트 |
| `-B, --background-file <path>` | Markdown 파일에서 비즈니스 컨텍스트 읽기 (`-b`보다 우선) |
| `-f, --format <text\|json>` | 출력 형식; 에이전트 연동에는 `json` 사용 |

## 주의사항

- **OCR 측에는 LLM이 필요 없음** — 위임 모드는 절대 LLM을 호출하지 않습니다. 모든 지능은 호스트 에이전트에서 나옵니다.
- **규칙은 그룹화됨** — 같은 규칙을 공유하는 파일은 출력에서 함께 그룹화됩니다. 호출당 경로 수에는 제한이 없으며, 변경 규모가 크면 리뷰 진행에 맞춰 배치별로 규칙을 가져오세요.
- **작업 디렉토리가 중요** — `ocr delegate`는 현재 디렉토리의 Git 저장소에서 작동합니다. `--repo /path`로 재정의할 수 있습니다.
- **워크스페이스 모드의 추적되지 않은 파일** — `preview`는 추적되지 않은 파일도 포함합니다. 이런 파일은 `git diff` 대신 파일을 직접 읽으세요.
- **배경 컨텍스트** — 요구사항 컨텍스트가 있으면 `preview`에 `--background`를 전달하세요. 리뷰 중 참고할 수 있도록 출력에 나타납니다.
- **커버리지는 필수** — 모든 `reviewable_files` 항목은 reviewed 또는 명시적 skipped로 끝나야 합니다. 파일을 조용히 누락하지 마세요.

### 너무 큰 배경 컨텍스트 복구

`--background-file`에는 서로 독립적인 두 가지 제한이 있습니다. 원본 파일은
1 MiB를 초과할 수 없고, 정제된 내용은 8000자를 초과할 수 없습니다. 둘 중 하나라도
걸리면 명령이 중단됩니다. 명령이 두 제한 중 하나를 보고하면:

1. 원본 파일을 조용히 잘라내지 마세요.
2. 요구사항, 제약, 수용 기준 및 기타 리뷰에 중요한 세부사항을 보존하면서 원본 자료를 요약하세요.
3. 요약을 셸에서 안전한 하나의 인자로 전달하여 해당 명령을 다시 시도하세요(예: 호스트
   셸이 생성한 따옴표/이스케이프 처리된 인자를 사용하거나, 크기 제한 내의 새 파일에
   기록하여 그 파일을 전달). 신뢰할 수 없는 요약 텍스트를 큰따옴표 셸 템플릿에 직접
   넣지 마세요. `$()`, 백틱, 따옴표, 변수 참조가 여전히 평가될 수 있습니다.
   CLI가 같은 초과 파일을 다시 로드해 또 실패하지 않도록 원래의 `--background-file`은
   생략하세요.
4. 충실한 요약이 불가능하면 OCR 배경 컨텍스트를 아예 생략하고, 리뷰 중에 원본 자료를
   직접 읽으세요.

### CLI 버전 호환성 문제 해결

`--format` 플래그는 `ocr` v1.9.0 이상에서 사용할 수 있습니다. 스킬과 설치된 CLI는
독립적으로 업데이트될 수 있습니다. `--format json`을 사용한 `preview` 또는 `rule`
명령이 특별히 `unknown flag: --format` 오류로 실패하면, 플래그 없이 다시 실행하고
나머지 위임 실행에서는 텍스트 출력을 사용하세요. 해당 출력에서 명시적인 mode, ref,
file, rule 정보를 그대로 보존하세요. 텍스트 출력을 JSON으로 파싱하거나 누락된 스키마
필드를 임의로 만들어내지 마세요. 다른 오류에 대해서는 플래그를 빼고 재시도하지 말고,
오류를 보고한 뒤 해당 워크플로우를 중단하세요.

호스트 에이전트용 스킬은 동등한 텍스트 출력을 사용해 리뷰 체크리스트를 완성할 수
있습니다. `schema_version`이나 기타 JSON 필드를 요구하는 프로그래밍 방식 연동은
JSON 지원 CLI를 요구해야 합니다. `ocr --version`으로 확인하고 필요하면 업그레이드하세요:

```bash
npm install -g @alibaba-group/open-code-review
```
