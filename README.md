# WhatsApp Twilio Bot

This project is a WhatsApp chatbot using Twilio's API and OpenAI for AI-generated responses. It is built with Flask and handles user interactions for services and exploratory questions.

## Features
- Responds to user messages via WhatsApp
- Provides information about available services
- Integrates with OpenAI to generate responses in "Explore" mode

## Requirements
- Python 3.13
- Twilio account with a verified WhatsApp number
- OpenAI API key
- Flask

## Setup Instructions
### 0. Install venv
```bash
pip -m venv venv
```

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Twilio
- Sign up at [Twilio](https://www.twilio.com/)
- Get a Twilio WhatsApp-enabled number
- Verify your number in Twilio Sandbox
- Note your **Account SID** and **Auth Token**

### 3. Configure OpenAI
- Sign up at [OpenAI](https://openai.com/)
- Get an API key from the OpenAI dashboard

### 4. Run the Flask App

```bash
python main.py
```

### 5. Expose the Local Server
Use **ngrok** to expose your local server:
```bash
ngrok http 8001
```
Copy the generated `https://xxxx.ngrok.io` URL.

### 6. Configure Twilio Webhook
- Go to Twilio Console → **Messaging Services**
- Set the Webhook URL to `https://xxxx.ngrok.io/webhook` from previoud step

### 7. Test the Bot
Send messages to your WhatsApp Twilio number and see the responses.

## Usage Commands
- `hello bot!` - Start the bot
- `service` - Enter service mode
- `explore` - Enter AI response mode
- `exit` - Exit any mode

## License
MIT License
