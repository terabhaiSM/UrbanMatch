import requests

user_id = "user_id_to_delete"  # Replace with actual user ID
url = f"http://localhost:8000/users/{user_id}"

response = requests.delete(url)
print(response.status_code)
print(response.json())
