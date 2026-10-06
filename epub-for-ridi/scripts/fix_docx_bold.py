#!/usr/bin/env python3
"""DOCX 볼드/밑줄 복원 — Calibre 변환 후처리.

Calibre가 HTML의 <strong>을 캐릭터 스타일(예: Text0/Text1)로 매핑하면서
<w:b/> 없이 색상만 남겨 DOCX에서 볼드가 사라지는 사례가 있다. 이 스크립트는
그런 캐릭터 스타일에 <w:b/>·<w:bCs/>를 주입한다.

--em-underline을 주면 한국어 표기 규칙(의미 강조는 이탤릭 대신 밑줄)에 맞춰:
  - <w:i> 캐릭터 스타일을 <w:u w:val="single"/>로 바꾸고
  - Calibre가 rStyle 없이 평문 run으로 떨어뜨린 강조 run(역주/서명 등)을 찾아
    <w:u w:val="single"/>를 주입한다.

휴리스틱: "TextN" id를 가진 캐릭터 스타일 중 <w:b>·<w:i>가 모두 없는 것을
볼드로 간주한다. 도구 버전에 따라 다를 수 있으므로 실행 전후로
word/styles.xml과 실제 렌더를 확인한다. 이탤릭이 굵어지는 오탐이 보이면
해당 styleId를 EXCLUDE에 넣는다.

사용: python3 fix_docx_bold.py [--em-underline] a.docx [b.docx ...]
"""
import sys, re, zipfile, os

STYLE_ID_RE = r'Text\d+'          # 필요 시 스타일 id 패턴을 조정
EXCLUDE = set()                    # 굵게 만들면 안 되는 styleId
ACCENT_RE = r'역주'                # 밑줄 주입 대상 강조 run의 텍스트 패턴(필요 시 확장)


def underline_italics(styles):
    """한국어는 의미 강조에 이탤릭을 쓰지 않는다. <w:i> 스타일을 밑줄로 바꾼다."""
    changed = []

    def repl(m):
        sid, rpr = m.group(1), m.group(2)
        if '<w:i ' not in rpr and '<w:i/>' not in rpr:
            return m.group(0)
        new = re.sub(r'<w:i\s+[^>]*/>', '', rpr).replace('<w:i/>', '')
        if '<w:u ' not in new and '<w:u/>' not in new:
            new = '<w:u w:val="single"/>' + new
        changed.append(sid)
        return m.group(0).replace(rpr, new)

    styles = re.sub(
        r'<w:style [^>]*w:styleId="(' + STYLE_ID_RE + r')".*?<w:rPr>(.*?)</w:rPr></w:style>',
        repl, styles, flags=re.S)
    return styles, sorted(set(changed))


def underline_note_runs(styles, document):
    """Calibre가 rStyle 없이 떨어뜨린 강조 run에 밑줄을 주입한다."""
    count = 0

    def repl(m):
        nonlocal count
        run = m.group(0)
        if '<w:u ' in run or '<w:u/>' in run:
            return run
        count += 1
        if '<w:rPr>' in run:
            return run.replace('<w:rPr>', '<w:rPr><w:u w:val="single"/>', 1)
        return run.replace('<w:t', '<w:rPr><w:u w:val="single"/></w:rPr><w:t', 1)

    document = re.sub(
        r'<w:r>(?:(?!</w:r>).)*?<w:t[^>]*>[^<]*' + ACCENT_RE + r'[^<]*</w:t>.*?</w:r>',
        repl, document, flags=re.S)
    return document, count


def fix(path, em_underline=False):
    tmp = path + ".tmp"
    zin = zipfile.ZipFile(path)
    names = zin.namelist()
    if 'word/styles.xml' not in names:
        zin.close()
        print(f"fix_docx_bold: {os.path.basename(path)}에 styles.xml 없음, 건너뜀")
        return
    styles = zin.read('word/styles.xml').decode('utf-8')

    italic_ids = []
    if em_underline:
        styles, italic_ids = underline_italics(styles)

    def patch(style_id, add):
        nonlocal styles
        m = re.search(
            r'(<w:style [^>]*w:styleId="%s".*?<w:rPr>)(.*?)(</w:rPr></w:style>)'
            % re.escape(style_id), styles, re.S)
        if not m:
            return False
        body = m.group(2)
        ins = ''.join(a for a in add if a not in body)
        if not ins:
            return False
        styles = styles[:m.start(2)] + ins + body + styles[m.end(2):]
        return True

    bold_ids = []
    for m in re.finditer(
            r'<w:style [^>]*w:styleId="(' + STYLE_ID_RE + r')".*?<w:rPr>(.*?)</w:rPr></w:style>',
            styles, re.S):
        sid, rpr = m.group(1), m.group(2)
        if sid in EXCLUDE or '<w:i ' in rpr or '<w:i/>' in rpr or '<w:b' in rpr:
            continue
        bold_ids.append(sid)

    changed = [sid for sid in bold_ids if patch(sid, ['<w:b/>', '<w:bCs/>'])]
    if italic_ids:
        changed.extend('underline:' + i for i in italic_ids)

    document, note_runs = (None, 0)
    if em_underline and 'word/document.xml' in names:
        document = zin.read('word/document.xml').decode('utf-8')
        document, note_runs = underline_note_runs(styles, document)

    if not changed and not note_runs:
        zin.close()
        print("fix_docx_bold: 변경 없음")
        return
    zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
    for n in names:
        data = zin.read(n)
        if n == 'word/styles.xml':
            data = styles.encode('utf-8')
        elif n == 'word/document.xml' and document is not None:
            data = document.encode('utf-8')
        zout.writestr(n, data)
    zout.close()
    zin.close()
    os.replace(tmp, path)
    print(f"fix_docx_bold: styles={changed}, underline-note-runs={note_runs} "
          f"in {os.path.basename(path)}")


if __name__ == '__main__':
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith('--')]
    em_underline = '--em-underline' in argv
    if not args:
        sys.exit("usage: python3 fix_docx_bold.py [--em-underline] file.docx [file2.docx ...]")
    for p in args:
        fix(p, em_underline=em_underline)
