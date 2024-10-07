import json
import typing as t

from pydantic import BaseModel, field_validator, ConfigDict

from ._base import BaseXUIResponseSchema


class SettingsClientBaseSchema(BaseModel):
    email: str
    enable: bool
    expiryTime: int
    limitIp: int
    subId: str
    totalGB: int

    model_config = ConfigDict(extra="allow")


class VLESSSettingsClientSchema(SettingsClientBaseSchema):
    flow: str
    id: str


class SSSettingsClientSchema(SettingsClientBaseSchema):
    method: str
    password: str


class SettingsSchema(BaseModel):
    clients: list[VLESSSettingsClientSchema | SSSettingsClientSchema]


class InboundSchema(BaseModel):
    id: int
    up: int
    down: int
    total: int
    remark: str
    enable: bool
    expiryTime: int
    listen: str
    port: int
    protocol: t.Literal["vless", "shadowsocks"]
    settings: SettingsSchema
    streamSettings: str
    tag: str

    @field_validator("settings", mode="before")
    @classmethod
    def parse_json_fields(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class InboundsResponseSchema(BaseXUIResponseSchema):
    obj: list[InboundSchema]
