# 마무리 게이트

검사기가 고칠 수 있는 FAIL을 아직 찾아내는 동안에는 빌드가 끝난 것이 아닙니다. `scripts/gate.mjs`는
중요한 검사를 돌리고, 열려 있는 항목을 나열하고, 라운드를 세므로, 빌드는 실제로 반복해서 고치면서도
결국 끝납니다.

## 켜기

1단계에서, 페이지가 생기기 전에 켭니다.

```bash
node <skill>/scripts/gate.mjs --start index.html --kind <kind> --category "<what is sold>" --primary "<main action>"
```

- 프레임워크 빌드는 브라우저가 열 수 있는 것을 지정합니다. 개발 서버 URL(`--start http://localhost:5173/`,
  게이트를 돌릴 때 서버가 실행 중이어야 함)이나 빌드된 페이지(`--start dist/index.html --root dist`)입니다.
  빌드된 페이지는 빌드된 그대로 검사하므로, 게이트를 돌리기 전마다 다시 빌드하지 않으면 라운드를 옛
  빌드에 낭비합니다. 게이트는 로컬 페이지만 엽니다. 파일이거나 `localhost`, `127.0.0.1`, `[::1]`,
  `*.localhost`, `*.test`의 URL입니다.
- 라운드가 아직 열려 있는 빌드에 `--start`를 해도 라운드는 초기화되지 않습니다. 검사 대상인 페이지, URL,
  root, kind, category, primary만 갱신됩니다. `--start --new`는 새 빌드를 시작합니다. `--rounds N`(기본
  3)은 빌드를 시작할 때만 설정합니다.
- 그 폴더에 열린 빌드가 없으면 `start.mjs deal`도 폴더를 켭니다. `css`와 `brand`는 켜지 않습니다.

## 하는 일

- **빌드가 활성 상태**인 때는 프로젝트 폴더(또는 한두 단계 아래)에 `.taste-skill/build.json`이 있는 동안,
  또는 `.taste-skill/gate.json`이 라운드가 아직 열려 있다고 말하는 동안입니다. 마커를 지워도 빌드는
  끝나지 않습니다. 열린 빌드의 한두 단계 아래 폴더에서 `start.mjs deal`을 하면 두 번째 빌드를 켜지 않고
  그 빌드에 합류합니다.
- **페이지:** 지정한 것, 없으면 마커의 페이지나 URL, 없으면 `index.html`, 없으면 유일한 `.html` 파일,
  없으면 그것이 있는 유일한 하위 폴더의 `index.html`입니다.
- **검사**는 하나씩, 각각 새 프로필의 헤드리스 Chrome 안에서 돌립니다.
  `consistency.mjs --quick --widths 1440,390`(페이지가 선언한 kind, 없으면 마커의 kind와, 그 category,
  primary, root로, 6단계에서 돌리는 방식 그대로)과 `assets/layout/check.mjs --sizes 1440x900,390x844`입니다.
  consistency 실행에는 `empty-area`(컨테이너 안에서 35% 넘게 비면 WARN, 50% 넘게 비면 FAIL)와 `basics`
  블록(이름, alt, 레이블, 제목 순서, Tab 순회, lang, head 태그, 지도 링크, 가정한 사실)이 들어 있습니다.
  이들의 FAIL은 다른 것과 똑같이 막고, WARN(skip-link, share-meta, 두 번 나오는 action-repeat, assumed,
  양식의 `.example` 대체 값)은 절대 막지 않습니다. 빠른 실행은 6단계의 전체 실행만 검사하는 것을
  뺍니다. `forms`, `reduced-motion`, `hover-move`, `hover-spill`, `loop-pause`, `hidden-visual`, 스크롤
  순회입니다. 390 너비에서는 폰 검사(`collide`, `tap-size`)가 더해지고, 320에서 화면 밖으로 나가는
  것이 있는지 순회하며(`off-viewport`), `hidden-content`는 스크립트를 끈 채로도 페이지를 불러옵니다.
  그 밖에 파일에서 읽는 두 가지가 있습니다.
  - **kit-edited**: 페이지가 `assets/`에서 불러오는 파일이 스킬의 사본과 다릅니다(공백, 따옴표,
    세미콜론, 쉼표는 제외하므로 포매터는 수정이 아닙니다). 예전 스킬 버전의 키트 사본도 해당합니다.
    현재 것을 복사하세요.
  - **checker-gaming**: 페이지 자신의 코드가 `navigator.webdriver`, `window.__playwright`,
    `callPhantom`, 검사기의 `__cc` 훅을 테스트합니다(코드만 해당하며 문자열 안의 코드 예시는 테스트가
    아닙니다).
  - **gaming-suspect**(면제 가능): "headless"에 대한 user-agent 테스트, 또는 셀렉터가 찾은 모든 사진에서
    `aria-hidden`을 벗겨 내는 코드입니다. 키트 자신의 `assets/motion/motion.js`는 `HeadlessChrome`을
    테스트합니다(`shot()`: 헤드리스 브라우저에서는 페이지가 `data-motion="live"`를 설정하지 않는 한
    카운트와 히어로 등장 효과가 쓰인 그대로, 끝난 상태로 놓입니다). 바뀌지 않은 키트 사본은 텍스트로
    건너뜁니다. 그것을 번들하거나 포팅한 빌드(프레임워크의 `src/lib/motion.js`,
    `dist/assets/index-*.js`)는 키트의 그 줄 때문에 이 발견을 받으며, "the kit's motion.js shot() test,
    ported unchanged"를 이유로 면제합니다.
  - **문구**(면제 가능): 페이지 파일에 `scripts/copy-lint.mjs --json --kind <kind>`를 돌리고, 파일에
    섹션이 없으면(빌드된 앱, 개발 서버) 검사기의 브라우저가 만든 페이지에 돌립니다. 둘 다 안 되면 문구는
    검사하지 않은 것으로 올라가며 통과로 처리되지 않습니다. 그 FAIL은 막습니다(`copy-residue`,
    `copy-slop-word`, `copy-stock-phrase`, 예산의 두 배에 하나를 더한 횟수 이상 쓴 장치(두 조각 제목과
    숫자 쌍 제목, 대비 프레임, 부정의 연속, 미덕 단어. 라이더, 과장, 폭로, 반복된 약속은 WARN만),
    Kestrel이나 Halcyon으로 지은 브랜드). 그 WARN은 나열만 하고 막지 않습니다(`copy.md`,
    `copy-tells.md`. `copy-brand-word`는 고객 자신의 이름 안에 있는 목록의 단어입니다). 이것들은
    copy-lint의 id이고, 검사기의 copy-headline, copy-fact 등은 따로 있습니다. 브라우저 없이 1초 안에
    끝납니다.

  텍스트가 키트 파일과 같은 파일은 어디에 있든 키트의 것입니다. 두 검사기가 한 섹션의 한 결함에 붙이는
  id(section-height / screen-height / screen-short, one-section / neighbour)는 하나의 발견입니다. 전체
  실행은 CPU Chrome에서 몇 분 걸립니다.
- **WARN은 절대 막지 않습니다.** 다만 검사기는 WARN만 하고 게이트는 FAIL로 붙드는 하우스 규칙이 둘
  있습니다. `hero-enter`(히어로에 `data-enter`가 없거나 `html.m-enter`를 설정하는 head 줄이 없음)와
  `moment-none`(페이지가 모먼트를 뽑지 않음)입니다. 처음 몇 개의 WARN을 나열합니다.
- **면제.** 거짓이라고 판단한 FAIL은 `.taste-skill/waivers.json`에 넣습니다.

  ```json
  [{ "check": "one-section", "target": "section#visit", "reason": "the hours list is one screen at 390; the check counts the phone bar" }]
  ```

  `check`는 발견의 id, `target`은 그 위치의 일부(3자 이상, 짧은 위치는 전체), `reason`은 12자 이상입니다.
  면제 하나는 발견 하나를 덮습니다. 여러 개와 맞는 target은 무시되고 "name one"이라고 알려 줍니다.
  문구 단어, 상투 문구, 잔여물 적중은 각각 하나의 발견이며 그 단어와 문장으로 이름 붙입니다. 습관처럼 쓴
  문구 장치는 하나의 발견이며, 게이트가 출력하는 위치 전체(횟수와 적중 목록)로만 면제하므로 나중에
  추가된 것은 덮이지 않습니다. 고객 자신의 문구가 쓰는 단어(브리프가 인용함)는 브리프를 이유로 건별로
  면제합니다. 면제된 FAIL은 WAIVED로 출력되며 보고서에 들어갑니다. kit-edited와 checker-gaming은 면제할
  수 없습니다. 면제가 5개를 넘으면 그 자체가 FAIL입니다. "too many waivers: fix instead".
- **라운드**(`.taste-skill/gate.json`). 마지막 라운드 이후 페이지나 면제가 바뀐 실행은 한 라운드이고,
  바뀌지 않은 페이지를 손으로 다시 돌리는 것은 라운드가 아닙니다. 빌드에서 게이트를 손으로 처음 돌리기
  전의 훅 중단도 라운드가 아닙니다. FAIL을 나열하고 막으며(그 막힘은 따로 셉니다), 손으로 처음 돌린
  실행이 그 페이지의 라운드를 셉니다. 그래서 빌드 중간에 사용자에게 묻는 일은 비용이 들지 않습니다.
  훅이 막은 뒤 바뀌지 않은 페이지에서의 다음 종료는 라운드 없이 한 번 허용됩니다(사용자에게 묻는 경우.
  막힘 메시지가 "just stop again"이라고 합니다). 그 페이지의 다른 종료는 라운드 없이 두 번 막고("nothing
  changed"), 그 뒤로는 각각 한 라운드로 셉니다. 변경이 있으면 그 세기는 다시 시작합니다. 마지막 라운드
  전에는 FAIL, 고침, 다시 종료입니다. 마지막 라운드에서 게이트가 "rounds used up"이라고 한 번
  말하면 고치기를 멈추고, 열려 있는 FAIL을 보고서에 넣고 끝냅니다. 그 뒤의 모든 종료는 허용됩니다.
  PASS와 마지막 라운드의 OPEN은 `build.json`을 `build.done.json`으로 바꾸므로, 나중의 뽑기는 자기만의
  빌드를 시작합니다.
- **사용자가 끝낼 때.** 사용자가 멈추라고 하거나 페이지를 있는 그대로 내보내라고 할 때만
  `gate.mjs --done "<what they said>"`(12자 이상)가 그 말로 빌드를 닫습니다. `gate.json`의 status가
  `done`이 되고, `build.json`은 `build.done.json`으로 바뀌며, 그 뒤의 모든 종료가 허용됩니다. 마지막
  줄은 `GATE: DONE (...)`이며, 그 줄과 사용자의 말과 열려 있는 FAIL을 보고서에 넣습니다. 페이지가 이
  정도면 됐다는 스스로의 판단으로는 절대 쓰지 않습니다. 그것이 라운드가 있는 이유입니다.
- **에이전트를 가두지 않습니다.** 모든 막힘은 `.taste-skill/gate-blocks.json`에 세며, `--start`는 이를
  절대 지우지 않습니다. 한 빌드에서 라운드 수에 4를 더한 횟수의 막힘(손으로 처음 돌리기 전의 막힘은
  그만큼을 따로 가짐)이나 그 폴더에서 6시간 동안 30번의 막힘을 넘으면 모든 종료를 허용합니다. 페이지가
  없거나, 프레임워크 셸이거나, 검사가 죽거나 9.5분을 넘기면 할 일을 알려 주며 한 번 막고, 그 뒤에는
  허용합니다. 죽거나 시간 초과된 실행은 그 페이지에 대해 저장되며, 바뀌지 않은 페이지의 이후 종료는
  검사를 다시 돌리는 대신 그것을 재사용합니다(에이전트가 아직 듣지 못했다면 최대 한 번 더). 각 검사는
  게이트가 죽으면 그 검사와 Chrome을 죽이는 워치독과 함께 돌고, 그 밖의 것은 절대 죽이지 않습니다.

## 수동 게이트

```bash
node <skill>/scripts/gate.mjs index.html
```

마지막 줄은 정확히 다음 중 하나입니다.

```
GATE: PASS
GATE: FAIL <n> (round <k> of <max>)
GATE: OPEN <n> (rounds used up)
GATE: QUICK <n> (not a round; run without --quick to finish)
GATE: SETUP (...)
GATE: ERROR (...)
GATE: OFF (no build active)
GATE: DONE (<the user's words>)      after --done
```

PASS는 끝내라는 뜻입니다. FAIL은 나열된 것을 고치고 다시 돌립니다. OPEN은 고치기를 멈추고 열려 있는
FAIL과 면제를 보고서에 넣습니다. QUICK은 라운드 사이에 보는 것이며 빌드의 마지막 줄이 될 수 없습니다.
SETUP(페이지가 아직 없음, 프레임워크의 소스 셸, 로컬이 아닌 페이지)은 브라우저가 열 수 있는 것을
켜고(위의 `--start`) 다시 돌립니다. ERROR(검사 자체를 돌리지 못함)나 OFF(여기에 켜진 빌드가 없음)는 그
줄을 보고서에 넣고 끝내며, 다시 돌리지 않습니다. 줄 위에는 열려 있는 모든 FAIL과 그 위치와 고치는
방법, 모든 면제, 처음 몇 개의 WARN이 나옵니다. `--quick`(1440과 390의 검사기, 1440의 레이아웃 검사)은
라운드가 아닙니다. 잘라 낸 이미지는 `.taste-skill/gate/consistency`에 있습니다.

## 훅으로 쓰기

Claude Code에서는 스킬이 호출되면 스킬 자신의 frontmatter가 게이트를 Stop 훅으로 추가합니다. 명령은 POSIX
`sh` 한 줄(Windows는 Git Bash, macOS와 Linux는 `sh`)이며, 처음 찾은 `gate.mjs`를 이 순서로 실행합니다.
`$CLAUDE_SKILL_DIR/scripts/`, `$CLAUDE_PLUGIN_ROOT/scripts/`,
`$CLAUDE_PLUGIN_ROOT/skills/taste-skill/scripts/`(플러그인 설치)는 각각 그 변수가 설정돼 있을 때만
보고, 그다음 이름으로 찾는 설치 폴더 `$CLAUDE_PROJECT_DIR/.claude/skills/design-taste-frontend/`,
`$CLAUDE_PROJECT_DIR/.agents/skills/design-taste-frontend/`, `~/.claude/skills/design-taste-frontend/`,
`~/.agents/skills/design-taste-frontend/`(`npx skills`, `install.sh`)를 봅니다. 하나도 찾지 못하면
훅 오류 없이 종료가 허용됩니다. 폴더에 `.taste-skill`이 있으면
`.taste-skill/gate-hook-missing.txt`(시각과 읽은 변수)를 쓰고, 거기나 한 단계 아래에 빌드가 켜져 있으면
stderr에 `tasteskill gate: gate.mjs not found (CLAUDE_PLUGIN_ROOT=...)`를 출력하므로, 게이트에 닿지 못한
훅이 대화 기록에 드러납니다. 다른 폴더 이름으로 설치한 스킬, 다른 앱, 스킬 훅이 없는 Claude Code는
아래 중 하나를 씁니다. 각각은 프로젝트의 모든 세션에서 돌며 자기 폴더나 한두 단계 아래의 빌드를 찾습니다.
활성 빌드가 없는 곳에서는 즉시 종료하지만, 폴더나 그 한 단계 아래에서 지난 하루 안에 바뀌었고 한 번도
켜진 적 없는 tasteskill 페이지(`page-type` 메타가 있는 것)에 대해서는 한 번 켜는 방법을 알려 줍니다
(`.taste-skill/unarmed.json`이 알렸다는 사실을 기록합니다). 처음 막는 세션 하나만 붙들고, 빌드가 두 개
이상의 하위 폴더에 있는 오케스트레이터는 멈추게 하며, 24시간 동안 놀고 있는 빌드는 무시합니다.
`/path/to/skill`을 스킬 폴더로 바꿉니다.

**Claude Code**, `.claude/settings.json`(stdout의 JSON으로 막음):

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "node \"/path/to/skill/scripts/gate.mjs\" --hook claude", "timeout": 600 } ] }
    ]
  }
}
```

**Codex**, `.codex/hooks.json`(Claude Code와 같은 출력: `{"decision":"block","reason":...}`):

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "node \"/path/to/skill/scripts/gate.mjs\" --hook codex", "timeout": 600 } ] }
    ]
  }
}
```

**Antigravity**, `.agents/hooks.json`(에이전트가 계속 일하게 하려고 `{"decision":"continue","reason":...}`로 답함):

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "node \"/path/to/skill/scripts/gate.mjs\" --hook antigravity", "timeout": 600 } ] }
    ]
  }
}
```

모든 모드에서 게이트는 아무것도 출력하지 않고 0으로 종료해서 중단을 허용합니다. 훅의 stdin JSON(최대
2초)에서 `cwd`와 `session_id`를 읽습니다. `stop_hook_active`는 라운드를 일찍 끝내지 않으며, `gate.json`의
라운드 수가 끝냅니다.

모든 훅 호출은 `gate.json`의 `history`에 항목을 하나 남기며, 허용된 중단도 마찬가지입니다. `"mode": "hook"`,
`host`, `"decision": "allow"` 또는 `"block"`, 짧은 `reason`이 들어갑니다(검사를 돌렸다면 그 status, FAIL
수, 라운드가 더해집니다). PASS 뒤나 라운드를 다 쓴 뒤에는 그 빌드의 `gate.json`에 들어가고, 켜진 빌드가
없으면 폴더나 한두 단계 아래의 가장 새로운 `gate.json`에, 그것도 없으면 폴더 자신의 `.taste-skill`이
있을 때 거기에 들어갑니다. 새 `.taste-skill` 폴더를 만들지 않으며, 오케스트레이션하는 세션이 붙들고 있지
않은 아래 빌드에는 절대 쓰지 않습니다. 항목만 남기면 파일의 시각이 유지되므로, 놀고 있는 빌드가
활성처럼 보이게 되는 일은 없습니다.

스킬이 추가한 훅은 메인 세션의 것입니다. 스킬을 불러온 서브에이전트는 붙들리지 않고 그 부모가 대신
붙들립니다. 수동 게이트는 서브에이전트 안에서 돌립니다.
