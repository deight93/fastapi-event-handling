import threading

import requests

room_id = "room1"


def send_message():
    response = requests.post(
        f"http://127.0.0.1:8000/send/{room_id}", json={"message": "Hello, SSE!"}
    )
    print(response.json())


def sse_messages():
    response = requests.get(f"http://127.0.0.1:8000/sse/{room_id}", stream=True)
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))


# 메시지 보내기
send_message_thread = threading.Thread(target=send_message)
send_message_thread.start()

# SSE 메시지 수신
sse_messages_thread = threading.Thread(target=sse_messages)
sse_messages_thread.start()
