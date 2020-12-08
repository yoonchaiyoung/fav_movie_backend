Local 컴퓨터에서 테스트 하는 목적 : 파이썬 코드가 잘 실행되는 지 보기 위해서

<h1>Local에 MongoDB 설치방법</h1>
---
1. C:\data\db 폴더 생성
2. https://www.mongodb.com/try/download/community 홈페이지의 2번째 탭(on-premises) -> mongodb community server 다운로드
3. 설치 -> custom -> browse -> C:\data\db 폴더 선택 -> Location이 C:\data\db\로 바뀐 것 확인하기
4. Install MongoDB Compass 선택은 해지
5. 설치 완료
6. 컴퓨터 환경설정 환경변수 -> 시스템 변수 -> PATH -> C:\data\db\bin 등록하기
7. cmd(관리자 권한으로 실행) -> cd C:\data\db\bin -> mongod.exe 입력해서 정상 실행되는 지 확인
8. https://robomongo.org/download -> Robo 3T 설치
9. Robo 3T 실행 -> create -> name : Bit Connection, address: localhost, port : 27017 -> connect
10. pycharm 에서 DB에 담을 내용 파이썬 파일 작성 -> 파일 실행
11. Robo 3T 실행 -> Bit Connection 실행 -> 마우스 우클릭 -> refresh -> fav_movie -> Collections -> movie -> 데이터 잘 들어갔는 지 확인
12. 내가 좋아하는 영화 목록에 추가하고 싶은 ObjectId를 복사
13. 크롬 브라우저 -> http://localhost:5000/movie/register/5fcd8a3454e156e5e73abcf4 이런 식으로 맨 뒤에 object ID 넣으면 Robo 3T에 잘 추가 되는 지 확인하기
