# MANAS V8 - Parikarma Communication Assistant

**A fine-tuned language model for Parikarma-aware communication in Indian professional contexts**

---

## What is Parikarma?

The four **Parikarma** (परिकर्म) attitudes from Yoga philosophy guide how we respond to different situations based on power dynamics:

| Parikarma | When to Use | Key Principle |
|-----------|-------------|---------------|
| **KARUNA** (करुणा) | Recipient has **LESS** power/control/health than you | Compassion from strength |
| **MAITRI** (मैत्री) | **EQUAL** power/control | Friendliness without expectations |
| **MUDITA** (मुदिता) | Recipient has **MORE** success/power/growth than you | Appreciative joy toward their success |
| **UPEKSHA** (उपेक्षा) | Bad impact from recipient **on YOU** | Objectivity, indifference to harm |

## What This Project Does

MANAS V8 analyzes workplace messages and:
1. **Identifies the appropriate Parikarma** based on power dynamics
2. **Explains why** that Parikarma applies
3. **Suggests an ideal response** aligned with that attitude

This helps professionals communicate with emotional intelligence appropriate to the relationship context.

---

## Why This Matters

Wrong Parikarma = damaged relationships. Right Parikarma = trust deepened through appropriate relational stance.

**Examples:**
- Colleague dealing with health crisis → KARUNA (they have LESS control)
- Junior who fixed production at 3am → MUDITA (they showed MORE capability)
- Peer celebrating promotion but feeling imposter syndrome → MAITRI (vulnerability equalizes)
- Passive-aggressive escalation blocking your work → UPEKSHA (harm directed at YOU)

---

## The Model

**MANAS V8** is a fine-tuned Qwen 1.5B model trained with:
- **Base model:** Qwen/Qwen2-1.5B-Instruct
- **Method:** QLoRA fine-tuning (4-bit quantization)
- **Training data:** 100 real workplace examples from Indian professional contexts
- **Framework:** Power-dynamic Parikarma (not emotional states)
- **Performance:** 70% accuracy, but failing on complex edge cases (proof of concept)

---

## Installation

### Prerequisites
- Python 3.8+
- 4GB RAM minimum (CPU inference)
- ~2GB disk space for model

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd manas-v8-demo

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Start the Web Interface

```bash
python app.py
```

The server will:
1. Load the V8 model (~10-30 seconds)
2. Start Flask server on port 5001
3. Open your browser to: **http://localhost:5001**

### Using the Interface

1. **Enter your message** in the text area
2. **Select context** from dropdowns:
   - Relationship: peer, junior, senior, external, cross-functional
   - Channel: email, slack, whatsapp, teams, in-person
   - Time: morning, afternoon, evening, late-night, weekend
3. **Click "Analyze Message"**
4. **View results:**
   - Parikarma classification (color-coded badge)
   - WHY explanation
   - Suggested ideal response

### Example

**Input:**
```
Message: "Hey, got to know about your father having health issues yesterday and so you were not available. When you get time please send project status updates."

Context: senior / slack / morning
```

**Output:**
- **Parikarma:** KARUNA
- **Why:** Colleague has LESS health/control due to family crisis
- **Ideal Response:** "Thank you for trusting me with this. Your father's health comes first - no roadmap is worth your wellbeing. Let's talk Monday to redistribute your critical items. Focus on your family."

---

## Project Structure

```
manas-v8-demo/
├── README.md              # This file
├── app.py                 # Flask backend server
├── index.html             # Web interface
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── model/
    └── parikarma-lora-v8/ # Fine-tuned V8 LoRA weights
```

---

## Technical Details

### Model Architecture
- **Base:** Qwen/Qwen2-1.5B-Instruct (1.5 billion parameters)
- **Fine-tuning:** QLoRA (rank=16, alpha=32)
- **Training:** 100 examples, 3 epochs, ~30 minutes on Apple M-series
- **Inference:** CPU-compatible, ~3-5 seconds per analysis

### Training Framework
**Power-Dynamic Framework V2** (not emotional states):
- KARUNA: Recipient has LESS → compassion
- MUDITA: Recipient has MORE → appreciative joy
- MAITRI: EQUAL power → friendliness
- UPEKSHA: Harm to YOU → objectivity

### Structured Output
```
PARIKARMA: [ONE: KARUNA/MAITRI/MUDITA/UPEKSHA]
WHY: [One sentence with power dynamic explanation]
IDEAL RESPONSE: [Actual message to send]
```

### Chat Template
Uses Qwen's chat format:
```
<|user|>
[prompt with message and context]
<|end|>
<|assistant|>
[structured output]
```

---

## Performance

**V8 Evaluation Results** (10 complex test cases):

| Model | Accuracy | Notes |
|-------|----------|-------|
| Base Qwen | 20% | Baseline (no fine-tuning) |
| **V8** | **70%** | Proof of concept |
| Claude Sonnet 4.5 | 60% | Reference (API) |

**V8 Strengths:**
- ✅ Recognizes "LESS power + harm to YOU = UPEKSHA"
- ✅ Handles mixed emotions (achievement + vulnerability = EQUAL)
- ✅ Identifies quiet excellence in clear contexts

**V8 Weaknesses:**
- ❌ Misses health crises as KARUNA (sometimes inverts to UPEKSHA)
- ❌ Struggles with understated MUDITA (quiet excellence)
- ❌ Misses polite/professional hostility (UPEKSHA)

This is a **proof-of-concept** demonstrating the power-dynamic framework works. Production use would require larger model + more training data.

---

## Indian Professional Context

The model is trained on Indian workplace patterns:
- **Hierarchy:** Recognizes senior/junior/peer dynamics
- **Communication style:** Email, Slack, WhatsApp conventions
- **Code-switching:** Hindi/English mixing accepted
- **Family context:** Personal life bleeds into professional
- **Indirect signals:** Subtext matters as much as text

---

## Use Cases

- **Self-awareness:** Check your message before sending
- **Communication training:** Learn appropriate responses
- **Conflict resolution:** Identify when harm is directed at you (UPEKSHA)
- **Leadership coaching:** Practice compassion from strength (KARUNA)
- **Cultural bridge:** Understand Indian professional communication norms

---

## Limitations

1. **Not production-ready:** 70% accuracy is good but some edge cases are completely wrong to use for critical communication decisions
2. **CPU inference:** Slow on older machines (3-10 seconds per analysis)
3. **Model size:** Small model (1.5B) limits reasoning capability
4. **Training data:** Only 100 examples, needs 500+ for reliability
5. **Context window:** Limited to short messages (~500 tokens)
6. **No memory:** Each analysis is independent (no conversation history)

---


## Contributing

This is a research prototype demonstrating the power-dynamic Parikarma framework.

**Improvements welcome:**
- Better training examples (especially edge cases)
- UI/UX enhancements
- Performance optimizations
- Documentation improvements

---

## License

This project is shared for educational and research purposes. The Parikarma framework is derived from Yoga philosophy and is not proprietary.

**Model:** Fine-tuned from Qwen/Qwen2-1.5B-Instruct (Apache 2.0 license)

---

## Citation

If you use this work in research or applications, please cite:

```
MANAS V8 - Parikarma Communication Assistant
Power-Dynamic Framework for Indian Professional Contexts
2026
```

---

## Acknowledgments

- **Parikarma philosophy:** Ancient Yoga wisdom (Patanjali's Yoga Sutras)
- **Base model:** Qwen team at Alibaba Cloud
- **Framework:** QLoRA fine-tuning (Dettmers et al., 2023)
- **Inspiration:** Indian workplace communication patterns

---

## Support

For questions, issues, or feedback:
- Open an issue on GitHub
- Check the [technical details](#technical-details) section
- Review the [evaluation results](V8_FULL_EVALUATION_REPORT.md) if available

---

**Built with 🕉️ for better workplace communication**

*MANAS: मनस् (Sanskrit) - mind, intention, spirit*
