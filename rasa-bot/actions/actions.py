

from transformers import GPT2LMHeadModel, GPT2Tokenizer
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import SlotSet
import torch  # Import torch for tensor operations

# Load the GPT-2 model and tokenizer locally
model_name = "gpt2"  # You can use other variants like "gpt2-medium" if you need a larger model
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Ensure the model knows what the pad token is
tokenizer.pad_token = tokenizer.eos_token  # Use eos_token as pad_token to avoid warnings


class ActionEscalateToAgent(Action):
    def name(self):
        return "action_escalate_to_agent"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text = "I'am escalating this issue to a human agent. Please hold on.")
        return []


    
class ActionAnswerAboutMe(Action):
    def name(self) -> str:
        return "action_answer_about_me"

    def run(self, dispatcher, tracker, domain):
        # Get the user's latest message
        user_message = tracker.latest_message.get('text')

        # Define responses for each question
        if "master" in user_message.lower():
            response = "Blessed Siden is my master."
        elif "programmed" in user_message.lower():
            response = "Blessed Siden programmed me."
        elif "programming language" in user_message.lower():
            response = "Blessed Siden used Python, Machine Learning, and JavaScript (ES6+) to program me."
        elif "blessed siden" in user_message.lower() and "who is" in user_message.lower():
            response = """
            Blessed Siden is a multidisciplinary professional based in Nigeria with a unique blend of civil engineering field experience and modern software development expertise. He has experience supervising road construction works, conducting soil and concrete strength testing, and managing site documentation.
            
            In addition to his civil engineering background, Blessed is proficient in various programming languages, including Python, JavaScript (ES6+), and TypeScript. He specializes in backend/frontend development and cloud technologies, with experience in tools like React.js, React Native, TensorFlow, and more.
            
            He integrates his engineering expertise with software development to optimize infrastructure projects. For example, he uses machine learning models and cloud solutions to improve the efficiency, safety, and management of construction sites.
            
            Blessed holds a Bachelor of Science (B.Sc.) in Computer Science from the University of the People (USA), and a Bachelor of Science (B.Sc.) in Quantity Surveying from the University of Benin (Nigeria). His goal is to leverage his technical skills to address real-world challenges at the intersection of technology and construction.
            """
        elif "educational qualifications" in user_message.lower():
            response = "Blessed Siden holds a B.Sc. in Computer Science from the University of the People, USA (2021-2025) and a B.Sc. in Quantity Surveying from the University of Benin, Nigeria (2017-2022)."
        elif "skills" in user_message.lower():
            response = """Blessed Siden is proficient in various technical skills, including:
                          - Programming Languages: Python, Java, JavaScript (ES6+), TypeScript
                          - Mobile App Development: React Native
                          - Machine Learning & AI: TensorFlow, Keras, Scikit-learn, Neural Networks, Data Preprocessing
                          - Frontend Development: React.js, Next.js, Tailwind CSS
                          - Backend Development: Node.js, Express.js, RESTful APIs, MongoDB, PostgreSQL
                          - Cloud & DevOps: Microsoft Azure, Docker, GitHub Actions, CI/CD
                          - Civil Engineering Tools: AutoCAD (basic), MS Project, Material Testing (Soil/Cube), Site Supervision"""
        elif "civil engineering" in user_message.lower():
            response = "Blessed Siden worked as a Civil Engineering Intern at Levant Construction Company, where he gained hands-on experience in soil testing, concrete strength testing, road construction supervision, and site documentation."
        elif "integrating technology with construction" in user_message.lower():
            response = "Blessed Siden integrates software development skills with civil engineering to optimize construction processes and improve safety using machine learning models and cloud technologies."
        elif "software and programming skills" in user_message.lower():
            response = "Blessed Siden uses React Native for mobile app development, and also has expertise in JavaScript, TypeScript, React.js, Next.js for frontend, and Python for backend services."
        elif "cloud technologies" in user_message.lower():
            response = "Blessed Siden is familiar with Microsoft Azure, Docker, GitHub Actions, and CI/CD for continuous deployment."
        elif "internship" in user_message.lower():
            response = "During his internship at Levant Construction Company, Blessed Siden assisted with soil and concrete testing, road construction supervision, and site inspections."
        elif "combine civil engineering and software development" in user_message.lower():
            response = "Blessed Siden combines his civil engineering background with software development to develop solutions that improve construction site efficiency and optimize project management using technology."
        elif "machine learning and ai" in user_message.lower():
            response = "Blessed Siden applies machine learning tools such as TensorFlow, Keras, and Scikit-learn for neural networks, data analysis, and predictive models."
        elif "safety and quality" in user_message.lower():
            response = "Blessed Siden ensures safety and quality in construction by conducting thorough inspections and maintaining compliance with engineering standards and health & safety regulations."
        elif "construction software" in user_message.lower():
            response = "Blessed Siden uses AutoCAD for basic design and MS Project for scheduling and managing construction projects."
        elif "project progress documentation" in user_message.lower():
            response = "Blessed Siden documents progress through detailed reports, tracking milestones and material usage to ensure timely delivery of projects."
        else:
            
            # 🚀 Hand off to GPT action for generic queries
            return [FollowupAction("action_query_gpt2")]

        # Send the response back to the user
        dispatcher.utter_message(text=response)

        return []
    
class ActionQueryGPT2(Action):
    def name(self) -> str:
        return "action_query_gpt2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Get the user's latest message
        user_message = tracker.latest_message.get('text')

        # Tokenize the input text
        input_ids = tokenizer.encode(user_message, return_tensors="pt")

        # Create an attention mask (use ones because GPT-2 doesn't require padding)
        attention_mask = torch.ones(input_ids.shape, device=input_ids.device)

        # Generate a response from the GPT-2 model with better control over sentence generation
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=150,                # Adjust to your preference
            num_return_sequences=1,        # Generate only 1 response
            pad_token_id=tokenizer.eos_token_id,  # Use eos_token as pad_token_id
            top_k=50,                      # Use top-k sampling
            top_p=0.95,                    # Use top-p (nucleus) sampling
            temperature=0.7,               # Controls randomness
            no_repeat_ngram_size=2,        # Prevent repetition of n-grams
            early_stopping=True,           # Stop generating when an end-of-sequence token is encountered
            num_beams=5,                  # Use beam search for better sentence structure
        )

        # Decode the generated response
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Log the generated response (for debugging purposes)
        print("Generated Response:", response)

        # Check if the response ends naturally (based on punctuation)
        if response[-1] not in ['.', '!', '?']:  # If not a sentence-ending punctuation
            response += '.'  # Add a period at the end if needed

        # Send the generated response back to the user
        dispatcher.utter_message(text=response)

        return []


