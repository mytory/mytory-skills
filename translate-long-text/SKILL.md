---
name: translate-long-text
description: 긴 글(PDF/DOCX/EPUB/TXT/MD)을 병렬 하위 에이전트로 청크 단위로 나눠 다른 언어로 번역합니다. 책·논문·보고서·매뉴얼 등 장문 문서 번역, 텍스트/마크다운 파일 번역, 또는 파일 전체를 일관된 용어로 일괄 번역해야 할 때 사용합니다.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
metadata: {"openclaw":{"requires":{"bins":["python3","pandoc","ebook-convert"],"anyBins":["calibre","ebook-convert"]},"homepage":"https://github.com/deusyu/translate-book"}}
---

# 긴 글 번역 스킬

긴 문서(책, 논문, 보고서, 매뉴얼, 플레인 텍스트)를 한 언어에서 다른 언어로 번역하는 다단계 파이프라인입니다. 원문 → Markdown 청크 → 병렬 하위 에이전트 번역 → 병합/빌드 순서로 진행되며, 문서 전체에 걸친 용어 일관성을 유지합니다.

## 파이프라인 개요

```
입력 파일 (PDF/DOCX/EPUB/TXT/MD)
  → convert.py: Markdown 청크(chunkNNNN.md) + manifest.json + config.txt
  → 용어집 구축 (glossary.json)
  → 병렬 하위 에이전트 번역 (청크당 1개, 배치 단위 실행)
  → merge_meta.py: 하위 에이전트 관찰을 용어집에 병합
  → merge_and_build.py: output.md + book.html/docx/epub/pdf
```

## 1. 파라미터 수집

사용자 메시지에서 다음을 확인하세요:

- **file_path**: 입력 파일 경로 — 필수. 지원 형식: `.pdf`, `.docx`, `.epub` (Calibre 사용), `.txt`, `.md`, `.markdown` (네이티브 처리, Calibre 불필요)
- **target_lang**: 대상 언어 코드 (기본값: `zh`) — 예: zh, en, ja, ko, fr, de, es
- **concurrency**: 배치당 병렬 하위 에이전트 수 (기본값: `8`)
- **temp_root**: `{filename}_temp/`를 만들 상위 디렉토리 (선택, 기본값: 현재 작업 디렉토리)
- **epub_cover**: EPUB에 사용할 표지 이미지 경로 (선택)
- **export_name**: 사용자에게 제공할 출력 파일명의 이름 부분 (선택)
- **custom_instructions**: 사용자의 추가 번역 지시사항 (선택)

파일 경로가 제공되지 않으면 사용자에게 물어보세요.

## 2. 전처리 — Markdown 청크로 변환

변환 스크립트를 실행하여 청크를 생성합니다:

```bash
python3 {baseDir}/scripts/convert.py "<file_path>" --olang "<target_lang>"
```

학술·기술 PDF에서 수식, 표, 다단 레이아웃이 Calibre 변환 중 손상될 수 있습니다.
레이아웃을 인식하는 파서가 이미 설치되어 있거나 사용자가 요청했다면
그 도구로 Markdown을 먼저 추출한 뒤 `.md` 파일을 `convert.py`에 입력하세요.
예: MinerU 4 이상은 `mineru-kit parse "<file_path>" -o "<name>.md"`,
Marker는 `marker_single "<file_path>" --output_dir "<dir>"`를 사용할 수 있습니다.
옵션은 설치된 버전의 `--help`로 확인하세요. 대형 모델을 내려받는 파서는
사용자 동의 없이 설치하지 마세요. 현재 로컬 Markdown 입력은 이미지 파일을
temp 디렉토리로 복사하지 않으므로 이미지 참조 경로를 별도로 확인하세요.

선택적 인자:
- `--temp-root "<dir>"` — temp 디렉토리 위치 지정
- `--chunk-size <N>` — 청크당 목표 문자 수 (기본값: 6000)
- `--strip-page-numbers` — PDF/DOCX/EPUB에서 독립된 숫자 행을 적극 제거 (기본값: off)

이 명령은 `{filename}_temp/` 디렉토리를 생성하며 다음 파일들을 포함합니다:
- `input.html`, `input.md` — 중간 파일 (TXT/MD 입력 시 `input.md`가 원문 그대로, `input.html`은 파이프라인 통과용 아티팩트)
- `chunk0001.md`, `chunk0002.md`, ... — 번역할 소스 청크
- `manifest.json` — 추적 및 검증용 청크 매니페스트
- `config.txt` — 메타데이터가 포함된 파이프라인 설정
- `source_fingerprint.json` — 원본 파일 해시 (캐시 검증용)

**참고**: TXT/MD 입력은 Calibre/pandoc 없이 네이티브로 처리됩니다. 이미지 추출은 없지만, Markdown 이미지 참조는 원문에 그대로 남아 `output.md`에서 상대 경로로 해석됩니다. 같은 파일명의 다른 확장자를 연달아 변환하면 `source_fingerprint`가 원본 변경을 감지하고 중단하므로, temp 디렉토리는 파일당 고유해야 합니다.

## 3. 청크 발견

Glob을 사용하여 모든 소스 청크를 찾고 아직 번역이 필요한 청크를 확인하세요:

```
Glob: {filename}_temp/chunk*.md
Glob: {filename}_temp/output_chunk*.md
```

소스 청크 목록을 확인하세요. 이번 실행의 번역 대상은 용어집을 준비한 다음
`run_state.py`로 정합니다.

## 4. 용어집 구축 (용어 일관성)

각 청크는 별도의 하위 에이전트가 새로운 컨텍스트로 번역합니다. 공유 상태가 없으면 동일한 고유명사가 여러 번역에서 다르게 번역될 수 있습니다. 용어집은 각 하위 에이전트가 자신의 청크에 나타나는 용어에 대해 동일한 정규 번역을 사용하도록 합니다.

`<temp_dir>/glossary.json`이 이미 존재하면 재빌드를 건너뛰세요 — 스킬을 다시 실행해도 수동 편집된 용어집을 덮어쓰지 않아야 합니다. 강제로 재빌드하려면 파일을 삭제하세요.

그 외의 경우:

1. **청크 샘플링**: `chunk0001.md`, 마지막 청크, 그리고 균등한 간격의 중간 청크 3개를 읽으세요. `chunk_count < 5`이면 모두 샘플링하세요.
2. **용어 추출**: 샘플에서 문서 전체에 걸쳐 일관된 번역이 필요한 고유명사와 반복되는 도메인 용어를 식별하세요 — 일반적으로 인물, 장소, 조직, 기술 개념 등입니다. 각각을 대상 언어로 번역하세요. 어떤 번역가라도 동일하게 번역할 일반적인 어휘는 건너뛰세요.
3. **`glossary.json` 작성** — temp 디렉토리에 다음 v2 스키마로 작성하세요:

   ```json
   {
     "version": 2,
     "terms": [
       {"id": "Manhattan", "source": "Manhattan", "target": "맨해튼",
        "category": "place", "aliases": [], "gender": "unknown",
        "confidence": "medium", "frequency": 0,
        "evidence_refs": [], "notes": ""}
     ],
     "high_frequency_top_n": 20,
     "applied_meta_hashes": {}
   }
   ```

   기존 v1 `glossary.json` 파일은 첫 로드 시 v2로 자동 업그레이드됩니다. v2는 동일한 표면 형태(source 또는 alias)가 두 개의 다른 용어에 나타나는 것을 금지합니다. v1 파일에 다의어 중복 소스가 있으면 업그레이드가 중단되고 명확화 메시지가 표시됩니다.

4. **빈도 계산** — 다음을 실행하세요:

   ```bash
   python3 {baseDir}/scripts/glossary.py count-frequencies "<temp_dir>"
   ```

   이 명령은 모든 `chunk*.md`(`output_chunk*.md` 제외)를 스캔하고 각 용어의 `frequency` 필드를 업데이트한 후 원자적으로 다시 작성합니다.

용어집은 수동 편집이 가능합니다. `target`, `aliases`, `category`를 바꾸면
아래 계획 단계에서 영향을 받는 청크만 선택적으로 재번역합니다.

### 선택적 재번역 계획

```bash
python3 {baseDir}/scripts/run_state.py plan "<temp_dir>"
```

`translation_chunk_ids`가 이번 작업 목록입니다. `record_only_chunk_ids`가 있으면
`python3 {baseDir}/scripts/run_state.py record "<temp_dir>" chunk0001 ...`로
기존 유효 출력을 기록하세요. `unchanged_chunk_ids`는 그대로 둡니다.
기존 `run_state.json`이 없는 출력에도 용어집 편집을 적용하라는 명시적 요청이
있을 때만 `plan`에 `--retranslate-untracked`를 붙이세요.
`translation_chunk_ids`가 비어 있으면 번역 배치를 건너뛰세요.

## 5. 병렬 번역 (하위 에이전트)

**각 청크는 독립적인 하위 에이전트를 받습니다** (1청크 = 1하위 에이전트 = 1신규 컨텍스트). 이는 컨텍스트 누적과 출력 잘림을 방지합니다.

API rate limit을 준수하기 위해 청크를 배치로 실행하세요:
- 각 배치: 최대 `concurrency`개의 하위 에이전트를 병렬로 실행 (기본값: 8)
- 현재 배치가 완료될 때까지 기다린 후 다음 배치 실행

**각 하위 에이전트를 다음 태스크로 생성하세요.** 런타임이 제공하는 하위 에이전트/백그라운드 에이전트 메커니즘(예: Agent 도구, sessions_spawn 등)을 사용하세요.

출력 파일은 소스 파일명에 `output_` 접두사가 붙습니다: `chunk0001.md` → `output_chunk0001.md`.

> 파일 `<temp_dir>/chunk<NNNN>.md`를 {TARGET_LANGUAGE}로 번역하고 결과를 `<temp_dir>/output_chunk<NNNN>.md`에 작성하세요. 아래 번역 규칙을 따르세요. 번역된 내용만 출력하세요 — 설명이나 코멘트 없이.

각 하위 에이전트는 다음을 받습니다:
- 자신이 담당하는 단일 청크 파일
- temp 디렉토리 경로
- 대상 언어
- 번역 프롬프트 (아래 참조)
- 청크별 용어 테이블 (아래 "용어 테이블 조립" 참조)
- 이웃 청크의 읽기 전용 문맥. 필요하면
  `python3 {baseDir}/scripts/chunk_context.py "<temp_dir>" "chunk<NNNN>.md"`로
  추출하세요. 번역 대상은 담당 청크 하나뿐입니다.
- 모든 사용자 정의 지시사항

**용어 테이블 조립** — 하위 에이전트를 생성하기 전에 실행:

```bash
python3 {baseDir}/scripts/glossary.py print-terms-for-chunk "<temp_dir>" "chunk<NNNN>.md"
```

stdout을 캡처하세요. CLI는 이 청크에 나타나는(source OR alias) 모든 용어 또는 문서 전체에서 가장 빈도가 높은 top-N 용어의 3열 마크다운 테이블(`원문 | 별칭 | 번역문`)을 출력합니다. 테이블을 번역 프롬프트의 규칙 #13에 `{TERM_TABLE}`로 주입하세요. **stdout이 비어 있으면(용어집 없음 또는 관련 용어 없음) 이 청크의 프롬프트에서 규칙 #13을 완전히 생략하세요** — `{TERM_TABLE}` 플레이스홀더를 남기지 마세요.

**각 하위 에이전트의 태스크**:
1. 소스 청크 파일 읽기 (예: `chunk0001.md`)
2. 아래 번역 규칙에 따라 내용 번역
3. 번역된 내용을 `output_chunk0001.md`에 작성
4. 관찰 내용을 `output_chunk0001.meta.json`에 아래 스키마로 작성. **비차단(Non-blocking)** — 확실하지 않으면 필드를 비워두고 엔터티를 임의로 생성하지 마세요. 항상 파일을 내보내세요(모든 배열이 비어 있더라도). 파일의 존재와 내용 해시가 메인 에이전트가 피드백이 이미 병합되었는지 추적하는 방식이기 때문입니다.

**하위 에이전트 메타 스키마** (`output_chunk<NNNN>.meta.json`):

```json
{
  "schema_version": 1,
  "new_entities": [
    {"source": "Taig", "target_proposal": "타이그", "category": "person",
     "evidence": "<청크에서 가져온 ≤200자 인용문>"}
  ],
  "alias_hypotheses": [
    {"variant": "Taig", "may_be_alias_of_source": "Tai",
     "evidence": "<≤200자 인용문>"}
  ],
  "attribute_hypotheses": [
    {"entity_source": "Tai", "attribute": "gender", "value": "male",
     "confidence": "high", "evidence": "<≤200자 인용문>"}
  ],
  "used_term_sources": ["Tai", "Manhattan"],
  "conflicts": [
    {"entity_source": "Tai", "field": "target", "injected": "타이",
     "observed_better": "타이_원", "evidence": "<≤200자 인용문>"}
  ]
}
```

**`chunk_id` 필드를 포함하지 마세요** — 청크 정체는 파일명에서 파생됩니다. 페이로드에 넣으면 환각 구멍이 생기고 검증에서 파일이 거부됩니다.

메타 파일은 나중에 메인 에이전트가 읽어 `glossary.json`에 병합합니다(`merge_meta.py` 참조). 하위 에이전트는 스키마를 정직하게 채워야 합니다: 청크에서 실제 인용문을 인용하고, "생산적으로 보이기 위해" 엔터티를 절대 임의로 생성하지 마세요. 빈 메타도 완전히 유효한 출력입니다.

**중요**: 각 하위 에이전트는 정확히 **하나**의 청크를 번역하고 결과를 직접 출력 파일에 작성합니다. START/END 마커가 필요하지 않습니다.

### 한국어 번역의 서명·강조 표기

한국어 번역에서는 다음 규칙을 하위 에이전트의 번역 지시와 병합 후 검수에
함께 반영한다. 사용자가 별도 표기 방식을 지정하면 그 지시를 우선한다.

- 책·소책자·잡지·신문 등 출판물 이름은 《》, 개별 글 이름은 〈〉 등
  문서의 일관된 서명 부호로 표시한다. 서명을 나타내는 원문의 이탤릭은
  번역문에서 제거한다. 괄호 안의 원어 이름에도 이탤릭을 덧붙이지 않는다.
- 서명과 의미상 강조를 구분한다. 서명에 서명 부호와 강조를 중복 적용하지 않는다.
- 한국어 의미상 강조에는 기울임꼴을 쓰지 않는다. Markdown `*강조*`는
  의미상의 em으로 유지할 수 있으나, 최종 출력에서는 `em`을 밑줄로,
  `strong`/`**강조**`를 볼드로 표시한다. 문법 보존 규칙보다 이 표기 규칙을 우선한다.
- HTML·EPUB은 `em { font-style: normal; text-decoration: underline; }`와
  `strong { font-weight: bold; }`를 적용한다. DOCX는 이탤릭 서식 대신
  밑줄 서식을 사용한다. 변환 후 실제 텍스트의 스타일을 검사한다.
- 병합 후 모든 em 구간을 전수 확인해 서명이 강조로 남지 않았는지 검사한다.
  서명 부호 추가 외에는 본문이 바뀌지 않았는지 확인하고, 강조·볼드·제목·인용이
  출력물에 유지되는지 대조한다.
- **출판물 서명 부호는 한 문서에서 한 세트만 쓴다**(국립국어원). 이 프로젝트에서는
  책·소책자·잡지·신문 모두 《…》(겹낫표)로 통일했고, 조문·법률·개별 글 제목만
  〈…〉(홑낫표)로 남겼다. 서명을 나타내던 원문 이탤릭(`*...*`)은 서명 부호로
  바꾸면서 함께 제거한다. `『…』`(홑화살괄호)는 쓰지 않는다.

#### Calibre 변환에서 밑줄이 사라지는 함정 (실측)

- Calibre용 사전 준비 스크립트가 `* { text-decoration: none !important; }` 같은
  전역 규칙을 넣으면 **em의 밑줄까지 지운다.** 링크 밑줄만 없애려면 `a { text-decoration: none !important }`로 한정한다.
- 원문에서 강조한 `<u>...</u>`는 Calibre가 밑줄 없는 `<span>`으로 바꿔 버린다.
  밑줄 강조는 **`*em*`(→`<em>`)으로 마크다운에 남기고** CSS
  `em, i { font-style: normal; text-decoration: underline; }`로 표시하는 편이 안전하다.
- DOCX는 Calibre가 `<em>`을 캐릭터 스타일(rStyle) 없이 평문 run으로 떨어뜨리는 경우가
  있어, 변환 후 `word/document.xml`에서 강조 run을 찾아 `<w:u w:val="single"/>`를
  주입해야 할 수 있다(`epub-for-ridi`의 `fix_docx_bold.py --em-underline` 참조).
- 변환 후 실제 산출물에서 `text-decoration: underline` 규칙과 강조 run이
  살아 있는지 검사한다. HTML 단계에서 통과해도 변환기가 지울 수 있다.

### 하위 에이전트용 번역 프롬프트

각 하위 에이전트의 지시사항에 이 번역 프롬프트를 포함하세요(`{TARGET_LANGUAGE}`를 실제 언어명(예: "한국어")으로 바꾸세요):

---

마크다운 파일을 {TARGET_LANGUAGE}로 번역하세요.
중요 요구사항:
1. Markdown 형식을 엄격하게 유지하세요 — 제목, 링크, 이미지 참조 등
2. 텍스트 내용만 번역하고 모든 Markdown 문법과 파일명은 유지하세요
   - 한국어 번역은 위의 서명·강조 표기 규칙을 함께 적용하세요. 서명 이탤릭은
     〈〉·《》로 바꾸고, 의미상 em은 최종 출력에서 밑줄, strong은 볼드로 표시하세요.
3. 빈 링크, 불필요한 문자(예: 행 끝의 '\\')를 제거하세요. 페이지 번호는 convert.py에서 이미 처리했으므로, 독립적인 숫자 행(연도 1984, 장 번호, 참조 번호 등 본문 내용)은 삭제하지 마세요.
4. 형식과 의미를 보장하고 내용을 자연스럽고 유창하게 번역하세요
5. 번역된 본문 내용만 출력하고 설명, 힌트, 주석 또는 대화 내용을 포함하지 마세요.
6. 표현은 명확하고 간결하게, 복잡한 문장 구조를 사용하지 마세요. 순서대로 번역하고 내용을 건너뛰지 마세요.
7. 모든 이미지 참조를 반드시 유지하세요:
   - 모든 ![alt](path) 형식의 이미지 참조를 완전히 유지
   - 이미지 파일명과 경로를 수정하지 마세요 (예: media/image-001.png)
   - 이미지 alt 텍스트는 번역할 수 있지만 이미지 참조 구조는 유지
   - 이미지 관련 내용을 삭제, 필터링 또는 무시하지 마세요
   - 이미지 참조 예: ![Figure 1: Data Flow](media/image-001.png) -> ![그림 1: 데이터 흐름](media/image-001.png)
8. 다단계 제목을 지능적으로 인식하고 처리하여 다음 규칙에 따라 마크다운 표시를 추가하세요:
   - 주제목(책 제목, 장 제목 등)은 # 사용
   - 1단계 제목(큰 절 제목)은 ## 사용
   - 2단계 제목(작은 절 제목)은 ### 사용
   - 3단계 제목(하위 제목)은 #### 사용
   - 4단계 이하 제목은 ##### 사용
9. 제목 인식 규칙:
   - 독립적으로 있는 짧은 텍스트(보통 50자 미만)
   - 요약적 또는 개괄적인 성격의 문장
   - 문서 구조에서 구분 및 정리 역할을 하는 텍스트
   - 글꼴 크기가 확연히 다르거나 특별한 형식이 있는 텍스트
   - 숫자 번호로 시작하는 장 텍스트(예: "1.1 개요", "제3장" 등)
10. 제목 계층 판단:
    - 컨텍스트와 내용 중요성에 따라 제목 계층 판단
    - 장 수준 제목은 일반적으로 높은 계층 (# 또는 ##)
    - 절, 하위 절 제목은 순서대로 낮은 계층 (###, ####, #####)
    - 동일 문서 내 제목 계층 일관성 유지
11. 주의사항:
    - 진짜 제목 텍스트에만 제목 표시를 추가하고 과도하게 추가하지 마세요
    - 본문 단락에 제목 표시를 추가하지 마세요
    - 원문에 이미 마크다운 제목 표시가 있으면 그 계층 구조를 유지하세요
12. {CUSTOM_INSTRUCTIONS if provided}
13. 용어 일관성: 다음 용어는 지정된 번역을 엄격히 사용해야 하며 임의로 변경하지 마세요. 표의 "원문" 열 **또는** "별칭" 열의 형태가 본문에 나타나면 반드시 "번역문" 열의 해당 형태로 번역하세요.

{TERM_TABLE}

마크다운 파일 본문:

---

## 6. 하위 에이전트 메타를 용어집에 병합 (각 배치 후)

각 하위 에이전트는 번역된 청크와 함께 `output_chunk<NNNN>.meta.json`을 출력합니다. 각 배치가 완료된 후 메인 에이전트는 이러한 관찰 내용을 정규 용어집에 병합하여 이후 배치가 향상된 용어집을 사용할 수 있게 합니다.

1. 병합 준비 실행:

   ```bash
   python3 {baseDir}/scripts/merge_meta.py prepare-merge "<temp_dir>"
   ```

   stdout JSON을 캡처하세요. 다음 네 개의 배열을 포함합니다:
   - `auto_apply` — 용어집 충돌이 없고 모든 제안 청크에서 (target, category)가 일치하는 새 엔터티.
   - `decisions_needed` — 메인 에이전트의 판단이 필요한 항목. 각 항목은 `id`, `kind`, `options` 배열, 그리고 선택에 필요한 데이터를 포함합니다. 종류:
     - `alias` — `{variant, candidate_source, evidence}`. 선택지: `yes_alias` / `no_separate_entity` / `skip`.
     - `conflict` — `{entity_source, field, current, proposed, evidence}`. 선택지: `keep_current` / `accept_proposed` / `record_in_notes`.
     - `new_entity_existing_alias` — 하위 에이전트가 `proposed_source`를 새 엔터티로 제안했지만 이미 다른 엔터티의 별칭인 경우. `{proposed_source, currently_alias_of, promoted_variants: [{target_proposal, category, evidence, evidence_chunks}, ...]}`. 선택지: 고유한 (target, category) 승격 변형마다 하나의 `use_variant_N` (proposed_source를 독립 엔터티로 승격, 호스트의 aliases에서 제거) / `keep_as_alias` / `skip`.
     - `existing_entity_conflict` — 하위 에이전트가 `entity_source`에 대해 정규 버전과 다른 (target, category)를 제안한 경우. 서로 다른 여러 제안이 모두 노출됨. `{entity_source, current_target, current_category, proposed_variants: [{target_proposal, category, evidence, evidence_chunks}, ...]}`. 선택지: `keep_current` / 경쟁 제안마다 하나의 `use_variant_N` (target과 category를 모두 덮어쓰고 이전 값을 notes에 기록) / `record_in_notes` (정규 버전 유지, 모든 제안 변형이 notes에 기록됨).
     - `alias_or_new_entity` — `variant`가 v2의 표면 형태 고유성 규칙 아래에서 공존할 수 없는 여러 경쟁 옵션을 가짐. (a) `variant`가 새 독립 엔터티와 하나 이상의 후보의 별칭으로 모두 제안된 경우, 또는 (b) `variant`가 독립 경쟁자 없이 둘 이상의 다른 후보의 별칭으로 제안된 경우 발생. `{variant, alias_candidates: [{candidate_source, evidence, evidence_chunks}, ...], standalone_variants: [{target_proposal, category, evidence, evidence_chunks}, ...]}`. 선택지: 각 후보마다 하나의 `use_alias_N` (해당 후보의 별칭으로 추가), 각 경쟁 독립 제안마다 하나의 `use_standalone_N` (해당 target+category로 독립 엔터티 추가), 또는 `skip`.
     - `conflicting_new_entity_proposals` — `{source, variants: [{target_proposal, category, evidence, evidence_chunks}, ...]}`. 선택지: `use_variant_0`, `use_variant_1`, ..., `skip`.
   - `consumed_chunk_ids` — 이번 라운드에서 스캔한 모든 메타 파일 (결과 생성 여부와 관계없음). 적용 시 이러한 해시가 `applied_meta_hashes`에 기록됩니다.
   - `malformed_meta_chunk_ids` — 검증에 실패한 메타 파일. 격리됨: 소비되지 않으며 실행이 중단되지 않음. 배치 진행 상황에 표시하세요.

2. **`consumed_chunk_ids`가 비어 있으면** → 스캔된 것이 없음; 다음 단계로 건너뛰세요.

3. **`consumed_chunk_ids`가 비어 있지 않지만 `auto_apply`와 `decisions_needed`가 모두 비어 있으면** → 그래도 `{"auto_apply": [], "decisions": [], "consumed_chunk_ids": [...]}`를 `apply-merge`에 파이프하여 해시가 기록되도록 하세요. **이 단계를 건너뛰는 것이 버그입니다** — 효과 없는 메타가 영원히 재스캔됩니다.

4. **그 외의 경우, 각 결정을 해결하세요**:
   - 증거 인용문을 인라인으로 읽으세요.
   - `options` 배열에서 하나를 선택하세요.
   - 원래 결정과 선택 사항을 왕복시키는 `decisions` 항목을 빌드하세요. 항목에는 원래 `kind`와 (`conflicting_new_entity_proposals`의 경우) `variants` 배열이 포함되어야 apply-merge가 검증하고 실행할 수 있습니다:

     ```json
     {"id": "d1", "kind": "alias", "variant": "Taig", "candidate_source": "Tai", "choice": "yes_alias"}
     ```

5. 결정 JSON을 apply-merge에 파이프하세요:

   ```bash
   echo '{"auto_apply": [...], "decisions": [...], "consumed_chunk_ids": [...]}' \
     | python3 {baseDir}/scripts/merge_meta.py apply-merge "<temp_dir>"
   ```

   배치 진행 메시지에 요약 JSON(`auto_applied`, `decisions_resolved`, `consumed_chunks`, `errors`)을 표시하세요.

   **apply-merge는 트랜잭션입니다.** 어떤 결정이라도 잘못된 형식(kind에 맞지 않는 choice, 필드 누락, 존재하지 않는 엔터티 참조)이면 전체 배치가 0이 아닌 종료 코드와 stderr 상세 정보로 중단됩니다 — 용어집 변경 없음, 해시 기록 없음. 0이 아닌 종료 시 잘못된 결정을 수정하고 다시 파이프하세요; 아무것도 소비되지 않았으므로 `prepare-merge`는 동일한 제안을 다시 표시합니다.

   **입력 목록의 결정 순서는 중요하지 않습니다.** `apply-merge`는 내부적으로 엔터티 생성 결정을 별칭 연결 결정보다 먼저 처리하므로, 동일한 배치의 다른 결정에 의해 후보가 생성되는 경우(`use_standalone_N`, `use_variant_N`, 또는 `promote_to_separate_entity`) `yes_alias` 결정은 전달된 순서와 관계없이 성공합니다. 별칭 체인(예: `Taighi → Taig`와 `Taig → Tai`가 모두 보류 중인 별칭 결정)은 별칭 연결 패스 내에서 고정점 루프를 통해 해결됩니다 — 수동으로 위상 정렬하거나 연결된 별칭을 순서대로 지정할 필요가 없습니다.

이전에 중단된 배치 후 새로 실행하면 `prepare-merge`는 남겨진 메타 파일을 모두 선택합니다. 수동으로 삭제하지 마세요.

각 배치의 번역 파일을 확인한 뒤 완료된 청크를
`python3 {baseDir}/scripts/run_state.py record "<temp_dir>" chunk0001 ...`로
기록하세요.

## 7. 완전성 확인 및 재시도

모든 배치가 완료된 후 Glob을 사용하여 모든 소스 청크에 해당 출력 파일이 있는지 확인하세요.

누락된 경우 각 누락 청크를 자체 하위 에이전트로 재시도하세요. 청크당 최대 2회 시도(초기 + 1회 재시도).

또한 `manifest.json`을 읽고 다음을 확인하세요:
- 모든 청크 id에 해당 출력 파일이 있음
- 출력 파일이 비어 있지 않음 (0바이트)

그런 다음 메타 병합 관찰 가능성 스냅샷을 실행하세요:

```bash
python3 {baseDir}/scripts/merge_meta.py status "<temp_dir>"
```

확인 보고서에 한 줄 요약을 표시하세요:

> 번역된 청크: 50개 • 메타 파일: 48개 발견 / 47개 소비 • 형식 오류: 1개 (chunk0099 — stderr 참조) • 메타 누락 청크: chunk0017, chunk0042

심각도 규칙(다음 중 어떤 것도 실행을 실패시키지 않습니다 — 메타는 비차단입니다):

- `unmerged_meta_files > 0` (6단계 실행 후) → 버그, 눈에 띄게 표시. 재개 시 발견되어야 함.
- `malformed_meta_files > 0` → 하위 에이전트가 잘못된 메타를 출력함. chunk_id와 "파일을 수동으로 수정하고 다시 실행하면 이 청크의 피드백이 병합됩니다" 메모를 출력.
- `meta_files_found < translated_chunks` → 하위 에이전트 준수 문제(일부 청크가 메타를 전혀 출력하지 않음). 누락된 chunk_id 출력.

재시도 후에도 번역에 실패한 청크를 보고하세요.

## 8. 제목 번역

temp 디렉토리에서 `config.txt`를 읽어 `original_title` 필드를 가져오세요. (PDF/DOCX/EPUB는 메타데이터에서 추출되고, TXT/MD는 파일명 스템입니다.)

제목을 대상 언어로 번역하세요. 한국어의 경우 필요시 적절한 표기를 사용하세요.

### 번역자 표기

완성된 번역서의 속표지나 크레딧에 번역자를 명시한다. AI가 번역했다면 도구명
(Codex·ChatGPT 등)이 아니라 실제 사용한 모델명을 쓴다. 예: GPT-6가 번역한
한국어 책에는 `번역: GPT-6`를 쓴다. 모델명은 런타임에서 확인된 이름을 사용하고
확인되지 않은 버전·세부 모델명을 추측하지 않는다. 여러 모델이 번역을 분담했다면
실제 참여 모델을 구분해 기록한다. 사용자가 지정한 이름·표기·생략 지시를 우선한다.

원저자와 번역자를 구분하고, 번역자 이름 때문에 원저자 메타데이터를 바꾸지
않는다. 병합한 원고에 크레딧을 넣고, DOCX·EPUB 등 모든 납품 형식의 본문에
표기가 실제로 들어갔는지 확인한다. 본문 보존 검사에서는 크레딧 추가를
의도한 변경으로 기록한다.

## 9. 후처리 — 병합 및 빌드

번역된 제목으로 빌드 스크립트를 실행하세요:

```bash
python3 {baseDir}/scripts/merge_and_build.py --temp-dir "<temp_dir>" --title "<translated_title>" --cleanup
```

`--cleanup` 플래그는 완전히 성공적인 빌드 후 중간 파일(청크, input.html 등)을 제거합니다. 사용자가 중간 파일 유지를 요청한 경우 `--cleanup`을 생략하세요.

`epub_cover`가 지정되면 `--cover "<epub_cover>"`를, `export_name`이 지정되면
`--export-name "<export_name>"`을 추가하세요.

스크립트는 `config.txt`에서 `output_lang`을 자동으로 읽습니다. 선택적 재정의: `--lang`, `--author`. `--export-name "<stem>"`으로 출력 파일명을 사용자 친화적으로 변경할 수 있습니다 (예: `--export-name report` → `report.html`, `report.docx`, ...).

이 명령은 temp 디렉토리에 다음 파일들을 생성합니다:
- `output.md` — 병합된 번역 마크다운 (모든 입력 형식의 1차 산출물)
- `book.html` — 떠다니는 목차가 있는 웹 버전
- `book_doc.html` — 전자책 버전
- `book.docx`, `book.epub`, `book.pdf` — 형식 변환 결과 (Calibre 필요)

비책(非책) 문서의 경우 `book.*` 파일명은 호환성을 위해 유지되며, `output.md`가 실질 결과물입니다. 형식 변환은 각각 독립적으로 시도되며, 실패해도 파이프라인은 중단되지 않습니다.

## 10. 결과 보고

사용자에게 알리세요:
- 출력 파일 위치
- 번역된 청크 수
- 번역된 제목
- 생성된 출력 파일 목록과 크기
- 형식 생성 실패 사항

## 이어가기 (재개)

파이프라인은 멱등적으로 재개할 수 있습니다:
- `convert.py` 재실행 — 기존 `input.html`/`input.md`/청크가 있으면 해당 단계를 건너뜁니다.
- 이미 번역된 청크(`output_` 파일)는 3단계에서 자동으로 제외됩니다.
- `glossary.json`은 재빌드되지 않으며, `merge_meta.py`는 남은 메타 파일만 선택합니다.
- `source_fingerprint.json`이 원본 변경을 감지하면 안전하게 중단합니다 — temp 디렉토리를 지우고 다시 실행하세요.
