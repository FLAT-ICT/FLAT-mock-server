from dataclasses import dataclass
from typing import Literal, Optional
from pydantic import BaseModel


class ToGetUserInfo(BaseModel):
    id: int


class Message(BaseModel):
    message: str


class User(BaseModel):
    """id: int
    name: str
    status: int
    spot: Optional[str] = None
    icon: str"""
    id: int
    name: str
    status: int
    spot: str = ""
    icon_path: str
    loggedin_at: str


class IsLoggedIn(BaseModel):
    """own(bool): 自分の端末でログインしているかどうか
    others(bool): 他の端末でログインしているかどうか
    """
    own: bool
    others: bool


class Friends(BaseModel):
    """mutual: list[User]
    one_side: list[User]"""
    mutual: list[User]
    one_side: list[User]


class Result(BaseModel):
    """result: Literal["correct", "error"]
    message: str"""
    result: Literal["correct", "error"]
    message: str


class IdPair(BaseModel):
    my_id: int
    target_id: int


class NameAndPassword(BaseModel):
    name: str
    password: str


class IdAndPassword(BaseModel):
    id: int
    password: str


class IdAndName(BaseModel):
    my_id: int
    target_name: str


class IdAndStatus(BaseModel):
    id: int
    status: str


class ScannedBeacon(BaseModel):
    user_id: int
    # uuid: str
    major: int
    minor: int
    rssi: float
    # distance: int


class IdAndIcon(BaseModel):
    id: int
    icon: str  # base64 encoding


class SearchUser(BaseModel):
    """id: int  
    name: str  
    icon_path: str  
    applied: bool  
    requested: bool  
"""
    id: int
    name: str
    icon_path: str
    applied: bool
    requested: bool


class CustomError(Exception):
    status_code: int
    message: str


class CustomNotFoundException(CustomError):
    status_code = 404
    message = f"id is not found"


class CustomValidationException(CustomError):
    status_code = 422
    message = "invalid validation"


class CustomRecordStructureException(CustomError):
    # def __init__(self):
    #     super.__init__()
    # self.status_code = 422
    # self.message = "invalid structure"
    status_code = 422
    message = "invalid structure"


class CustomSameIdException(CustomError):
    status_code = 471
    message = "can't assign same id"


class CustomInvalidPassword(CustomError):
    status_code = 400
    massge = "invalid password"


def error_response(error_types: list[CustomError]) -> dict:
    # error_types に列挙した ApiError を OpenAPI の書式で定義する
    d = {}
    for et in error_types:
        if not d.get(et.status_code):
            d[et.status_code] = {
                'description': f'"{et.message}"',
                'content': {
                    'application/json': {
                        'example': {
                            'message': et.message
                        }
                    }
                }}
        else:
            # 同じステータスコードなら description を追記
            d[et.status_code]['description'] += f'<br>"{et.message}"'
    return d
