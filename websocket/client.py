import asyncio

import websockets

room_id = "room1"


async def send_message():
    async with websockets.connect(f"ws://127.0.0.1:8000/ws/{room_id}") as websocket:
        await websocket.send("Hello, WebSocket!")
        while True:
            message = await websocket.recv()
            print(message)


asyncio.get_event_loop().run_until_complete(send_message())
