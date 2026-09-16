#!/usr/bin/env node
// 삶 응원 메시지 CLI — references/messages.json에서 무작위로 하나를 골라 출력한다.
// 의존성 없음. Node 18+.
//
//   node scripts/cheer.mjs                      무작위 1개
//   node scripts/cheer.mjs --mode=calm          모드 지정
//   node scripts/cheer.mjs --tone=dark --count=3
//   node scripts/cheer.mjs --tag=외로움
//   node scripts/cheer.mjs --list               모드 목록
//   node scripts/cheer.mjs --json               JSON으로 출력

import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = JSON.parse(readFileSync(join(HERE, '..', 'references', 'messages.json'), 'utf8'));

function parseArgs(argv) {
  const opts = { count: 1, json: false };
  for (const arg of argv) {
    const [key, value] = arg.replace(/^--?/, '').split('=');
    if (key === 'list') opts.list = true;
    else if (key === 'json') opts.json = true;
    else if (key === 'm' || key === 'mode') opts.mode = value;
    else if (key === 'tone') opts.tone = value;
    else if (key === 'tag') opts.tag = value;
    else if (key === 'count' || key === 'c') opts.count = Number(value);
    else if (key === 'seed') opts.seed = Number(value);
    else if (key === 'help' || key === 'h') opts.help = true;
  }
  return opts;
}

function makeRandom(seed) {
  if (seed === undefined) return Math.random;
  let state = seed >>> 0;
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

function pick(items, count, random) {
  const pool = [...items];
  const picked = [];
  while (pool.length && picked.length < count) {
    picked.push(pool.splice(Math.floor(random() * pool.length), 1)[0]);
  }
  return picked;
}

const opts = parseArgs(process.argv.slice(2));
const modeById = new Map(DATA.modes.map((m) => [m.id, m]));

if (opts.help) {
  console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').slice(1, 12).join('\n').replace(/^\/\/ ?/gm, ''));
  process.exit(0);
}

if (opts.list) {
  const counts = new Map();
  for (const m of DATA.messages) counts.set(m.mode, (counts.get(m.mode) ?? 0) + 1);
  for (const mode of DATA.modes) {
    console.log(`${mode.id.padEnd(12)} ${mode.tone.padEnd(6)} ${String(counts.get(mode.id) ?? 0).padStart(2)}개  ${mode.label}`);
  }
  console.log(`\n총 ${DATA.messages.length}개 메시지 / ${DATA.modes.length}개 모드`);
  process.exit(0);
}

let pool = DATA.messages;
if (opts.mode) {
  pool = pool.filter((m) => m.mode === opts.mode);
  if (!pool.length) {
    console.error(`알 수 없는 모드: ${opts.mode}. --list 로 모드 목록을 확인해.`);
    process.exit(1);
  }
}
if (opts.tone) {
  pool = pool.filter((m) => {
    const tone = modeById.get(m.mode)?.tone;
    if (opts.tone === 'bright') return tone === 'bright' || tone === 'any';
    return tone === opts.tone;
  });
}
if (opts.tag) pool = pool.filter((m) => (m.tags ?? []).some((t) => t.includes(opts.tag)) || m.text.includes(opts.tag));

if (!pool.length) {
  console.error('조건에 맞는 메시지가 없어.');
  process.exit(1);
}

const random = makeRandom(opts.seed);
const picked = pick(pool, Math.max(1, Math.min(opts.count || 1, pool.length)), random);

if (opts.json) {
  console.log(JSON.stringify(picked, null, 2));
} else {
  for (const m of picked) console.log(`${m.text}\n  (${m.id} · ${modeById.get(m.mode)?.label ?? m.mode})\n`);
}
