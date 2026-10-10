# 음성 설명(내레이션)

캡션 `.srt`의 큐를 Supertonic 3(한국어, 기본 음성 M1)로 합성해 큐 시작 시각에 맞춰 mp4에 입힌다. 설치·경로는 `supertonic-tts` 스킬을 따른다(`~/Supertonic/.venv/bin/python`, 모델 캐시 `~/Supertonic/.model-cache`). 재설치하지 않는다.

## 흐름

```bash
cd 보고서폴더/videos
node ~/.claude/skills/browser-repro-video/scripts/narrate.mjs final.mp4 --plan   # 1. 합성 + 계획표. 초과/밀림 있으면 종료 코드 1
node ~/.claude/skills/browser-repro-video/scripts/narrate.mjs final.mp4          # 2. final-narrated.mp4 생성
ffprobe -v error -show_streams final-narrated.mp4 | grep codec_type              # 3. video + audio 두 스트림 확인
```

옵션: `--srt 읽기용.srt`(기본 `영상.srt`), `--out 출력.mp4`, `--voice M1`, `--lang ko`.

산출물: `영상-narrated.mp4`, `narration-plan.json`(큐별 시작·배치 시각·음성 길이·여유·초과·밀림), `.narration/`(큐별 WAV·텍스트 캐시, 보고서에 넣지 않음).

## 배치 규칙

- 음성은 큐 시작 시각에 놓는다. 앞 음성이 아직 재생 중이면 끝난 뒤 0.25초 후로 민다 → `drift`.
- `room` = 이 큐 시작부터 다음 큐 시작까지. `overflow = duration - room`이 0.5초를 넘거나 `drift`가 2초를 넘으면 `--plan`이 경고하고 실패한다. **영상 속도를 늦추거나 음성을 빠르게 돌리지 않는다.** 캡션을 줄이거나 그 장면의 `hold`를 늘려 다시 찍는다(한국어 음성은 대략 1초에 5~6글자).
- 영상 트랙은 `-c:v copy`라 화질·길이가 바뀌지 않는다. 오디오는 AAC 96k 모노.
- **정지 화면 허용은 30초**(소리가 흐르는 동안은 멈춰도 된다). 녹화 때 `REC_NARRATION=1`로 `holdToRead` 상한을 30초로 올리고, 검수는 `check-freeze.sh 영상.mp4 30`. 단 내레이션 영상에서도 소리 없는 정지는 5초까지만 허용하는데, check-freeze는 오디오를 구분하지 못하므로 이런 구간은 눈으로 확인한다.

## 캡션을 읽히는 문장으로

- 화면 캡션과 읽기용 문장이 달라야 하면 큐 시각이 같은 `.srt`를 하나 더 만들어 `--srt`로 넘긴다. 녹화 스크립트에서 `cap(S, 화면용)`과 별개로 읽기용 문자열을 모아 두면 `merge-captions.mjs`와 같은 방식으로 합칠 수 있다.
- `tts-batch.py`의 `SPOKEN` 표가 `→ · ≤ ≥ + % px # / |` 와 괄호·따옴표를 말로 바꾸거나 쉼표로 바꾼다. 그래도 모델이 "unsupported character"로 거부하면 그 문자만 지우고 한 번 더 합성한다(stderr에 기록).
- 숫자·단위·영문 약어는 모델이 읽는 대로 나온다. 꼭 정확히 읽혀야 하면 한글로 풀어 쓴다(예: "픽셀", "에이트 제로 에이트 제로" 대신 "포트 팔천팔십").
- 커밋 해시·URL·파일 경로는 읽어도 의미가 없다. 읽기용 문장에서는 뺀다.

## 성능

- 모델은 한 번 로드하고 큐를 순서대로 합성한다. 큐당 수 초(M1 Mac 기준 58큐 ≈ 8분).
- `.narration/<id>.txt`에 적힌 문장과 같으면 다시 합성하지 않는다. 캡션을 일부만 고쳤을 때 빠르다. 큐 순서가 바뀌면 id가 달라져 다시 합성되므로 순서 변경은 마지막에.

## 보고서

- 내레이션 본을 `<video controls>`의 소스로 쓰고 `<track kind="subtitles" src="final.vtt">`를 함께 둔다. 캡션은 영상에 박혀 있으니 소리를 끄고 봐도 된다.
- `narration-plan.json`은 증거 폴더에 두고, 보고서에는 "음성 설명 N큐, 합계 M초, 밀림 최대 K초"를 한 줄 적는다.
