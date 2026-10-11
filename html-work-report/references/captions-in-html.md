# HTML 보고서에 자막 넣기

영상에 캡션을 박지 않았을 때만 쓴다. 자막 파일(`.vtt`)은 `browser-repro-video`가 영상과 함께 만든다.

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
