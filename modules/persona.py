import os
import json
import logging
from modules.config import Config
from modules.actions import create_file, view_file, list_files, interact_with_discord, join_discord_server


logging.basicConfig(level=logging.INFO)


class Persona:
    def __init__(self, name=None, background=None, interests=None, computer_directory=None):
        config = Config()
        persona_defaults = config.get_persona_defaults()
        self.name = name or persona_defaults.get('default_name', 'DefaultName')
        self.background = background or persona_defaults.get('default_background', 'DefaultBackground')
        self.interests = interests or persona_defaults.get('default_interests', [])
        self.computer_directory = computer_directory or f"computers/{self.name.replace(' ', '_')}"
        self.history = []
        self.file_system = {}
        logging.info(f"Persona created: {self.name}")

    def create_file(self, file_name, content):
        create_file(self.file_system, self.history, file_name, content)

    def view_file(self, file_name):
        return view_file(self.file_system, file_name)

    def list_files(self):
        return list_files(self.file_system)

    def interact_with_discord(self, message):
        interact_with_discord(self.history, message)

    def save_state(self):
        state = {
            "name": self.name,
            "background": self.background,
            "interests": self.interests,
            "history": self.history,
            "file_system": self.file_system
        }
        os.makedirs(self.computer_directory, exist_ok=True)
        with open(f"{self.computer_directory}/persona_state.json", "w") as file:
            json.dump(state, file)

    def load_state(self):
        try:
            with open(f"{self.computer_directory}/persona_state.json", "r") as file:
                state = json.load(file)
                self.name = state["name"]
                self.background = state["background"]
                self.interests = state["interests"]
                self.history = state["history"]
                self.file_system = state["file_system"]
        except FileNotFoundError:
            logging.warning("State file not found. Loading default state.")

    def add_to_history(self, entry):
        self.history.append(entry)
        logging.info(f"Added to history: {entry}")

