#!/usr/bin/env python3
"""
Advanced Voice Assistant with Gemini AI Integration
Features: Voice recognition, text-to-speech, web browsing, system control, AI chat
"""

import sys
import os
import datetime
import re
import random
import webbrowser
import time
import subprocess
import json
from pathlib import Path

# Core libraries
import speech_recognition as sr
import pyttsx3
import psutil
from dotenv import load_dotenv

# AI and web libraries
import google.generativeai as genai
import wikipedia
import pywhatkit
import pyautogui
import requests
from datetime import timedelta

# Improved importing and environment setup
import logging

# Load environment variables
load_dotenv()

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with all necessary components"""
        self.setup_ai()
        self.setup_voice()
        self.setup_speech_recognition()
        self.load_config()
        self.command_history = []  # Store past commands for context-based processing
        self.start_time = datetime.datetime.now()  # Track assistant runtime
        
    def setup_ai(self):
        """Configure Gemini AI"""
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✓ Gemini AI configured successfully")
        except Exception as e:
            print(f"✗ Error configuring Gemini AI: {e}")
            self.model = None
    
    def setup_voice(self):
        """Initialize text-to-speech engine"""
        try:
            self.engine = pyttsx3.init('sapi5')
            voices = self.engine.getProperty('voices')
            
            # Set voice properties
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)  # Female voice
            
            self.engine.setProperty('rate', int(os.getenv('VOICE_RATE', 200)))
            self.engine.setProperty('volume', float(os.getenv('VOICE_VOLUME', 0.9)))
            print("✓ Text-to-speech engine initialized")
        except Exception as e:
            print(f"✗ Error initializing voice engine: {e}")
            self.engine = None
    
    def setup_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✓ Speech recognition initialized")
        except Exception as e:
            print(f"✗ Error initializing speech recognition: {e}")
            self.recognizer = None
    
    def load_config(self):
        """Load configuration from environment variables"""
        self.assistant_name = os.getenv('ASSISTANT_NAME', 'Jarvis')
        self.music_dir = os.getenv('MUSIC_DIR', 'C:\\Music')
        self.downloads_dir = os.getenv('DOWNLOADS_DIR', 'C:\\Users\\nanda\\Downloads')
        self.documents_dir = os.getenv('DOCUMENTS_DIR', 'C:\\Users\\nanda\\Documents')
        
        # Application mappings
        self.app_mappings = {
            'youtube': 'https://www.youtube.com',
            'google': 'https://www.google.com',
            'gmail': 'https://mail.google.com',
            'github': 'https://github.com',
            'chatgpt': 'https://chat.openai.com',
            'gemini': 'https://gemini.google.com',
            'spotify': 'https://open.spotify.com',
            'netflix': 'https://www.netflix.com',
            'amazon': 'https://www.amazon.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://twitter.com',
            'instagram': 'https://www.instagram.com'
        }
    
    def speak(self, text):
        """Convert text to speech"""
        if self.engine:
            try:
                print(f"🎵 {self.assistant_name}: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"✗ Error in text-to-speech: {e}")
        else:
            print(f"{self.assistant_name}: {text}")
    
    def listen(self, timeout=5):
        """Listen for voice input"""
        if not self.recognizer:
            return None
            
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
            print("🔍 Recognizing...")
            command = self.recognizer.recognize_google(audio, language='en-US')
            print(f"👤 User said: {command}")
            return command.lower()
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            return None
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return None
    
    def get_ai_response(self, prompt, context=None):
        """Get response from Gemini AI"""
        if not self.model:
            return "AI service is not available."

        if context:
            prompt = context + " " + prompt
        try:
            full_prompt = f"You are {self.assistant_name}, a helpful voice assistant. Use full context and respond: {prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"✗ Error with Gemini AI: {e}")
            return "I'm having trouble processing your request right now."

    
    def log_command(self, command):
        logging.info(f"Processing command: {command}")

    def handle_repetitive_commands(self, command):
        if self.command_history.count(command) > 2:
            self.speak("You've requested this several times. Would you like to set this as a routine?")
    
    def wish_user(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        
        if 0 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
            
        welcome_message = f"{greeting} I'm {self.assistant_name}, your voice assistant. How can I help you today?"
        self.speak(welcome_message)
    
    def get_current_time(self):
        """Get and announce current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        message = f"The current time is {current_time}"
        self.speak(message)
        return current_time
    
    def get_current_date(self):
        """Get and announce current date"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        message = f"Today is {current_date}"
        self.speak(message)
        return current_date
    
    def open_website(self, site_name):
        """Open a website based on site name"""
        if site_name in self.app_mappings:
            url = self.app_mappings[site_name]
            webbrowser.open(url)
            self.speak(f"Opening {site_name}")
        else:
            # Try to open as a generic website
            url = f"https://www.{site_name}.com"
            webbrowser.open(url)
            self.speak(f"Opening {site_name}")
    
    def search_web(self, query):
        """Search the web using pywhatkit"""
        try:
            pywhatkit.search(query)
            self.speak(f"Searching for {query}")
        except Exception as e:
            print(f"Error searching web: {e}")
            self.speak("I couldn't perform the search right now")
    
    def search_youtube(self, query):
        """Search YouTube"""
        try:
            pywhatkit.playonyt(query)
            self.speak(f"Playing {query} on YouTube")
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            self.speak("I couldn't search YouTube right now")
    
    def get_wikipedia_info(self, query):
        """Get information from Wikipedia"""
        try:
            self.speak("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=3)
            self.speak("According to Wikipedia:")
            self.speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"Multiple results found for {query}. Please be more specific.")
        except wikipedia.exceptions.PageError:
            self.speak(f"No Wikipedia page found for {query}")
        except Exception as e:
            print(f"Error with Wikipedia: {e}")
            self.speak("I couldn't get Wikipedia information right now")
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            screenshot_path = os.path.join(self.downloads_dir, f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            self.speak("Screenshot taken and saved to downloads")
            return screenshot_path
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            self.speak("I couldn't take a screenshot right now")
            return None
    
    def get_system_info(self):
        """Get system information"""
        try:
            # Battery info
            battery = psutil.sensors_battery()
            battery_info = f"Battery is at {battery.percent}% "
            if battery.power_plugged:
                battery_info += "and charging"
            else:
                battery_info += "and not charging"
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_info = f"Memory usage is at {memory.percent}%"
            
            # CPU info
            cpu_info = f"CPU usage is at {psutil.cpu_percent()}%"
            
            full_info = f"{battery_info}. {memory_info}. {cpu_info}"
            self.speak(full_info)
            return full_info
        except Exception as e:
            print(f"Error getting system info: {e}")
            self.speak("I couldn't get system information right now")
            return None
    
    def shutdown_system(self, delay=10):
        """Shutdown the system after a delay"""
        try:
            self.speak(f"Shutting down the system in {delay} seconds")
            time.sleep(delay)
            os.system("shutdown /s /t 1")
        except Exception as e:
            print(f"Error shutting down: {e}")
            self.speak("I couldn't shut down the system")
    
    def restart_system(self, delay=10):
        """Restart the system after a delay"""
        try:
            self.speak(f"Restarting the system in {delay} seconds")
            time.sleep(delay)
            os.system("shutdown /r /t 1")
        except Exception as e:
            print(f"Error restarting: {e}")
            self.speak("I couldn't restart the system")
    
    def extract_numbers(self, text):
        """Extract numbers from text"""
        return re.findall(r'\d+', text)
    
    def track_session_duration(self):
        """Track session duration and suggest breaks"""
        session_duration = datetime.datetime.now() - self.start_time
        if session_duration > timedelta(hours=2):
            self.speak("You've been interacting for over 2 hours. Consider taking a break.")

    
    def process_command(self, command):
        """Process and manage voice commands"""
        if not command:
            return True

        command = command.lower().strip()
        self.command_history.append(command)
        self.log_command(command)
        self.handle_repetitive_commands(command)
        self.track_session_duration()

        # Check for repetitive commands to suggest alternatives
        if self.command_history.count(command) > 2:
            self.speak("You've requested this several times. Would you like to set this as a routine?")

        # Calculate session duration
        session_duration = datetime.datetime.now() - self.start_time
        if session_duration > timedelta(hours=2):
            self.speak("You've been interacting for over 2 hours. Consider taking a break.")

        # Exit commands
        if any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye! Have a great day!")
            return False

        # Time and date
        elif 'time' in command:
            self.get_current_time()

        elif 'date' in command:
            self.get_current_date()

        # Web browsing
        elif 'open' in command:
            # Extract the site name
            site_name = self.extract_site_name(command)
            if site_name:
                self.open_website(site_name)
            else:
                self.speak("Please specify a website to open.")

        # Search commands
        elif 'search' in command:
            if 'youtube' in command:
                query = command.replace('search', '').replace('youtube', '').replace('on', '').replace('for', '').strip()
                self.search_youtube(query)
            else:
                query = command.replace('search', '').replace('for', '').strip()
                self.search_web(query)

        elif 'play' in command:
            query = command.replace('play', '').strip()
            self.search_youtube(query)

        # Wikipedia
        elif 'wikipedia' in command:
            query = command.replace('wikipedia', '').strip()
            self.get_wikipedia_info(query)

        # System commands
        elif 'screenshot' in command:
            self.take_screenshot()

        elif 'system info' in command or 'system status' in command or 'battery' in command:
            self.get_system_info()

        elif 'shutdown' in command:
            self.handle_shutdown(command)

        elif 'restart' in command:
            self.handle_restart(command)

        # AI chat
        else:
            response = self.get_ai_response(command, "Use advanced logic")
            self.speak(response)

        return True
    
    def handle_shutdown(self, command):
        """Handle smart shutdown logic"""
        numbers = self.extract_numbers(command)
        delay = int(numbers[0]) if numbers else 10
        self.shutdown_system(delay)

    def handle_restart(self, command):
        """Handle smart restart logic"""
        numbers = self.extract_numbers(command)
        delay = int(numbers[0]) if numbers else 10
        self.restart_system(delay)

    def extract_site_name(self, command):
        """Custom extraction to identify website URLs"""
        return command.replace('open', '').strip()

    def run(self):
        """Main loop for the voice assistant"""
        print("🚀 Starting Voice Assistant...")
        print("=" * 50)

        # Welcome user and provide info based on time
        self.wish_user()

        # Main loop
        while True:
            try:
                # Automatically listen for voice commands
                command = self.listen()

                if command:
                    # Process the command
                    should_continue = self.process_command(command)
                    if not should_continue:
                        break
                else:
                    # If no audio, ask for text command
                    print("\n💬 Type a command (or 'voice' to continue using voice input, 'quit' to exit):")
                    text_input = input("You: ").strip()

                    if text_input.lower() == 'voice':
                        continue
                    elif text_input.lower() in ['quit', 'exit']:
                        self.speak("Goodbye!")
                        break
                    elif text_input:
                        should_continue = self.process_command(text_input)
                        if not should_continue:
                            break

            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                self.speak("I encountered an unexpected error. Please try again.")

def main():
    """Main function to run the voice assistant"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Failed to start voice assistant: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
