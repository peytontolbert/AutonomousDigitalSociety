
import json

def select_three_personas(state_file):
    with open(state_file, 'r') as file:
        state = json.load(file)
    
    characters = state['characters']
    if len(characters) < 3:
        raise ValueError("Not enough characters to select three personas.")
    
    return characters[:3]

def update_persona_state(state_file, persona_name, new_state):
    with open(state_file, 'r') as file:
        state = json.load(file)
    
    for character in state['characters']:
        if character['name'] == persona_name:
            character.update(new_state)
            break
    
    with open(state_file, 'w') as file:
        json.dump(state, file, indent=4)

def handle_persona_actions(personas):
    actions = []
    for persona in personas:
        actions.append({
            "name": persona['name'],
            "actions": persona['actions']
        })
    return actions

if __name__ == "__main__":
    state_file = 'testScene_state.json'
    personas = select_three_personas(state_file)
    actions = handle_persona_actions(personas)
    print(json.dumps(actions, indent=4))
