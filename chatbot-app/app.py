from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ✅ Rasa REST API URL (make sure your Rasa server is running with --enable-api)
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    sender_id = data.get("sender", "anonymous")

    print(f"Received message from {sender_id}: {user_message}")

    bot_text = get_bot_response(user_message, sender_id)

    print(f"Sending response to {sender_id}: {bot_text}")
    return jsonify({"response": bot_text})

def get_bot_response(message, sender_id):
    payload = {"sender": sender_id, "message": message}
    try:
        r = requests.post(RASA_API_URL, json=payload, timeout=8)
    except Exception as e:
        print("❌ ERROR contacting Rasa API:", e)
        return "Sorry — unable to reach the NLP server right now."

    if r.status_code != 200:
        print("❌ Rasa returned HTTP", r.status_code, r.text)
        return "Sorry — NLP server returned an error."

    replies = r.json()

    # ✅ Normal case: Rasa returned one or more messages
    if isinstance(replies, list) and len(replies) > 0:
        messages = []
        for item in replies:
            if item.get("text"):
                messages.append(item["text"])
            elif item.get("image"):
                messages.append(f"[image] {item['image']}")
            elif item.get("custom"):
                messages.append(str(item["custom"]))
        return "\n".join(messages)

    # ✅ If no reply from Rasa
    return "Sorry, I didn't understand that."

if __name__ == "__main__":
    app.run(debug=True)
