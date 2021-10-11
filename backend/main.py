from typing import Optional

from fastapi import FastAPI

from backend.types.types import Friends, IdAndBeacon, IdAndIcon, IdAndName, IdAndPassword, IdAndStatus, IdPair, Message, NameAndPassword, User

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 認証系
@app.post("/v1/registor")
async def registor(name_and_pass: NameAndPassword):
    name, _ = name_and_pass.name, name_and_pass.password
    if name:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/login")
async def login(id_and_password: IdAndPassword):
    id, _ = id_and_password.id, id_and_password.password
    if len(id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


# データ取得系
@app.get("/v1/user", response_model=User)
async def get_user(id: str):
    "return user by id"
    # ここ何返すか迷ってる
    # list[User] を返すようにするのもあり
    if len(id) != 6:
        return []
    result = {"id": id,
              "name": "hoge",
              "status": 0,
              "beacon": "595教室",
              "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"}
    return result


@app.get("/v1/friends", response_model=Friends)
async def get_friends(id: str):
    # icon -> QueryString
    if len(id) != 6:
        return {"mutual": [], "one_side": []}
    result = {
        "mutual": [
            {"id": "000000",
             "name": "usr01",
             "status": 0,
             "beacon": "595教室",
             "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"},
            {"id": "000001",
             "name": "usr02",
             "status": 0,
             "beacon": "講堂",
             "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"},
            {"id": "000002",
             "name": "usr03",
             "status": 0,
             "beacon": "体育館",
             "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"}
        ],
        "one_side": [
            {"id": "000010",
             "name": "usr10",
             "status": 0,
             "beacon": "情報ライブラリー",
             "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"}
        ]
    }
    return result


# ユーザーデータ変更系
@app.post("/v1/user/name", response_model=Message)
async def update_profile(id_and_name: IdAndName):
    id, name = id_and_name.id, id_and_name.name
    if len(id) == 6 and name:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/user/status", response_model=Message)
async def update_status(id_and_status: IdAndStatus):
    id, status = id_and_status.id, id_and_status.status
    if len(id) == 6 and status in list(range(4)):
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/user/icon", response_model=Message)
async def update_icon(id_and_icon: IdAndIcon):
    id, icon = id_and_icon.id, id_and_icon.icon
    # ファイルを投げる方法を調べる
    if len(id) == 6 and icon:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/user/beacon", response_model=Message)
async def update_profile(id_and_beacon: IdAndBeacon):
    id, beacon = id_and_beacon.id, id_and_beacon.beacon
    # feature: check(beacon)
    if len(id) == 6 and beacon:
        return {"message": "Ok"}
    return {"message": "Ng"}


# 友達登録・削除周りの処理
@app.post("/v1/friends/add", response_model=Message)
async def add_friend(id_pair: IdPair):
    follower_id, followee_id = id_pair.my_id, id_pair.opponents_id
    if len(follower_id) == 6 and len(followee_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/friends/remove", response_model=Message)
async def remove_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.my_id, id_pair.opponents_id
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/friends/reject", response_model=Message)
async def reject_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.my_id, id_pair.opponents_id
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}
