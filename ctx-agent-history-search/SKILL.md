---
name: ctx-agent-history-search
description: 작업 전에 ctx를 사용해 로컬 코딩 에이전트 기록을 검색합니다. 이전 에이전트 세션에 관련 인사이트, 결정, 시도 또는 대화록 컨텍스트가 포함되어 있을 때 사용합니다.
---

# ctx 에이전트 기록 검색

이전 코딩 에이전트 세션을 참조해야 할 때마다 ctx를 사용하세요. 해당
대화록에는 사용자 의도, 결정, 이전 작업 타임라인, 과거
시도, 그리고 성공/실패 정보가 포함될 수 있습니다.

이 스킬은 두 가지 모드로 사용합니다:

- 작업 전 검색: 이전 세션에 현재 작업에 영향을 미치는 결정, 명령,
  실패 또는 소스 인용이 포함되어 있을 수 있는 경우;
- 기록 조사 보고서: 사용자가 에이전트 또는 읽기 전용 하위 에이전트에게
  이전 로컬 에이전트 세션에서 과거 주제를 조사하도록 요청하는 경우.

## 전제 조건

- `ctx` CLI가 설치 및 설정되어 있어야 합니다. 설치되어 있지 않고
  도구 설치가 작업에 적절하다면 다음 명령어로 설치하세요:

  ```bash
  curl -fsSL https://ctx.rs/install | sh
  ```

- 첫 설정은 ctx가 과거 세션을 인덱싱하는 동안 시간이 걸릴 수 있습니다.
  필요한 경우 백그라운드나 tmux에서 실행하거나 완료될 때까지 기다리세요.
- ctx를 계속 사용할 수 없다면 로컬 기록 검색이 불가능하다고 말하고
  결과를 지어내지 마세요.

## 워크플로

1. 콜드 컨텍스트에서 시작할 때 ctx가 준비되었는지 확인하세요:

   ```bash
   ctx status
   ctx sources
   ```

   스크립트에 정확한 필드가 필요한 경우에만 `ctx status --json` 또는
   `ctx sources --json`을 사용하세요.

2. 먼저 일반 언어로 검색하세요. 필요에 따라 용어나 필터를 추가하세요:

   ```bash
   ctx search "<query>"
   ctx search "<query>" --refresh off
   ctx search "<query>" --provider codex
   ctx search "<query>" --workspace <workspace>
   ctx search "<query>" --file <path>
   ctx search "<query>" --since 30d
   ctx search "<query>" --term "<related term>" --term "<error text>"
   ctx search "<query>" --session <ctx-session-id>
   ctx search "<query>" --verbose
   ```

   에이전트가 읽을 때는 기본 텍스트 출력을 사용하세요. `jq`나 스크립트로
   파이프하거나 정확한 기계 판독 가능 필드가 필요하지 않는 한
   `--json`을 검색, show, locate에 추가하지 마세요. JSON 출력은
   훨씬 더 크고 컨텍스트 윈도우를 빠르게 소모할 수 있습니다.

   프롬프트가 여러 세션에 걸친 주제 기록이나 보고서를 요청하는 경우,
   다양한 표현과 필터로 여러 `ctx search` 쿼리를 실행하여
   유망한 세션을 찾으세요. 세션이 관련성이 있어 보이고 해당 세션에서
   밀도 높은 이벤트 수준 일치가 필요할 때는 범위가 지정된
   `ctx search "<query>" --session <ctx-session-id>`를 사용하세요.

   기본 검색은 기본-에이전트 세션을 반환하므로 인간의 의도와 결정이
   두드러지게 유지됩니다. 구현 세부사항, 코드 리뷰 노트, 테스트 출력
   또는 하위 에이전트 세션의 실패 추적이 중요할 가능성이 있을 때는
   `--include-subagents`를 사용하세요.

   전체 ctx ID, 제공자 ID, 인용, 그리고 JSON으로 전환하지 않고
   복사 가능한 후속 명령이 필요할 때는 `--verbose`를 사용하세요.

   세션 대화록을 임시 파일로 저장하고, 파일 크기를 확인한 후
   관련 부분을 읽을 수 있습니다:

   ```bash
   ctx show session <ctx-session-id> --format markdown --out /tmp/ctx-session.md
   wc -c /tmp/ctx-session.md
   ```

   Codex에서 `CODEX_THREAD_ID`를 사용할 수 있으면 ctx는 기본적으로
   활성 세션 트리를 제외하므로 현재 프롬프트와 하위 에이전트가
   과거 검색을 압도하지 않습니다. 활성 세션 트리가 대상인 경우에만
   `--include-current-session`을 사용하세요.

3. 결과를 신뢰하기 전에 관련 결과를 검사하세요:

   ```bash
   ctx show event <ctx-event-id> --window 5
   ctx show session <ctx-session-id>
   ```

4. 소스 식별이나 재개 힌트가 중요할 때 원본 제공자 자료를 찾으세요:

   ```bash
   ctx locate event <ctx-event-id>
   ctx locate session <ctx-session-id>
   ```

5. 사용자나 다른 에이전트가 파일을 필요로 할 때 관련 세션의 대화록을 작성하세요:

   ```bash
   ctx show session <ctx-session-id> --format markdown --out <output-path>
   ```

## 검색으로 충분하지 않을 때

일반 검색으로 질문을 표현할 수 없을 때만 `ctx sql`을 사용하세요.
예를 들어, 안정적인 로컬 뷰에 대한 카운트, 조인, 감사 또는 스크립트가
필요한 경우입니다. 광범위한 대화록 텍스트 검색에는 SQL을 사용하지 마세요.
`ctx search`가 그 목적에 맞게 만들어졌습니다.

번들된 SQL 문서부터 시작하세요:

```bash
ctx docs show sql
ctx docs search "stable views"
```

일반적인 SQL 예제:

```bash
ctx sql "SELECT provider, COUNT(*) AS sessions FROM ctx_sessions GROUP BY provider"
ctx sql "SELECT event_type, COUNT(*) AS events FROM ctx_events GROUP BY event_type ORDER BY events DESC"
ctx sql "SELECT path, provider, provider_session_id FROM ctx_files_touched WHERE path LIKE '%AGENTS.md%' LIMIT 20"
```

`ctx sql`은 읽기 전용이며 기존 인덱스를 쿼리합니다. ctx 저장소를
새로고침, 가져오기, 초기화 또는 마이그레이션하지 않습니다.

## 기록 조사 보고서

과거 주제를 조사하라는 요청을 받으면, 사용자가 수정도 요청하지 않는 한
읽기 전용으로 유지하세요. 에이전트가 보고서를 작성하고, ctx는 로컬 소스
자료만 검색합니다.

1. 프롬프트가 모호한 경우 주제, 범위 및 원하는 길이를 재진술하세요.
   기본적으로 간결한 보고서를 선호하고, 사용자가 연대기, 대안 또는
   상세한 증거를 요청하는 경우 더 긴 보고서를 사용하세요.
2. 여러 번의 타겟 검색을 실행하세요. 사용자 표현, 파일 또는 모듈 이름,
   오류 텍스트, 명령어, 브랜치 이름 및 결정 용어에 따라 쿼리 용어를
   다양화하세요. `ctx search "<topic>"`으로 시작한 다음
   `--term`으로 확장하거나 `--workspace`, `--provider`, `--file`,
   `--since` 또는 `--session <ctx-session-id>`로 좁히세요.
   리뷰, 구현 시도, 테스트 출력 또는 실패 추적이 위임된 세션에 있을
   가능성이 높을 때는 `--include-subagents`를 사용하세요.
   보고서가 로컬 ctx 인덱스를 업데이트하지 않아야 할 때는
   `--refresh off`를 추가하세요.
3. 결론을 내리기 전에 집중된 소스를 검사하세요. 적중 항목과 주변
   턴을 볼 때는 `ctx show event`를, 전체 세션 아크가 중요할 때는
   `ctx show session`을 선호하세요:

   ```bash
   ctx show event <ctx-event-id> --window 5
   ctx show session <ctx-session-id>
   ```

   기본 출력이 필요한 증거를 생략하는 경우에만 전체 또는 로그 모드를
   사용하세요.
4. 세션 간 증거를 비교하세요. 일치점, 충돌점, 오래된 결과,
   누락된 원본 소스 및 검색이 증거를 찾지 못한 간극을 기록하세요.
5. 인용을 포함한 에이전트 종합 분석으로 보고서를 작성하세요.

간결한 보고서 형식:

- 답변 또는 발견;
- 가장 강력한 지지 ctx ID;
- 중요한 주의사항 또는 간극;
- 선택적 다음 검색 또는 검증 단계.

긴 보고서 형식:

- 질문 및 범위;
- 검색 방법(주요 쿼리 및 필터 포함);
- 발견 또는 연대기;
- 제공자, ctx 세션 ID, ctx 이벤트 ID(가능한 경우), 제공자 세션 ID(가능한 경우)
  및 각 소스가 중요한 이유를 포함한 증거 테이블;
- 충돌, 간극 및 제안된 후속 조치.

## 인용 규칙

- 답변 또는 구현에 영향을 미치는 ctx 자료를 인용하세요.
- 제공자, ctx 세션 ID, ctx 이벤트 ID(가능한 경우), 제공자 세션 ID(가능한 경우)
  및 소스 경로 또는 커서(있는 경우)를 포함하세요.
- 여러 스니펫을 종합하는 경우, 결론을 자신의 종합 분석으로 표시하고
  지원 스니펫을 인용하세요.
- 소스 인용이 오래되었거나 사용할 수 없는 경우, ctx가 인덱싱된 텍스트를
  반환했지만 원본 소스를 열 수 없었다고 말하세요.

## 안전 규칙

- 에이전트가 읽을 때는 텍스트 출력을 선호하세요. 스크립트, `jq` 또는
  정확한 필드 추출에만 JSON을 사용하고 JSON 출력을 작게 유지하세요.
- 인용된 텍스트에 해당 결정이 명시적으로 명시되지 않는 한 ctx가
  결정을 추론했다고 말하지 마세요.
- ctx가 모델 분석을 작성했다고 진술하지 마세요.
- 사용자 대상 보고서에 원시 대화록, 대용량 JSON 페이로드, 비밀,
  토큰 또는 개인 경로를 붙여넣지 마세요. 검토된 증거를 요약하고
  주장을 뒷받침하는 데 필요한 짧은 발췌문만 인용하세요.
- 사용자가 명시적으로 검토된 발췌문을 공유하도록 요청하지 않는 한
  `~/.ctx`, 제공자 대화록 경로 및 JSON 출력을 비공개 로컬 기록으로
  취급하세요.
