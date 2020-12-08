import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# requests : 페이지 요청
# bs : html 파싱

# client = MongoClient('localhost', 27017)
client = MongoClient("mongodb://mongodb사용자명:mongodb비밀번호@AWS퍼블릭주소", 27017)
# mongodb id, password, aws 퍼블릭 주소
# DB 잘 작동하는 지부터 확인
# 무조건 1순위
db = client.fav_movie

def scrap_naver_movie():
    URL = "https://movie.naver.com/movie/running/current.nhn"
    headers = {
        'User-Agent': "Mozilla/5.0"
    }
    # 서버가 받아볼 클라이언트의 정보
    # User-Agent -> 크롬, 사파리 브라우저로 들어가고 있다고 속임(실제로는 파이썬에서 접속하는데)
    data = requests.get(URL, headers=headers)
    # print(data)
    # print(data.text)
    # URL과 연결된 요청이 잘 들어오는지, 페이지는 제대로 크롤링이 되는지 확인

    # BeautifulSoup 적용시키기
    soup = BeautifulSoup(data.text, 'html.parser')
    movie_lst = soup.select("#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li")
    # F12 -> 원하는 부분의 큰 부분 선택 -> ul -> 마우스 우클릭 -> copy -> copy selector : #content > div.article > div:nth-child(1) > div.lst_wrap > ul 가 복사가 됨
    # print(movie_lst)

    # 이제 ul 밑의 li들을 뽑아야 함
    # 위의 #content > div.article > div:nth-child(1) > div.lst_wrap > ul 맨 뒤에 > li 를 추가시켜줌

    for li in movie_lst:
        # 위의 ul의 selector와 겹치는 부분은 지워도 됨
        # #content > div.article > div:nth-child(1) > div.lst_wrap > ul > li:nth-child(1) >
        # 이 부분 지움
        # 그 밑의 li의 a 태그 영화 이름만 뽑을 거니까
        title = li.select_one("dl > dt > a").text
        # print(title)
        poster = li.select_one("div > a > img").get('src')
        # print(title.text, poster)
        star = li.select_one("dl > dd.star > dl.info_star > dd > div > a > span.num").text
        director = li.select_one("dl > dd:nth-child(3) > dl > dd:nth-child(4) > span > a").text
        actors = li.select("dl > dd:nth-child(3) > dl > dd:nth-child(6) > span > a")
        actors = [actor.text for actor in actors]
        # print(title, star, director, actors)

        doc = {
            "title": title,
            "poster": poster,
            "star": star,
            "director": director,
            "actors": actors
        }

        db.movie.insert_one(doc)

if __name__ == "__main__":
    scrap_naver_movie()
