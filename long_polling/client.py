import threading

import requests

room_id = "room1"


def send_message():
    response = requests.post(
        f"http://127.0.0.1:8000/send/{room_id}",
        json={"message": "Hello, Long Polling!"},
    )
    print(response.json())


def poll_messages():
    while True:
        response = requests.get(f"http://127.0.0.1:8000/poll/{room_id}")
        print(response.json())


# 메시지 보내기
send_message_thread = threading.Thread(target=send_message)
send_message_thread.start()

# 메시지 폴링
poll_messages_thread = threading.Thread(target=poll_messages)
poll_messages_thread.start()
