import speech_recognition as sr
from gtts import gTTS
from transformers import Conversation, pipeline
import os
import time
import datetime
import numpy as np
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button

# Building the AI
class ChatBot():
    def __init__(self, name):
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("Listening...")
            audio = recognizer.listen(mic)
            self.text = "ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        print("Dev --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start res.mp3')  # if you are using mac->afplay or else for windows->start
        time.sleep(int(50 * duration))
        os.remove("res.mp3")

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    def process_conversation(self):
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": self.text}
        ]
        chat = nlp(conversation)
        user_response = chat[0]['content'].strip()
        assistant_response = chat[1]['content'].strip()

        return user_response, assistant_response

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')

# GUI for Chat Window
class ChatWindow(tk.Tk):
    def __init__(self, ai):
        super().__init__()

        self.ai = ai

        self.title("Chat Window")
        self.geometry("400x400")

        self.text_widget = Text(self, wrap="word", state="disabled")
        self.text_widget.pack(expand=True, fill="both")

        self.scrollbar = Scrollbar(self, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.input_entry = Entry(self)
        self.input_entry.pack(expand=True, fill="x")

        self.send_button = Button(self, text="Send", command=self.send_message)
        self.send_button.pack()

        self.listen_button = Button(self, text="Listen", command=self.listen_and_send)
        self.listen_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.listen_and_send()

    def send_message(self):
        user_input = self.input_entry.get()
        self.display_message(f"You --> {user_input}")

        # Process user input
        ai.text = user_input
        user_response, assistant_response = ai.process_conversation()
        self.display_message(f"Dev --> {assistant_response}")

        # Speak the response
        ai.text_to_speech(assistant_response)

        self.input_entry.delete(0, "end")

    def listen_and_send(self):
        self.ai.speech_to_text()
        self.display_message(f"You --> {self.ai.text}")

        # Process user input
        user_response, assistant_response = self.ai.process_conversation()
        self.display_message(f"Dev --> {assistant_response}")

        # Speak the response
        self.ai.text_to_speech(assistant_response)

    def display_message(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", message + "\n")
        self.text_widget.config(state="disabled")

    def on_closing(self):
        self.destroy()

# Running the AI with the Chat Window
if __name__ == "__main__":
    ai = ChatBot(name="dev")
    nlp = pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    chat_window = ChatWindow(ai)
    chat_window.mainloop()

    print("----- Closing down Dev -----")
