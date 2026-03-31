#!/usr/bin/env python3
"""
V8 Web Application Backend
Serves HTML UI and processes Parikarma analysis requests
"""

from flask import Flask, request, jsonify, send_file
from pathlib import Path
import re

app = Flask(__name__)

# Global model variables
model = None
tokenizer = None

def load_v8_model():
    """Load V8 model once at startup"""
    global model, tokenizer

    if model is not None:
        return True

    print("🔄 Loading V8 model...")

    try:
        from transformers import AutoTokenizer
        from peft import AutoPeftModelForCausalLM
        import torch

        model_path = "model/parikarma-lora-v8"

        if not Path(model_path).exists():
            print(f"❌ Model not found at {model_path}")
            return False

        model = AutoPeftModelForCausalLM.from_pretrained(
            model_path,
            device_map="cpu",
            torch_dtype=torch.float32,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        print("✅ V8 model loaded successfully")
        return True

    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

def format_prompt(message, relationship, channel, time):
    """Format message with context for V8"""
    return f"""MY MESSAGE:
{message}

CONTEXT:
- Relationship: {relationship}
- Channel: {channel}
- Time: {time}

Analyze this message and respond with EXACTLY this format (no additional text):

PARIKARMA: [Choose ONE: KARUNA/MAITRI/MUDITA/UPEKSHA]
WHY: [One sentence explaining why]
IDEAL RESPONSE: [The actual message to send]

Remember (Power-Dynamic Framework):
- KARUNA: Recipient has LESS (power/control/health/options) than you → compassion from strength
- MUDITA: Recipient has MORE (success/power/growth) than you → appreciative joy toward their success
- MAITRI: EQUAL power/control → friendliness (not friendship), no expectations
- UPEKSHA: Bad impact from recipient on YOU → objectivity not subjectivity, indifference to harm

Output the three fields above ONLY. Do not explain or list multiple options."""

def parse_v8_response(response):
    """Parse PARIKARMA / WHY / IDEAL RESPONSE from V8 output"""
    parikarma = "Not identified"
    why = "Not provided"
    ideal_response = "Not provided"

    # Extract PARIKARMA
    parikarma_match = re.search(r'(?:PARIKARMA|Parikarma):\s*([A-Z]+)', response, re.IGNORECASE)
    if parikarma_match:
        parikarma = parikarma_match.group(1).upper()

    # Extract WHY
    why_match = re.search(
        r'(?:WHY|Reason):\s*(.+?)(?=(?:IDEAL RESPONSE|Parikarma|PARIKARMA|WHY|Reason|$))',
        response,
        re.IGNORECASE | re.DOTALL,
    )
    if why_match:
        why = why_match.group(1).strip().split('\n')[0].strip()

    # Extract IDEAL RESPONSE
    ideal_match = re.search(
        r'IDEAL RESPONSE:\s*(.+?)(?=(?:Parikarma|PARIKARMA|WHY|Reason|IDEAL RESPONSE|<\|end\|>|$))',
        response,
        re.IGNORECASE | re.DOTALL,
    )
    if ideal_match:
        ideal_text = ideal_match.group(1).strip()
        if not ideal_text.startswith('['):
            lines = ideal_text.split('\n')
            ideal_response = ' '.join(line.strip() for line in lines[:3] if line.strip())
            if len(ideal_response) < 20:
                ideal_response = "Not provided"

    return {
        "parikarma": parikarma,
        "why": why,
        "ideal_response": ideal_response,
    }

@app.route('/')
def index():
    """Serve the HTML interface"""
    return send_file('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process Parikarma analysis request"""
    global model, tokenizer

    # Load model if not loaded
    if model is None:
        if not load_v8_model():
            return jsonify({
                'error': 'Model failed to load. Check that models/parikarma-lora-v8 exists.'
            }), 500

    try:
        data = request.json
        message = data.get('message', '').strip()
        relationship = data.get('relationship', 'peer')
        channel = data.get('channel', 'email')
        time = data.get('time', 'afternoon')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Format prompt with chat template
        prompt = format_prompt(message, relationship, channel, time)
        formatted_prompt = f"<|user|>\n{prompt}<|end|>\n<|assistant|>\n"

        # Generate response
        inputs = tokenizer(formatted_prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract assistant part
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1].strip()

        # Remove end token if present
        if "<|end|>" in response:
            response = response.split("<|end|>")[0].strip()

        # Parse structured output
        parsed = parse_v8_response(response)
        parsed['raw_output'] = response  # Include raw for debugging

        return jsonify(parsed)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n🕉️  MANAS V8 Web Interface")
    print("=" * 70)
    print("Starting server...")
    print("=" * 70)

    # Load model at startup
    load_v8_model()

    print("\n✅ Server ready at http://localhost:5001")
    print("=" * 70)

    app.run(debug=True, host='0.0.0.0', port=5001)
