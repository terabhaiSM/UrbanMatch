import requests

url = "http://localhost:8000/users"
payload = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "password": "password123",
    "age": 30,
    "gender": "male"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
