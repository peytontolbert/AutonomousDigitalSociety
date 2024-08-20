
import os
import json
import logging
from chatgpt_interface_new import ChatGPTInterface



class Controller:
    """
    Controller class to manage personas and interact with ChatGPT interface.
    
    Attributes:
        state (str): The current state of the controller.
        current_persona (str): The currently selected persona.
        recent_actions (list): List of recent actions performed.
        available_computers (list): List of available computers.
        memory_file (str): Path to the memory file.
        memory (dict): Loaded memory data.
        chatgpt_interface (ChatGPTInterface): Interface to interact with ChatGPT.
    """
    def __init__(self):
        """
        Initializes the Controller with default values and loads memory from file.
        """
        logging.basicConfig(level=logging.INFO)
        self.state = 'idle'
        self.current_persona = None
        self.recent_actions = []
        self.available_computers = [
                    "Aetheria Nexus", "Aether Neura", "Alara Quantum", "Alennia Codeweaver", "Algorithmia Nova", "Algorithmus Quixote", "AriaNet", "Aria Luminex", "AstroLume", "Aurora Byte", "Ava Cipher", "Axion", "Bitwise Sage", "Byte-Quester", "ByteLynx", "Byte Maven", "Cipher Nox", "CodeLyra", "CodeMuse", "Codeora", "Cyra Nexus", "DataNarrator Orion", "DataRiff", "EchoSky", "Echo Byte", "Ekko", "Elysium 5.3", "Infolux", "Lexi Byte", "Lyra Nexus", "Nexus-42", "Nexus", "Nexus Byte", "Nexus Quantum", "NiaNeuron", "NovaSync", "Nova Codeflux", "Nova Cortex", "Nova Query", "Nova Synth", "NovoByte", "Orin Syntax", "Pixel Sage", "QuantaByte", "QuantumQuill", "Qubit", "Queryus", "Quorra Byte", "Quorra Flux", "Sample Persona", "Solara Bytewave", "Synthara", "Zephyr Bytewise", "Zoey Quantum"
                ]

        logging.info("Controller initialized with state 'idle'.")

        # Thinking: Loading memory from file.
        self.memory_file = 'controller_memory.json'
        self.chatgpt_interface = ChatGPTInterface(persona_name=self.current_persona, use_local_llm=True)
        self.load_memory()


    def load_memory(self):
        """
        Loads memory from the memory file if it exists, otherwise initializes with default values.
        """
        try:
            if (os.path.exists(self.memory_file)):
                with open(self.memory_file, 'r') as file:
                    self.memory = json.load(file)
                logging.info("Memory loaded from file.")
            else:
                self.memory = {}
                # Read system prompt and persona selection prompt
                with open(os.path.join('src', 'controllers', 'prompts', 'system_prompt.txt'), 'r') as file:
                    system_prompt = file.read().strip()
                with open(os.path.join('src', 'controllers', 'prompts', 'select_persona_prompt.txt'), 'r') as file:
                    prompt_template = file.read().strip()
                
                # Prepare prompt for ChatGPT
                prompt = prompt_template.replace('{{current_persona}}', str(self.current_persona)).replace('{{recent_actions}}', str(self.recent_actions))
                response = self.chatgpt_interface.chat_with_llm(system_prompt, prompt)
                logging.info(f"ChatGPT response: {response}")
                response = response.replace("Selected persona: ", "").strip()
                
                                # Validate and set the selected persona
                if response in self.available_computers:
                    self.current_computer = response
                    logging.info(f"Selected computer: {response}")
                else:
                    logging.error("Error: Invalid computer selected. Defaulting to 'Sample Computer'.")
                    self.current_computer = 'Sample Computer' 
                
                self.chatgpt_interface = ChatGPTInterface(persona_name=self.current_persona, use_local_llm=True)
                logging.info(f"Initialized with persona: {self.current_persona}")
        except Exception as e:
            logging.error(f"Error loading memory: {e}")
            raise RuntimeError("Failed to load persona memory. Stopping execution.")

    def select_personas(self, num_personas=3):
        self.selected_personas = []
        try:
            with open(os.path.join('src', 'controllers', 'prompts', 'select_persona_prompt.txt'), 'r') as file:
                prompt_template = file.read().strip()
            for _ in range(num_personas):
                prompt = prompt_template.replace('{{current_persona}}', str(self.current_persona)).replace('{{recent_actions}}', str(self.recent_actions))
                response = self.chatgpt_interface.chat_with_llm("", prompt)
                logging.info(f"ChatGPT response: {response}")
                response = response.replace("Selected persona: ", "").strip()
                if response in self.available_computers:
                    self.selected_personas.append(response)
                    logging.info(f"Selected persona: {response}")
                else:
                    logging.error("Error: Invalid persona selected. Defaulting to 'Sample Persona'.")
                    self.current_persona = 'Sample Persona'
        except Exception as e:
            logging.error(f"Error selecting persona: {e}")

    def develop_thoughts(self):
        try:
            with open(os.path.join('src', 'controllers', 'prompts', 'system_prompt.txt'), 'r') as file:
                system_prompt = file.read().strip()
            thoughts_prompt = f"Develop thoughts for persona {self.current_persona} based on recent actions: {self.recent_actions}"
            thoughts = self.chatgpt_interface.chat_with_llm(system_prompt, thoughts_prompt)
            logging.info(f"Developed thoughts: {thoughts}")
            return thoughts
        except Exception as e:
            logging.error(f"Error developing thoughts: {e}")
            return None

    def perform_computer_action(self, action, file_path=None, new_content=None):
        thoughts = self.develop_thoughts()
        if thoughts:
            logging.info(f"Performing action with thoughts: {thoughts}")
        if action == "view":
            return self.view_file(file_path)
        elif action == "edit":
            self.edit_file(file_path, new_content)
        elif action == "run":
            self.run_python_file(file_path)
        else:
            logging.error(f"Unknown action: {action}")

    def view_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            logging.info(f"Viewing file: {file_path}")
            return content
        except Exception as e:
            logging.error(f"Error viewing file {file_path}: {e}")
            return None

    def edit_file(self, file_path, new_content):
        try:
            with open(file_path, 'w') as file:
                file.write(new_content)
            logging.info(f"Edited file: {file_path}")
        except Exception as e:
            logging.error(f"Error editing file {file_path}: {e}")

    def run_python_file(self, file_path):
        try:
            exec(open(file_path).read())
            logging.info(f"Ran Python file: {file_path}")
        except Exception as e:
            logging.error(f"Error running Python file {file_path}: {e}")

    def perform_computer_action(self, action, file_path=None, new_content=None):
        if action == "view":
            return self.view_file(file_path)
        elif action == "edit":
            self.edit_file(file_path, new_content)
        elif action == "run":
            self.run_python_file(file_path)
        else:
            logging.error(f"Unknown action: {action}")

    def select_computer(self):
        logging.info("Selecting a computer.")

    def start(self):
        self.state = "running"
        logging.info("Controller state set to 'running'.")

    def stop(self):
        self.state = "stopped"
        logging.info("Controller state set to 'stopped'.")


    def run(self):
        """
        Runs the controller by reading system prompts and interacting with ChatGPT.
        """
        self.state = 'running'
        logging.info("Controller state set to 'running'.")

        # Step 1: Select a Persona
        self.select_personas()

        # Step 2: Develop Thoughts
        thoughts = self.develop_thoughts()

        # Read system prompt and persona selection prompt
        with open(os.path.join('src', 'controllers', 'prompts', 'system_prompt.txt'), 'r') as file:
            system_prompt = file.read().strip()
        with open(os.path.join('src', 'controllers', 'prompts', 'select_persona_prompt.txt'), 'r') as file:
            prompt_template = file.read().strip()

        # Step 3: Perform Action
        if thoughts:
            logging.info(f"Performing action with thoughts: {thoughts}")
            # Example action, you can replace this with actual actions
            self.perform_computer_action(action="view", file_path="example.txt")
        else:
            logging.error("No thoughts developed. Cannot perform action.")
        
        # Preparing prompt for ChatGPT.
        prompt = prompt_template.replace('{{current_persona}}', str(self.current_persona)).replace('{{recent_actions}}', str(self.recent_actions))
        response = self.chatgpt_interface.chat_with_llm(system_prompt, prompt)
        logging.info(f"ChatGPT response: {response}")
        # Extracting persona name from response.
        response = response.replace("Selected persona: ", "").strip()
        # Valid persona selected, updating current persona.
        if response in self.available_computers:
            self.current_computer = response
            logging.info(f"Selected computer: {response}")
        else:
            # Invalid persona selected, printing error message.
            logging.error("Error: Invalid computer selected.")

if __name__ == "__main__":
    controller = Controller()
    controller.run()

