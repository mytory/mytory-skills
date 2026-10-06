// 사용 예시 겸 스모크 테스트.
// 실행: node example.mjs <출력.mp4> [--freeze=초] [--no-burn]   → 출력.mp4, 출력.srt, 출력.vtt
// --no-burn: 캡션을 화면에 박지 않고 자막 파일만 만든다.
// "TODO(프로젝트)" 표시된 곳이 프로젝트마다 채울 부분이다. 나머지는 그대로 쓴다.
import {writeFileSync, mkdtempSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {openRecording, caption, highlight, notePanel, tablePanel, humanClick, humanType, holdToRead, saveVideo, saveCaptions, COLORS} from './rec-lib.mjs';

const out = process.argv[2] ?? 'smoke.mp4';
const freezeArg = process.argv.find(a => a.startsWith('--freeze='));
const burn = !process.argv.includes('--no-burn');
const freezeSec = freezeArg ? Number(freezeArg.split('=')[1]) : 0; // 일부러 정지 화면을 만들어 검사 스크립트를 시험할 때만 쓴다

const work = mkdtempSync(join(tmpdir(), 'rec-example-'));
const demo = join(work, 'demo.html');
writeFileSync(demo, `<!doctype html><meta charset=utf-8><body style="font:18px sans-serif;margin:120px 40px">
<h2>데모 화면</h2><input id=name placeholder="이름" style="font-size:18px;padding:6px">
<button id=save style="font-size:18px;padding:6px 14px">저장</button><ul id=list></ul>
<script>document.getElementById('save').onclick=()=>{
  const li=document.createElement('li');li.className='row';li.textContent=document.getElementById('name').value;
  document.getElementById('list').appendChild(li);}</script>`);

// TODO(프로젝트): 상태별 서버 주소. 실제로는 수정 전/후 서버를 포트로 나눠 띄운다.
const states = [{tag: 'before', title: '수정 전 (master)', url: pathToFileURL(demo).href}];

const {browser, context, page} = await openRecording({videoDir: work});
for (const s of states) {
    // TODO(프로젝트): 로그인 등 준비 동작
    await page.goto(s.url);
    await caption(page, `${s.title}\n같은 조작: 이름 입력 → 저장`, {color: COLORS.head, burn});
    await holdToRead(page, 2000);

    await caption(page, '이름 칸에 hello를 입력하고 저장을 누른다', {color: COLORS.head, burn}); // 장면 캡션: 지금 무엇을 하는가
    await humanType(page, page.locator('#name'), 'hello');           // TODO(프로젝트): 재현 조작
    await humanClick(page, page.locator('#save'));

    // TODO(프로젝트): 실제 응답·DB 조회 결과로 판정한다. 아래 expected만 상수(정답 기준값)다.
    const expected = 'hello';
    const actual = await page.locator('.row').first().textContent();
    const ok = actual === expected;

    await highlight(page, [{selector: '.row', ok}]);
    await tablePanel(page, {
        heading: 'DB 상태(예시)', columns: ['id', 'name'], keyColumn: 'id',
        before: [{id: 1, name: null}], after: [{id: 1, name: actual}], css: 'bottom:16px;left:40px',
    });
    await caption(page, `${s.title}\n결과: ${ok ? '기대와 같음' : '기대와 다름'} (기대 "${expected}", 실제 "${actual}")`, {color: ok ? COLORS.good : COLORS.bad, burn});
    await notePanel(page, {lines: [{text: `실제 "${actual}"`, ok}], css: 'top:300px;left:40px'});
    await holdToRead(page, 3000);                                    // 읽기 대기는 5초 이하(끝의 녹화 마무리 시간이 정지로 더해지니 여유를 둔다)
    if (freezeSec) {
        await page.waitForTimeout(freezeSec * 1000);                 // 검사 스크립트 시험용: 일부러 정지
    }
}
await saveVideo(context, page, out);
const {srt, vtt} = saveCaptions(page, out);
await browser.close();
console.log('저장:', out, srt, vtt);
