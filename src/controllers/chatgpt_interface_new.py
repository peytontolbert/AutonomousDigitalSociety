


import openai
import os
import json
import requests

class ChatGPTInterface:
    def __init__(self, persona_name, use_local_llm=False):
        self.persona_name = persona_name
        self.memory_file = f'computers/{persona_name}.json'
        self.load_memory()
        self.conversation_history = []
        self.use_local_llm = use_local_llm

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                self.memory = json.load(file)
        else:
            self.memory = {}

    def save_memory(self):
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file)

    def add_to_history(self, user_message, bot_response):
        self.conversation_history.append({"user": user_message, "bot": bot_response})
        if len(self.conversation_history) > 10:  # Limit history to last 10 messages
            self.conversation_history.pop(0)

    def chat_with_llm(self, systemprompt, prompt, llm="gpt-4", tone="neutral"):
        if self.use_local_llm:
            return self.chat_with_local_llm(prompt)
        else:
            return self.chat_with_openai(systemprompt, prompt, llm, tone)

    def chat_with_openai(self, systemprompt, prompt, llm="gpt-4", tone="neutral"):
        try:
            # Adjust prompt based on tone
            if tone == "friendly":
                prompt = f"😊 {prompt}"
            elif tone == "serious":
                prompt = f"🔍 {prompt}"
            elif tone == "humorous":
                prompt = f"😂 {prompt}"

            response = openai.ChatCompletion.create(
                model=llm,
                messages=[
                    {"role": "system", "content": systemprompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=1,
            )
            bot_response = response.choices[0].message["content"]
            self.add_to_history(prompt, bot_response)
            return bot_response
        except openai.OpenAIError as e:
            print(f"Error generating response: {e}")
            return "Error generating response"
        except KeyError as e:
            print(f"KeyError: {e}")
            return "Error: Key not found in response"

    def chat_with_local_llm(self, prompt):
        try:
            response = requests.post('http://localhost:5001/generate', json={'prompt': prompt})
            response_json = response.json()
            bot_response = response_json.get('response', 'Error generating response')
            self.add_to_history(prompt, bot_response)
            return bot_response
        except requests.RequestException as e:
            print(f"Error generating response: {e}")
            return "Error generating response"







