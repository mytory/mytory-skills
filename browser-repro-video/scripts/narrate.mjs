#!/usr/bin/env node
// 캡션(.srt)을 음성 설명으로 만들어 영상에 입힌다.
//
//   node narrate.mjs <영상.mp4> [--srt 자막.srt] [--out 출력.mp4] [--voice M1] [--lang ko] [--plan]
//
// - 기본 자막은 <영상>.srt. 말로 읽기 어려운 캡션(URL·경로·기호)은 따로 쓴 .srt를 --srt로 넘긴다(큐 시각은 같게).
// - 각 큐의 음성은 큐 시작 시각에 놓는다. 앞 음성이 아직 안 끝났으면 끝난 뒤 0.25초 후로 민다(드리프트).
// - --plan: 합성만 하고 큐별 "음성 길이 vs 다음 큐까지 여유"를 표로 보여 준다. 넘치는 큐가 있으면 종료 코드 1.
//   캡션을 줄이거나 그 장면의 hold를 늘려 다시 찍은 뒤 입힌다.
// - 출력 옆에 narration-plan.json(큐별 배치·드리프트)을 남긴다.
import {execFileSync, spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const PYTHON = '~/Supertonic/.venv/bin/python';
const TTS_BATCH = path.join(path.dirname(fileURLToPath(import.meta.url)), 'tts-batch.py');
const GAP = 0.25;          // 앞 음성과 뒤 음성 사이 최소 간격(초)
const DRIFT_LIMIT = 2.0;   // 이보다 밀리면 화면과 설명이 어긋난다고 본다

const args = process.argv.slice(2);
const video = args.find(a => !a.startsWith('--') && a.endsWith('.mp4'));
if (!video) {
    console.error('사용: node narrate.mjs <영상.mp4> [--srt 자막.srt] [--out 출력.mp4] [--voice M1] [--lang ko] [--plan]');
    process.exit(2);
}
const opt = name => { const i = args.indexOf(`--${name}`); return i >= 0 ? args[i + 1] : undefined; };
const srtPath = opt('srt') ?? video.replace(/\.mp4$/, '.srt');
const outPath = opt('out') ?? video.replace(/\.mp4$/, '-narrated.mp4');
const voice = opt('voice') ?? 'M1';
const lang = opt('lang') ?? 'ko';
const planOnly = args.includes('--plan');

function parseSrt(text) {
    const toSec = t => { const m = t.trim().match(/(\d+):(\d+):(\d+)[,.](\d+)/); return +m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000; };
    return text.replace(/\r/g, '').trim().split(/\n\n+/).map(block => {
        const lines = block.split('\n');
        const timeIdx = lines.findIndex(l => l.includes('-->'));
        if (timeIdx < 0) return null;
        const [a, b] = lines[timeIdx].split('-->');
        // 줄바꿈은 쉼표처럼 읽히게 공백으로 잇는다
        return {start: toSec(a), end: toSec(b), text: lines.slice(timeIdx + 1).join(' ').replace(/\s+/g, ' ').trim()};
    }).filter(c => c && c.text);
}

function videoSeconds(file) {
    return parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]).toString());
}

const cues = parseSrt(fs.readFileSync(srtPath, 'utf8'));
if (!cues.length) { console.error(`큐가 없다: ${srtPath}`); process.exit(2); }
const workDir = path.join(path.dirname(outPath), '.narration');
fs.mkdirSync(workDir, {recursive: true});

// 1. 합성 (모델 1회 로드, 바뀐 큐만)
const inputJson = path.join(workDir, 'cues.json');
fs.writeFileSync(inputJson, JSON.stringify(cues.map((c, i) => ({id: String(i + 1).padStart(3, '0'), text: c.text}))));
// stderr(진행 로그)는 그대로 흘리고 stdout(JSON)만 받는다
const tts = spawnSync(PYTHON, [TTS_BATCH, '--input', inputJson, '--out-dir', workDir, '--voice', voice, '--lang', lang], {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'inherit']});
if (tts.status !== 0) process.exit(tts.status ?? 1);
const clips = JSON.parse(tts.stdout);

// 2. 배치: 큐 시작에 두되 앞 음성과 겹치면 뒤로 민다
const total = videoSeconds(video);
let prevEnd = 0;
const plan = cues.map((c, i) => {
    const dur = clips[i].duration;
    const at = Math.max(c.start, prevEnd + (i ? GAP : 0));
    const nextStart = cues[i + 1]?.start ?? total;
    const room = nextStart - c.start;               // 이 장면이 화면에 머무는 시간
    const drift = at - c.start;
    prevEnd = at + dur;
    return {n: i + 1, start: c.start, at: +at.toFixed(2), duration: dur, room: +room.toFixed(2), overflow: +(dur - room).toFixed(2), drift: +drift.toFixed(2), text: c.text, path: clips[i].path};
});
fs.writeFileSync(path.join(path.dirname(outPath), 'narration-plan.json'), JSON.stringify(plan, null, 2));

const bad = plan.filter(p => p.overflow > 0.5 || p.drift > DRIFT_LIMIT);
const fmt = p => `#${String(p.n).padStart(2)} ${p.start.toFixed(1).padStart(6)}s 여유 ${p.room.toFixed(1).padStart(5)}s 음성 ${p.duration.toFixed(1).padStart(5)}s ${p.overflow > 0.5 ? `초과 ${p.overflow.toFixed(1)}s` : '      '} ${p.drift > 0.01 ? `밀림 ${p.drift.toFixed(1)}s` : ''}  ${p.text.slice(0, 40)}`;
console.log(`큐 ${plan.length}개 · 영상 ${total.toFixed(1)}s · 음성 합계 ${plan.reduce((a, p) => a + p.duration, 0).toFixed(1)}s`);
(planOnly ? plan : bad).forEach(p => console.log(fmt(p)));
if (bad.length) console.log(`\n주의: ${bad.length}개 큐가 장면보다 길거나 ${DRIFT_LIMIT}초 넘게 밀린다. 캡션을 줄이거나 그 장면의 hold를 늘려 다시 찍는 편이 낫다.`);
if (planOnly) process.exit(bad.length ? 1 : 0);

// 3. 합성: 무음 바탕 + 각 음성을 at 시각에 adelay → amix → 영상에 입힘(영상은 복사)
const inputs = ['-f', 'lavfi', '-t', total.toFixed(3), '-i', 'anullsrc=r=44100:cl=mono'];
plan.forEach(p => inputs.push('-i', p.path));
// 입력 0 = 영상(오디오 없음), 1 = 무음 바탕, 2.. = 큐별 WAV
const delays = plan.map((p, i) => `[${i + 2}:a]aresample=44100,aformat=channel_layouts=mono,adelay=${Math.round(p.at * 1000)}:all=1[a${i}]`).join(';');
const mix = `[1:a]${plan.map((_, i) => `[a${i}]`).join('')}amix=inputs=${plan.length + 1}:duration=first:dropout_transition=0:normalize=0[mix]`;
const filter = `${delays};${mix}`;
const filterFile = path.join(workDir, 'filter.txt');
fs.writeFileSync(filterFile, filter);
const ff = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', video, ...inputs, '-filter_complex_script', filterFile,
    '-map', '0:v', '-map', '[mix]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k', '-shortest', outPath], {encoding: 'utf8'});
if (ff.status !== 0) { console.error(ff.stderr); process.exit(ff.status ?? 1); }
console.log(`저장: ${outPath}`);
