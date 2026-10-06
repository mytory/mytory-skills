# 제목(헤딩) CSS — 뷰어 호환판

## 왜 이렇게 쓰는가

전자책 뷰어(리디, Apple Books, 교보 등)는 CSS를 온전히 해석하지 않는다.
특히 헤딩에 대해 다음 두 가지 문제가 반복적으로 나타난다.

1. **리디 앱에서 제목 마진이 보이지 않는 사례가 있었다.** 마진 접힘이나
   뷰어의 스타일 처리 등이 원인일 수 있으며, 확인 없이 하나로 단정하지 않는다.
   패딩으로 대체한 뒤 실제 앱에서 확인한다.
2. **Calibre가 제목 크기를 재매핑할 수 있다.** 필요하면
   `--disable-font-rescaling`을 사용하고 결과 CSS를 확인한다.
   `em`은 해당 요소의 글꼴 크기, `rem`은 루트 글꼴 크기 기준이다.
   둘 다 사용자 글꼴 설정의 영향을 받을 수 있으므로 `rem`을 무조건 배제하지 않는다.
   아래 2.5rem/1rem 여백은 이번 사용자의 설정 예시이며 보편적인 필수값은 아니다.

## Calibre 폰트 리스케일링 실측

`body { font-size: 12pt }` + em 위계 CSS로 EPUB3를 만들었을 때 실측값이다.

| 태그 | CSS 지정 | 리스케일링 ON | OFF |
| --- | --- | --- | --- |
| h1 | 2em | 2em | 2em |
| h2 | 1.6em | **1.66667em** | 1.6em |
| h3 | 1.3em | **1.41667em** | 1.3em |
| h4 | 1.15em | **1.125em** | 1.15em |

리스케일링을 켜면 기본 글꼴(12pt)을 XHTML 기본값(16px≈12pt)에 맞추는
과정에서 각 단계가 반올림·재매핑되어 위계가 흐트러진다. h3가 h2보다
과대평가되어 간격이 좁아지고, h4는 지정값보다 작아진다. 표의 값에서는 h1 > h2 > h3 > h4 순서 자체는 유지된다.
`--disable-font-rescaling`을 주면 CSS 지정값이 그대로 보존된다.

위 수치는 기존 제작 사례의 측정값이다. 도구 버전과 입력 CSS가 달라지면
같은 값으로 재현된다고 가정하지 말고 출력 CSS를 확인한다.

## 권장 CSS

```css
body {
    line-height: 1.7;
    word-break: keep-all;          /* 한국어 단어 중간 줄바꿈 방지 */
    overflow-wrap: break-word;
    text-align: left;              /* 양끝정렬 대신 왼쪽 정렬 */
    font-size: 1em;
}

p {
    margin-bottom: 1.25rem;
    word-break: keep-all;
    overflow-wrap: break-word;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    word-break: keep-all;
    overflow-wrap: break-word;
    margin: 0;                     /* 마진 대신 패딩으로 여백 확보 */
    padding-top: 2.5rem;
    padding-bottom: 1rem;
    line-height: 1.35;
    page-break-after: avoid;       /* 제목이 페이지 끝에 홀로 남지 않게 */
    break-after: avoid;
    -webkit-column-break-after: avoid;
}

h1 { font-size: 2em;    }
h2 { font-size: 1.6em;  }
h3 { font-size: 1.3em;  }
h4 { font-size: 1.15em; }
h5 { font-size: 1em;    }
h6 { font-size: 0.9em;  }
```

## 좁은 화면 대응

글꼴 크기 변경과 좁은 화면에서 먼저 확인한다. 사용자 지정 여백을 유지해야 한다면
아래처럼 미디어 쿼리로 덮어쓰지 않는다. 요청에 따라 줄이는 선택적 예시는 다음과 같다:

```css
@media (max-width: 768px) {
    h1 { font-size: 1.75em; }
    h2 { font-size: 1.45em; }
    h3 { font-size: 1.2em; }
    h4 { font-size: 1.08em; }
    h1, h2, h3, h4, h5, h6 { padding-top: 1.5rem; }
}
```

## 검증 방법

생성된 EPUB에서 실제 CSS를 꺼내 클래스별로 확인한다. Calibre는 선택자를
`.calibreN` 클래스로 바꾸므로, 태그→클래스 매핑을 먼저 구해야 한다.

```python
import zipfile, re
z = zipfile.ZipFile('book.epub')
css = z.read('stylesheet.css').decode()
mapping = {}
for n in z.namelist():
    if n.endswith(('.xhtml', '.html')):
        for m in re.finditer(r'<h([1-6])\b[^>]*class="([^"]+)"',
                             z.read(n).decode('utf-8', 'ignore')):
            mapping.setdefault(m.group(1), set()).add(m.group(2))
def decls(block, prop):
    # padding-top / padding-bottom / padding 축약을 모두 인식
    m = re.search(prop + r':\s*([^;\n]+)', block)
    if m:
        return m.group(1).strip()
    if prop in ('padding-top', 'padding-bottom') and 'padding:' in block:
        m = re.search(r'padding:\s*([^;\n]+)', block)
        return '(padding 축약: %s)' % m.group(1).strip()
    return '-'

for lvl in sorted(mapping):
    for cls in mapping[lvl]:
        m = re.search(r'\.' + cls + r'\s*\{(.*?)\}', css, re.S)
        b = m.group(1)
        print(f"h{lvl} .{cls}:"
              f" font-size={decls(b, 'font-size')}"
              f" padding-top={decls(b, 'padding-top')}"
              f" padding-bottom={decls(b, 'padding-bottom')}"
              f" margin={decls(b, 'margin')}")
```

각 단계의 `font-size`가 서로 다른지, `padding-top`/`padding-bottom`이
살아 있는지, `margin`이 0인지 확인한다. `padding` 축약으로 지정했다면
`(padding 축약: ...)`으로 표시된다.
