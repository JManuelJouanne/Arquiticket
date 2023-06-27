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


# validations.py
# dentro de la vadilacion del grupo 20
# from websockets import send_message
# data = {
#     "user_id": "admin",
#     "event_id": request.event_id,
#     "quantity": request.quantity,
# }
# await send_message(data)

# Frontend
# Event list
# useEffect(() => {
#     const socket = new w3cwebsocket(`${process.env.REACT_APP_BACKEND_HOST_WS}/ws/sales`) //editar
#     setSocket(socket)

#     socket.onopen = () => {
#       console.log('Conexión establecida')
#     };

#     socket.onmessage = (message) => {
#         console.log('Mensaje recibido:', message.data)
#         const data = JSON.parse(message.data)
#         for (let i = 0; i < events.length; i++) {
#             if (events[i].id === data.id) {
#                 if (data.user_id === "admin") {
#                     events[i].quantity += data.quantity
#                 } else {
#                     events[i].quantity -= data.quantity
#                 }
#                 setEvents(events)  //setEvents([...events])
#             }
#         }
#     }

#     return () => {
#       socket.close();
#     }
# }, [])

# Buy tickets
# socket.send(data)
# pasar el socket como atributo
