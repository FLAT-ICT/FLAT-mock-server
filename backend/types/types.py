from typing import Literal, Optional, Union
from pydantic import BaseModel

from dataclasses import dataclass

# class RegistorInfo(BaseModel):
#     name: str
#     password: str


# class LoginInfo(BaseModel):
#     id: str
#     passowrd: str

class ToGetUserInfo(BaseModel):
    id: str
    icon: Optional[bool] = None


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
