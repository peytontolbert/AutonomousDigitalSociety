
import torch
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM


app = Flask(__name__)

# Load the Hermes-3-Llama-3.1-8B model and tokenizer
model_name = "NousResearch/Hermes-3-Llama-3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = LlamaForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_8bit=False,
    load_in_4bit=False,
    use_flash_attention_2=False
)
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 8000)
    print(prompt)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    generated_ids = model.generate(input_ids, max_length=max_length, eos_token_id=tokenizer.eos_token_id)
    text = tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
    print(f"Response: {text}")
    return jsonify({'response': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


