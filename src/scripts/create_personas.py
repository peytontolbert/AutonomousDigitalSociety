import requests
import os
import json

# URL of the application
base_url = 'http://localhost:5000'

# Directory containing persona files
personas_dir = 'data/personas'

# Read personas from files
personas = []
for filename in os.listdir(personas_dir):
    if filename.endswith('.json'):
        with open(os.path.join(personas_dir, filename), 'r') as file:
            persona = json.load(file)
            personas.append({'username': persona['name'], 'role': 'user'})

# Create personas
for persona in personas:
    response = requests.post(f'{base_url}/create_user', data=persona)
    if response.status_code == 200:
        print(f"User {persona['username']} created successfully.")
    else:
        print(f"Failed to create user {persona['username']}. Response: {response.text}")

# List of channels to create
channels = ['general', 'random', 'development']

# Create channels
for channel in channels:
    response = requests.post(f'{base_url}/create_channel', json={'channel_name': channel})
    if response.status_code == 200:
        print(f"Channel {channel} created successfully.")
    else:
        print(f"Failed to create channel {channel}. Response: {response.text}")

