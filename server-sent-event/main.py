import asyncio
import uuid
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

rooms = {}
clients = {}

@app.post("/send/{room_id}")
async def send_message(room_id: str, message: str):
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(message)
    if room_id in clients:
        for client in clients[room_id].values():
            await client.put(message)
    return {"status": "Message sent"}

@app.get("/sse/{room_id}")
async def sse_messages(room_id: str):
    async def event_generator(client_queue: asyncio.Queue):
        try:
            while True:
                message = await client_queue.get()
                yield f"data: {message}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            # 연결이 끊어지면 큐를 삭제
            del clients[room_id][client_id]

    if room_id not in clients:
        clients[room_id] = {}

    client_queue = asyncio.Queue()
    client_id = str(uuid.uuid4())
    clients[room_id][client_id] = client_queue

    return StreamingResponse(event_generator(client_queue), media_type="text/event-stream", headers={"X-Client-ID": client_id})
