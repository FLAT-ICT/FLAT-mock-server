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
@app.get("/v1/me", response_model=list[User])
async def get_me(id: str, icon: Optional[bool] = None):
    # ここ何返すか迷ってる
    # list[User] を返すようにするのもあり
    if len(id) != 6:
        return []
    result = [{"id": id, "name": "hoge",
              "status": "学内にいる", "beacon": "595教室"}]
    if icon:
        result[0].update({"icon": "this_is_binary_icon"})
    return result


@app.get("/v1/friends", response_model=Friends)
async def get_friends(id: str, icon: Optional[bool] = None):
    # icon -> QueryString
    if len(id) != 6:
        return {"mutual": [], "one_side": []}
    result = {
        "mutual": [
            {"id": "000000", "name": "usr01",
             "status": "学内にいる", "beacon": "595教室"},
            {"id": "000001", "name": "usr02",
             "status": "学内にいる", "beacon": "講堂"},
            {"id": "000002", "name": "usr03",
             "status": "学内にいる", "beacon": "体育館"}
        ],
        "one_side": [
            {"id": "000010", "name": "usr10",
             "status": "学内にいる", "beacon": "情報ライブラリー"}
        ]
    }
    if icon:
        for item in result["mutual"]:
            item.update({"icon": b"binary_object"})
        for item in result["one_side"]:
            item.update({"icon": b"binary_object"})
    return result


# ユーザーデータ変更系
@app.post("/v1/me/name", response_model=Message)
async def update_profile(id_and_name: IdAndName):
    id, name = id_and_name.id, id_and_name.name
    if len(id) == 6 and name:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/me/status", response_model=Message)
async def update_status(id_and_status: IdAndStatus):
    id, status = id_and_status.id, id_and_status.status
    if len(id) == 6 and status in ["学校にいる", "今暇", "忙しい", "学校にいない"]:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/me/icon", response_model=Message)
async def update_icon(id_and_icon: IdAndIcon):
    id, icon = id_and_icon.id, id_and_icon.icon
    # ファイルを投げる方法を調べる
    if len(id) == 6 and icon:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/me/beacon", response_model=Message)
async def update_profile(id_and_beacon: IdAndBeacon):
    id, beacon = id_and_beacon.id, id_and_beacon.beacon
    # feature: check(beacon)
    if len(id) == 6 and beacon:
        return {"message": "Ok"}
    return {"message": "Ng"}


# 友達登録・削除周りの処理
@app.post("/v1/friends/add", response_model=Message)
async def add_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.id1, id_pair.id2
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/friends/remove", response_model=Message)
async def remove_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.id1, id_pair.id2
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@ app.post("/v1/friends/reject", response_model=Message)
async def reject_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.id1, id_pair.id2
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}
