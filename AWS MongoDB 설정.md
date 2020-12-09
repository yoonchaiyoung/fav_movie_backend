AWS MongoDB 목적 : 배포를 하기 위해

<h1>AWS MongoDB 설치방법</h1>

1. AWS 홈페이지 로그인
   
2. ec2 선택
   
3. 단계 1. ubuntu server 18.04 lts 선택
   
4. 단계 2. tw.micro 프리티어 선택
   
5. 검토 및 시작 -> 시작하기 -> 새 키 페어 생성 -> 키 페어 이름 : bit1207-keypair -> 키 페어 다운로드
   
6. 인스턴스 시작 -> 인스턴스 보기 -> 퍼블릭 IPv4 주소 복사
* git bash 켜기

```
ssh -i <keypair 주소(파일 끌어다 놓으면 자동 생성)> ubuntu@AWS퍼블릭IPv4주소

yes
```
* google 홈페이지 -> 파일질라 검색 -> 다운로드 -> 설치
  
1. 파일질라 켜기
   
2. 파일(F) 밑에 사이트 관리자 클릭
   
3. new site -> fav_movie -> 프로토콜 : SFTP 선택 -> 호스트 : AWS퍼블릭IPv4주소 -> 로그온 유형 : 키 파일 -> 사용자 : ubuntu -> 키파일: AWS keypair 아까 다운로드한 것 클릭
   
4. 연결 -> 확인
   
5. 왼쪽 D드라이브 (파이썬 파일 저장 경로 들어가서) hello.py를 오른쪽의 ubuntu로 드래그하여 복사
   
* git bash로 다시 가기
```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
python hello.py
```
- Hello AWS! 라고 뜨는 지 확인
```
sudo apt-get update
sudo apt-get install -y python3-pip
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
pip --version
```
- python 3.6 버전인지 확인하기
```
pip install flask pymongo requests bs4
```
- AWS 사이트로 다시 이동
  
1. 인스턴스 -> 보안 -> 보안 그룹 -> 인바운드 규칙 -> 인바운드 규칙 편집
   
2. SSH -> 소스 : 위치무관
   
3. 규칙 추가 -> HTTP -> 소스 : 위치무관
   
4. 규칙 추가 -> 사용자 지정 TCP -> 포트 범위 : 5000 -> 소스 : 위치무관
   
5. 규칙 추가 -> 사용자 지정 TCP -> 포트 범위 : 27017 -> 소스 : 위치무관
   
6. 규칙 저장
   
- git bash로 다시 이동

```wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -&&
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list&&
sudo apt-get update&&
sudo apt-get install -y mongodb-org
```
```
sudo service mongod start
```
- 아무 메시지 안 떠야지 정상
```
mongo
```
- mongoDB 쉘로 들어가짐
```
> use admin;
>db.createUser({user:"yoonchaiyoung", pwd:"9452", roles:["root"]})
```
- successfully added user라고 나오면 정상 작동된 것
- 비밀번호에 특수문자, 영어 들어가면 나중에 DB연결할 때 에러뜸 -> 아마도 숫자만 가능한 듯 싶다
```
> exit
```
- mongoDB 나가기
```
sudo service mongod restart;
sudo vi /etc/mongod.conf
```

```buildoutcfg
# network interfaces
  bindIp: 127.0.0.1을
  bindIp: 0.0.0.0 으로 바꿔주기

# security를
security:
  authorization: enabled 로 바꿔주기
앞에 2칸 띄워져있는 것 유의!
```
- Robo 3T 다시 열기
  
1. File 밑의 MongoDB Connections -> create
   
2. authentication 탭 -> perform authentication -> user name : yoonchaiyoung -> password : 9452
   
3. connection 탭 -> name : dbTest AWS -> address : AWS 퍼블릭 IPv4 주소
   
4. test 클릭 -> 에러 없으면 save
   
- 파일질라 다시 열기
  
1. 오른쪽 ubuntu 쪽 디렉터리 만들기 -> /home/ubuntu/fav_movie_backend -> 파이썬 app.py 파일을 지금 만든 fav_movie_backend 폴더에 넣기
   
- git bash 다시 열기
```
cd fav_movie_backend/
python app.py
```
- 크롬 브라우저 열기
  
1. AWS퍼블릭IPv4주소:5000/movie/list 들어가면 연결됨
   
- git bash 다시 열기
```
컨트롤 + C 해서 나온 후
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000
nohup python app.py &
```
- 기본 포트인 80포트로 들어오더라도 5000포트로 변경해주는 포트 포워딩
- 터미널을 끄더라도 서버가 돌 수 있게 해줌

+) 서버 끄는 법

- git bash 열기
  
```
ssh -i <keypair 파일 주소> ubuntu@AWS퍼블릭IPv4주소
ps -ef | grep 'python'
뜬 결과에서 python app.py랑 /usr/bin/python/home/ubuntu/fav_movie_backend/app.py를 꺼야함
왼쪽에서 2번째 줄에 해당하는 번호를 pid라고 하는 데 그 번호를 이용
kill -9 (pid1)
kill -9 (pid2)
예를 들어 숫자가 1385라고 하면 kill -9 1385 라고 입력하면 된다.
ps -ef | grep 'python' 으로 제대로 꺼졌는 지 확인
```
```
다시 서버 켜고 싶으면
cd fav_movie_backend/
nohup python app.py &
```