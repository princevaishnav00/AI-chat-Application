from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests


load_dotenv()


app = Flask(__name__)


GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"


SYSTEM_PROMPT = "You are a helpful, concise, and friendly AI assistant."


def format_messages(history):
    """Format chat history into llama instruction format."""
    prompt = f"<s>[INST] {SYSTEM_PROMPT} [/INST]</s>\n"
    for msg in history:
        if msg["role"] == "user":
            prompt += f"[INST] {msg['content']} [/INST]"
        else:
            prompt += f" {msg['content']}</s>\n"
    return prompt


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    history = data.get("history", [])

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "AI-Chat-App/1.0",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"].strip()
        return jsonify({"response": reply})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Please try again."}), 504

    except requests.exceptions.HTTPError:
        status = response.status_code
        print(f"[ERROR] Groq status {status}: {response.text}")
        if status == 401:
            return jsonify({"error": "Service temporarily unavailable."}), 401
        if status == 429:
            return jsonify({"error": "Service temporarily unavailable."}), 429
        return jsonify({"error": "Service error. Try again later."}), 500

    except Exception:
        return jsonify({"error": "An error occurred. Please try again."}), 500


@app.route('/health')
def health():
    return 'Server is up and running'


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False)
