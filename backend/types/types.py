from dataclasses import dataclass
from typing import Literal, Optional
from pydantic import BaseModel


class ToGetUserInfo(BaseModel):
    id: str


class Message(BaseModel):
    message: str


class User(BaseModel):
    """id: str
    name: str
    status: str
    beacon: Optional[str] = None
    icon: Optional[bytes] = None"""
    id: str
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
    my_id: str
    target_id: str


class NameAndPassword(BaseModel):
    name: str
    password: str


class IdAndPassword(BaseModel):
    id: str
    password: str


class IdAndName(BaseModel):
    id: str
    name: str


class IdAndStatus(BaseModel):
    id: str
    status: str


class IdAndBeacon(BaseModel):
    id: str
    beacon: Optional[str] = None


class IdAndIcon(BaseModel):
    id: str
    icon: bytes


class CheckFriend(BaseModel):
    """id: str
    name: str
    icon_path: str
    applied: bool
    requested: bool
"""
    id: str
    name: str
    icon_path: str
    applied: bool
    requested: bool


@dataclass
class CustomError(Exception):
    status_code: int
    message: str


class CustomNotFoundException(CustomError):
    def __init__(self, id: str):
        self.id = id
    status_code = 404
    message = f"id is not found"

@dataclass
class CustomValidationException(CustomError):
    status_code = 422
    message = "invalid validation"


@dataclass
class CustomRecordStructureException(CustomError):
    # def __init__(self):
    #     super.__init__()
        # self.status_code = 422
        # self.message = "invalid structure"
    status_code = 422
    message = "invalid structure"


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
