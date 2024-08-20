import json
import logging

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.set_logging_level()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            logging.info(f"Configuration loaded from {self.config_file}")
            return config
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_file} not found")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {self.config_file}: {e}")
            return {}

    def set_logging_level(self):
        level = self.config.get('logging_level', 'INFO').upper()
        logging.basicConfig(level=getattr(logging, level, logging.INFO))
        logging.info(f"Logging level set to {level}")

    def get_persona_defaults(self):
        return self.config.get('persona', {})

# Example usage
if __name__ == "__main__":
    config = Config()
    print(config.get_persona_defaults())
