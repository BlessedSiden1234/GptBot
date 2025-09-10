import os
import requests
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction


class ActionEscalateToAgent(Action):
    def name(self):
        return "action_escalate_to_agent"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I'm escalating this issue to a human agent. Please hold on.")
        return []


class ActionAnswerAboutMe(Action):
    def name(self) -> str:
        return "action_answer_about_me"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')

        if "master" in user_message.lower():
            response = "Blessed Siden is my master."
        elif "programmed" in user_message.lower():
            response = "Blessed Siden programmed me."
        elif "programming language" in user_message.lower():
            response = "Blessed Siden used Python, Machine Learning, and JavaScript (ES6+) to program me."
        elif "blessed siden" in user_message.lower() and "who is" in user_message.lower():
            response = "Blessed Siden is a multidisciplinary professional based in Nigeria ..."
        elif "educational qualifications" in user_message.lower():
            response = "Blessed Siden holds a B.Sc. in Computer Science (University of the People, USA) and a B.Sc. in Quantity Surveying (University of Benin, Nigeria)."
        elif "skills" in user_message.lower():
            response = "Blessed Siden is proficient in Python, JavaScript, TypeScript, React Native, TensorFlow, Docker, and more."
        else:
            # 🚀 Hand off to GPT action for generic queries
            return [FollowupAction("action_query_gpt2")]

        dispatcher.utter_message(text=response)
        return []


class ActionQueryGPT2(Action):
    def name(self) -> str:
        return "action_query_gpt2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get('text')

        api_url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

        payload = {
            "inputs": user_message,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.95,
                "do_sample": True
            }
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            result = response.json()

            if isinstance(result, list) and "generated_text" in result[0]:
                generated = result[0]["generated_text"]
            else:
                generated = "Hmm... I couldn’t generate a good answer right now."
        except Exception as e:
            print("Error calling Hugging Face API:", e)
            generated = "Sorry, my brain is taking a break 🛠️. Please try again later."

        dispatcher.utter_message(text=generated)
        return []
