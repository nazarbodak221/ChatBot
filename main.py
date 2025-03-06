from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)
app.secret_key = "supersecretkey"

OPENAI_API_KEY = ""  # Paste your API key here

SERVICES = {
    "development": "We specialize in web development, AI, and automation.",
    "consulting": "We provide IT consulting, business process analysis.",
    "support": "24/7 technical support for your projects.",
    "marketing": "We help with advertising, SEO, and promotion strategies."
}

def get_llm_response(prompt):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", # you can change the model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error when querying OpenAI: {str(e)}"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    response = MessagingResponse()
    msg = response.message()

    current_state = session.get("state", "normal")

    if current_state == "waiting_for_service":
        if incoming_msg == "exit":
            session["state"] = "normal"
            msg.body("You have exited the service mode. How can I assist you?")
        elif incoming_msg in SERVICES:
            msg.body(SERVICES[incoming_msg] + "\nType 'exit' to leave or choose another service.")
        else:
            msg.body("Please choose a service:\n- Development\n- Consulting\n- Support\n- Marketing\n(or type 'exit' to leave)")

    elif current_state == "explore_mode":
        if incoming_msg == "exit":
            session["state"] = "normal"
            msg.body("You have exited Explore mode. How can I assist you?")
        else:
            llm_response = get_llm_response(incoming_msg)
            msg.body(llm_response + "\n(Type 'exit' to leave)")

    else:
        if incoming_msg == "service":
            session["state"] = "waiting_for_service"
            msg.body("You have entered service mode. Choose a service:\n- Development\n- Consulting\n- Support\n- Marketing\n(or type 'exit' to leave)")
        elif incoming_msg == "explore":
            session["state"] = "explore_mode"
            msg.body("You have entered Explore mode. Type any question, and I will try to answer!\n(or type 'exit' to leave)")
        elif incoming_msg == "Hello bot!":
            msg.body("Hi! How can I assist you today?")
        else:
            msg.body("Sorry, I didn't understand that. Please 'Hello bot!' to start")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=8001)
