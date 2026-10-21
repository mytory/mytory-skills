#!/usr/bin/env python3
"""캡션 여러 개를 Supertonic 3로 한 번에 WAV로 만든다 (narrate.mjs가 호출).

입력 JSON(stdin 또는 --input): [{"id": "001", "text": "..."}, ...]
출력 JSON(stdout): [{"id": "001", "path": ".../001.wav", "duration": 3.21}, ...]

모델은 한 번만 로드한다. <id>.txt에 적힌 이전 목소리·문장과 같으면 다시 만들지 않는다.
실행: ~/Supertonic/.venv/bin/python tts-batch.py --out-dir DIR [--voice random] [--lang ko]
"""

import argparse
import json
import os
import random
import re
import sys
import wave
from pathlib import Path

MODEL_CACHE = Path("~/Supertonic/.model-cache")


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


# 캡션에 흔한 기호를 읽을 수 있는 말로. 그 밖의 미지원 문자는 synthesize가 알려 주면 지우고 다시 시도한다.
SPOKEN = {
    "≤": " 이하 ", "≥": " 이상 ", "→": " 에서 ", "←": " 으로 ", "↔": " 와 ",
    "·": ", ", "•": ", ", "—": ", ", "–": ", ", "…": ". ", "~": " 에서 ",
    "+": " 플러스 ", "%": " 퍼센트", "&": " 그리고 ", "#": " 번 ", "/": " 또는 ", "|": ", ",
    "(": ", ", ")": ", ", "[": ", ", "]": ", ", "{": " ", "}": " ", "`": "", "\"": "", "'": "",
    "px": "픽셀",
}


def spoken(text: str) -> str:
    for k, v in SPOKEN.items():
        text = text.replace(k, v)
    text = " ".join(text.split())
    return text.replace(" ,", ",").replace(",,", ",").strip(" ,")


def synthesize_lenient(tts, text, lang, style):
    """미지원 문자가 있으면 그 문자만 지우고 한 번 더 시도한다."""
    try:
        return tts.synthesize(text=text, lang=lang, voice_style=style)
    except ValueError as e:
        msg = str(e)
        if "unsupported character" not in msg:
            raise
        bad = [c.strip("'") for c in msg[msg.index("[") + 1:msg.rindex("]")].split(", ")]
        cleaned = text
        for c in bad:
            cleaned = cleaned.replace(c, " ")
        print(f"미지원 문자 제거 {bad}: {text[:40]}", file=sys.stderr)
        return tts.synthesize(text=" ".join(cleaned.split()), lang=lang, voice_style=style)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="큐 JSON 파일. 없으면 stdin")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--voice", default="random", help="목소리 이름(F1~F5, M1~M5). random이면 처음 한 번 무작위로 고른다")
    parser.add_argument("--lang", default="ko")
    args = parser.parse_args()

    cues = json.loads(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for cue in cues:
        cue["spoken"] = spoken(cue["text"])

    # Supertonic은 한국어 문장 속 영어·숫자를 제대로 읽지 못한다. supertonic-tts 스킬의 대본 규칙대로 풀어 써야 한다.
    if args.lang == "ko":
        latin = [cue for cue in cues if re.search(r"[A-Za-z0-9]", cue["spoken"])]
        if latin:
            print(f"대본에 영문자·숫자가 남은 큐 {len(latin)}개. supertonic-tts 스킬의 대본 규칙대로 한글 발음으로 풀어 쓴다:", file=sys.stderr)
            for cue in latin:
                print(f"  {cue['id']}: {cue['text']}", file=sys.stderr)
            sys.exit(3)

    # random은 처음 한 번만 고르고 기록해 둔다. --plan과 실제 합성, 재실행이 같은 목소리를 쓰게 하려는 것이다.
    voice_file = args.out_dir / "voice"
    voice = args.voice
    if voice == "random" and voice_file.exists():
        voice = voice_file.read_text(encoding="utf-8").strip()

    # 캐시는 목소리와 문장이 모두 같을 때만 재사용한다. 목소리가 섞이지 않게 하려는 것이다.
    def cache_key(cue):
        return f"{voice}\n{cue['spoken']}"

    todo = []
    for cue in cues:
        wav = args.out_dir / f"{cue['id']}.wav"
        txt = args.out_dir / f"{cue['id']}.txt"
        if voice != "random" and wav.exists() and txt.exists() and txt.read_text(encoding="utf-8") == cache_key(cue):
            continue
        todo.append(cue)

    if todo:
        os.environ["SUPERTONIC_CACHE_DIR"] = str(MODEL_CACHE)
        from supertonic import TTS  # 무거우니 필요할 때만 import

        tts = TTS(auto_download=True)
        if voice == "random":
            voice = random.choice(tts.voice_style_names)
            voice_file.write_text(voice, encoding="utf-8")
        print(f"목소리: {voice}", file=sys.stderr)
        style = tts.get_voice_style(voice_name=voice)
        for cue in todo:
            wav_data, _ = synthesize_lenient(tts, cue["spoken"], args.lang, style)
            wav = args.out_dir / f"{cue['id']}.wav"
            tts.save_audio(wav_data, str(wav))
            (args.out_dir / f"{cue['id']}.txt").write_text(cache_key(cue), encoding="utf-8")
            print(f"합성 {cue['id']}: {cue['spoken'][:40]}", file=sys.stderr)

    result = []
    for cue in cues:
        wav = args.out_dir / f"{cue['id']}.wav"
        result.append({"id": cue["id"], "path": str(wav), "duration": round(wav_seconds(wav), 3)})
    json.dump(result, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
