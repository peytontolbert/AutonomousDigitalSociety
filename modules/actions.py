import logging

logging.basicConfig(level=logging.INFO)


def create_file(file_system, history, file_name, content):
    try:
        file_system[file_name] = content
        history.append(f"Created file {file_name}")
        logging.info(f"File created: {file_name}")
    except Exception as e:
        logging.error(f"Error creating file {file_name}: {e}")


def view_file(file_system, file_name):
    try:
        logging.info(f"Viewing file: {file_name}")
        return file_system.get(file_name, "File not found")
    except Exception as e:
        logging.error(f"Error viewing file {file_name}: {e}")
        return "Error viewing file"


def list_files(file_system):
    try:
        logging.info("Listing files")
        return list(file_system.keys())
    except Exception as e:
        logging.error(f"Error listing files: {e}")
        return []


def interact_with_discord(history, message):
    try:
        # Simulate interaction with Discord
        history.append(f"Interacted with Discord: {message}")
        logging.info(f"Interacted with Discord: {message}")
    except Exception as e:
        logging.error(f"Error interacting with Discord: {e}")

