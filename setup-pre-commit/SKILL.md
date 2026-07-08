---
name: setup-pre-commit
description: 현재 저장소에 Husky 프리커밋 훅과 lint-staged(Prettier), 타입 검사, 테스트를 설정합니다. "프리커밋 훅 설정해줘", "Husky 추가해줘", "커밋할 때 자동 포맷팅", "lint-staged 구성해줘", "커밋 전에 타입 검사 실행하게 해줘"라고 할 때 사용합니다.
---

# 프리커밋 훅 설정

## 설정되는 것

- **Husky** 프리커밋 훅
- **lint-staged**가 모든 스테이징된 파일에 Prettier 실행
- **Prettier** 설정 (없는 경우)
- 프리커밋 훅에 **typecheck** 및 **test** 스크립트

## 단계

### 1. 패키지 매니저 감지

`package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun)을 확인하세요. 있는 것을 사용하세요. 불분명하면 npm을 기본값으로 하세요.

### 2. 의존성 설치

devDependencies로 설치:

```
husky lint-staged prettier
```

### 3. Husky 초기화

```bash
npx husky init
```

`.husky/` 디렉터리를 생성하고 package.json에 `prepare: "husky"`를 추가합니다.

### 4. `.husky/pre-commit` 생성

이 파일을 작성하세요 (Husky v9+에서는 shebang 불필요):

```
npx lint-staged
npm run typecheck
npm run test
```

**조정**: `npm`을 감지된 패키지 매니저로 교체하세요. 저장소의 package.json에 `typecheck` 또는 `test` 스크립트가 없으면 해당 줄을 생략하고 사용자에게 알리세요.

### 5. `.lintstagedrc` 생성

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. `.prettierrc` 생성 (없는 경우)

Prettier 설정이 없는 경우에만 생성하세요. 다음 기본값 사용:

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. 검증

- [ ] `.husky/pre-commit`이 존재하고 실행 가능함
- [ ] `.lintstagedrc`가 존재함
- [ ] package.json의 `prepare` 스크립트가 `"husky"`임
- [ ] `prettier` 설정이 존재함
- [ ] `npx lint-staged`를 실행하여 작동 확인

### 8. 커밋

변경/생성된 모든 파일을 스테이징하고 다음 메시지로 커밋: `Add pre-commit hooks (husky + lint-staged + prettier)`

새 프리커밋 훅을 통과하게 됩니다 — 모든 것이 작동하는지 확인하는 좋은 스모크 테스트입니다.

## 참고

- Husky v9+는 훅 파일에 shebang이 필요 없음
- `prettier --ignore-unknown`은 Prettier가 파싱할 수 없는 파일(이미지 등)을 건너뜀
- 프리커밋은 lint-staged를 먼저 실행하고(빠름, 스테이징된 파일만), 그 다음 전체 타입 검사와 테스트를 실행
