import requests
import json

url = "http://127.0.0.1:5001/generate"
data = {
    "prompt": "Once upon a time",
    "max_length": 50
}

response = requests.post(url, json=data)
print(response.text)  # This will print the raw response from the server