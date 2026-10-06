#!/usr/bin/env python3
"""Generate a WAV from a UTF-8 text file with the installed Supertonic 3 SDK."""

import argparse
import os
from pathlib import Path


MODEL_CACHE = Path("~/Supertonic/.model-cache")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--voice", default="M1")
    parser.add_argument("--lang", default="ko")
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8")
    if not text.strip():
        parser.error("--text-file must contain text")

    os.environ["SUPERTONIC_CACHE_DIR"] = str(MODEL_CACHE)
    from supertonic import TTS

    tts = TTS(auto_download=True)
    style = tts.get_voice_style(voice_name=args.voice)
    wav, duration = tts.synthesize(text=text, lang=args.lang, voice_style=style)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tts.save_audio(wav, str(args.output))
    print(f"Saved {args.output} ({duration[0]:.2f}s, {tts.sample_rate} Hz)")


if __name__ == "__main__":
    main()
