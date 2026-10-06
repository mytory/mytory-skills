// 클립별 .srt를 클립 길이만큼 밀어 합쳐 <출력>.srt, <출력>.vtt로 쓴다. concat-clips.sh가 호출한다.
// 사용: node merge-captions.mjs <출력.mp4> <클립1.mp4> <클립2.mp4> ...   (클립 옆에 같은 이름의 .srt가 있으면 합친다)
import {execFileSync} from 'node:child_process';
import {existsSync, readFileSync, writeFileSync} from 'node:fs';
import {toSrt, toVtt} from './rec-lib.mjs';

const [out, ...clips] = process.argv.slice(2);
const toMs = (h, m, s, ms) => ((+h * 60 + +m) * 60 + +s) * 1000 + +ms;
const parseSrt = text => text.replace(/\r/g, '').trim().split(/\n\n+/).flatMap(block => {
    const lines = block.split('\n');
    const m = lines[1]?.match(/(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)/);
    return m ? [{start: toMs(...m.slice(1, 5)), end: toMs(...m.slice(5, 9)), text: lines.slice(2).join('\n')}] : [];
});

let offset = 0;
const cues = [];
for (const clip of clips) {
    const srt = clip.replace(/\.[^.]+$/, '.srt');
    if (existsSync(srt)) {
        cues.push(...parseSrt(readFileSync(srt, 'utf8')).map(c => ({...c, start: c.start + offset, end: c.end + offset})));
    }
    offset += Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', clip]).toString()) * 1000;
}
if (cues.length) {
    const base = out.replace(/\.[^.]+$/, '');
    writeFileSync(`${base}.srt`, toSrt(cues));
    writeFileSync(`${base}.vtt`, toVtt(cues));
    console.log(`자막 ${cues.length}개 합침 → ${base}.srt, ${base}.vtt`);
}
