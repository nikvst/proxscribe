import json
import uuid

import httpx

from servers.models import Server, Client, Inbound
from servers.xui_client.schemas.add_client import AddClientResponseSchema
from servers.xui_client.schemas.get_inbounds import (
    InboundsResponseSchema,
    InboundSchema,
)
from servers.xui_client.schemas.login import LoginResponseSchema
from servers.xui_client.schemas.delete_client import DeleteClientResponseSchema


def login(server: Server) -> str:
    response = httpx.post(
        f"{server.api_url}login",
        json={"username": server.username, "password": server.password},
        timeout=30,
    )
    response.raise_for_status()

    data = LoginResponseSchema.model_validate_json(response.content)

    if data.success is not True:
        raise Exception("Failed to login")

    return response.cookies["3x-ui"]


def get_inbounds(server: Server) -> list[InboundSchema]:
    token = login(server)

    cookies = {"3x-ui": token}
    response = httpx.post(
        f"{server.api_url}panel/inbound/list", cookies=cookies, timeout=30
    )
    response.raise_for_status()

    return InboundsResponseSchema.model_validate_json(response.content).obj


def add_client(inbound: Inbound):
    client_id = str(uuid.uuid4())
    email = str(uuid.uuid4())[:8]

    client_data = {
        **inbound.client_default_config,
        "id": client_id,
        "email": email,
    }

    data = {
        "id": inbound.xui_id,
        "settings": f'{{"clients": [{json.dumps(client_data)}]}}',
    }

    token = login(inbound.server)
    cookies = {"3x-ui": token}

    response = httpx.post(
        f"{inbound.server.api_url}panel/inbound/addClient",
        cookies=cookies,
        json=data,
        timeout=30,
    )
    response.raise_for_status()

    data = AddClientResponseSchema.model_validate_json(response.content)

    if data.success is not True:
        raise Exception("Failed to update client")

    return client_id, email, client_data


def delete_client(client: Client):
    token = login(client.inbound.server)
    cookies = {"3x-ui": token}

    if client.inbound.protocol == "vless":
        client_id = client.settings["id"]
    else:
        client_id = client.email

    response = httpx.post(
        f"{client.inbound.server.api_url}panel/inbound/{client.inbound.xui_id}/delClient/{client_id}",
        cookies=cookies,
        timeout=30,
    )
    response.raise_for_status()

    data = DeleteClientResponseSchema.model_validate_json(response.content)

    if data.success is not True:
        raise Exception("Failed to update client")
