# 보고서 폴더와 HTML

## 폴더
보고서는 파일 하나보다 **폴더**로 만든다. 영상·이미지·증거가 보고서와 함께 움직이고 상대 경로가 깨지지 않는다. 사용자에게도 그렇게 조언한다. 폴더와 보고서 파일 이름은 `YYYY-MM-DD {주제 혹은 이슈번호}`(날짜 + 공백 + 주제, 밑줄 없음).
```
docs/2026-10-04 port-bug/
  2026-10-04 port-bug.html
  videos/       01-before-after.mp4, 01-before-after.srt, .vtt
  screenshots/  결과 스크린샷(WebP — html-work-report 스킬의 to-webp.sh로 변환)
  evidence/     request-before.json, response-after.json, db-before-after.json
```
- 위치는 프로젝트의 문서 관례를 따른다. 관례가 없으면 사용자에게 묻는다.
- 폴더 안의 영상·스크린샷·증거 파일명은 ASCII 권장(공유·URL 문제 방지). 이름 규칙 전체는 `html-work-report` 스킬.

## HTML
```html
<figure>
  <video controls preload="metadata" poster="images/01.png" src="videos/01-before-after.mp4" width="960"></video>
  <figcaption>01 수정 전 → 수정 후. 0:00 수정 전(master), 1:10 수정 후(브랜치)</figcaption>
</figure>
```
- 경로는 상대 경로. mp4는 `+faststart`(`saveVideo`·`concat-clips.sh`가 넣음)라 로딩 전에도 재생·탐색이 된다.
- 구간 시작 시각을 `figcaption`에 적는다(`concat-clips.sh`가 출력).
- 영상 옆에 상태별 비교표(기대/수정 전/수정 후)를 둔다. 값은 실제 결과에서 만든다.
- 자막 파일을 HTML에 넣는 법: [captions.md](captions.md). `file://`에서는 `<track src>`가 막히니 Blob 방식을 쓴다.

## 용량
- 실측(2026-10-04, 관리 화면 녹화 2개): 127초 2.1MB(분당 1.0MB), 212초 4.4MB(분당 1.2MB). 1440×900·25fps·h264·ffmpeg 기본 설정(CRF 23)이다. 화면 녹화는 **분당 1~2MB**면 충분하다. 헬퍼의 변환 설정은 그대로 둔다.
- 이보다 크면 줄인다: `ffmpeg -i in.mp4 -c:v libx264 -crf 28 -preset slow -r 15 -pix_fmt yuv420p -movflags +faststart out.mp4`. 60초 구간을 CRF 28로 다시 인코딩하니 약 30% 작아졌고, 화면의 글자는 CRF 32에서도 읽혔다. 줄인 뒤 프레임을 뽑아 글자가 뭉개지지 않았는지 본다.
- 타이핑·커서 이동 같은 작은 움직임이 많아 fps를 내리면 동작이 끊겨 보일 수 있다. 15fps 아래는 쓰지 않는다.

## 검수
- 보고서를 **실제 브라우저로 열어** 영상이 로드·재생되는지 본다(`video.readyState`가 4, `video.error`가 null). 상대 경로 오타, 이동 후 깨진 링크를 잡는다.
- 자막을 넣었다면 `video.textTracks[0].cues.length`가 0이 아닌지 본다.
