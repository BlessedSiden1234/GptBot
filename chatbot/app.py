
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# URL for Rasa's REST API (make sure Rasa is running)
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get the message from the request (it's now JSON)
    user_message = request.json.get('message')
    print(f"Received message: {user_message}")  # Debugging line to log the user's message
    
    # Call the function to get the bot's response
    response = get_bot_response(user_message)

    print(f"Sending response: {response}")  # Debugging line to log the response sent to the frontend
    
    return jsonify({"response": response})

def get_bot_response(message):
    # Send the user message to Rasa's REST API and get the response
    payload = {
        "sender": "user",
        "message": message
    }
    
    response = requests.post(RASA_API_URL, json=payload)
    bot_response = response.json()

    # Check if the response is valid and get the bot's generated response
    if response.status_code == 200:
        print(f"Rasa response: {bot_response}")  # Debugging line to log the Rasa response
        
        if bot_response and isinstance(bot_response, list):
            # Extract the generated text from the last message in the response
            bot_text = bot_response[-1].get('text', 'Sorry, I didn\'t understand that.') 

            # Prevent the bot from replying with the same message again
            if bot_text.strip().lower() == message.strip().lower():
                return "Sorry, I didn't understand that. Please rephrase your question."
            
            return bot_text 
    else:
        print(f"Error: {response.status_code}")  
     
    return 'Sorry, I didn\'t understand that.'   
 
if __name__ == "__main__": 
    app.run(debug=True)


