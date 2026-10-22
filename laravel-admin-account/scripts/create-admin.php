<?php
/**
 * Laravel 앱에 로그인용 관리자 계정을 만들거나 갱신한다.
 *
 * 사용 (프로젝트 루트에서):
 *   php <이 파일> <email> <password> [role] [--name=이름]
 *
 * - 같은 email이 있으면 비밀번호와 이름을 갱신한다.
 * - role을 주면 프로젝트의 역할 테이블에 연결한다. 지원하는 두 형태를 자동 판별한다.
 *   1) roles(user_id, name)          — 이 저장소(맑시즘) 방식
 *   2) model_has_roles + roles       — spatie/laravel-permission 방식
 * - 계정 정보는 표준출력으로만 알려 준다. 로그 파일에 남기지 않는다.
 */
$name = null;
$positional = [];

foreach (array_slice($argv, 1) as $arg) {
    if (str_starts_with($arg, '--name=')) {
        $name = substr($arg, 7);
        continue;
    }
    $positional[] = $arg;
}

$email = $positional[0] ?? null;
$password = $positional[1] ?? null;
$role = $positional[2] ?? null;

if (! $email || ! $password) {
    fwrite(STDERR, "사용: php create-admin.php <email> <password> [role] [--name=이름]\n");
    exit(2);
}

$root = getcwd();
if (! is_file($root.'/vendor/autoload.php')) {
    fwrite(STDERR, "프로젝트 루트(vendor/autoload.php가 있는 곳)에서 실행하세요.\n");
    exit(2);
}

require $root.'/vendor/autoload.php';
$app = require $root.'/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Schema;

$userModel = config('auth.providers.users.model', 'App\\User');
$model = new $userModel();
$table = $model->getTable();
$connection = $model->getConnectionName();

$attributes = [
    'name' => $name ?: '관리자',
    'password' => Hash::make($password),
];

if (Schema::connection($connection)->hasColumn($table, 'email_verified_at')) {
    $attributes['email_verified_at'] = now();
}

$user = $userModel::where('email', $email)->first();

if ($user) {
    $user->fill($attributes);
    $user->save();
    $action = '갱신';
} else {
    $user = $userModel::create(array_merge($attributes, ['email' => $email]));
    $action = '생성';
}

$roleResult = '없음';
if ($role) {
    $schema = Schema::connection($connection);
    if ($schema->hasTable('roles')) {
        $columns = $schema->getColumnListing('roles');
        if (in_array('user_id', $columns, true)) {
            DB::connection($connection)->table('roles')->where('user_id', $user->getKey())->delete();
            DB::connection($connection)->table('roles')->insert([
                'user_id' => $user->getKey(),
                'name' => $role,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            $roleResult = $role.' (roles.user_id)';
        } elseif ($schema->hasTable('model_has_roles')) {
            $roleId = DB::connection($connection)->table('roles')->where('name', $role)->value('id')
                ?? DB::connection($connection)->table('roles')->insertGetId([
                    'name' => $role,
                    'guard_name' => 'web',
                ]);
            DB::connection($connection)->table('model_has_roles')->updateOrInsert([
                'role_id' => $roleId,
                'model_type' => $userModel,
                'model_id' => $user->getKey(),
            ]);
            $roleResult = $role.' (model_has_roles)';
        }
    }
}

printf("%s 완료: id=%s email=%s name=%s role=%s\n", $action, $user->getKey(), $user->email, $user->name, $roleResult);
