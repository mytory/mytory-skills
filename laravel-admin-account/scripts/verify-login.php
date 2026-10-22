<?php
/**
 * 계정으로 실제 로그인이 되는지 확인한다.
 * 사용 (프로젝트 루트에서): php <이 파일> <email> <password>
 */
$email = $argv[1] ?? null;
$password = $argv[2] ?? null;
if (! $email || ! $password) {
    fwrite(STDERR, "사용: php verify-login.php <email> <password>\n");
    exit(2);
}

$root = getcwd();
require $root.'/vendor/autoload.php';
$app = require $root.'/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$ok = Illuminate\Support\Facades\Auth::attempt(['email' => $email, 'password' => $password]);
printf("login: %s (%s)\n", $ok ? 'ok' : 'failed', $email);
exit($ok ? 0 : 1);
