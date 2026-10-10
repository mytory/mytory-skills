// 완성된 HTML 보고서를 장면별로 훑으며 캡션을 붙여 "발표 영상"으로 녹화한다. 검토자가 보고서를 열기 전에 이 영상을 먼저 볼 수 있다.
// 실행: node present-report.mjs <report.html> <scenes.json> <출력.mp4>   → 출력.mp4, 출력.srt, 출력.vtt
// 이어서 `node narrate.mjs 출력.mp4 --plan`, `node narrate.mjs 출력.mp4`로 음성을 입힌다(항상 내레이션용이라 정지 상한은 30초).
// scenes.json: 배열. 장면마다 {target, caption, hold, open?}
//   target  보여줄 요소의 CSS 선택자(첫 번째 일치)
//   caption 화면 위 띠에 박히고 음성으로도 읽힐 1~2문장
//   hold    캡션을 읽는 동안 화면을 멈추는 시간(ms, 30000 이하)
//   open    true면 target을 감싼(또는 target인) <details>를 바깥쪽까지 모두 열고, 없으면 target 안의 첫 <details>를 연 뒤 스크롤.
//           접힌 <details> 안의 target에 open이 없으면 화면에 안 보이므로 녹화 전에 실패한다.
// 예: [{"target": "#review-guide", "caption": "위험도는 중간이고, 확인할 지점은 두 곳이다.", "hold": 6000},
//      {"target": "#qa", "caption": "수동 확인 결과는 접어 둔 영역에 있다.", "hold": 5000, "open": true}]
import {readFileSync, mkdtempSync, mkdirSync, existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve, dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {openRecording, caption, holdToRead, setMaxReadMs, saveVideo, saveCaptions} from './rec-lib.mjs';

const [report, scenesFile, out] = process.argv.slice(2);
if (!report || !scenesFile || !out) {
    console.error('사용: node present-report.mjs <report.html> <scenes.json> <출력.mp4>');
    process.exit(2);
}
if (!existsSync(report)) { console.error(`보고서가 없다: ${report}`); process.exit(2); }
const scenes = JSON.parse(readFileSync(scenesFile, 'utf8'));
if (!Array.isArray(scenes) || !scenes.length) { console.error('scenes.json은 장면이 하나 이상인 배열이어야 한다'); process.exit(2); }
setMaxReadMs(30000);

const work = mkdtempSync(join(tmpdir(), 'present-report-'));
// 보고서는 패널을 쓰지 않으므로 오른쪽 패널 없이 넓게, 축소 없이 찍는다(뷰포트 1872x912 + 캡션 띠·여백 = 1920x1080). 본문 폭이 좁은 보고서가 화면을 채우도록 확대한다.
const {browser, context, page} = await openRecording({videoDir: work, width: 1872, height: 912, displayWidth: 1872, sideBand: 0});
await page.goto(pathToFileURL(resolve(report)).href, {waitUntil: 'load'});
// 마우스를 쓰지 않으므로 커서 점은 숨긴다.
await page.addStyleTag({content: 'html { zoom: 1.3; } #__rec_cursor { display: none; }'});

// 녹화 전에 장면을 모두 검증한다.
const problems = [];
for (const [i, s] of scenes.entries()) {
    if (!s.target || !s.caption || !(s.hold > 0)) { problems.push(`장면 ${i + 1}: target, caption, hold(ms)가 모두 필요하다`); continue; }
    if (s.hold > 30000) { problems.push(`장면 ${i + 1}: hold가 ${s.hold}ms다. 30000ms 이하여야 한다`); }
    const el = page.locator(s.target).first();
    if (!await el.count()) { problems.push(`장면 ${i + 1}: 선택자 "${s.target}"에 해당하는 요소가 없다`); continue; }
    if (!s.open && await el.evaluate(e => !!e.parentElement?.closest('details:not([open])'))) {
        problems.push(`장면 ${i + 1}: "${s.target}"이 접힌 <details> 안에 있다. "open": true를 준다`);
    }
}
if (problems.length) {
    problems.forEach(p => console.error(p));
    await browser.close();
    process.exit(1);
}

for (const s of scenes) {
    const el = page.locator(s.target).first();
    if (s.open) {
        await el.evaluate(e => {
            let d = e.closest('details');
            if (!d) {
                e.querySelector('details')?.setAttribute('open', '');
            }
            for (; d; d = d.parentElement?.closest('details')) {
                d.setAttribute('open', '');
            }
        });
    }
    // 대상 위에 여백을 두고 맨 위로 스크롤한 뒤, 스크롤이 끝날 때까지 기다린다.
    await el.evaluate(e => {
        e.style.scrollMarginTop = '16px';
        e.scrollIntoView({behavior: 'smooth', block: 'start'});
    });
    await page.waitForFunction(() => new Promise(done => {
        let last = scrollY, same = 0;
        const tick = () => { same = scrollY === last ? same + 1 : 0; last = scrollY; same >= 5 ? done(true) : requestAnimationFrame(tick); };
        tick();
    }));
    // 이전 장면의 강조를 지우고 이번 대상에 파란 윤곽선을 둔다(highlight는 합격/불합격 색이라 쓰지 않는다).
    // 윤곽선은 보고서 템플릿의 강조색, 어두운 화면에서도 보이게 바깥에 흰 테를 두른다.
    await page.evaluate(() => document.querySelectorAll('[data-present]').forEach(e => {
        e.style.outline = '';
        e.style.boxShadow = '';
        e.removeAttribute('data-present');
    }));
    await el.evaluate(e => {
        e.dataset.present = '1';
        e.style.outline = '3px solid #2f5bd3';
        e.style.outlineOffset = '4px';
        e.style.boxShadow = '0 0 0 9px #ffffff';
    });
    await caption(page, s.caption);
    await holdToRead(page, s.hold);
}
mkdirSync(dirname(resolve(out)), {recursive: true});
await saveVideo(context, page, out);
const {srt, vtt} = saveCaptions(page, out);
await browser.close();
console.log('저장:', out, srt, vtt);
