---
name: web-design-guidelines
description: UI 코드가 Web Interface Guidelines를 지키는지 검토합니다. "UI 리뷰해줘", "접근성 확인해줘", "디자인 감사해줘", "UX 검토해줘", "사이트가 모범 사례를 따르는지 봐줘"라고 할 때 사용합니다.
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

파일이 Web Interface Guidelines를 지키는지 검토합니다.

## 작동 방식

1. 아래 원본 URL에서 최신 지침을 가져옵니다.
2. 지정된 파일을 읽습니다. 지정되지 않았다면 사용자에게 파일이나 패턴을 묻습니다.
3. 가져온 지침의 모든 규칙과 대조합니다.
4. 결과를 간결한 `file:line` 형식으로 출력합니다.

## 지침 원본

검토할 때마다 최신 지침을 가져옵니다.

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

WebFetch로 최신 규칙을 가져옵니다. 가져온 내용에 모든 규칙과 출력 형식 지시가 들어 있습니다.

## 사용법

사용자가 파일이나 패턴 인수를 주면:
1. 위 원본 URL에서 지침을 가져옵니다.
2. 지정된 파일을 읽습니다.
3. 가져온 지침의 모든 규칙을 적용합니다.
4. 지침에 지정된 형식으로 결과를 출력합니다.

파일을 지정하지 않았다면 어떤 파일을 검토할지 사용자에게 묻습니다.
