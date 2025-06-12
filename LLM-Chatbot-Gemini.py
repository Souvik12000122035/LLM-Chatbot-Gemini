# LLM-Chatbot-Gemini
!pip install -q google-generativeai
import google.generativeai as genai
import os
from getpass import getpass

# Enter your API key
api_key = getpass("Enter your Google API key: ")
os.environ["GOOGLE_API_KEY"] = api_key

# Configure and create chat object
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

# Web Chat UI with ipywidgets
from IPython.display import display
import ipywidgets as widgets

# Create input and output widgets
input_box = widgets.Text(
    description="You:",
    placeholder="Enter your message here...",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='100%')
)
send_button = widgets.Button(description="Send", button_style='success')
output_area = widgets.Output()

# Function to handle chat
def on_button_click(b):
    with output_area:
        prompt = input_box.value.strip()
        if not prompt:
            print("⚠️ Please enter a message.")
            return
        print(f"You: {prompt}")
        if prompt.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! (You can close this cell.)")
            input_box.disabled = True
            send_button.disabled = True
            return
        response = chat.send_message(prompt)
        print(f"Chatbot: {response.text}\n")
        input_box.value = ""  # Clear input

# Attach click event
send_button.on_click(on_button_click)

# Show chatbot UI
display(widgets.VBox([input_box, send_button, output_area]))

# Save Chat History
chat_log = []

def on_button_click(b):
    with output_area:
        prompt = input_box.value.strip()
        if not prompt:
            print("⚠️ Please enter a message.")
            return
        print(f"You: {prompt}")
        chat_log.append(f"You: {prompt}")
        if prompt.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! (You can close this cell.)")
            chat_log.append("Chatbot: Goodbye!")
            input_box.disabled = True
            send_button.disabled = True
            return
        response = chat.send_message(prompt)
        print(f"Chatbot: {response.text}\n")
        chat_log.append(f"Chatbot: {response.text}")
        input_box.value = ""

# Save as text file
def save_chat_to_file():
    with open("chat_log.txt", "w") as file:
        file.write("\n".join(chat_log))
    print("✅ Chat saved to chat_log.txt")

# Run this manually after chatting:
# save_chat_to_file()

# Add a Clear/Reset Button
clear_button = widgets.Button(description="Clear Chat", button_style='warning')

def on_clear_click(b):
    output_area.clear_output()
    chat.history.clear()
    input_box.disabled = False
    send_button.disabled = False
    input_box.value = ""

clear_button.on_click(on_clear_click)
display(widgets.HBox([send_button, clear_button]))

# Add Timestamp to Each Message
from datetime import datetime

chat_log = []

def on_button_click(b):
    with output_area:
        prompt = input_box.value.strip()
        if not prompt:
            print("⚠️ Please enter a message.")
            return

        timestamp = datetime.now().strftime("%H:%M:%S") # Define timestamp inside the function

        print(f"[{timestamp}] You: {prompt}") # Add timestamp to the printed output
        chat_log.append(f"[{timestamp}] You: {prompt}")

        if prompt.lower() in ["exit", "quit"]:
            print(f"[{timestamp}] Chatbot: Goodbye! (You can close this cell.)") # Add timestamp
            chat_log.append(f"[{timestamp}] Chatbot: Goodbye!") # Add timestamp
            input_box.disabled = True
            send_button.disabled = True
            return

        response = chat.send_message(prompt)
        print(f"[{timestamp}] Chatbot: {response.text}\n") # Add timestamp
        chat_log.append(f"[{timestamp}] Chatbot: {response.text}") # Add timestamp

        input_box.value = ""

# Save as text file
def save_chat_to_file():
    with open("chat_log.txt", "w") as file:
        file.write("\n".join(chat_log))
    print("✅ Chat saved to chat_log.txt")

# Add Download Button for Chat Log
from google.colab import files

download_button = widgets.Button(description="Download Chat Log", button_style='info')

def on_download_click(b):
    save_chat_to_file()
    files.download("chat_log.txt")

download_button.on_click(on_download_click)
display(widgets.HBox([send_button, clear_button, download_button]))
