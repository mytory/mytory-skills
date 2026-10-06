#!/usr/bin/env node
// 보고서 HTML을 실제 브라우저로 열어 이미지·영상이 로드되는지 검사한다.
// 사용: node check-report.mjs <report.html>   (playwright-core가 설치된 폴더에서. channel: 'chrome')
// 통과 0 / 깨진 이미지·영상 있음 1
import {chromium} from 'playwright-core';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const file = process.argv[2];
if (!file) { console.error('사용: node check-report.mjs <report.html>'); process.exit(2); }
const browser = await chromium.launch({channel: 'chrome'});
const page = await browser.newPage({viewport: {width: 1280, height: 900}});
await page.goto(pathToFileURL(path.resolve(file)).href, {waitUntil: 'load'});
await page.waitForTimeout(1500);
const r = await page.evaluate(() => {
    const images = [...document.images].filter(i => !(i.matches('dialog:not([open]) [data-image-full]') && !i.hasAttribute('src')));
    return {
    images: images.length,
    brokenImages: images.filter(i => !i.naturalWidth).map(i => i.getAttribute('src')),
    videos: [...document.querySelectorAll('video')].map(v => ({src: v.getAttribute('src'), readyState: v.readyState, error: v.error?.message ?? null})),
    brokenLinks: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => h && !/^(https?:|#|mailto:)/.test(h)),
    };
});
await browser.close();
const badVideos = r.videos.filter(v => v.readyState < 1 || v.error);
console.log(`이미지 ${r.images}개(깨짐 ${r.brokenImages.length}) · 영상 ${r.videos.length}개(로드 실패 ${badVideos.length}) · 상대 링크 ${r.brokenLinks.length}개(존재 여부는 따로 확인)`);
r.brokenImages.forEach(s => console.log(`  깨진 이미지: ${s}`));
badVideos.forEach(v => console.log(`  영상 로드 실패: ${v.src} ${v.error ?? ''}`));
process.exit(r.brokenImages.length || badVideos.length ? 1 : 0);
