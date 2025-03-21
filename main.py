from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import openai
import logging

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Used to sign the session cookie (should be kept secret)

# Set up logging
logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# OpenAI API key and services offered
OPENAI_API_KEY = ""  # Paste your OpenAI API key here
SERVICES = {
    "development": "We specialize in web development, AI, and automation.",
    "consulting": "We provide IT consulting, business process analysis.",
    "support": "24/7 technical support for your projects.",
    "marketing": "We help with advertising, SEO, and promotion strategies."
}

# Log the startup of the bot
logging.info("Bot is starting...")

# Function to get response from GPT-4
def get_llm_response(prompt):
    logging.info(f"Requesting GPT-4 with prompt: {prompt}")
    openai.api_key = OPENAI_API_KEY
    try:
        # Send the prompt to OpenAI's GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can change the model if needed
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        response_text = response["choices"][0]["message"]["content"].strip()
        logging.info(f"GPT-4 response: {response_text}")
        return response_text
    except Exception as e:
        # Log any error while querying OpenAI
        logging.error(f"Error when querying OpenAI: {str(e)}")
        return f"Error when querying OpenAI: {str(e)}"

# Main webhook that listens for incoming messages from WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()  # Get the message from WhatsApp
    logging.info(f"Received message: {incoming_msg}")  # Log the incoming message
    response = MessagingResponse()  # Create the response object
    msg = response.message()  # Get the message object for composing a reply

    current_state = session.get("state", "normal")  # Get the current state of the session
    logging.info(f"Current session state: {current_state}")  # Log the current state

    # Handle different states
    if current_state == "waiting_for_service":
        if incoming_msg == "exit":
            session["state"] = "normal"
            msg.body("You have exited the service mode. How can I assist you?")
            logging.info("User exited service mode.")
        elif incoming_msg in SERVICES:
            msg.body(SERVICES[incoming_msg] + "\nType 'exit' to leave or choose another service.")
            logging.info(f"User selected service: {incoming_msg}")
        else:
            msg.body("Please choose a service:\n- Development\n- Consulting\n- Support\n- Marketing\n(or type 'exit' to leave)")
            logging.info("User was prompted to choose a valid service.")

    elif current_state == "explore_mode":
        if incoming_msg == "exit":
            session["state"] = "normal"
            msg.body("You have exited Explore mode. How can I assist you?")
            logging.info("User exited explore mode.")
        else:
            llm_response = get_llm_response(incoming_msg)  # Get response from GPT-4
            msg.body(llm_response + "\n(Type 'exit' to leave)")
            logging.info(f"Exploring mode response: {llm_response}")

    else:
        # Default handling when in 'normal' state
        if incoming_msg == "service":
            session["state"] = "waiting_for_service"
            msg.body("You have entered service mode. Choose a service:\n- Development\n- Consulting\n- Support\n- Marketing\n(or type 'exit' to leave)")
            logging.info("User entered service mode.")
        elif incoming_msg == "explore":
            session["state"] = "explore_mode"
            msg.body("You have entered Explore mode. Type any question, and I will try to answer!\n(or type 'exit' to leave)")
            logging.info("User entered explore mode.")
        elif incoming_msg == "Hello bot!":
            msg.body("Hi! How can I assist you today?")
            logging.info("User said 'Hello bot!'")
        elif incoming_msg == "reset":
            session.clear()  # Clear the session
            msg.body("Session has been reset. How can I assist you?")
            logging.info("Session reset by user.")
        elif incoming_msg == "help":
            help_text = (
                "Commands available:\n"
                "service - Enter service mode\n"
                "explore - Enter explore mode\n"
                "reset - Reset session\n"
                "help - Show this help message\n"
            )
            msg.body(help_text)
            logging.info("User requested help.")
        else:
            msg.body("Sorry, I didn't understand that. Please type 'Hello bot!' to start")
            logging.warning(f"User sent an unrecognized message: {incoming_msg}")

    logging.info(f"Bot response: {msg.body}")  # Log the bot's response
    return str(response)

# Run the Flask application
if __name__ == "__main__":
    logging.info("Bot is running on port 8001")  # Log that the bot is starting to listen for requests
    app.run(debug=True, port=8001)
