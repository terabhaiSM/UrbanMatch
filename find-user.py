import requests

# Define the base URL of your API
base_url = "http://localhost:8000"  # Replace with your API's base URL

# Define the user ID you want to find
user_id = "ba402a7f-6cfc-45fd-83c3-04ccb60fe654"  # Replace with the actual user ID

# Send a GET request to retrieve the user information
response = requests.get(f"{base_url}/users/{user_id}")

# Check if the request was successful
if response.status_code == 200:
    user = response.json()
    print("User found:", user)
else:
    print("Failed to retrieve user:", response.status_code, response.text)
