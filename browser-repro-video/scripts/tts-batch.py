#!/usr/bin/env python3
"""캡션 여러 개를 Supertonic 3로 한 번에 WAV로 만든다 (narrate.mjs가 호출).

입력 JSON(stdin 또는 --input): [{"id": "001", "text": "..."}, ...]
출력 JSON(stdout): [{"id": "001", "path": ".../001.wav", "duration": 3.21}, ...]

모델은 한 번만 로드한다. 같은 텍스트는 <id>.txt에 적힌 이전 텍스트와 비교해 바뀌지 않았으면 다시 만들지 않는다.
실행: ~/Supertonic/.venv/bin/python tts-batch.py --out-dir DIR [--voice M1] [--lang ko]
"""

import argparse
import json
import os
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
    parser.add_argument("--voice", default="M1")
    parser.add_argument("--lang", default="ko")
    args = parser.parse_args()

    cues = json.loads(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for cue in cues:
        cue["spoken"] = spoken(cue["text"])

    todo = []
    for cue in cues:
        wav = args.out_dir / f"{cue['id']}.wav"
        txt = args.out_dir / f"{cue['id']}.txt"
        if wav.exists() and txt.exists() and txt.read_text(encoding="utf-8") == cue["spoken"]:
            continue
        todo.append(cue)

    if todo:
        os.environ["SUPERTONIC_CACHE_DIR"] = str(MODEL_CACHE)
        from supertonic import TTS  # 무거우니 필요할 때만 import

        tts = TTS(auto_download=True)
        style = tts.get_voice_style(voice_name=args.voice)
        for cue in todo:
            wav_data, _ = synthesize_lenient(tts, cue["spoken"], args.lang, style)
            wav = args.out_dir / f"{cue['id']}.wav"
            tts.save_audio(wav_data, str(wav))
            (args.out_dir / f"{cue['id']}.txt").write_text(cue["spoken"], encoding="utf-8")
            print(f"합성 {cue['id']}: {cue['spoken'][:40]}", file=sys.stderr)

    result = []
    for cue in cues:
        wav = args.out_dir / f"{cue['id']}.wav"
        result.append({"id": cue["id"], "path": str(wav), "duration": round(wav_seconds(wav), 3)})
    json.dump(result, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
