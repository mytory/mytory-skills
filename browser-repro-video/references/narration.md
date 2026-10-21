# 음성 설명(내레이션)

읽기용 대본 `.srt`의 큐를 Supertonic 3(한국어, 목소리는 무작위로 하나)로 합성해 큐 시작 시각에 맞춰 mp4에 입힌다. 설치·경로는 `supertonic-tts` 스킬을 따른다(`~/Supertonic/.venv/bin/python`, 모델 캐시 `~/Supertonic/.model-cache`). 재설치하지 않는다.

## 화면 자막과 읽기용 대본

두 파일을 따로 둔다. 화면 자막을 고치지 않는다.

| 파일 | 내용 | 쓰임 |
|---|---|---|
| `영상.srt` (화면 자막) | 화면에 보이는 글자 그대로. 영어·숫자·이름을 살린다(`oacore`, `9001`, `"Saved"`) | 녹화 때 프레임에 박힌 캡션, 보고서용 `.srt`·`.vtt` |
| `영상-speech.srt` (읽기용 대본) | 같은 큐 번호·시각. 문장만 귀로 듣기 좋게 바꾼다 | `narrate.mjs`가 음성으로 합성 |

읽기용 대본 쓰는 법:

1. `영상.srt`를 `영상-speech.srt`로 복사한다. 큐 번호와 시각 줄은 건드리지 않고 문장 줄만 고친다.
2. 문장은 쓰는 음성 엔진 스킬의 대본 규칙대로 고친다. 기본 엔진은 Supertonic이므로 **`supertonic-tts` 스킬을 먼저 읽고** 그 "음성 합성" 절의 대본 규칙을 따른다. `narrate.mjs`는 Supertonic을 직접 부르므로 그 스킬이 저절로 읽히지 않는다.
3. 다시 읽어 의미와 수치가 화면 자막과 같은지 확인한다.

`narrate.mjs`는 `영상-speech.srt`가 있으면 그것을 쓴다. 큐 수·시각이 `영상.srt`와 다르면 합성하지 않고 종료 코드 1로 끝난다. 엔진의 대본 규칙에 어긋나면 엔진 어댑터 `tts-batch.py`가 남은 부분을 출력하고 멈춘다(종료 코드 3).

## 흐름

```bash
cd 저장폴더
# 0. final.srt를 보고 final-speech.srt를 쓴다(위 절)
node ~/.claude/skills/browser-repro-video/scripts/narrate.mjs final.mp4 --plan   # 1. 검사 + 합성 + 계획표. 대본 규칙 위반, 초과/밀림 있으면 0이 아닌 종료 코드
node ~/.claude/skills/browser-repro-video/scripts/narrate.mjs final.mp4          # 2. final-narrated.mp4 생성
ffprobe -v error -show_streams final-narrated.mp4 | grep codec_type              # 3. video + audio 두 스트림 확인
```

옵션: `--srt 읽기용.srt`(기본 `영상-speech.srt`, 없으면 `영상.srt`), `--out 출력.mp4`, `--voice random`(기본. 처음 한 번 고른 목소리를 `.narration/voice`에 적어 두고 그 영상에는 계속 쓴다), `--lang ko`.

산출물: `영상-narrated.mp4`, `narration-plan.json`(큐별 시작·배치 시각·음성 길이·여유·초과·밀림), `.narration/`(큐별 WAV·텍스트 캐시, 전달할 결과물에 넣지 않음).

## 배치 규칙

- 음성은 큐 시작 시각에 놓는다. 앞 음성이 아직 재생 중이면 끝난 뒤 0.25초 후로 민다 → `drift`.
- `room` = 이 큐 시작부터 다음 큐 시작까지. `overflow = duration - room`이 0.5초를 넘거나 `drift`가 2초를 넘으면 `--plan`이 경고하고 실패한다. **영상 속도를 늦추거나 음성을 빠르게 돌리지 않는다.** 캡션을 줄이거나 그 장면의 `hold`를 늘려 다시 찍는다(한국어 음성은 대략 1초에 5~6글자).
- 영상 트랙은 `-c:v copy`라 화질·길이가 바뀌지 않는다. 오디오는 AAC 96k 모노.
- **정지 화면 허용은 30초**(소리가 흐르는 동안은 멈춰도 된다). 녹화 때 `REC_NARRATION=1`로 `holdToRead` 상한을 30초로 올리고, 검수는 `check-freeze.sh 영상.mp4 30`. 단 내레이션 영상에서도 소리 없는 정지는 5초까지만 허용하는데, check-freeze는 오디오를 구분하지 못하므로 이런 구간은 눈으로 확인한다.

## 기호 처리

- `tts-batch.py`의 `SPOKEN` 표가 `→ · ≤ ≥ + % px # / |` 와 괄호·따옴표를 말로 바꾸거나 쉼표로 바꾼다. 그래도 모델이 "unsupported character"로 거부하면 그 문자만 지우고 한 번 더 합성한다(stderr에 기록).
- 이 표는 기호만 바꾼다. 영어·숫자 같은 엔진별 발음은 읽기용 대본에서 엔진 스킬의 규칙대로 직접 풀어 쓴다.

## 성능

- 모델은 한 번 로드하고 큐를 순서대로 합성한다. 큐당 수 초(M1 Mac 기준 58큐 ≈ 8분).
- `.narration/<id>.txt`에 적힌 문장과 같으면 다시 합성하지 않는다. 캡션을 일부만 고쳤을 때 빠르다. 큐 순서가 바뀌면 id가 달라져 다시 합성되므로 순서 변경은 마지막에.
