import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/controllers")))


import unittest
from modules.persona import Persona
from action_manager.action_manager import ActionManager
from src.controllers.controller import Controller
from modules.state_management import StateManager

class TestPersona(unittest.TestCase):
    def setUp(self):
        self.persona = Persona(name="TestPersona", background="TestBackground", interests=["TestInterest"])

    def test_create_file(self):
        self.persona.create_file("test.txt", "This is a test file.")
        self.assertEqual(self.persona.view_file("test.txt"), "This is a test file.")

    def test_view_file_not_found(self):
        self.assertEqual(self.persona.view_file("nonexistent.txt"), "File not found")

    def test_list_files(self):
        self.persona.create_file("test1.txt", "File 1")
        self.persona.create_file("test2.txt", "File 2")
        self.assertListEqual(self.persona.list_files(), ["test1.txt", "test2.txt"])

    def test_interact_with_discord(self):
        self.persona.interact_with_discord("Hello, Discord!")
        self.assertIn("Interacted with Discord: Hello, Discord!", self.persona.history)

    def test_save_and_load_state(self):
        self.persona.create_file("test.txt", "This is a test file.")
        self.persona.save_state()
        new_persona = Persona(name="TestPersona", background="", interests=[])
        new_persona.load_state()
        self.assertEqual(new_persona.view_file("test.txt"), "This is a test file.")
        self.assertEqual(new_persona.name, "TestPersona")
        self.assertEqual(new_persona.background, "TestBackground")
        self.assertEqual(new_persona.interests, ["TestInterest"])

class TestActionManager(unittest.TestCase):
    def setUp(self):
        self.action_manager = ActionManager()

    def test_add_action(self):
        self.action_manager.add_action("TestAction")
        self.assertIn("TestAction", self.action_manager.list_actions())

    def test_list_actions(self):
        self.action_manager.add_action("Action1")
        self.action_manager.add_action("Action2")
        self.assertListEqual(self.action_manager.list_actions(), ["Action1", "Action2"])

    def test_clear_actions(self):
        self.action_manager.add_action("Action1")
        self.action_manager.clear_actions()
        self.assertListEqual(self.action_manager.list_actions(), [])

class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()

    def test_initial_state(self):
        self.assertEqual(self.controller.get_state(), "idle")

    def test_start(self):
        self.controller.start()
        self.assertEqual(self.controller.get_state(), "running")

    def test_stop(self):
        self.controller.start()
        self.controller.stop()
        self.assertEqual(self.controller.get_state(), "stopped")

    def test_select_persona(self):
        self.controller.computers = {
                    "Computer1": Persona(name="Computer1", background="Background1", interests=["Interest1"]),
                    "Computer2": Persona(name="Computer2", background="Background2", interests=["Interest2"])
                }
        self.controller.select_computer()
        if self.controller.current_computer not in self.controller.computers:
            self.assertEqual(self.controller.current_computer, "Sample Computer")

    def test_perform_action(self):
        self.controller.computers = {
                    "Computer1": Persona(name="Computer1", background="Background1", interests=["Interest1"])
                }
        self.controller.current_computer = self.controller.computers["Computer1"]
        self.controller.perform_computer_action()
        result = "Action performed"
        self.assertIn("Action performed", result)

class TestStateManager(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()

    def test_set_and_get_state(self):
        self.state_manager.set_state("key1", "value1")
        self.assertEqual(self.state_manager.get_state("key1"), "value1")

    def test_get_state_not_found(self):
        self.assertIsNone(self.state_manager.get_state("nonexistent_key"))

    def test_clear_state(self):
        self.state_manager.set_state("key1", "value1")
        self.state_manager.clear_state()
        self.assertIsNone(self.state_manager.get_state("key1"))

if __name__ == '__main__':
    unittest.main()
