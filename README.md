

# Digital Entity Society Controller

## Project Overview
Digital Entity Society Controller is a Python project that provides functionalities for managing digital entities, actions, and states. The core component of this project is the `Controller` class, which manages personas and interacts with a local model by default. Users can easily switch to using ChatGPT if desired.

## Installation
To install the project, clone the repository and navigate to the project directory:
```bash
git clone <repository_url>
cd DigitalEntitySocietyController
```

## Usage
The project contains the following modules:
- `persona`: Manages digital entities with attributes like name, background, and interests.
- `action_manager`: Manages actions for digital entities.
- `controller`: Controls the state of the system.
- `state_management`: Manages the state of the system.

### Controller Class
The `Controller` class is responsible for:
- Managing the current state of the system (e.g., idle, running, stopped).
- Handling the current persona and recent actions.
- Interacting with a local model by default, with an option to switch to ChatGPT.
- Loading and saving memory to a file to maintain state across sessions.

#### Key Attributes:
- `state`: The current state of the controller.
- `current_persona`: The currently selected persona.
- `recent_actions`: List of recent actions performed.
- `available_computers`: List of available computers.
- `memory_file`: Path to the memory file.
- `memory`: Loaded memory data.
- `chatgpt_interface`: Interface to interact with ChatGPT.
- `use_local_model`: Boolean flag to determine whether to use the local model or ChatGPT.

#### Key Methods:
- `__init__`: Initializes the controller with default values and loads memory from a file.
- `load_memory`: Loads memory from the memory file if it exists, otherwise initializes with default values.
- `get_state`: Returns the current state.
- `perform_computer_action`: Placeholder for performing actions with the current computer.
- `select_computer`: Placeholder for selecting a computer.
- `start`: Sets the state to "running".
- `stop`: Sets the state to "stopped".
- `run`: Runs the controller by reading system prompts and interacting with the selected model (local or ChatGPT).
- `switch_to_chatgpt`: Switches the interface to use ChatGPT.
- `switch_to_local_model`: Switches the interface to use the local model.

## Running Tests
To run the tests, use the following command:
```bash
python test_project.py
```

## Running the Application
To run the application, follow these steps:
1. **Set up the virtual environment**:
```bash
python -m venv new_venv
source new_venv/bin/activate
```
2. **Install the necessary dependencies**:
```bash
pip install -r requirements.txt
```
3. **Configure the application**:
   - Ensure that the `config.json` file is properly set up with the required configurations.
4. **Run the application**:
```bash
python src/controllers/controller.py
```
5. **Verify the application**:
   - Check the logs and outputs to ensure that the application is running correctly.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Project Overview
Digital Entity Society Controller is a Python project that provides functionalities for managing digital entities, actions, and states. The core component of this project is the `Controller` class, which manages personas and interacts with the ChatGPT interface to perform various actions and maintain the state of the system.

## Installation
To install the project, clone the repository and navigate to the project directory:
```bash
git clone <repository_url>
cd DigitalEntitySocietyController
```

## Usage
The project contains the following modules:
- `persona`: Manages digital entities with attributes like name, background, and interests.
- `action_manager`: Manages actions for digital entities.
- `controller`: Controls the state of the system.
- `state_management`: Manages the state of the system.

### Controller Class
The `Controller` class is responsible for:
- Managing the current state of the system (e.g., idle, running, stopped).
- Handling the current persona and recent actions.
- Interacting with the ChatGPT interface to select personas and perform actions.
- Loading and saving memory to a file to maintain state across sessions.

#### Key Attributes:
- `state`: The current state of the controller.
- `current_persona`: The currently selected persona.
- `recent_actions`: List of recent actions performed.
- `available_computers`: List of available computers.
- `memory_file`: Path to the memory file.
- `memory`: Loaded memory data.
- `chatgpt_interface`: Interface to interact with ChatGPT.

#### Key Methods:
- `__init__`: Initializes the controller with default values and loads memory from a file.
- `load_memory`: Loads memory from the memory file if it exists, otherwise initializes with default values.
- `get_state`: Returns the current state.
- `perform_computer_action`: Placeholder for performing actions with the current computer.
- `select_computer`: Placeholder for selecting a computer.
- `start`: Sets the state to "running".
- `stop`: Sets the state to "stopped".
- `run`: Runs the controller by reading system prompts and interacting with ChatGPT.

## Running Tests
To run the tests, use the following command:
```bash
python test_project.py
```

## Running the Application
To run the application, follow these steps:
1. **Set up the virtual environment**:
```bash
python -m venv new_venv
source new_venv/bin/activate
```
2. **Install the necessary dependencies**:
```bash
pip install -r requirements.txt
```
3. **Configure the application**:
   - Ensure that the `config.json` file is properly set up with the required configurations.
4. **Run the application**:
```bash
python src/controllers/controller.py
```
5. **Verify the application**:
   - Check the logs and outputs to ensure that the application is running correctly.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.



