from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

rooms = {}


@app.post("/send/{room_id}")
async def send_message(room_id: str, message: str):
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(message)
    return {"status": "Message sent"}


@app.get("/poll/{room_id}")
async def poll_messages(room_id: str):
    if room_id in rooms:
        return JSONResponse(content={"messages": rooms[room_id]})
    return JSONResponse(content={"messages": []})
