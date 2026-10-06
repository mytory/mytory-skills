# 리디북스 EPUB 검증 규칙

출처: [ridi/ePub-Validator](https://github.com/ridi/ePub-Validator) (검증기 소스 + `config/defaults.config`).
이 저장소는 2018-12-18 보관 처리된 CP 업로드용 검증기다. 현재 리디 앱의
모든 요구사항을 나타내지 않으며, 함께 제공한 Python 검사는 일부 규칙만 구현한다.
이미지 비교는 [ImageValidator.js](https://github.com/ridi/ePub-Validator/blob/master/lib/ImageValidator.js),
기본 모드는 [defaults.config](https://github.com/ridi/ePub-Validator/blob/master/config/defaults.config)를 확인했다(2026-10-03).
기준 EPUB 표준 검증은 [w3c/epubcheck](https://github.com/w3c/epubcheck)를 함께 사용한다.

## 왜 epubcheck만으로 부족한가

`epubcheck`는 EPUB 표준 준수를 검사한다. 공개 리디 검증기는 별도 규칙으로
NCX를 요구하지만 EPUB3 표준에서는 선택 사항이다. 기존 Calibre 제작 사례의
목차 누락은 호환성 점검의 근거이며, 현재 모든 리디 뷰어가 nav를 읽지 못한다는
증거로 확대하지 않는다. 실제 목차 이동을 앱에서도 확인한다.

## 오류 코드 (검증기 소스에서 확인)

| 코드 | 심각도 | 내용 | 확인 위치 |
| --- | --- | --- | --- |
| EPUB-301 | 오류 | NCX `content src`가 `./`로 시작 | `EPubValidator.js` |
| EPUB-302 | 오류 | 매니페스트에 `application/x-dtbncx+xml` 항목이 없음 | `EPubValidator.js` |
| EPUB-401 | 심각 | NCX 인코딩/파싱 실패 | `EPubValidator.js` |
| CSS-301 | 오류 | `html`·`body` 선택자에 width/height 계열 속성 | `CssValidator.js` |
| CSS-302 | 오류 | `column-*` 속성 사용 | `CssValidator.js` |
| CSS-303 | 오류 | `img`에 `position: relative` | `CssValidator.js` |
| CSS-006 | 오류 | `position: fixed` | `CssValidator.js` |
| CSS-201 | 경고 | `word-break: break-all` | `CssValidator.js` |
| HTML-301 | 오류 | 본문 파일이 300KB 초과 | `HtmlValidator.js` |
| HTML-302 | 오류 | 한 엘리먼트의 자식이 500개 초과 | `HtmlValidator.js` |
| HTML-303 | 오류 | `body`의 인라인 `background-color` | `HtmlValidator.js` |
| HTML-304 | 오류 | `body` 태그 없음 | `HtmlValidator.js` |
| IMG-301 | 오류 | 표지 이미지가 최소 크기 미달 | `ImageValidator.js` |
| IMG-302 | 오류 | 본문 이미지가 최대 크기 초과 | `ImageValidator.js` |
| IMG-303 | 오류 | 이미지 파일이 5000KB 초과 | `ImageValidator.js` |
| IMG-305 | 오류 | 픽셀 면적 기준 표지 최소 미달 | `ImageValidator.js` |
| IMG-306 | 오류 | 픽셀 면적 기준 본문 이미지 최대 초과 | `ImageValidator.js` |

### 주의: 검증기 코드의 허점

`CSS-301` 검사는 선택자가 **정확히 `html` 또는 `body`**일 때만 발동한다.
Calibre는 템플릿의 `body { max-width: ... }`를 `body class="calibreN"` +
`.calibreN { max-width: ... }` 로 바꿔 내보낸다(클래스名은 CSS 순서에 따라
매번 달라지므로 하드코딩하면 안 된다). 그래서 **리디 검증기는 통과하지만
실제 뷰어에는 크기 제한이 그대로 적용된다.** "검증 통과 = 안전"이 아니다.

`scripts/check_ridi.py`는 이 우회 형태를 별도로 탐지해 `CSS-301-L`
경고로 알려 준다. 템플릿 단계에서 `body`의 `max-width`·`background-color`를
빼는 편이 확실하다.

`HTML-303`도 `body` 태그의 **인라인 `style` 속성**만 본다. CSS로 준
`body { background-color }`는 잡지 못한다.

## 기준값 (defaults.config)

```
cover_image_min_width: 560
cover_image_min_height: 800
cover_image_recommend_width: 1120
cover_image_recommend_height: 1600

content_image_max_width: 1080
content_image_max_height: 1600
image_file_max_size: 5000        # KB
html_file_max_size: 300          # KB
html_file_recommend_file_size: 150
child_nodes_limit: 500
image_compare_type: 1
```

- 기본 `image_compare_type: 1`은 너비×높이의 **면적**으로 비교한다.
  표지 최소 면적 미달은 IMG-305, 본문 최대 면적 초과는 IMG-306이다.
  모드 0에서만 표지는 어느 한 축의 최소 미달(IMG-301), 본문은
  **두 축이 동시에** 최대 초과(IMG-302)를 검사한다.
- 표지는 최소 미달이면 오류, 권장 미달이면 경고.

## 실제 사례

Calibre `--epub-version 3`으로 만든 EPUB에서:

- `body class="calibre1"` (속성: `max-width: 800px`, `background-color: #fff`)
- `html class="calibre"`
- `stylesheet.css`에 `.calibre1 { max-width: 800px; ... }`

리디 검증기는 위 `.calibre1`을 잡지 못하고 통과시켰다. NCX 누락
(`EPUB-302`)만 잡혔다. 즉 "목차 없는 작품" 문제를 해결한 뒤에도 body
크기 제한은 조용히 남아 있었다.

## 최소 NCX 예시

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" xml:lang="ko" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:…"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>책 제목</text></docTitle>
  <navMap>
    <navPoint id="navPoint-1" playOrder="1">
      <navLabel><text>1장</text></navLabel>
      <content src="chapter1.xhtml"/>
      <navPoint id="navPoint-2" playOrder="2">
        <navLabel><text>1.1절</text></navLabel>
        <content src="chapter1.xhtml#sec-1"/>
      </navPoint>
    </navPoint>
  </navMap>
</ncx>
```

OPF 쪽에는 다음 두 가지가 필요하다.

```xml
<manifest>
  <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
</manifest>
<spine toc="ncx">
```

## 패키징 규칙

- `mimetype`은 **첫 번째 엔트리**여야 하고 **무압축(STORED)**이어야 한다.
  Python `zipfile`로 재패킹할 때:
  ```python
  zi = zipfile.ZipInfo('mimetype')
  zi.compress_type = zipfile.ZIP_STORED
  out.writestr(zi, b'application/epub+zip')
  ```
- 나머지는 DEFLATED로 무방하다.
