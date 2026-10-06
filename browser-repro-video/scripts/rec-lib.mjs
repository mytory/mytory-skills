// 브라우저 재현 녹화 헬퍼. 프로젝트 특화 코드(로그인, URL, DB 조회)는 넣지 않는다. 사용 예시는 example.mjs.
// 의존성: playwright-core (시스템 Chrome 사용), ffmpeg.
import {chromium} from 'playwright-core';
import {execFileSync} from 'node:child_process';
import {writeFileSync} from 'node:fs';

export const COLORS = {head: '#1f3a93', bad: '#9f1239', good: '#166534'};

// headless 녹화에는 커서가 찍히지 않으므로 마우스를 따라다니는 점(클릭 시 커졌다 줄어듦)을 페이지에 그려 넣는다.
const cursorOverlayScript = () => {
    const install = () => {
        if (window.top !== window || document.getElementById('__rec_cursor')) {
            return;
        }
        const cursor = document.createElement('div');
        cursor.id = '__rec_cursor';
        cursor.style.cssText = 'position:fixed;z-index:2147483647;left:0;top:0;width:22px;height:22px;margin:-11px 0 0 -11px;'
            + 'border-radius:50%;background:rgba(255,40,40,.55);border:2px solid #fff;box-shadow:0 0 0 1px rgba(0,0,0,.5);'
            + 'pointer-events:none;transition:transform .12s';
        document.documentElement.appendChild(cursor);
        document.addEventListener('mousemove', e => {
            cursor.style.left = `${e.clientX}px`;
            cursor.style.top = `${e.clientY}px`;
        }, true);
        document.addEventListener('mousedown', () => { cursor.style.transform = 'scale(1.9)'; }, true);
        document.addEventListener('mouseup', () => { cursor.style.transform = 'scale(1)'; }, true);
    };
    if (document.documentElement) {
        install();
    }
    document.addEventListener('DOMContentLoaded', install);
};

// 녹화 세션을 연다. 로그인 등 준비는 호출 쪽에서 한다. videoDir를 주면 녹화하고 커서 오버레이를 켠다.
export async function openRecording({videoDir, width = 1440, height = 900, cookies = []}) {
    const browser = await chromium.launch({channel: 'chrome', headless: true});
    const context = await browser.newContext({
        viewport: {width, height},
        recordVideo: {dir: videoDir, size: {width, height}},
    });
    if (cookies.length) {
        await context.addCookies(cookies);
    }
    await context.addInitScript(cursorOverlayScript);
    const page = await context.newPage();
    // 영상의 0초는 페이지 생성이 아니라 첫 화면이 그려진 시점이다(실측: 빈 페이지를 한 번 그린 직후). 그래서 먼저 빈 화면을 그리고 그 직후를 기준 시각으로 잡는다.
    await page.goto('data:text/html,<body style="margin:0;background:%23fff">');
    const t0 = Date.now();
    records.set(page, {t0, cues: [], last: null, end: null});
    return {browser, context, page};
}

// 사람이 따라갈 수 있는 속도의 조작. 커서를 먼저 대상 위로 옮기고 잠시 멈춘 뒤 동작한다.
export const pause = (page, ms = 700) => page.waitForTimeout(ms);
export async function humanClick(page, locator, {before = 600, after = 800} = {}) {
    await locator.scrollIntoViewIfNeeded();
    await locator.hover();
    await page.waitForTimeout(before);
    await locator.click();
    await page.waitForTimeout(after);
}
export async function humanType(page, locator, text, {delay = 180, before = 500, after = 800} = {}) {
    await locator.hover();
    await page.waitForTimeout(before);
    await locator.click();
    await locator.pressSequentially(text, {delay});
    await page.waitForTimeout(after);
}

// 읽으라고 멈추는 대기. 상한을 넘기면 예외를 던져 정지 화면 규칙을 어기지 못하게 한다.
// 기본 5초. 내레이션을 입힐 영상은 음성이 흐르는 동안 화면이 멈춰도 되므로 10초(REC_NARRATION=1 또는 setMaxReadMs(10000)).
export let MAX_READ_MS = process.env.REC_NARRATION ? 10000 : 5000;
export function setMaxReadMs(ms) { MAX_READ_MS = ms; }
export async function holdToRead(page, ms) {
    if (ms > MAX_READ_MS) {
        throw new Error(`읽기 대기는 ${MAX_READ_MS}ms 이하여야 한다(요청 ${ms}ms). 주석을 줄이거나 화면을 나눈다.`);
    }
    await page.waitForTimeout(ms);
}

// 캡션: 화면 위 배너로 박고(burn: false면 생략), 녹화 시작 기준 시각과 함께 기록해 saveCaptions가 .srt/.vtt로 쓴다.
// 페이지 이동(goto)하면 배너가 사라지므로 마지막 캡션을 기억했다가 reapplyCaption으로 다시 그린다(자막 기록에는 영향 없음).
// 녹화 기준 시각: Playwright 영상은 페이지 생성 시점부터 시작하므로 openRecording이 newPage 직전 시각을 기준으로 잡는다.
const records = new WeakMap(); // page -> {t0, cues: [{start, end, text}], last: [text, color, burn] | null, end: ms | null}
const nowMs = rec => Date.now() - rec.t0;
const recordOf = page => {
    const rec = records.get(page);
    if (!rec) {
        throw new Error('openRecording으로 연 page가 아니다');
    }
    return rec;
};
const closeOpenCue = rec => {
    const open = rec.cues.at(-1);
    if (open && open.end === null) {
        open.end = nowMs(rec);
    }
};
const drawBanner = (page, text, color) => page.evaluate(([text, color]) => {
    let el = document.getElementById('__rec_banner');
    if (!el) {
        el = document.createElement('div');
        el.id = '__rec_banner';
        el.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:2147483646;padding:8px 20px;'
            + 'font:700 20px/1.35 sans-serif;color:#fff;text-align:center;pointer-events:none;'
            + 'box-shadow:0 2px 8px rgba(0,0,0,.4);white-space:pre-line';
        document.documentElement.appendChild(el);
    }
    el.style.background = color;
    el.textContent = text;
}, [text, color]);
export async function caption(page, text, {color = COLORS.head, burn = true} = {}) {
    const rec = recordOf(page);
    closeOpenCue(rec);
    rec.cues.push({start: nowMs(rec), end: null, text});
    rec.last = [text, color, burn];
    if (burn) {
        await drawBanner(page, text, color);
    }
}
export async function clearCaption(page) {
    const rec = recordOf(page);
    closeOpenCue(rec);
    rec.last = null;
    await page.evaluate(() => document.getElementById('__rec_banner')?.remove());
}
export async function reapplyCaption(page) {
    const last = recordOf(page).last;
    if (last && last[2]) {
        await drawBanner(page, last[0], last[1]);
    }
}
// 호환용 이름
export const banner = (page, text, color) => caption(page, text, {color});
export const reapplyBanner = reapplyCaption;

const pad = (n, w = 2) => String(n).padStart(w, '0');
const stamp = (ms, sep) => {
    ms = Math.max(0, Math.round(ms));
    return `${pad(Math.floor(ms / 3600000))}:${pad(Math.floor(ms / 60000) % 60)}:${pad(Math.floor(ms / 1000) % 60)}${sep}${pad(ms % 1000, 3)}`;
};
// 자막 본문 정리: "-->"는 시각 줄로 오해되므로 "→"로, 빈 줄은 큐를 끊으므로 제거. VTT는 &, <를 이스케이프, SRT는 태그처럼 보이는 <만 전각으로.
const cleanText = t => t.replace(/-->/g, '→').split('\n').map(l => l.trim()).filter(Boolean);
const escapeVtt = l => l.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const escapeSrt = l => l.replace(/<(?=[a-zA-Z/])/g, '\uFF1C');
export function toSrt(cues) {
    return cues.map((c, i) => `${i + 1}\n${stamp(c.start, ',')} --> ${stamp(c.end, ',')}\n${cleanText(c.text).map(escapeSrt).join('\n')}\n`).join('\n');
}
export function toVtt(cues) {
    return 'WEBVTT\n\n' + cues.map(c => `${stamp(c.start, '.')} --> ${stamp(c.end, '.')}\n${cleanText(c.text).map(escapeVtt).join('\n')}\n`).join('\n');
}
// 기록된 캡션을 <기준경로>.srt와 <기준경로>.vtt로 쓴다. 기준경로 예: 'out'(확장자 없음) 또는 'out.mp4'(확장자 제거).
// 끝나지 않은 마지막 캡션은 saveVideo 시각(없으면 지금)에 닫는다. saveVideo 뒤에 불러도 된다.
export function saveCaptions(pageOrSession, basePath) {
    const rec = recordOf(pageOrSession.page ?? pageOrSession);
    const end = rec.end ?? nowMs(rec);
    const cues = rec.cues.map(c => ({...c, end: c.end ?? end})).filter(c => c.end > c.start);
    const base = basePath.replace(/\.(mp4|webm|srt|vtt)$/i, '');
    writeFileSync(`${base}.srt`, toSrt(cues));
    writeFileSync(`${base}.vtt`, toVtt(cues));
    return {srt: `${base}.srt`, vtt: `${base}.vtt`, cues};
}

// 요소에 테두리와 번호를 붙인다. items: [{selector, ok(true=초록/false=빨강), label}] — 번호는 순서대로 [1], [2]...
export async function highlight(page, items) {
    await page.evaluate(items => {
        items.forEach(({selector, ok, label}, i) => {
            const color = ok ? '#16a34a' : '#e11d48';
            document.querySelectorAll(selector).forEach(el => {
                el.style.outline = `3px solid ${color}`;
                el.style.outlineOffset = '1px';
                const tag = document.createElement('span');
                tag.textContent = label ?? `[${i + 1}]`;
                tag.style.cssText = `color:${color};font-weight:700;margin-left:10px;white-space:nowrap`;
                el.appendChild(tag);
            });
        });
    }, items);
}

// 설명 패널. 앱 화면의 핵심을 가리지 않는 위치(css의 top/left/bottom 등)에 둔다.
// lines: [{text, ok}] — ok가 true면 초록, false면 빨강, 없으면 검정.
export async function notePanel(page, {heading = '', lines, css = 'bottom:16px;left:252px;width:1164px'}) {
    await page.evaluate(({heading, lines, css}) => {
        document.getElementById('__rec_note')?.remove();
        const panel = document.createElement('div');
        panel.id = '__rec_note';
        panel.style.cssText = `position:fixed;${css};z-index:2147483645;background:#fff;border:2px solid #444;`
            + 'padding:8px 14px;font:700 18px/1.7 sans-serif;pointer-events:none;box-shadow:0 2px 8px rgba(0,0,0,.3)';
        if (heading) {
            const h = document.createElement('div');
            h.textContent = heading;
            panel.appendChild(h);
        }
        for (const {text, ok} of lines) {
            const d = document.createElement('div');
            d.textContent = text;
            d.style.color = ok === undefined ? '#111' : ok ? '#16a34a' : '#e11d48';
            panel.appendChild(d);
        }
        document.body.appendChild(panel);
    }, {heading, lines, css});
}

// 표 패널. rows: 객체 배열, columns: 표시할 열, keyColumn: 행을 맞추는 열.
// after를 주면 "이전 → 이후"로 바뀐 칸을 빨갛게 표시하고, 새 행·삭제된 행도 표시한다.
// rows/after는 실제 조회 결과(DB 조회, 응답 JSON)에서 만든 것이어야 한다. 하드코딩 금지.
export async function tablePanel(page, {heading, columns, keyColumn, before, after = null, css = 'bottom:16px;left:252px'}) {
    await page.evaluate(({heading, columns, keyColumn, before, after, css}) => {
        document.getElementById('__rec_table')?.remove();
        const fmt = v => (v === null || v === undefined ? 'NULL' : String(v));
        const keys = [...new Set([...before.map(r => r[keyColumn]), ...(after ?? before).map(r => r[keyColumn])])]
            .sort((a, b) => (a > b ? 1 : a < b ? -1 : 0));
        const panel = document.createElement('div');
        panel.id = '__rec_table';
        panel.style.cssText = `position:fixed;${css};z-index:2147483645;background:#fff;border:3px solid #222;`
            + 'padding:8px 14px;font:600 16px/1.5 sans-serif;pointer-events:none;box-shadow:0 2px 10px rgba(0,0,0,.4)';
        let html = `<div style="font-weight:800;margin-bottom:4px">${heading}</div>`
            + '<table style="border-collapse:collapse;font-size:16px"><tr>'
            + columns.map(c => `<th style="border:1px solid #888;padding:2px 10px;background:#eee">${c}</th>`).join('') + '</tr>';
        for (const key of keys) {
            const b = before.find(r => r[keyColumn] === key);
            const a = after ? after.find(r => r[keyColumn] === key) : b;
            html += '<tr>' + columns.map(c => {
                const bv = b?.[c], av = a?.[c];
                const changed = after && (!b || !a || fmt(bv) !== fmt(av));
                const text = !after ? fmt(bv) : !b ? `${fmt(av)} (새 행)` : !a ? `${fmt(bv)} (삭제됨)`
                    : changed ? `${fmt(bv)} → ${fmt(av)}` : fmt(av);
                const style = changed ? 'color:#e11d48;font-weight:800;background:#ffe4e6' : '';
                return `<td style="border:1px solid #888;padding:2px 10px;${style}">${text}</td>`;
            }).join('') + '</tr>';
        }
        panel.innerHTML = html + '</table>';
        document.body.appendChild(panel);
    }, {heading, columns, keyColumn, before, after, css});
}

// 네트워크 응답 가로채기. urlPart가 URL에 포함된 응답을 JSON으로 파일에 저장하고 파싱한 값을 돌려준다.
// 클릭 등 응답을 일으키는 동작(trigger)과 함께 쓴다: const json = await captureResponse(page, '/api/x', outPath, () => button.click());
export async function captureResponse(page, urlPart, outPath, trigger, timeout = 30000) {
    const [response] = await Promise.all([
        page.waitForResponse(r => r.url().includes(urlPart), {timeout}),
        trigger(),
    ]);
    const json = await response.json();
    writeFileSync(outPath, JSON.stringify(json, null, 2));
    return json;
}
// 요청 본문도 남기려면 page.on('request', ...)로 따로 가로챈다. (예: request.postData())

// 녹화를 끝내고 webm을 mp4로 바꿔 저장한다. 변환 옵션은 ffmpeg 기본(libx264 CRF 23)으로 충분하다(분당 1MB 안팎, references/report.md).
export async function saveVideo(context, page, mp4Path) {
    const video = page.video();
    const rec = recordOf(page);
    closeOpenCue(rec);
    rec.end = nowMs(rec);
    await context.close();
    const webm = await video.path();
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', webm, '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4Path]);
    return mp4Path;
}
