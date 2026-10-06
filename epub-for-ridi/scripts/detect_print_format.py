#!/usr/bin/env python3
"""인쇄본 PDF에서 볼드·소제목·블록인용 검출 (출발점 스크립트).

PDF 텍스트 레이어의 단어 좌표 + 렌더 픽셀의 수평 잉크 런 중앙값으로
단어별 굵기를 추정하고, 줄/문단 단위로 서식을 분류한다.

출력 JSON (기본 print_format.json):
  { "<printed_page>": [ {kind, x, y, text, bold:[[s,e],...]} ] }
  kind: h(소제목) | p(문단) | q(블록인용) | li(목록)

중요: 아래 CONFIG 값은 특정 책(Strike!) 실측값이다. 다른 책에 쓰려면
first/last(0-based 페이지 인덱스), offset(인쇄 페이지 = index-offset+1),
head_y(머리글 높이 pt), dpi를 반드시 조정하고 검출 결과를 눈으로 확인한다.

의존성: pymupdf, numpy
"""
import json
from collections import Counter

import pymupdf
import numpy as np

# ---- CONFIG (책마다 조정) ----
SRC = "book.pdf"
OUT = "print_format.json"
DPI = 400
FIRST, LAST = 8, 236          # 0-based page index 범위
OFFSET = 7                    # printed_page = page_index - OFFSET
HEAD_Y = 38.0                 # 이 높이(pt) 위의 단어는 머리글로 보고 제외
DARK = 110                    # 이 값 미만 픽셀을 잉크로 봄 (회색조)
BOLD_ABS = 1.6                # 굵기 임계 = max(본문중앙값+1.6, 본문중앙값*1.28)
BOLD_REL = 1.28
GAP_PAR = 15.5                # 이 값 초과 세로 간격이면 새 문단
GAP_HEAD = 11.0               # 제목 후보 최소 간격
INDENT = 8.0                  # 본문 기준선 대비 들여쓰기 허용 오차(pt)
# -----------------------------

STOP = {"on", "the", "a", "an", "of", "to", "and", "in", "for", "with", "that",
        "is", "was", "were", "be", "been", "as", "at", "by", "from", "or", "but",
        "not", "it", "this", "its", "their", "his", "her", "you", "we", "they",
        "he", "she", "which", "who", "when", "if"}


def looks_heading(t):
    """질문형(?/!) 제목을 살리기 위해 ?!는 종결부호에서 제외한다."""
    if not (2 < len(t) < 52):
        return False
    if t[-1] in ".,;:'\")\u2019\u201d\u2026-\u2014":
        return False
    if t.startswith(("\u2022", "-", "\u2013", "(")):
        return False
    ws = t.split()
    if not ws or len(ws) > 8:
        return False
    if ws[-1].lower().strip(".,;:!?") in STOP:
        return False
    return True


def stroke_of(arr, sc, x0, y0, x1, y1):
    """단어 bbox 안 수평 잉크 런 길이의 중앙값."""
    sub = arr[max(0, int(y0 * sc)):int(y1 * sc), max(0, int(x0 * sc)):int(x1 * sc)]
    dk = sub < DARK
    runs = []
    for row in dk:
        c = 0
        for v in row:
            if v:
                c += 1
            elif c:
                runs.append(c)
                c = 0
        if c:
            runs.append(c)
    runs = [r for r in runs if 1 <= r <= 60]
    return float(np.median(runs)) if runs else 0.0


def append_word(text, marks, w, bold):
    """단어 사이 공백을 문자 하나로 계산해 오프셋 밀림을 막는다."""
    if text and not text.endswith(("-", "/")):
        text += " "
        marks.append(False)
    text += w
    marks.extend([bold] * len(w))
    return text


def main():
    doc = pymupdf.open(SRC)
    sc = DPI / 72.0
    out = {}
    for pno in range(FIRST, LAST + 1):
        page = doc[pno - 1]
        printed = pno - OFFSET
        pm = page.get_pixmap(dpi=DPI, colorspace=pymupdf.csGRAY)
        arr = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width)
        words = []
        for x0, y0, x1, y1, w, b, l, wn in page.get_text("words"):
            if y0 < HEAD_Y:
                continue
            st = stroke_of(arr, sc, x0, y0, x1, y1)
            if st <= 0:
                continue
            words.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1,
                          "w": w, "b": b, "l": l, "st": st})
        if not words:
            out[printed] = []
            continue
        body = float(np.median([w["st"] for w in words]))
        bold_th = max(body + BOLD_ABS, body * BOLD_REL)

        lines = {}
        for w in words:
            lines.setdefault((w["b"], w["l"]), []).append(w)
        order = sorted(lines, key=lambda k: (min(x["y0"] for x in lines[k]),
                                             min(x["x0"] for x in lines[k])))
        L = []
        for k in order:
            ws = sorted(lines[k], key=lambda x: x["x0"])
            med = float(np.median([x["st"] for x in ws]))
            L.append({"y": min(x["y0"] for x in ws), "x": min(x["x0"] for x in ws),
                      "ws": ws, "line_bold": med >= bold_th})
        L.sort(key=lambda d: (d["y"], d["x"]))
        unit = float(Counter(round(l["x"] / 2) * 2 for l in L).most_common(1)[0][0])

        paras = []
        cur = None
        prev = None

        def flush():
            nonlocal cur
            if cur:
                paras.append(cur)
                cur = None

        for l in L:
            gap = l["y"] - prev["y"] if prev else 999.0
            indented = l["x"] > unit + INDENT
            bullet = any(w["w"].startswith("\u2022") for w in l["ws"])
            lt = " ".join(w["w"] for w in l["ws"])
            heading = (l["line_bold"] and looks_heading(lt)
                       and l["x"] <= unit + 10 and gap > GAP_HEAD)
            if not heading and prev is not None and gap > 12.5 \
                    and looks_heading(lt) and l["x"] <= unit + 10:
                heading = True
            newpar = (cur is None) or gap > GAP_PAR or bullet \
                or (indented and (prev is None or prev["x"] <= unit + INDENT))

            if heading:
                flush()
                paras.append({"kind": "h", "x": l["x"], "y": l["y"],
                              "text": lt,
                              "bold": [[0, len(lt)]]})
            elif bullet:
                flush()
                ws = [w for w in l["ws"] if w["w"] != "\u2022"]
                cur = {"kind": "li", "x": l["x"], "y": l["y"], "text": "",
                       "marks": [], "lxs": [l["x"]]}
                for w in ws:
                    cur["text"] = append_word(cur["text"], cur["marks"],
                                              w["w"], w["st"] >= bold_th)
            elif cur is not None and cur["kind"] in ("p", "li") and not newpar:
                cur["lxs"].append(l["x"])
                for w in l["ws"]:
                    cur["text"] = append_word(cur["text"], cur["marks"],
                                              w["w"], w["st"] >= bold_th)
            else:
                flush()
                cur = {"kind": "p", "x": l["x"], "y": l["y"], "text": "",
                       "marks": [], "lxs": [l["x"]]}
                for w in l["ws"]:
                    cur["text"] = append_word(cur["text"], cur["marks"],
                                              w["w"], w["st"] >= bold_th)
            prev = l
        flush()

        for p in paras:
            lxs = p.pop("lxs", [p["x"]])
            # 블록인용: 문단의 '모든' 줄이 본문 기준선보다 오른쪽일 때만.
            # (첫 줄만 들여쓰는 일반 문단·리스트 hanging indent는 제외)
            if p["kind"] == "p":
                n = len(lxs)
                ind = sum(1 for x in lxs if x > unit + INDENT)
                if (n >= 1 and ind == n and min(lxs) > unit + 6
                        and len(p["text"]) >= 40 and len(p["text"].split()) >= 5):
                    p["kind"] = "q"
            marks = p.pop("marks", [])
            runs = []
            i = 0
            while i < len(marks):
                if marks[i]:
                    j = i
                    while j < len(marks) and marks[j]:
                        j += 1
                    runs.append([i, j])
                    i = j
                else:
                    i += 1
            p["bold"] = runs
        out[printed] = paras

    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    nh = sum(1 for v in out.values() for p in v if p["kind"] == "h")
    nq = sum(1 for v in out.values() for p in v if p["kind"] == "q")
    nb = sum(1 for v in out.values() for p in v if p["bold"])
    nl = sum(1 for v in out.values() for p in v if p["kind"] == "li")
    print("paras", sum(len(v) for v in out.values()),
          "| heading", nh, "| quote", nq, "| bold-para", nb, "| li", nl)


if __name__ == "__main__":
    main()
