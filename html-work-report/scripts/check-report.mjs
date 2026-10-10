#!/usr/bin/env node
// 보고서 HTML을 실제 브라우저로 열어 이미지·영상이 로드되는지, 상대 링크·src가 가리키는 파일이 있는지,
// 템플릿 자리표시자({{ }})가 남지 않았는지, warn/bad 판정이 접힌 <details> 안에 숨지 않았는지 검사한다.
// 사용: node check-report.mjs <report.html>   (playwright-core가 설치된 폴더에서. channel: 'chrome')
// 통과 0 / 위 항목 중 하나라도 걸리면 1
import {chromium} from 'playwright-core';
import path from 'node:path';
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';

const file = process.argv[2];
if (!file) { console.error('사용: node check-report.mjs <report.html>'); process.exit(2); }
const browser = await chromium.launch({channel: 'chrome'});
const page = await browser.newPage({viewport: {width: 1280, height: 900}});
await page.goto(pathToFileURL(path.resolve(file)).href, {waitUntil: 'load'});
await page.waitForTimeout(1500);
// 판정 위치 검사는 열기 전에 한다. <summary>는 접혀도 보이므로 제외.
const hidden = await page.evaluate(() => [...document.querySelectorAll('details .warn, details .bad')].filter(e => !e.closest('summary')).map(e => e.textContent.trim().slice(0, 60)));
// 닫힌 <details> 안의 이미지·영상도 Chrome이 로드하지만(실측), loading="lazy"는 화면 밖이면 로드되지 않으므로 지우고 전부 연 뒤 측정한다.
await page.evaluate(() => {
    document.querySelectorAll('details').forEach(d => d.setAttribute('open', ''));
    document.querySelectorAll('img[loading]').forEach(i => i.removeAttribute('loading'));
});
await page.waitForTimeout(1500);
const r = await page.evaluate(() => {
    const images = [...document.images].filter(i => !(i.matches('dialog:not([open]) [data-image-full]') && !i.hasAttribute('src')));
    const attrs = [...document.querySelectorAll('*')].flatMap(e => [...e.attributes].filter(a => a.value.includes('{{')).map(a => `${e.tagName.toLowerCase()}[${a.name}]=${a.value.slice(0, 60)}`));
    const text = [document.title, ...document.body.innerText.split('\n')].filter(l => l.includes('{{')).map(l => l.trim().slice(0, 60));
    return {
    images: images.length,
    brokenImages: images.filter(i => !i.naturalWidth).map(i => i.getAttribute('src')),
    videos: [...document.querySelectorAll('video')].map(v => ({src: v.getAttribute('src'), readyState: v.readyState, error: v.error?.message ?? null})),
    refs: [...document.querySelectorAll('a[href], img[src], video[src], source[src]')].map(e => e.getAttribute('href') ?? e.getAttribute('src')),
    placeholders: [...text, ...attrs],
    };
});
await browser.close();
const badVideos = r.videos.filter(v => v.readyState < 1 || v.error);
// 상대 경로가 가리키는 파일이 디스크에 있는지는 Node에서 확인한다(쿼리·해시 제거, 퍼센트 인코딩 해제).
const dir = path.dirname(path.resolve(file));
const missing = [...new Set(r.refs)].filter(h => h && !/^([a-z][a-z0-9+.-]*:|#|\/\/)/i.test(h))
    .filter(h => {
        try { return !fs.existsSync(path.resolve(dir, decodeURIComponent(h.split('#')[0].split('?')[0]))); } catch { return true; }
    });
console.log(`이미지 ${r.images}개(깨짐 ${r.brokenImages.length}) · 영상 ${r.videos.length}개(로드 실패 ${badVideos.length}) · 없는 상대 경로 ${missing.length}개 · 남은 자리표시자 ${r.placeholders.length}개 · 접힌 영역의 warn/bad ${hidden.length}개`);
r.brokenImages.forEach(s => console.log(`  깨진 이미지: ${s}`));
badVideos.forEach(v => console.log(`  영상 로드 실패: ${v.src} ${v.error ?? ''}`));
missing.forEach(h => console.log(`  없는 파일: ${h}`));
r.placeholders.slice(0, 10).forEach(p => console.log(`  남은 자리표시자: ${p}`));
if (hidden.length) { console.log('  warn/bad 판정이 접힌 영역에 있음(판정은 항상 보이게 둔다):'); hidden.forEach(t => console.log(`    ${t}`)); }
process.exit(r.brokenImages.length || badVideos.length || missing.length || r.placeholders.length || hidden.length ? 1 : 0);
