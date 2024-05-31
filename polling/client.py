import time

import requests

room_id = "room1"

# 메시지 보내기
response = requests.post(
    f"http://127.0.0.1:8000/send/{room_id}", json={"message": "Hello, Polling!"}
)
print(response.json())

# 메시지 폴링
while True:
    response = requests.get(f"http://127.0.0.1:8000/poll/{room_id}")
    print(response.json())
    time.sleep(5)  # 5초마다 폴링
