#!/usr/bin/env python3
"""RIDI Books 업로드 전 EPUB 점검 스크립트.

2018년에 보관 처리된 CP 업로드용 공개 검증기의 일부 규칙을 검사한다.
공식 검증기 전체나 현재 앱 표시를 대체하지 않는다.

사용법:
    python3 check_ridi.py <book.epub> [--config defaults.config]

종료 코드:
    0 = 오류 없음 (경고만 있거나 통과)
    1 = 리디 오류 규칙 위반 발견
    2 = 파일을 열 수 없음
"""

import argparse
import os
import re
import struct
import sys
import zipfile
from xml.etree import ElementTree as ET

# 리디 검증기 config/defaults.config 기본값
DEFAULTS = {
    'image_compare_type': 1,
    'cover_image_min_width': 560,
    'cover_image_min_height': 800,
    'cover_image_recommend_width': 1120,
    'cover_image_recommend_height': 1600,
    'content_image_max_width': 1080,
    'content_image_max_height': 1600,
    'image_file_max_size': 5000,      # KB
    'html_file_max_size': 300,        # KB
    'html_file_recommend_file_size': 150,
    'child_nodes_limit': 500,
}

# html/body에서 금지되는 CSS 속성 (CSS-301: width/height/max-width/max-height)
DIMENSION_PROPS = ('width', 'height', 'max-width', 'max-height',
                   'min-width', 'min-height')


class Finding:
    __slots__ = ('code', 'severity', 'message')

    def __init__(self, code, severity, message):
        self.code = code
        self.severity = severity
        self.message = message

    def __str__(self):
        return '[%s] %s: %s' % (self.severity, self.code, self.message)


def _read_config(path):
    cfg = dict(DEFAULTS)
    if not path or not os.path.isfile(path):
        return cfg
    for line in open(path, encoding='utf-8'):
        line = line.split('//')[0].strip()
        if not line or ':' not in line:
            continue
        k, v = line.split(':', 1)
        k, v = k.strip(), v.strip()
        try:
            cfg[k] = int(v)
        except ValueError:
            cfg[k] = v
    return cfg


def _jpeg_size(data):
    if data[:2] != b'\xff\xd8':
        return None
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack('>HH', data[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg = struct.unpack('>H', data[i + 2:i + 4])[0]
        i += 2 + seg
    return None


def _png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    w, h = struct.unpack('>II', data[16:24])
    return w, h


def _gif_size(data):
    if data[:6] not in (b'GIF87a', b'GIF89a'):
        return None
    w, h = struct.unpack('<HH', data[6:10])
    return w, h


def image_size(data):
    for fn in (_png_size, _gif_size, _jpeg_size):
        size = fn(data)
        if size:
            return size
    return None


def _strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def _css_rules(css):
    """(selector_lowercase, {prop: value}) 목록으로 단순 파싱."""
    out = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', _strip_comments(css)):
        selectors = [s.strip().lower() for s in m.group(1).split(',')]
        decls = {}
        for d in m.group(2).split(';'):
            if ':' in d:
                k, v = d.split(':', 1)
                decls[k.strip().lower()] = v.strip()
        if decls:
            out.append((selectors, decls))
    return out


def check(epub_path, cfg):
    findings = []
    if not zipfile.is_zipfile(epub_path):
        return None, findings

    with zipfile.ZipFile(epub_path) as z:
        names = z.namelist()
        bad_zip = z.testzip()
        data = {n: z.read(n) for n in names if not n.endswith('/')}

    if bad_zip:
        findings.append(Finding('ZIP', '오류', '손상된 엔트리: %s' % bad_zip))

    # --- mimetype 규칙 ---
    with zipfile.ZipFile(epub_path) as z:
        infos = z.infolist()
    if infos and infos[0].filename == 'mimetype':
        if infos[0].compress_type != zipfile.ZIP_STORED:
            findings.append(Finding('MIME-001', '오류',
                                    'mimetype이 압축되어 있음(STORED여야 함)'))
    else:
        findings.append(Finding('MIME-001', '오류',
                                'mimetype이 첫 엔트리가 아님'))

    # --- OPF / NCX (EPUB-302) ---
    opf_name = None
    if 'META-INF/container.xml' in data:
        try:
            root = ET.fromstring(data['META-INF/container.xml'])
            ns = {'c': 'urn:oasis:names:tc:opendocument:xmlns:container'}
            rf = root.find('.//c:rootfile', ns)
            if rf is not None:
                opf_name = rf.get('full-path')
        except ET.ParseError as e:
            findings.append(Finding('OPF-001', '오류', 'container.xml 파싱 실패: %s' % e))

    opf = data.get(opf_name, b'').decode('utf-8', 'ignore') if opf_name else ''

    has_ncx_item = 'application/x-dtbncx+xml' in opf
    ncx_href = None
    for m in re.finditer(r'<item\b[^>]*>', opf):
        tag = m.group(0)
        if 'application/x-dtbncx+xml' in tag:
            hm = re.search(r'href="([^"]+)"', tag)
            if hm:
                ncx_href = hm.group(1)

    if not has_ncx_item:
        findings.append(Finding('EPUB-302', '오류',
                                'NCX 파일(media-type="application/x-dtbncx+xml")이 '
                                '매니페스트에 없음 → 리디 뷰어가 목차를 못 읽음'))

    if not re.search(r'<spine\b[^>]*\btoc=', opf):
        findings.append(Finding('EPUB-002', '경고',
                                '<spine toc="ncx"> 속성이 없음(EPUB2 호환 목차 연결 누락)'))

    # NCX 내용 검사 (EPUB-301: './' 금지)
    if ncx_href:
        ncx_data = data.get(opf_name.rsplit('/', 1)[0] + '/' + ncx_href
                            if opf_name and '/' in opf_name else ncx_href)
        if ncx_data is None:
            findings.append(Finding('EPUB-302', '오류',
                                    'NCX 파일을 찾을 수 없음: %s' % ncx_href))
        else:
            ncx = ncx_data.decode('utf-8', 'ignore')
            try:
                ET.fromstring(ncx)
            except ET.ParseError as e:
                findings.append(Finding('EPUB-401', '오류', 'NCX XML 파싱 실패: %s' % e))
            for src in re.findall(r'<content\s+src="([^"]+)"', ncx):
                if src.startswith('./'):
                    findings.append(Finding('EPUB-301', '오류',
                                            "NCX 경로가 './'로 시작: %s" % src))
                    break

    # --- CSS 규칙 ---
    html_names = [n for n in names
                  if n.lower().endswith(('.html', '.xhtml', '.htm'))]
    body_classes = set()
    for n in html_names:
        for m in re.finditer(r'<(?:body|html)\b[^>]*\bclass="([^"]*)"',
                             data[n].decode('utf-8', 'ignore'), re.I):
            for cls in m.group(1).split():
                body_classes.add(cls.strip().lower())

    css_files = [n for n in names if n.lower().endswith('.css')]
    for n in css_files:
        css = data[n].decode('utf-8', 'ignore')
        for selectors, decls in _css_rules(css):
            for sel in selectors:
                base = sel.split()[-1].rsplit(':', 1)[0].lstrip('.')
                if base == 'img' and decls.get('position') == 'relative':
                    findings.append(Finding('CSS-303', '오류',
                                            'img에 position:relative 사용 금지'))
                dim_prop = next((p for p in decls if p in DIMENSION_PROPS), None)
                if not dim_prop:
                    continue
                if base in ('html', 'body'):
                    # 리디 검증기가 실제로 잡는 형태
                    findings.append(Finding(
                        'CSS-301', '오류',
                        '%s { %s } — html/body의 크기 조절 속성 금지'
                        % (base, dim_prop)))
                elif base in body_classes:
                    # Calibre가 body를 클래스로 옮겨 검증기를 우회한 형태.
                    # 리디 검증기는 통과하지만 뷰어에는 적용될 수 있다.
                    findings.append(Finding(
                        'CSS-301-L', '경고',
                        '%s { %s } — body에 적용되는 클래스. '
                        '리디 검증기는 선택자가 정확히 body일 때만 검사하므로 '
                        '통과하지만, 뷰어 렌더링에 영향을 줄 수 있다'
                        % (base, dim_prop)))
            for prop in decls:
                if prop.startswith('column'):
                    findings.append(Finding('CSS-302', '오류',
                                            '%s — 다단(column) 속성 금지' % prop))
                if prop == 'position' and decls[prop] == 'fixed':
                    findings.append(Finding('CSS-006', '오류',
                                            'position:fixed 사용 금지'))
                if prop == 'word-break' and decls[prop] == 'break-all':
                    findings.append(Finding('CSS-201', '경고',
                                            'word-break:break-all — 양끝정렬 시 줄 끝 들쭉날쭉'))

    # --- HTML 규칙 ---
    html_files = [n for n in names if n.lower().endswith(('.html', '.xhtml', '.htm'))]
    for n in html_files:
        raw = data[n]
        size_kb = len(raw) / 1024.0
        if size_kb > cfg['html_file_max_size']:
            findings.append(Finding(
                'HTML-301', '오류',
                '%s — 본문 파일 %.0fKB (한도 %dKB)'
                % (n, size_kb, cfg['html_file_max_size'])))
        elif size_kb > cfg['html_file_recommend_file_size']:
            findings.append(Finding(
                'HTML-301', '경고',
                '%s — 본문 파일 %.0fKB (권장 %dKB 이하)'
                % (n, size_kb, cfg['html_file_recommend_file_size'])))

        text = raw.decode('utf-8', 'ignore')
        if 'background-color' in text:
            # 큰따옴표/작은따옴표/비인용 style 속성 모두 검사
            for m in re.finditer(r'<body\b[^>]*>', text, re.I):
                tag = m.group(0)
                style_m = re.search(
                    r'''style\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))''',
                    tag, re.I)
                if style_m:
                    style_val = next(g for g in style_m.groups() if g is not None)
                    if re.search(r'background-color', style_val, re.I):
                        findings.append(Finding('HTML-303', '오류',
                                                'body 인라인 background-color 금지'))
                        break

    # --- 이미지 규칙 ---
    cover_href = None
    for m in re.finditer(r'<item\b[^>]*>', opf):
        tag = m.group(0)
        if 'properties="' in tag and 'cover-image' in tag:
            hm = re.search(r'href="([^"]+)"', tag)
            if hm:
                cover_href = hm.group(1)

    for n in names:
        if not n.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            continue
        raw = data[n]
        size_kb = len(raw) / 1024.0
        if size_kb > cfg['image_file_max_size']:
            findings.append(Finding('IMG-303', '오류',
                                    '%s — 이미지 %.0fKB (한도 %dKB)'
                                    % (n, size_kb, cfg['image_file_max_size'])))
        size = image_size(raw)
        if not size:
            continue
        w, h = size
        is_cover = cover_href and n.endswith(os.path.basename(cover_href))
        area_mode = cfg['image_compare_type'] == 1
        if is_cover:
            minimum = cfg['cover_image_min_width'] * cfg['cover_image_min_height']
            too_small = (w * h < minimum if area_mode else
                         w < cfg['cover_image_min_width'] or h < cfg['cover_image_min_height'])
            if too_small:
                findings.append(Finding(
                    'IMG-305' if area_mode else 'IMG-301', '오류',
                    '표지 %s %dx%d — 최소 %dx%d 필요'
                    % (n, w, h, cfg['cover_image_min_width'],
                       cfg['cover_image_min_height'])))
            elif (w * h < cfg['cover_image_recommend_width'] * cfg['cover_image_recommend_height']
                  if area_mode else
                  w < cfg['cover_image_recommend_width'] or h < cfg['cover_image_recommend_height']):
                findings.append(Finding(
                    'IMG-RECOMMEND', '경고',
                    '표지 %s %dx%d — 권장 %dx%d'
                    % (n, w, h, cfg['cover_image_recommend_width'],
                       cfg['cover_image_recommend_height'])))
        else:
            maximum = cfg['content_image_max_width'] * cfg['content_image_max_height']
            too_large = (w * h > maximum if area_mode else
                         w > cfg['content_image_max_width'] and h > cfg['content_image_max_height'])
            if too_large:
                findings.append(Finding(
                    'IMG-306' if area_mode else 'IMG-302', '오류',
                    '본문 이미지 %s %dx%d — 최대 %dx%d 초과'
                    % (n, w, h, cfg['content_image_max_width'],
                       cfg['content_image_max_height'])))

    return names, findings


def main():
    ap = argparse.ArgumentParser(description='RIDI Books EPUB 업로드 전 점검')
    ap.add_argument('epub')
    ap.add_argument('--config', help='리디 검증기 defaults.config 경로')
    ap.add_argument('--quiet', action='store_true', help='오류만 출력')
    args = ap.parse_args()

    cfg = _read_config(args.config)
    names, findings = check(args.epub, cfg)
    if names is None:
        print('EPUB을 열 수 없습니다: %s' % args.epub)
        return 2

    errors = [f for f in findings if f.severity == '오류']
    warns = [f for f in findings if f.severity != '오류']

    print('검사 파일: %s (%d entries)' % (args.epub, len(names)))
    for f in errors:
        print(f)
    if not args.quiet:
        for f in warns:
            print(f)

    print()
    print('오류 %d건 / 경고 %d건' % (len(errors), len(warns)))
    if errors:
        print('→ 리디 업로드 전 수정이 필요합니다.')
        return 1
    print('→ 구현된 공개 규칙 검사 통과(공식 검증·현재 앱 표시 보증 아님).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
