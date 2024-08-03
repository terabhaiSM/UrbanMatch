
import requests

user_id = "user_id_for_match_finding"  # Replace with actual user ID
url = f"http://localhost:8000/users/{user_id}/matches"

response = requests.get(url)
print(response.status_code)
print(response.json())
