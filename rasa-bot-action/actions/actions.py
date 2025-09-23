import re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionAnswerAboutMe(Action):
    def name(self) -> str:
        return "action_answer_about_me"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_message = tracker.latest_message.get('text', '').lower()
        # Strip punctuation to improve matching
        user_message = re.sub(r'[^\w\s]', '', user_message)

        # FAQ responses
        if "master" in user_message:
            response = "Blessed Siden is my master."
        elif any(word in user_message for word in ["created", "made", "built", "developed", "author", "wrote"]):
            response = "I was created and developed by Blessed Siden."
        elif any(word in user_message for word in ["programmed", "programmer"]):
            response = "Blessed Siden programmed me."
        elif "programming language" in user_message:
            response = "Blessed Siden used Python, Machine Learning, and JavaScript (ES6+) to program me."
        elif ("who is blessed siden" in user_message 
              or "who is blessed" in user_message 
              or "tell me about blessed siden" in user_message
              or user_message.strip() in ["blessed", "siden", "blessed siden"]):
            response = (
                "Blessed Siden is a multidisciplinary professional based in Nigeria with civil engineering and "
                "software development expertise. He holds a B.Sc. in Computer Science from the University of the People, USA, "
                "and a B.Sc. in Quantity Surveying from the University of Benin, Nigeria. "
                "He is also the founder and CEO of SubnetExpress.com, a platform for purchasing and selling data bundles, "
                "airtime, cable subscriptions, electricity tokens, educational services, and more. "
                "Blessed Siden combines cutting-edge technology with engineering principles to deliver innovative solutions, "
                "streamline complex projects, and create practical tools that impact businesses and communities positively."
            )
        elif "educational qualifications" in user_message:
            response = "Blessed Siden holds a B.Sc. in Computer Science (University of the People, USA) and a B.Sc. in Quantity Surveying (University of Benin, Nigeria)."
        elif "skills" in user_message:
            response = (
                "Blessed Siden is skilled in Python, Java, JavaScript, TypeScript, React.js, React Native, TensorFlow, "
                "Keras, Scikit-learn, Node.js, Express.js, MongoDB, PostgreSQL, Microsoft Azure, Docker, GitHub Actions, CI/CD, "
                "Artificial Intelligence (AI), and Machine Learning (ML), AutoCAD, MS Project, and site supervision."
            )
        elif "civil engineering" in user_message:
            response = "Blessed Siden worked as a Civil Engineering Intern at Levant Construction Company, gaining experience in soil testing, concrete strength testing, road supervision, and site documentation."
        elif "background" in user_message:
            response = (
                "Blessed Siden has a dual background in civil engineering and computer science. "
                "He combines technical knowledge in construction with advanced programming and software development skills."
            )
        elif "computer science" in user_message:
            response = "Blessed Siden studied Computer Science at the University of the People, USA."
        elif "quantity surveying" in user_message:
            response = "Blessed Siden studied Quantity Surveying at the University of Benin, Nigeria."
        elif "motivates" in user_message:
            response = (
                "Blessed Siden is motivated by the desire to integrate technology with traditional fields like construction, "
                "making projects more efficient, safe, and sustainable."
            )
        elif "mobile apps" in user_message:
            response = (
                "Blessed Siden has developed mobile apps using React Native, Node.js, and cloud backends. "
                "His focus is on practical, user-friendly solutions."
            )
        elif "full-stack" in user_message:
            response = "Yes, Blessed Siden is experienced in full-stack development using Node.js, Express.js, React.js, and databases like MongoDB and PostgreSQL."
        elif "frameworks" in user_message or "machine learning" in user_message:
            response = "Blessed Siden uses TensorFlow, Keras, and Scikit-learn for building and training machine learning models."
        
        # --- Open-source projects ---
        elif any(phrase in user_message for phrase in ["open-source", "open source", "opensource", "github", "git", "repo", "repository", "contribute", "contributions"]):
            response = (
                "Yes, Blessed Siden has contributed to open-source projects, particularly in Python and React-based tools. "
                "He actively shares solutions on GitHub that support both developers and engineering teams."
            )

        # --- Leadership roles ---
        elif any(phrase in user_message for phrase in ["leadership", "leader", "roles", "positions", "ceo", "founder", "startup", "subnetexpress", "management"]):
            response = (
                "Blessed Siden has taken leadership roles in both engineering and software projects. "
                "He is the founder and CEO of SubnetExpress.com, a platform for data, airtime, cable subscriptions, "
                "electricity tokens, educational services, and more. "
                "Through this venture, he demonstrates strong leadership and innovation by bridging civil engineering with technology."
            )

        elif "future" in user_message or "career aspirations" in user_message:
            response = (
                "Blessed Siden aims to become a leader in the integration of civil engineering and AI-driven solutions, "
                "helping to solve infrastructure and development challenges in Africa and beyond."
            )
        elif "teamwork" in user_message or "collaboration" in user_message:
            response = (
                "Blessed Siden values teamwork and collaboration, and he often works in agile teams where he contributes "
                "as both a developer and an engineering consultant."
            )
        elif "agile" in user_message:
            response = "Yes, Blessed Siden has experience working with agile methodologies, especially Scrum and Kanban."
        elif "impact" in user_message:
            response = (
                "Blessed Siden wants to make a lasting impact by advancing safe, technology-driven solutions in "
                "engineering and software development, particularly across Africa."
            )
        elif "safety" in user_message or "innovation" in user_message:
            response = (
                "Blessed Siden integrates safety with innovation by following engineering standards while applying "
                "modern digital tools to improve efficiency and reduce risks."
            )
        elif "continuous learning" in user_message or "learning" in user_message:
            response = (
                "Blessed Siden ensures continuous learning by taking online certifications, contributing to open-source projects, "
                "and staying up-to-date with emerging trends in AI, cloud, and engineering."
            )
        elif "cloud" in user_message:
            response = (
                "Blessed Siden uses cloud technologies like Microsoft Azure and Docker to deploy, manage, and scale applications "
                "efficiently while ensuring security and reliability."
            )
        elif "biggest challenge" in user_message or "internship" in user_message:
            response = (
                "During his internship at Levant Construction Company, his biggest challenge was coordinating between different site teams "
                "to ensure quality documentation, but it helped him develop strong leadership and problem-solving skills."
            )
        else:
            response = "Sorry, I can only answer questions about Blessed Siden's background, skills, and experience."

        dispatcher.utter_message(text=response)
        return []
