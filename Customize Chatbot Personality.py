# Customize Chatbot Personality

genai.configure(api_key=api_key)

personality_history = [
    {"role": "user", "parts": ["Hello!"]},
    {"role": "model", "parts": ["Greetings, human. I am an AI with a dry sense of humor."]},
    {"role": "user", "parts": ["Tell me a joke."]},
    {"role": "model", "parts": ["Why don't scientists trust atoms? Because they make up everything! *cricket sounds*"]},
]

model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=personality_history)

# Create input and output widgets
input_box = widgets.Text(
    description="You:",
    placeholder="Enter your message here...",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='100%')
)
send_button = widgets.Button(description="Send", button_style='success')
output_area = widgets.Output()

chat_log = []

# Function to handle chat
def on_button_click(b):
    with output_area:
        prompt = input_box.value.strip()
        if not prompt:
            print("⚠️ Please enter a message.")
            return

        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"[{timestamp}] You: {prompt}")
        chat_log.append(f"[{timestamp}] You: {prompt}")

        if prompt.lower() in ["exit", "quit"]:
            print(f"[{timestamp}] Chatbot: Goodbye! (You can close this cell.)")
            chat_log.append(f"[{timestamp}] Chatbot: Goodbye!")
            input_box.disabled = True
            send_button.disabled = True
            return

        response = chat.send_message(prompt)
        print(f"[{timestamp}] Chatbot: {response.text}\n")
        chat_log.append(f"[{timestamp}] Chatbot: {response.text}")

        input_box.value = ""

# Save as text file
def save_chat_to_file():
    with open("chat_log.txt", "w") as file:
        file.write("\n".join(chat_log))
    print("✅ Chat saved to chat_log.txt")


# Attach click event
send_button.on_click(on_button_click)
clear_button = widgets.Button(description="Clear Chat", button_style='warning')

def on_clear_click(b):
    output_area.clear_output()
    # When clearing, restart the chat with the original personality history
    chat.history.clear()
    for exchange in personality_history:
        chat.history.append(exchange)
    chat_log.clear() # Also clear the local chat log
    input_box.disabled = False
    send_button.disabled = False
    input_box.value = ""

clear_button.on_click(on_clear_click)

download_button = widgets.Button(description="Download Chat Log", button_style='info')

def on_download_click(b):
    save_chat_to_file()
    files.download("chat_log.txt")

download_button.on_click(on_download_click)

# Show chatbot UI
display(widgets.VBox([input_box, widgets.HBox([send_button, clear_button, download_button]), output_area]))
