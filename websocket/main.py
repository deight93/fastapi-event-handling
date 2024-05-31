from typing import Dict, List

from fastapi import FastAPI, WebSocket

app = FastAPI()

rooms: Dict[str, List[WebSocket]] = {}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in rooms[room_id]:
                if client != websocket:
                    await client.send_text(data)
    except Exception:
        rooms[room_id].remove(websocket)
