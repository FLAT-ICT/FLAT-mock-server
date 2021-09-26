from typing import Optional

from fastapi import FastAPI

from backend.types.types import Friends, User

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 認証系
@app.post("/v1/registor")
async def registor(name: str, password: str):
    return {"message": "Ok"}


@app.post("/v1/login")
async def login(id: str, password: str):
    return {"message": "Ok"}


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
@app.post("/v1/me/name")
async def update_profile(id: str, name: str):
    pass


@app.post("/v1/me/status")
async def update_status(id: str, status: str):
    pass


@app.post("/v1/me/icon")
async def update_icon(id: str, icon: str):
    # ファイルを投げる方法を調べる
    pass


@app.post("/v1/me/beacon")
async def update_profile(id: str, profile: str):
    pass


# 友達登録・削除周りの処理
@app.post("v1/friends/add")
async def add_friend(user_id: str, follow_id: str):
    pass


@app.post("v1/friends/remove")
async def remove_friend(user_id: str, follower_id: str):
    pass


@app.post("v1/friends/reject")
async def reject_friend(user_id: str, follow_id: str):
    pass
