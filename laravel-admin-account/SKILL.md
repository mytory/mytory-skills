---
name: laravel-admin-account
description: Laravel 앱에 로그인 가능한 관리자(또는 역할이 붙은) 계정을 만들고 실제 로그인까지 확인합니다. "관리자 계정 만들어줘", "테스트 계정 하나 만들어줘", "로그인해서 화면 확인해야 해", "권한 있는 계정으로 테스트" 같은 요청에 사용합니다.
---

로그인 뒤에만 볼 수 있는 화면을 확인하려면 계정이 필요하다. 이 스킬은 계정을 만들고, 비밀번호가 실제로 통하는지 확인하고, 끝나면 되돌리는 절차까지 정한다.

## 언제 쓰나

- 로그인 후 화면(관리자·접수·대시보드)을 브라우저로 확인해야 할 때
- 역할(role)에 따라 다른 화면을 확인해야 할 때
- 기존 계정의 비밀번호를 모를 때 (덮어쓰지 말고 새 계정을 만든다)

## 먼저 확인할 것

```bash
# 1) 프로젝트 루트인가
ls vendor/autoload.php artisan

# 2) 어떤 모델·테이블이 인증에 쓰이는가
grep -n "providers" -A6 config/auth.php
# 3) 역할을 어떻게 붙이는가 (둘 중 하나)
mysql ... -e "show columns from roles;"
#    roles(user_id, name)       → 이 저장소 방식
#    model_has_roles + roles    → spatie/laravel-permission
# 4) 앱 환경 (운영이면 계정을 만들지 않는다)
grep -E "^APP_ENV|^DB_DATABASE" .env
```

`APP_ENV`가 `production`이면 멈추고 사용자에게 확인을 받는다. 로컬·스테이징에서만 만든다.

## 계정 만들기

```bash
php ~/.agents/skills/laravel-admin-account/scripts/create-admin.php <email> <password> [role] [--name=이름]
```

- 같은 이메일이 있으면 비밀번호·이름을 갱신하고, 없으면 만든다.
- `role`을 주면 프로젝트의 역할 구조를 자동 판별해 연결한다(`roles.user_id` 또는 `model_has_roles`).
- 역할 없이 만들면 "일반 관리자" 권한이 된다. 앱이 특정 역할로 분기하면(예: `hasRole('지회')` → 다른 화면) 역할 없이 만드는 쪽이 기본 화면을 보기 좋다.
- 출력 예: `생성 완료: id=30 email=qa@example.test name=관리자 role=없음`

## 로그인 확인

```bash
php ~/.agents/skills/laravel-admin-account/scripts/verify-login.php <email> <password>
# login: ok (qa@example.test)
```

그다음 브라우저로 실제 로그인한다.

```bash
agent-browser open http://127.0.0.1:8000/login
agent-browser snapshot -i          # 이메일·비밀번호·버튼 ref 확인
agent-browser fill @e1 "<email>"
agent-browser fill @e2 "<password>"
agent-browser click @e3
agent-browser wait --url "**/reception"   # 앱마다 이동 경로가 다르다
agent-browser screenshot /tmp/after-login.png
```

브라우저에서 로그인했는데 계속 로그인 화면이면: 세션 드라이버(`SESSION_DRIVER`), CSRF 토큰, 쿠키 도메인(`APP_URL`)을 본다.

## 비밀번호·정리

- 비밀번호는 가능하면 생성해서 쓰고, 명령 기록에 남기지 않는다. 공유 문서·보고서에는 쓰지 않는다.
- 확인이 끝나면 계정을 지우거나 비밀번호를 무작위로 바꾼다. 남겨야 하면 보고서에 "테스트 계정 남음(이메일만 표기)"이라고 적는다.
- 삭제:
  ```bash
  php artisan tinker --execute="App\User::where('email','<email>')->delete();"
  # 역할 행도 함께: DB::table('roles')->where('user_id', <id>)->delete();
  ```

## 하지 말 것

- 운영 DB에 계정을 만들지 않는다.
- 기존 계정의 비밀번호를 덮어쓰지 않는다. 누군가 쓰던 계정이면 새 이메일로 만든다.
- 실제 사용자 개인정보가 들어 있는 계정을 복제하지 않는다.
