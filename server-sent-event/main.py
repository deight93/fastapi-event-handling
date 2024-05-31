import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

rooms = {}


@app.post("/send/{room_id}")
async def send_message(room_id: str, message: str):
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(message)
    return {"status": "Message sent"}


@app.get("/sse/{room_id}")
async def sse_messages(room_id: str):
    async def event_generator():
        while True:
            if room_id in rooms and rooms[room_id]:
                message = rooms[room_id].pop(0)
                yield f"data: {message}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
