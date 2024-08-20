import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import pyautogui

MODEL_PATH = "Qwen/Qwen-VL-Chat-Int4"
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, device_map="cuda", trust_remote_code=True).eval()

def interpret_command(response):
    # This function needs to be tailored to the specifics of the commands expected.
    if "open file" in response:
        pyautogui.hotkey('ctrl', 'o')  # Example for opening a file dialog
    elif "write code" in response:
        code_to_write = response.split("write code")[1].strip()
        pyautogui.write(code_to_write)
    elif "check status" in response:
        pyautogui.hotkey('ctrl', 'alt', 's')  # Custom shortcut for status check

while True:
    image_path = input("image path >>>>> ")
    image = Image.open(image_path).convert('RGB') if image_path else None
    history = []

    while True:
        query = input("Human:")
        if query.lower() in ["exit", "quit"]:
            break

        inputs = tokenizer.from_list_format([
            {'image': image_path},
            {'text': query},
        ])
        
        response, history = model.chat(tokenizer, query=inputs, history=history)
        print("Assistant:", response)
        interpret_command(response)
        history.append((query, response))
