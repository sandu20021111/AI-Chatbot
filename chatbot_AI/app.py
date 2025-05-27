import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

API_KEY = "Your_API_Key"

def call_chat_api(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",  # Required by OpenRouter
        "X-Title": "My Chatbot App"              # Required by OpenRouter
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # You can use other models too
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_reply = call_chat_api(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)