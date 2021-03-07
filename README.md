# LearnUsDownloader
LearnUs video download
* v1.1 수정사항 : url 뒷부분 /xxx.ts 자동 삭제(기존 방식대로 직접 삭제해도 똑같이 작동합니다), .mp4확장자 자동 추가, 4시간 넘는 영상 대응, 한글 깨지는 문제 수정
1. 초록색 다운로드 버튼을 눌러 파일을 다운받습니다.
2. mac os 유저는 `for mac /learn_us_downloader_for_mac` 을 사용하시고, 윈도우 유저는 `LearnUsDownloaderv1.1/learn_us_downloader.exe` 를 사용하세요.

* 3,4 과정은 설명서를 보시고 하면 수월합니다
3. 크롬 브라우저로 강의 영상을 재생하고 우클릭이 가능한 아래쪽 빈공간을 찾아 우클릭, 검사를 클릭합니다.
4. 상단 네트워크 탭을 클릭하시고 `segment-xx-v1-a1.ts` 파일들이 보이실텐데 아무거나 우클릭 > copy > copy link address 클릭합니다.
5. 다운받은 파일을 실행합니다.
6. 검은 창이 나올텐데 처음에는 복사해온 링크를 붙여넣기 하시면 됩니다.
7. 그리고 저장할 파일 명을 입력합니다.(v1.1 미만의 경우에 윈도우에서 다운로드는 잘되었으나 영상재생이 안되는 경우가 있는데, 이는 파일명에 `.mp4`를 붙이지 않아서 그렇습니다)
8. mac 은 다운로드 폴더에, 윈도우는 실행파일이 있는 위치에 동영상 파일이 생성됩니다.


* FAQ
1. 동영상이 생성되었는데 크기가 0kb입니다. 무엇이 문제인가요?<br>
대부분의 경우 입력한 링크가 잘못되어서 입니다. 브라우져의 동영상 플레이어 창에서 링크를 그냥 복사해온 경우, v1.1미만에서 /xxxx.ts를 지우지 않고 입력한 경우, 
네트워크탭에서 `segmanet-xx-v1-a1.ts`파일이 아니라 `action.php` 파일을 선택하여 링크를 가져온 경우

2. 윈도우에서 `지정한 장치, 경로 또는 파일에 액세스 할 수 없습니다.` 오류가 나는 경우 어떻게 해야하나요?<br>
백신프로그램 실시간 검사에서 프로그램 실행을 막아서 오류가 발생하는 경우입니다. 실시간 검사를 꺼주시면 해결될거에요.

