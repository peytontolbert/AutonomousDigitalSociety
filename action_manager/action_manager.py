
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ActionManager:
    def __init__(self):
        self.actions = []
        logging.info("ActionManager initialized")

    def add_action(self, action):
        try:
            self.actions.append(action)
            logging.info(f"Action added: {action}")
        except Exception as e:
            logging.exception(f"Exception occurred while adding action {action}")

    def list_actions(self):
        try:
            logging.info("Listing actions")
            return self.actions
        except Exception as e:
            logging.exception("Exception occurred while listing actions")
            return []

    def clear_actions(self):
        try:
            self.actions = []
            logging.info("Actions cleared")
        except Exception as e:
            logging.exception("Exception occurred while clearing actions")

    def perform_action(self, action):
        try:
            # Simulate performing an action
            logging.info(f"Performing action: {action}")
            return f"Action performed: {action}"
        except Exception as e:
            logging.exception(f"Exception occurred while performing action {action}")
            return f"Error performing action: {e}"