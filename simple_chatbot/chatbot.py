import random
import string
import nltk
from nltk.stem import PorterStemmer

# Initialize NLTK
nltk.download("punkt")
stemmer = PorterStemmer()

# Load data from data.py
from data import data

# Tokenize and stem the user input
def preprocess(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return [stemmer.stem(token) for token in tokens]

# Generate a response based on user input
def get_response(user_input):
    user_input = preprocess(user_input)
    
    for intent, patterns in data.items():
        for pattern in patterns:
            if all(word in user_input for word in preprocess(pattern)):
                return random.choice(data[intent])
    
    return "I'm sorry, I don't understand."

# Chat loop
def chat():
    print("Chatbot: Hello! I'm your friendly chatbot. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            break
        
        response = get_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    chat()