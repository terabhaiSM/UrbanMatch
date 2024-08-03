import requests

user_id = "user_id_to_update"  # Replace with actual user ID
url = f"http://localhost:8000/users/{user_id}"
payload = {
    "name": "John Doe Updated",
    "email": "johnupdated@example.com",
    "password": "newpassword123",
    "age": 31
}

headers = {
    "Content-Type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
