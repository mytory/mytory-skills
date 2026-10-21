#!/usr/bin/env python3
"""Generate a WAV from a UTF-8 text file with the installed Supertonic 3 SDK."""

import argparse
import os
import random
import re
from pathlib import Path


MODEL_CACHE = Path("~/Supertonic/.model-cache")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--voice", default="random", help="목소리 이름(F1~F5, M1~M5). random이면 무작위로 고른다")
    parser.add_argument("--lang", default="ko")
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8")
    if not text.strip():
        parser.error("--text-file must contain text")
    # 한국어 문장 속 영어·숫자는 제대로 읽히지 않는다. SKILL.md의 대본 규칙대로 풀어 쓴 대본만 받는다.
    if args.lang == "ko" and re.search(r"[A-Za-z0-9]", text):
        left = sorted(set(re.findall(r"[A-Za-z0-9][A-Za-z0-9_.:%-]*", text)))
        parser.error(f"대본에 영문자·숫자가 남아 있다: {', '.join(left[:20])}. 한글 발음으로 풀어 쓴 뒤 다시 실행한다.")

    os.environ["SUPERTONIC_CACHE_DIR"] = str(MODEL_CACHE)
    from supertonic import TTS

    tts = TTS(auto_download=True)
    voice = random.choice(tts.voice_style_names) if args.voice == "random" else args.voice
    print(f"목소리: {voice}")
    style = tts.get_voice_style(voice_name=voice)
    wav, duration = tts.synthesize(text=text, lang=args.lang, voice_style=style)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tts.save_audio(wav, str(args.output))
    print(f"Saved {args.output} ({duration[0]:.2f}s, {tts.sample_rate} Hz)")


if __name__ == "__main__":
    main()
