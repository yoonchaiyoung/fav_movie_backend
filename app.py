from flask import request, jsonify, Flask
from pymongo import MongoClient

# MongoDB의 _id를 파이썬에서 사용할 수 있게 해주는 패키지
# ObjectId : key
from bson.objectid import ObjectId

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient("mongodb://mongodb사용자명:mongodb비밀번호@18.222.131.248", 27017)
# mongodb id, password, aws 퍼블릭 주소
db = client.fav_movie


# api 설계하기

# 전체 영화 목록 보여주기
# "/movie/list" - GET
@app.route("/movie/list", methods=["GET"])
def movie_list():
    movie_lst = list(db.movie.find({}))

    # ObjectId는 JSON 자체에서는 지원하지 않는다.
    # 따라서 ObjectId를 문자열 형태로 바꿔주는 코드가 필요하다.

    # 1. ObjectId를 문자열로 만들어주는 함수를 정의
    def pre_processing(movie):
        movie['_id'] = str(movie['_id'])
        return movie

    # 2. movie_lst를 컴프리헨션을 이용해 ObjectId를 텍스트화
    movie_lst = [pre_processing(movie) for movie in movie_lst]

    return jsonify({'result': movie_lst})


# 영화 등록
# "/movie/register" - GET
# parameter : 영화의 _id
@app.route("/movie/register/<oid>", methods=["GET"])
def movie_register(oid):
    # 보고 싶은 영화가 이미 등록이 되어 있으면 새롭게 등록 안한다.
    # 등록이 안되어있으면 새롭게 추가

    # 사용자가 좋아하는 영화의 문서구조
    fav_movie_list = db.user_movie.find_one({"fav_movie": oid})

    if not fav_movie_list:
        db.user_movie.insert_one({"fav_movie": oid})

    fav_movie_list = list(db.user_movie.find({}, {"_id": False}))

    return jsonify({"result": fav_movie_list})
    # 영화 _id 로 찾고 없으면 리스트에 추가해줌



# 영화 등록 해제
# "/movie/unregister" - GET
@app.route("/movie/unregister/<oid>", methods=["GET"])
def movie_unregister(oid):
    db.user_movie.delete_one({"fav_movie": oid})

    fav_movie_list = list(db.user_movie.find({}, {"_id": False}))
    return jsonify({"result": fav_movie_list})


# 장바구니 영화 리스트 확인
# "/movie/user_favorite"
@app.route("/movie/user_favorite", methods=["GET"])
def movie_user_favorite():
    # 좋아하는 영화의 리스트
    movie_lst = list(db.user_movie.find({}, {"_id": False}))

    def pre_processing(movie):
        movie['_id'] = str(movie['_id'])
        return movie

    # 2. 좋아하는 영화의 리스트를 얻어냈고, 이 리스트를 토대로 영화 정보를 조회하기 위해
    # _id를 ObjectId화시킴
    fav_movie_list = [ObjectId(movie["fav_movie"]) for movie in movie_lst]

    # $in을 활용해 배열안에 있는 좋아하는 영화의 ObjectId를 토대로 모든 정보를 얻어내기
    # $in : 배열 안 쪽에 있는 것만 찾아내기 -> 연산자 : mongoDB 교재에 있음
    movie_detail_info = db.movie.find({"_id": {"$in": fav_movie_list}})

    # _id pre_processing
    movie_lst = [pre_processing(movie) for movie in movie_detail_info]
    return jsonify({'result': movie_lst})


if __name__ == "__main__":
    print("Server Start! ✅")
    app.run("0.0.0.0", 5000, debug=True)
