from typing import Optional
from fastapi import FastAPI


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
@app.get("/v1/me")
async def get_me(id: str, icon: bool = False) -> None:
    return {"message": "Ok"}


@app.get("/v1/friends")
async def get_friends(id: str, icon: bool = False):
    # icon -> QueryString
    pass


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
