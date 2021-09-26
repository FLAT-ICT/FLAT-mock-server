from typing import Literal, Optional
from pydantic import BaseModel


class ToGetUserInfo(BaseModel):
    id: str
    icon: Optional[bool] = None


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
    icon: Optional[bytes] = None


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
    id1: str
    id2: str

class NameAndPassword(BaseModel):
    name: str
    password: str

class IdAndPassword(BaseModel):
    id: str
    password: str