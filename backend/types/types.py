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
    opponents_id: str


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
