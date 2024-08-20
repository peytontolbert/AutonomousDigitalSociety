
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.controllers.controller import Controller

def test_controller():
    controller = Controller()
    controller.start()
    print("Controller started successfully.")
    controller.stop()
    print("Controller stopped successfully.")
    state = controller.get_state()
    print(f"Controller state: {state}")

if __name__ == "__main__":
    test_controller()
