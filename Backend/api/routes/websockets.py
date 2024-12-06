from fastapi import WebSocket
from fastapi import APIRouter

router_websocket = APIRouter()

active_connections = []


@router_websocket.websocket("/ws/sales")
async def echo(websocket: WebSocket):
    await websocket.accept()

    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await send_message(data)
    except Exception:
        active_connections.remove(websocket)
        await websocket.close()


async def send_message(message: str):
    for connection in active_connections:
        await connection.send_text(message)
