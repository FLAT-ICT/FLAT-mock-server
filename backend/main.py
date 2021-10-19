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

# 友達検索ボタンを押したとき


@app.get("/v1/user/check",
         response_model=CheckFriend,
         responses=error_response([CustomNotFoundException, CustomValidationException, CustomRecordStructureException, CustomSameIdException]))
async def check_friend(my_id: str, target_id: str):
    """検索ボタンを押したときに、友だち関係を取得する必要がある
target_id によって結果が変わる。
```
100000: どちらも片思いしていない
100001: 片思いをしている
100002: 片思いされている
100003: 既に友だち
900000: not found (IDなし)
900001: 返ってくるデータの形が違う
900002: validation error
900003: same id error
```
    """

    result = {"id": target_id, "name": "usr0",
              "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": False}

    if target_id == "100000":
        result = {"id": target_id, "name": "usr1",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": False}
    if target_id == "100001":
        result = {"id": target_id, "name": "usr2",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": True, "requested": False}
    if target_id == "100002":
        result = {"id": target_id, "name": "usr3",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": False, "requested": True}
    if target_id == "100003":
        result = {"id": target_id, "name": "usr4",
                  "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon", "applied": True, "requested": True}
    if target_id == "900000":
        raise CustomNotFoundException()
    if target_id == "900001":
        raise CustomRecordStructureException()
    if target_id == "900002":
        raise CustomValidationException()
    if target_id == "900003" or my_id == target_id:
        raise CustomSameIdException()
    return result


@app.get("/v1/friends",
         response_model=Friends,
         responses=error_response([CustomNotFoundException, CustomValidationException, CustomRecordStructureException]))
async def get_friends(my_id: str):
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

    def user(my_id: str):
        return {"id": f"0000{my_id}",
                "name": f"usr{my_id}",
                "status": 0,
                "beacon": "595教室",
                "icon_path": "https://dummyimage.com/64x64/000/fff&text=icon"}

    def result(id: str) -> dict[list[dict[str]]]:
        result = {"mutual": [], "one_side": []}

        mutual = int(id[2:4])
        one_side = int(id[4:])

        for i in range(1, mutual+1):
            tmp_id = str(i).zfill(2)
            result["mutual"].append(user(tmp_id))
        for i in range(1, one_side+1):
            tmp_id = str(i+mutual).zfill(2)
            result["one_side"].append(user(tmp_id))
        return result

    if len(my_id) != 6:
        return {"mutual": [], "one_side": []}

    if my_id == "900000":
        raise CustomNotFoundException()
    if my_id == "900001":
        raise CustomRecordStructureException()
    if my_id == "900002":
        raise CustomValidationException()

    return result(my_id)


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
    follower_id, followee_id = id_pair.my_id, id_pair.target_id
    if len(follower_id) == 6 and len(followee_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/friends/remove", response_model=Message)
async def remove_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.my_id, id_pair.target_id
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


@app.post("/v1/friends/reject", response_model=Message)
async def reject_friend(id_pair: IdPair):
    user_id, follow_id = id_pair.my_id, id_pair.target_id
    if len(user_id) == 6 and len(follow_id) == 6:
        return {"message": "Ok"}
    return {"message": "Ng"}


# Error Handling

@app.exception_handler(CustomNotFoundException)
async def custom_not_found_exception(request: Request, exception: CustomNotFoundException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})


@app.exception_handler(CustomValidationException)
async def custom_validation_exception(request: Request, exception: CustomValidationException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})


@app.exception_handler(CustomRecordStructureException)
async def custom_record_structure_exception(request: Request, exception: CustomRecordStructureException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})


@app.exception_handler(CustomSameIdException)
async def custom_same_id_exception(request: Request, exception: CustomSameIdException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message})
