from typing import Optional

from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.types.types import *

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
async def login(name_and_pass: NameAndPassword):
    name, _ = name_and_pass.name, name_and_pass.password
    if name:
        return {"message": "Ok"}
    return {"message": "Ng"}


# データ取得系
@app.get("/v1/user", response_model=User)
async def get_user(id: int):
    "return user by id"
    # ここ何返すか迷ってる
    # list[User] を返すようにするのもあり
    result = {"id": id,
              "name": "hoge",
              "status": 0,
              "beacon": "595教室",
              "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"}
    return result

# 友達検索ボタンを押したとき


@app.get("/v1/user/search",
         response_model=list[SearchUser],
         responses=error_response([CustomNotFoundException, CustomValidationException, CustomRecordStructureException, CustomSameIdException]))
async def search_users(my_id: int, target_name: str):
    """検索ボタンを押したときに、友だち関係を取得する必要がある
名前によって結果が変わる。
```
あ: どちらも片思いしていない
い: 片思いをしている
う: 片思いされている
え: 既に友だち
お: あ-え すべて
ア: not found (IDなし)
イ: 返ってくるデータの形が違う
ウ: validation error
```
    """

    result = [{"id": target_name, "name": "usr0",
              "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": False}]

    if target_name == "あ":
        result = [{"id": 100000, "name": "usr1",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": False}]
    if target_name == "い":
        result = [{"id": 100001, "name": "usr2",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": True, "requested": False}]
    if target_name == "う":
        result = [{"id": 100002, "name": "usr3",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": True}]
    if target_name == "え":
        result = [{"id": 100003, "name": "usr4",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": True, "requested": True}]
    if target_name == "お":
        result = [{"id": 100000, "name": "usr1",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": False},
                  {"id": 100001, "name": "usr2",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": True, "requested": False},
                  {"id": 100002, "name": "usr3",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": True},
                  {"id": 100003, "name": "usr4",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": True, "requested": True}
                  ]
    if target_name == "ア":
        raise CustomNotFoundException()
    if target_name == "イ":
        raise CustomRecordStructureException()
    if target_name == "ウ":
        raise CustomValidationException()
    # if target_name == "900003":
    #     raise CustomSameIdException()
    return result


@app.get("/v1/friends",
         response_model=Friends,
         responses=error_response([CustomNotFoundException, CustomValidationException, CustomRecordStructureException]))
async def get_friends(my_id: int):
    """友達一覧を返すやつ
正常
```
id: xxyyzz
```
`xx` -> 任意
`yy` -> 相互の数
`zz` -> 片思いの数

エラー
```
900000: not found (IDなし)
900001: 返ってくるデータの形が違う
900002: validation error -> 500吐くかも
```
    """
    # icon -> QueryString

    def user(my_id: int):
        return {"id": my_id,
                "name": f"usr{str(my_id).zfill(2)}",
                "status": 0,
                "beacon": "595教室",
                "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"}

    def result(id: int) -> dict[list[dict[str]]]:
        result = {"mutual": [], "one_side": []}

        mutual = id // 100 % 100
        one_side = id % 100

        for i in range(1, mutual+1):
            tmp_id = str(i).zfill(2)
            result["mutual"].append(user(tmp_id))
        for i in range(1, one_side+1):
            tmp_id = str(i+mutual).zfill(2)
            result["one_side"].append(user(tmp_id))
        return result

    if len(my_id) != 6:
        return {"mutual": [], "one_side": []}

    if my_id == 900000:
        raise CustomNotFoundException()
    if my_id == 900001:
        raise CustomRecordStructureException()
    if my_id == 900002:
        raise CustomValidationException()

    return result(my_id)


# ユーザーデータ変更系
@ app.post("/v1/user/name", response_model=Message)
async def update_profile(id_and_name: IdAndName):
    id, name = id_and_name.id, id_and_name.name
    if id and name:
        return {"message": "Ok"}
    return {"message": "Ng"}


@ app.post("/v1/user/status", response_model=Message)
async def update_status(id_and_status: IdAndStatus):
    id, status = id_and_status.id, id_and_status.status
    if id and status in list(range(4)):
        return {"message": "Ok"}
    return {"message": "Ng"}


@ app.post("/v1/user/icon", response_model=Message)
async def update_icon(id_and_icon: IdAndIcon):
    id, icon = id_and_icon.id, id_and_icon.icon
    # ファイルを投げる方法を調べる
    if id and icon:
        return {"message": "Ok"}
    return {"message": "Ng"}


@ app.post("/v1/user/beacon", response_model=Message)
async def update_profile(id_and_beacon: IdAndBeacon):
    id, beacon = id_and_beacon.id, id_and_beacon.beacon
    # feature: check(beacon)
    if id and beacon:
        return {"message": "Ok"}
    return {"message": "Ng"}


# 友達登録・削除周りの処理
@ app.post("/v1/friends/add", response_model=Message)
async def add_friend(id_pair: IdPair):
    follower_id, followee_id = id_pair.my_id, id_pair.target_id
    if len(follower_id) == 6 and len(followee_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@ app.post("/v1/friends/remove", response_model=Message)
async def remove_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.my_id, id_pair.target_id
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@ app.post("/v1/friends/reject", response_model=Message)
async def reject_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.my_id, id_pair.target_id
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


# Error Handling

@ app.exception_handler(CustomNotFoundException)
async def custom_not_found_exception(request: Request, exception: CustomNotFoundException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})


@ app.exception_handler(CustomValidationException)
async def custom_validation_exception(request: Request, exception: CustomValidationException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})


@ app.exception_handler(CustomRecordStructureException)
async def custom_record_structure_exception(request: Request, exception: CustomRecordStructureException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})


@ app.exception_handler(CustomSameIdException)
async def custom_same_id_exception(request: Request, exception: CustomSameIdException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})
