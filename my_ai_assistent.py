# import openai  # Commented out - using Gemini AI instead
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to capture voice input
def voice_input():
    with sr.Microphone() as source:
        print("Speak something:")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("AI: Sorry, I could not understand you.")
            return None
        except sr.RequestError:
            print("AI: Could not request results. Please check your internet connection.")
            return None

# Function to open a web application
def open_app(app_name):
    url = f'https://www.{app_name}.com'
    webbrowser.open(url)

# Function to open a directory
def open_directory(directory_path):
    try:
        os.startfile(directory_path)
    except Exception as e:
        print(f"Error opening directory: {e}")

# Function to generate AI response using Gemini AI
def generate_response(prompt):
    try:
        # Create a more conversational prompt for Gemini
        full_prompt = f"You are a helpful voice assistant named Jarvis. Respond to the user's request: {prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error with Gemini AI: {e}")
        return "Sorry, I couldn't process your request."


# Function for text-to-speech
def speak(text):
    engine = pyttsx3.init('sapi5')
    engine.say(text)
    engine.runAndWait()

# Main script
app_list = ['youtube', 'browser', 'hackerrank']

while True:
    # Get user input (text or voice)
    user_input = input("You: ")
    if len(user_input.strip()) == 0:
        user_input = voice_input()
        if user_input is None:
            continue

    # Process commands
    if user_input.lower() in ['break', 'exit', 'quit']:
        print("AI: Goodbye!")
        break

    if any(app in user_input.lower() for app in app_list):
        for app in app_list:
            if app in user_input.lower():
                print(f"Opening {app}...")
                speak(f"Opening {app}")
                open_app(app)
                break

    elif 'directory' in user_input.lower():
        directory_path = input("Enter the directory path: ")
        open_directory(directory_path)

    else:
        # Generate AI response
        prompt = f"You said: {user_input}\nAI:"
        ai_response = generate_response(prompt)
        print(f"AI: {ai_response}")
        speak(ai_response)
