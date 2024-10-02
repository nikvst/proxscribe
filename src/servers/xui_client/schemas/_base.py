import typing as t

from pydantic import BaseModel


class BaseXUIResponseSchema(BaseModel):
    success: bool
    msg: str
    obj: t.Any
