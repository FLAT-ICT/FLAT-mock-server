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
    status: str
    beacon: Optional[str] = None
    icon: Optional[bytes] = None"""
    id: int
    name: str
    status: str
    beacon: Optional[str] = None
    icon_path: str


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
    id: int
    name: str


class IdAndStatus(BaseModel):
    id: int
    status: str


class ScannedBeacon(BaseModel):
    user_id: int
    uuid: str
    major: int
    minor: int
    rssi: int
    distance: int


class IdAndIcon(BaseModel):
    id: int
    icon: bytes


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
