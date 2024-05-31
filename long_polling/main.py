import asyncio

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

rooms = {}
clients = {}


@app.post("/send/{room_id}")
async def send_message(room_id: str, message: str):
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(message)
    if room_id in clients:
        for client in clients[room_id]:
            await client.put(message)
        clients[room_id].clear()
    return {"status": "Message sent"}


@app.get("/poll/{room_id}")
async def poll_messages(room_id: str):
    if room_id not in clients:
        clients[room_id] = []
    client_queue = asyncio.Queue()
    clients[room_id].append(client_queue)
    message = await client_queue.get()
    return JSONResponse(content={"messages": [message]})
