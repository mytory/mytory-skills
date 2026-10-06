#!/usr/bin/env python3
"""EPUB을 리디북스 규격에 맞게 보정한다.

처리 항목:
  1. 공개 CP 검증기 호환용 NCX 생성 및 OPF 연결 (EPUB-302).
     기존 NCX는 보존하고 없을 때 nav 문서에서 생성한다. 현재 앱 지원 보증은 아니다.
  2. NCX content src의 './' 접두 제거 (EPUB-301)
  3. OPF 매니페스트·스파인에 NCX 등록
  4. body에 적용되는 크기·배경 속성 제거 (CSS-301, HTML-303)
     — Calibre가 body를 클래스 선택자로 옮겨 검증기를 우회하므로,
       body/html 태그의 class를 읽어 그 클래스도 함께 처리한다.

사용법:
    python3 fix_epub_for_ridi.py <book.epub>

제자리(in-place) 수정한다. 종료 코드: 0=성공(보정 또는 변경 없음), 2=오류.
"""

import os
import posixpath
import re
import shutil
import sys
import zipfile
from html.parser import HTMLParser
from html import unescape as html_unescape
from urllib.parse import urlsplit, urlunsplit
from xml.sax.saxutils import escape, quoteattr
from xml.etree import ElementTree as ET


# --------------------------------------------------------------------------
# nav.xhtml → toc.ncx
# --------------------------------------------------------------------------

class _NavParser(HTMLParser):
    """EPUB3 nav.xhtml의 TOC를 중첩 트리로 파싱한다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []
        self._lists = [self.items]
        self.in_nav = False
        self._in_anchor = False
        self._href = ''
        self._text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'nav':
            if a.get('epub:type') == 'toc' or a.get('type') == 'toc':
                self.in_nav = True
            return
        if not self.in_nav:
            return
        if tag == 'ol':
            top = self._lists[-1]
            if top and top[-1].get('href'):
                self._lists.append(top[-1]['children'])
            else:
                self._lists.append(top)
        elif tag == 'a':
            self._in_anchor = True
            self._href = a.get('href', '')
            self._text = []

    def handle_endtag(self, tag):
        if tag == 'a':
            if self.in_nav and self._in_anchor:
                self._lists[-1].append({
                    'href': self._href,
                    'text': ''.join(self._text).strip(),
                    'children': [],
                })
            self._in_anchor = False
        elif tag == 'ol' and self.in_nav:
            if len(self._lists) > 1:
                self._lists.pop()
        elif tag == 'nav' and self.in_nav:
            self.in_nav = False

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if self.in_nav and self._in_anchor:
            self._text.append(data)


def _clean_href(href):
    """NCX content src 정규화. './' 접두만 제거한다 (EPUB-301).

    str.lstrip('./')은 선행 '.', '/' 문자를 모두 지워 '../x'를 'x'로
    망가뜨리므로 쓰지 않는다.
    """
    return re.sub(r'^\./', '', href)


def _rebase_href(href, source_path, target_path):
    """source_path 기준 href를 target_path 기준으로 바꾼다."""
    parts = urlsplit(href)
    if parts.scheme or parts.netloc:
        return href
    source_dir = posixpath.dirname(source_path)
    target_dir = posixpath.dirname(target_path) or '.'
    resolved = (posixpath.normpath(posixpath.join(source_dir, parts.path))
                if parts.path else source_path)
    rebased = posixpath.relpath(resolved, target_dir)
    return urlunsplit(('', '', rebased, parts.query, parts.fragment))


def _rebase_nav_hrefs(nodes, nav_path, ncx_path):
    for node in nodes:
        node['href'] = _rebase_href(node['href'], nav_path, ncx_path)
        _rebase_nav_hrefs(node['children'], nav_path, ncx_path)


def _write_navpoints(nodes, lines, counter, indent):
    for node in nodes:
        counter[0] += 1
        play = counter[0]
        lines.append('%s<navPoint id="navPoint-%d" playOrder="%d">'
                     % (indent, play, play))
        lines.append('%s  <navLabel><text>%s</text></navLabel>'
                     % (indent, escape(node['text'])))
        lines.append('%s  <content src=%s/>'
                     % (indent, quoteattr(_clean_href(node['href']))))
        if node['children']:
            _write_navpoints(node['children'], lines, counter, indent + '  ')
        lines.append('%s</navPoint>' % indent)


def build_ncx(nav_html, uid, title, lang='ko', nav_path=None, ncx_path=None):
    parser = _NavParser()
    parser.feed(nav_html)
    parser.close()
    if not parser.items or not any(n.get('href') for n in parser.items):
        raise RuntimeError('nav.xhtml 에서 목차 항목을 찾지 못했습니다. '
                           'Calibre에서 --level1-toc 등으로 목차를 지정했는지 확인하세요.')
    if nav_path and ncx_path:
        _rebase_nav_hrefs(parser.items, nav_path, ncx_path)

    def depth_of(nodes, d=1):
        best = d
        for n in nodes:
            if n['children']:
                best = max(best, depth_of(n['children'], d + 1))
        return best

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" '
        '"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">',
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" '
        'xml:lang=%s version="2005-1">' % quoteattr(lang),
        '  <head>',
        '    <meta name="dtb:uid" content=%s/>' % quoteattr(uid),
        '    <meta name="dtb:depth" content="%d"/>' % depth_of(parser.items),
        '    <meta name="dtb:totalPageCount" content="0"/>',
        '    <meta name="dtb:maxPageNumber" content="0"/>',
        '  </head>',
        '  <docTitle><text>%s</text></docTitle>' % escape(title),
        '  <navMap>',
    ]
    _write_navpoints(parser.items, lines, [0], '    ')
    lines.append('  </navMap>')
    lines.append('</ncx>')
    return '\n'.join(lines) + '\n'


# --------------------------------------------------------------------------
# OPF / CSS 패치
# --------------------------------------------------------------------------

def patch_opf(opf, ncx_href='toc.ncx'):
    """실제 NCX 항목의 id로 매니페스트와 spine을 연결한다."""
    root = ET.fromstring(opf)
    namespace = root.tag.partition('}')[0][1:] if root.tag.startswith('{') else ''
    prefix = '{%s}' % namespace if namespace else ''
    if namespace:
        ET.register_namespace('', namespace)
    ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
    manifest = root.find(prefix + 'manifest')
    spine = root.find(prefix + 'spine')
    if manifest is None or spine is None:
        raise FixError('OPF manifest 또는 spine이 없습니다.')
    item = next((e for e in manifest if e.get('media-type') == 'application/x-dtbncx+xml'), None)
    if item is None:
        used = {e.get('id') for e in manifest}
        ncx_id = 'ncx'
        while ncx_id in used:
            ncx_id += '-toc'
        item = ET.SubElement(manifest, prefix + 'item', {
            'id': ncx_id, 'href': ncx_href, 'media-type': 'application/x-dtbncx+xml'})
    if not item.get('id'):
        raise FixError('기존 NCX 항목에 id가 없습니다.')
    if not item.get('href'):
        item.set('href', ncx_href)
    if spine.get('toc') == item.get('id') and item.get('href') == ncx_href and opf.find('application/x-dtbncx+xml') >= 0:
        return opf
    spine.set('toc', item.get('id'))
    return ET.tostring(root, encoding='unicode')


def _opf_metadata(opf, name):
    try:
        root = ET.fromstring(opf)
    except ET.ParseError:
        m = re.search(r'<dc:%s\b[^>]*>(.*?)</dc:%s\s*>' % (name, name), opf, re.S)
        return html_unescape(m.group(1)) if m else ''
    for element in root.iter():
        if element.tag.rsplit('}', 1)[-1] == name:
            return ''.join(element.itertext()).strip()
    return ''


def _clean_existing_ncx(ncx):
    """기존 NCX의 content src에서 불필요한 './' 접두를 제거한다."""
    def clean_tag(match):
        tag = match.group(0)
        return re.sub(
            r'(\bsrc\s*=\s*)(["\'])(.*?)\2',
            lambda attr: attr.group(1) + attr.group(2)
            + _clean_href(attr.group(3)) + attr.group(2),
            tag, count=1)

    return re.sub(r'<(?:[\w.-]+:)?content\b[^>]*>', clean_tag, ncx)


def find_body_classes(html_texts):
    """본문 파일들에서 body/html 태그에 붙은 클래스명을 모은다.

    Calibre는 `body { ... }`를 `body class="calibreN"` + `.calibreN { ... }`
    로 바꿔 내보낸다. 리디 검증기는 선택자가 정확히 `body`일 때만 잡으므로
    검사를 통과하지만 뷰어에는 크기 제한이 그대로 적용된다. 클래스명을
    알아내 같은 기준으로 제거한다. 클래스 이름은 변환마다 달라지므로
    하드코딩하지 않는다.
    """
    classes = set()
    for text in html_texts:
        for m in re.finditer(r'<(?:body|html)\b[^>]*\bclass="([^"]*)"', text, re.I):
            for cls in m.group(1).split():
                classes.add(cls.strip().lower())
    return classes


def strip_body_dimensions(css_text, body_classes=()):
    """body/html에 적용되는 규칙에서 크기·배경 속성을 제거한다.

    CSS-301(width/height 계열)과 HTML-303(background-color) 대응.
    완전한 CSS 파서가 아니라 리디가 문제 삼는 속성만 제거한다.
    제거 후 빈 규칙이 되면 규칙 자체를 삭제한다.
    """
    banned = ('max-width', 'min-width', 'width', 'max-height', 'min-height',
              'height', 'background-color', 'background')
    targets = {'html', 'body'} | {c for c in body_classes if c}

    def fix_rule(m):
        selector, body = m.group(1), m.group(2)
        bases = []
        for sel in selector.split(','):
            sel = sel.strip().lower()
            # 후손결합·의사클래스 제거 후 클래스 접두 '.' 제거
            sel = sel.split()[-1].rsplit(':', 1)[0].lstrip('.')
            bases.append(sel)
        if not any(b in targets for b in bases):
            return m.group(0)
        kept = []
        for d in body.split(';'):
            d = d.strip()
            if not d:
                continue
            prop = d.split(':', 1)[0].strip().lower()
            if prop not in banned:
                kept.append(d)
        if not kept:
            return ''
        return '%s { %s }' % (selector.strip(), '; '.join(kept))

    return re.sub(r'([^{}]+)\{([^{}]*)\}', fix_rule, css_text)


# --------------------------------------------------------------------------
# 메인
# --------------------------------------------------------------------------

class FixError(Exception):
    pass


def fix_epub(epub_path, add_ncx=True, strip_css=True, verbose=True):
    """EPUB을 제자리에서 보정한다. 변경이 있으면 True를 반환."""
    with zipfile.ZipFile(epub_path) as z:
        names = z.namelist()
        infos = {i.filename: i for i in z.infolist()}
        data = {n: z.read(n) for n in names if not n.endswith('/')}

    # OPF 경로
    opf_name = None
    if 'META-INF/container.xml' in data:
        m = re.search(rb'full-path="([^"]+)"', data['META-INF/container.xml'])
        if m:
            opf_name = m.group(1).decode()
    if not opf_name or opf_name not in data:
        raise FixError('OPF(content.opf)를 찾지 못했습니다.')
    opf_dir = opf_name.rsplit('/', 1)[0] + '/' if '/' in opf_name else ''
    opf = data[opf_name].decode('utf-8', 'ignore')

    changed = []

    # NCX 항목과 nav는 파일명 대신 OPF 등록 정보를 우선한다.
    try:
        package = ET.fromstring(opf)
    except ET.ParseError as e:
        raise FixError('OPF XML 파싱 실패: %s' % e)
    items = [e for e in package.iter() if e.tag.rsplit('}', 1)[-1] == 'item']
    ncx_item = next((e for e in items if e.get('media-type') == 'application/x-dtbncx+xml'), None)
    ncx_href = ncx_item.get('href') if ncx_item is not None else None
    ncx_path = posixpath.normpath(opf_dir + ncx_href) if ncx_href else None
    if ncx_path is None:
        ncx_path = next((n for n in names if n.endswith('.ncx')), opf_dir + 'toc.ncx')
        ncx_href = posixpath.relpath(ncx_path, opf_dir or '.')
    if add_ncx:
        if ncx_path not in data:
            nav_item = next((e for e in items if 'nav' in e.get('properties', '').split()), None)
            nav_key = (posixpath.normpath(opf_dir + nav_item.get('href', ''))
                       if nav_item is not None else None)
            if nav_key not in data:
                nav_key = next((n for n in names if n.endswith('nav.xhtml')), None)
            if nav_key is None:
                raise FixError('nav 문서가 없어 NCX를 생성할 수 없습니다.')
            ncx = build_ncx(data[nav_key].decode('utf-8'),
                            _opf_metadata(opf, 'identifier'), _opf_metadata(opf, 'title'),
                            _opf_metadata(opf, 'language') or 'ko', nav_key, ncx_path)
            data[ncx_path] = ncx.encode('utf-8')
            names.append(ncx_path)
            changed.append('%s 생성' % ncx_path)
        cleaned = _clean_existing_ncx(data[ncx_path].decode('utf-8'))
        if cleaned.encode('utf-8') != data[ncx_path]:
            data[ncx_path] = cleaned.encode('utf-8')
            changed.append('기존 NCX의 ./ 접두 제거')
        new_opf = patch_opf(opf, ncx_href)
        if new_opf != opf:
            data[opf_name] = new_opf.encode('utf-8')
            changed.append('OPF의 NCX 연결 보정')

    # 2) CSS 보정
    if strip_css:
        html_names = [x for x in names
                      if x.lower().endswith(('.html', '.xhtml', '.htm'))]
        body_classes = find_body_classes(
            [data[x].decode('utf-8', 'ignore') for x in html_names])
        for n in [x for x in names if x.lower().endswith('.css')]:
            css = data[n].decode('utf-8', 'ignore')
            fixed = strip_body_dimensions(css, body_classes)
            if fixed != css:
                data[n] = fixed.encode('utf-8')
                changed.append('%s: body 크기·배경 속성 제거' % n)

    if not changed:
        if verbose:
            print('보정 대상 변경 사항 없음.')
        return False

    # 재패킹: mimetype 첫 엔트리 + 무압축
    tmp = epub_path + '.ridi.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        zi = zipfile.ZipInfo('mimetype')
        zi.compress_type = zipfile.ZIP_STORED
        out.writestr(zi, data.get('mimetype', b'application/epub+zip'))
        for n in names:
            if n == 'mimetype' or n.endswith('/'):
                continue
            info = infos.get(n)
            if info is not None:
                out.writestr(info, data[n])
            else:
                out.writestr(n, data[n])

    shutil.move(tmp, epub_path)
    if verbose:
        print('보정 완료:')
        for c in changed:
            print('  - %s' % c)
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    if not zipfile.is_zipfile(path):
        print('EPUB 파일이 아닙니다: %s' % path)
        return 2
    try:
        fix_epub(path)
    except FixError as e:
        print('오류: %s' % e, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
