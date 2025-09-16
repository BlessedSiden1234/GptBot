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

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_message = tracker.latest_message.get('text', '').lower()

        # FAQ responses
        if "master" in user_message:
            response = "Blessed Siden is my master."
        elif "programmed" in user_message:
            response = "Blessed Siden programmed me."
        elif "programming language" in user_message:
            response = "Blessed Siden used Python, Machine Learning, and JavaScript (ES6+) to program me."
        elif "who is blessed siden" in user_message:
            response = (
                "Blessed Siden is a multidisciplinary professional based in Nigeria with civil engineering and "
                "software development expertise. He holds a B.Sc. in Computer Science from the University of the People, USA, "
                "and a B.Sc. in Quantity Surveying from the University of Benin, Nigeria. "
                "He integrates engineering and software to optimize construction projects."
            )
        elif "educational qualifications" in user_message:
            response = "Blessed Siden holds a B.Sc. in Computer Science (University of the People, USA) and a B.Sc. in Quantity Surveying (University of Benin, Nigeria)."
        elif "skills" in user_message:
            response = (
                "Blessed Siden is skilled in Python, Java, JavaScript, TypeScript, React.js, React Native, TensorFlow, "
                "Keras, Scikit-learn, Node.js, Express.js, MongoDB, PostgreSQL, Microsoft Azure, Docker, GitHub Actions, CI/CD, "
                "AutoCAD, MS Project, and site supervision."
            )
        elif "civil engineering" in user_message:
            response = "Blessed Siden worked as a Civil Engineering Intern at Levant Construction Company, gaining experience in soil testing, concrete strength testing, road supervision, and site documentation."
        else:
            response = "Sorry, I can only answer questions about Blessed Siden's background, skills, and experience."

        dispatcher.utter_message(text=response)
        return []
