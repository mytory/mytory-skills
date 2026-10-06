---
name: supertonic-tts
description: 에이전트 작업 보고나 내레이션을 로컬 Supertonic 3로 한국어 WAV로 만들 때 사용합니다. 미설치 시 환경 준비, 텍스트 파일 합성, CLI, 요청된 경우 로컬 HTTP API를 안내합니다.
---

# Supertonic TTS

사용자 계정의 `~/Supertonic/.venv/bin/python`과 `~/Supertonic/.model-cache`를 이용합니다. 기존 환경이 있으면 재설치하지 않습니다.

## 설치 확인과 미설치 시 준비

먼저 가상환경의 Python이 존재하는지 확인한 뒤 SDK와 CLI를 확인합니다.

```sh
rtk proxy test -x ~/Supertonic/.venv/bin/python
rtk proxy ~/Supertonic/.venv/bin/python -c 'from supertonic import TTS; import importlib.metadata; print(importlib.metadata.version("supertonic"))'
rtk proxy ~/Supertonic/.venv/bin/supertonic tts --help
```

가상환경이 없을 때만 다음 명령으로 만듭니다. Python 3.9 이상과 `venv`가 필요하며, 없으면 운영체제의 Python 설치 방법으로 준비한 뒤 진행합니다. 저장소를 복제할 필요 없이 Python SDK를 설치하면 아래 헬퍼와 CLI를 사용할 수 있습니다.

```sh
rtk proxy mkdir -p ~/Supertonic
rtk proxy python3 -m venv ~/Supertonic/.venv
```

가상환경은 있지만 `supertonic` 패키지가 없거나, 위에서 새로 만든 경우에만 설치합니다.

```sh
rtk proxy ~/Supertonic/.venv/bin/python -m pip install supertonic
```

설치 후 위의 SDK·CLI 확인을 다시 실행합니다. 합성은 아래 텍스트 파일 예제로 확인하고 출력 WAV를 재생합니다. 첫 합성에는 Hugging Face 모델 다운로드를 위한 인터넷 연결과 약 400MB의 모델 저장 공간이 필요합니다. 헬퍼는 캐시 경로를 설정하며 CLI·서버에서는 `SUPERTONIC_CACHE_DIR`을 지정해 같은 캐시를 사용합니다.

HTTP 서버를 요청받았을 때만 같은 가상환경에 추가 의존성을 설치합니다.

```sh
rtk proxy ~/Supertonic/.venv/bin/python -m pip install 'supertonic[serve]'
rtk proxy ~/Supertonic/.venv/bin/supertonic serve --help
```

설치·서버 의존성의 공식 근거: [Supertonic Python 패키지](https://pypi.org/project/supertonic/).

## 음성 합성

반복해서 대본 파일을 WAV로 만들 때는 UTF-8 텍스트 파일을 사용합니다. 한국어 대본을 셸 명령에 직접 넣으면 따옴표와 문장부호가 잘못 해석될 수 있으므로 파일 입력을 우선합니다.

```sh
rtk proxy ~/Supertonic/.venv/bin/python \
  ~/.agents/skills/supertonic-tts/scripts/synthesize.py \
  --text-file /path/to/narration.txt \
  --output /path/to/narration.wav \
  --voice M2 --lang ko
```

헬퍼는 `--voice` 기본값 `M2`, `--lang` 기본값 `ko`를 사용하며 출력 WAV 경로를 인자로 받습니다. SDK를 직접 쓸 때는 `TTS(auto_download=True)`, `get_voice_style(voice_name="M2")`, `synthesize(..., lang="ko")`, `save_audio(...)`를 사용합니다. 패키지 기본 모델은 `supertonic-3`입니다.

요청 범위가 내레이션 WAV 생성이면 WAV 경로를 전달하고 마칩니다. 사용자가 별도로 요청한 경우에만 ffmpeg나 전체 영상 제작 흐름을 연결합니다.

짧은 문장은 CLI로도 만들 수 있습니다.

```sh
rtk proxy env SUPERTONIC_CACHE_DIR=~/Supertonic/.model-cache \
  ~/Supertonic/.venv/bin/supertonic tts \
  '작업을 완료했습니다.' -o output.wav --lang ko --voice M2
```

HTTP 연동이 필요할 때만 서버를 포그라운드로 실행합니다.

```sh
rtk proxy env SUPERTONIC_CACHE_DIR=~/Supertonic/.model-cache \
  ~/Supertonic/.venv/bin/supertonic serve \
  --host 127.0.0.1 --port 7788
```

`POST http://127.0.0.1:7788/v1/audio/speech` 본문은 JSON 객체로 전달합니다. 설치된 서버 스키마에서 `lang` 필드를 지원하는 것을 확인했습니다.

```json
{
  "model": "supertonic-3",
  "input": "에이전트 작업 보고가 완료되었습니다.",
  "voice": "M2",
  "response_format": "wav",
  "lang": "ko"
}
```

HTTP 클라이언트의 구조화된 JSON 직렬화를 사용하고 JSON 문자열을 직접 이어붙이지 않습니다. 서버는 `127.0.0.1`에만 바인딩하고 사용 후 Ctrl+C로 종료합니다. 사용자가 명시적으로 요청하지 않으면 백그라운드 상시 실행이나 자동 시작을 설정하지 않습니다.
