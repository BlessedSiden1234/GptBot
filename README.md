# GPT Bot - Rasa + Flask Integration

This project integrates a **GPT-2 model** with **Rasa** and **Flask** to create an intelligent chatbot. The bot can answer general questions, respond to queries about **Blessed Siden**, and perform custom actions such as escalation to a human agent.

## Features

- **Rasa Framework**: Manages natural language understanding (NLU) and dialog management.
- **Flask**: Serves as the backend to handle API requests and process responses.
- **GPT-2 Model**: Used for generating responses to general questions.
- **Custom Actions**: Action handlers for specific use cases, including responses about Blessed Siden.

## Prerequisites

- Python 3.8+
- Rasa 3.x
- Flask 2.x
- PyTorch (for GPT-2)
- transformers library

## Installation

Follow these steps to get your development environment set up.

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/chatbot.git
    cd chatbot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Rasa:
    - Initialize Rasa:
      ```bash
      rasa init
      ```

    - Train your Rasa model:
      ```bash
      rasa train
      ```

5. Install GPT-2 dependencies (from `transformers` library):
    ```bash
    pip install transformers torch
    ```

6. Run the Flask app:
    ```bash
    python app.py
    ```

7. Start Rasa:
    ```bash
    rasa run --enable-api
    ```

## Running the Bot

Once the Flask app and Rasa are running, you can interact with the bot through the web interface. The chatbot will respond to general queries using GPT-2 and provide specific answers about Blessed Siden.

- Visit `http://localhost:5005` to interact with the bot.

## Files Structure

