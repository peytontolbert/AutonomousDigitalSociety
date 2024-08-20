import logging

logging.basicConfig(level=logging.INFO)

import logging

logging.basicConfig(level=logging.INFO)

class StateManager:
    def __init__(self):
        self.state = {}
        logging.info("StateManager initialized")

    def set_state(self, key, value):
        try:
            self.state[key] = value
            logging.info(f"State set: {key} = {value}")
        except Exception as e:
            logging.error(f"Error setting state {key} = {value}: {e}")

    def get_state(self, key):
        try:
            value = self.state.get(key, None)
            logging.info(f"State requested: {key} = {value}")
            return value
        except Exception as e:
            logging.error(f"Error getting state {key}: {e}")
            return None

    def clear_state(self):
        try:
            self.state = {}
            logging.info("State cleared")
        except Exception as e:
            logging.error(f"Error clearing state: {e}")
