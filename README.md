# imweb_site

돈보라 아임웹(Imweb) 사이트 작업 저장소입니다.
HTML 코드와 이미지를 함께 관리하며, 이미지는 jsDelivr CDN으로 서빙합니다.

## 폴더 구조

    main-banner/
      donbora-rolling-banner.html   아임웹 코드 위젯에 붙여넣는 코드
      images/                       배너 이미지

## 이미지 주소 규칙

    https://cdn.jsdelivr.net/gh/bjssh12/imweb_site@main/<폴더>/images/<파일명>

예) https://cdn.jsdelivr.net/gh/bjssh12/imweb_site@main/main-banner/images/banner1_pc.png

## 이미지 교체 시 주의

같은 파일명을 덮어쓰면 CDN이 최대 7일간 이전 이미지를 계속 보여줍니다.
교체할 때는 파일명 뒤에 _v2 를 붙이고, HTML의 주소도 함께 바꿔주세요.
