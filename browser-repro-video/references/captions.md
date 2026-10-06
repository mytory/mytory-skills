# 캡션 쓰는 법

캡션은 영상을 보는 사람에게 "지금 무엇을 보고 있고 어디를 봐야 하는가"를 알려 준다. 강조 표시(`highlight`)와 짝으로 쓴다.

## 무엇을 쓰는가
- **구간 시작**: 어느 상태인지. `수정 전 (master)` / `수정 후 (브랜치명)` + 같은 조작 한 줄.
- **장면마다**: 지금 하는 조작과 봐야 할 곳. 예: `포트 칸에 80을 입력하고 저장 — 아래 [1]번 행의 방향 표기를 본다`
- **결과 문장**: 기대와 같은지 다른지. 값은 실제 결과에서 만든다. 하드코딩 금지, 예상과 다르면 "예상과 다름"으로 쓴다([annotation.md](annotation.md)).
- 한 캡션은 한두 문장, **5초 안에 읽을 분량**. 길면 장면을 나눈다.

## 두 방식
| | 영상에 박기 (`caption`, 기본) | 자막 파일 (`burn: false` + `saveCaptions`) |
|---|---|---|
| 장점 | 어디서 열어도 보임. 보고서·메신저 공유에 안전 | 화면을 가리지 않음. 글자를 나중에 고칠 수 있음(다시 찍지 않아도 됨) |
| 단점 | 고치려면 다시 찍어야 함. 상단 약 70px를 가림 | 플레이어가 자막을 지원해야 함. 메신저로 mp4만 보내면 사라짐 |

- 기본은 **박기**. 공유될 영상은 박는다.
- 박으면서 `.srt`도 함께 남기는 것을 권한다(`saveCaptions`는 `burn: true`여도 기록한다). 검색·오탈자 수정·번역용이다.
- 자막 파일만 쓸 때는 `caption(page, 텍스트, {burn: false})`.

## API (`rec-lib.mjs`)
```js
await caption(page, '수정 전 (master)\n같은 조작: 이름 입력 → 저장', {color: COLORS.head, burn: true});
await clearCaption(page);        // 배너를 지우고 자막 구간을 끝낸다
await reapplyCaption(page);      // goto 뒤에 배너를 다시 그린다(자막 기록은 그대로)
const {srt, vtt} = saveCaptions(page, 'out');   // out.srt, out.vtt. saveVideo 앞뒤 어느 쪽에서 불러도 된다
```
- 캡션의 끝은 다음 캡션의 시작, `clearCaption`, 또는 `saveVideo` 시각이다.
- 시각은 영상과 맞춰 둔다. Playwright 영상의 0초는 페이지 생성이 아니라 **첫 화면이 그려진 시점**이라서, `openRecording`이 빈 화면을 한 번 그린 직후를 기준으로 삼는다. 실측 오차는 0.2초 안쪽이다.
- 여러 줄은 `\n`. `-->`는 `→`로 바뀌고, VTT에서는 `&`·`<`가 이스케이프된다.
- 클립을 `concat-clips.sh`로 이으면 같은 이름의 `.srt`를 클립 길이만큼 밀어 합친다.

## HTML 보고서에 자막 넣기
`file://`로 여는 보고서에서 `<track src="x.vtt">`는 **Chrome이 막는다**(`'file:' URLs are treated as unique security origins`, 자막이 0개로 읽힘). 확인한 우회책: VTT를 HTML 안에 넣고 Blob URL로 붙인다. http로 서빙하면 `<track src>`가 된다.
```html
<video id="v" controls preload="metadata" src="videos/01.mp4"></video>
<script type="text/vtt" id="v-cap">
WEBVTT
...(x.vtt 내용)</script>
<script>
const track = document.createElement('track');
track.kind = 'captions'; track.srclang = 'ko'; track.label = '한국어'; track.default = true;
track.src = URL.createObjectURL(new Blob([document.getElementById('v-cap').textContent.trim()], {type: 'text/vtt'}));
document.getElementById('v').appendChild(track);
</script>
```
- **`.trim()` 필수.** `<script>` 안 첫 줄 앞의 개행 때문에 `WEBVTT`가 첫 글자가 아니면 자막이 0개로 읽힌다.
- Chrome(Playwright `channel: 'chrome'`, `file://`)에서 위 방식·`data:` URL·`addTextTrack`+`VTTCue` 세 가지로 큐가 로드되고 재생 위치에 맞게 활성화되며 화면에 그려지는 것을 확인했다. `<track src>` 직접 지정은 막혔다.
- Safari·Firefox는 확인하지 못했다.
- 영상에 이미 박았다면 이 자막을 또 켜지 않는다(겹친다). 박은 영상 + `.srt`는 파일로만 곁들인다.

## 자막을 영상에 나중에 박기
이 머신의 ffmpeg 8.0은 `subtitles` 필터(libass)가 되고 한글은 글꼴 지정 없이도 나온다(fontconfig 대체 글꼴). 기본 크기는 1440×900에서 작고 흰 배경에서는 윤곽만 보이니 스타일을 준다.
```bash
ffmpeg -i out.mp4 -vf "subtitles=out.srt:force_style='FontSize=12,BorderStyle=3,Outline=3,BackColour=&H99000000,MarginV=20'" -pix_fmt yuv420p -movflags +faststart out-subbed.mp4
```
- 다시 인코딩하므로 화질이 한 단계 떨어진다. 가능하면 원본을 보존한다.
- `ffmpeg -filters | grep subtitles`로 빌드를 확인한다. 안 나오면 libass가 없는 빌드이니 이 방법은 쓸 수 없다.

## 배치 요령
- 배너는 화면 맨 위 전체 폭이다. 앱 상단 메뉴나 첫 줄을 가리므로, 봐야 할 곳이 위쪽이면 `burn: false`로 하거나 스크롤해서 내려 둔다.
- 설명이 길면 배너를 늘리지 말고 `notePanel`을 앱 핵심 아래쪽 빈 곳에 둔다.
- 캡션이 가린 곳에 강조한 요소가 있으면 안 된다. 프레임을 뽑아 확인한다.
