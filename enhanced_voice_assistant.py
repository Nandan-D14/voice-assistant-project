#!/usr/bin/env python3
"""
Enhanced Voice Assistant with Advanced Features
Features: Weather, News, Reminders, Smart Home Controls, Email, Calendar, and more
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
import smtplib
import sqlite3
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import schedule

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

# Enhanced libraries
import pyjokes
import qrcode
from PIL import Image
import cv2
import numpy as np

# Load environment variables
load_dotenv()

class EnhancedVoiceAssistant:
    def __init__(self):
        """Initialize the enhanced voice assistant"""
        self.setup_database()
        self.setup_ai()
        self.setup_voice()
        self.setup_speech_recognition()
        self.load_config()
        self.command_history = []
        self.start_time = datetime.datetime.now()
        self.reminders = []
        self.user_preferences = self.load_user_preferences()
        self.setup_scheduler()
        
    def setup_database(self):
        """Initialize SQLite database for storing user data"""
        self.conn = sqlite3.connect('assistant_data.db')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                datetime TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        self.conn.commit()
        print("✓ Database initialized")
    
    def setup_ai(self):
        """Configure Gemini AI with enhanced prompts"""
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✓ Gemini AI configured successfully")
        except Exception as e:
            print(f"✗ Error configuring Gemini AI: {e}")
            self.model = None
    
    def setup_voice(self):
        """Initialize enhanced text-to-speech"""
        try:
            self.engine = pyttsx3.init('sapi5')
            voices = self.engine.getProperty('voices')
            
            # Set voice properties
            voice_preference = self.user_preferences.get('voice_gender', 'female')
            if voice_preference == 'female' and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            elif voice_preference == 'male' and len(voices) > 0:
                self.engine.setProperty('voice', voices[0].id)
            
            self.engine.setProperty('rate', int(self.user_preferences.get('voice_rate', 200)))
            self.engine.setProperty('volume', float(self.user_preferences.get('voice_volume', 0.9)))
            print("✓ Enhanced text-to-speech initialized")
        except Exception as e:
            print(f"✗ Error initializing voice engine: {e}")
            self.engine = None
    
    def setup_speech_recognition(self):
        """Initialize speech recognition with improved settings"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Enhanced recognition settings
            self.recognizer.energy_threshold = 4000
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✓ Enhanced speech recognition initialized")
        except Exception as e:
            print(f"✗ Error initializing speech recognition: {e}")
            self.recognizer = None
    
    def load_config(self):
        """Load enhanced configuration"""
        self.assistant_name = os.getenv('ASSISTANT_NAME', 'Jarvis')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
        # Enhanced application mappings
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
            'instagram': 'https://www.instagram.com',
            'whatsapp': 'https://web.whatsapp.com',
            'linkedin': 'https://www.linkedin.com',
            'reddit': 'https://www.reddit.com',
            'discord': 'https://discord.com',
            'slack': 'https://slack.com',
            'zoom': 'https://zoom.us',
            'teams': 'https://teams.microsoft.com'
        }
    
    def load_user_preferences(self):
        """Load user preferences from database"""
        try:
            self.cursor.execute("SELECT key, value FROM user_preferences")
            preferences = dict(self.cursor.fetchall())
            return preferences
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return {}
    
    def save_user_preference(self, key, value):
        """Save user preference to database"""
        try:
            self.cursor.execute("INSERT OR REPLACE INTO user_preferences (key, value) VALUES (?, ?)", 
                              (key, value))
            self.conn.commit()
            self.user_preferences[key] = value
            print(f"✓ Saved preference: {key} = {value}")
        except Exception as e:
            print(f"Error saving preference: {e}")
    
    def setup_scheduler(self):
        """Setup background scheduler for reminders"""
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("✓ Background scheduler started")
    
    def speak(self, text, urgent=False):
        """Enhanced speak function with urgency levels"""
        if self.engine:
            try:
                if urgent:
                    self.engine.setProperty('rate', 250)
                    print(f"🚨 {self.assistant_name}: {text}")
                else:
                    self.engine.setProperty('rate', int(self.user_preferences.get('voice_rate', 200)))
                    print(f"🎵 {self.assistant_name}: {text}")
                
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"✗ Error in text-to-speech: {e}")
        else:
            print(f"{self.assistant_name}: {text}")
    
    def listen(self, timeout=5):
        """Enhanced listening with better error handling"""
        if not self.recognizer:
            return None
            
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                
            print("🔍 Recognizing...")
            command = self.recognizer.recognize_google(audio, language='en-US')
            print(f"👤 User said: {command}")
            return command.lower()
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            return None
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return None
    
    def get_weather(self, city=None):
        """Get weather information using OpenWeatherMap API"""
        if not self.weather_api_key:
            self.speak("Weather API key not configured. Please set WEATHER_API_KEY in your environment.")
            return
        
        if not city:
            city = self.user_preferences.get('default_city', 'New York')
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                
                weather_info = f"Weather in {city}: {description}. Temperature is {temp}°C, feels like {feels_like}°C. Humidity is {humidity}%"
                self.speak(weather_info)
                return weather_info
            else:
                self.speak(f"Sorry, I couldn't get weather information for {city}")
                return None
                
        except Exception as e:
            print(f"Error getting weather: {e}")
            self.speak("Sorry, I couldn't get the weather information right now")
            return None
    
    def get_news(self, category='general', country='us'):
        """Get latest news using NewsAPI"""
        if not self.news_api_key:
            self.speak("News API key not configured. Please set NEWS_API_KEY in your environment.")
            return
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data['articles']:
                articles = data['articles'][:5]  # Get top 5 articles
                
                self.speak("Here are the latest news headlines:")
                for i, article in enumerate(articles, 1):
                    headline = article['title']
                    source = article['source']['name']
                    self.speak(f"{i}. {headline} - {source}")
                    
                return articles
            else:
                self.speak("Sorry, I couldn't get news right now")
                return None
                
        except Exception as e:
            print(f"Error getting news: {e}")
            self.speak("Sorry, I couldn't get the news right now")
            return None
    
    def create_reminder(self, title, description, remind_time):
        """Create a reminder"""
        try:
            self.cursor.execute(
                "INSERT INTO reminders (title, description, datetime) VALUES (?, ?, ?)",
                (title, description, remind_time.isoformat())
            )
            self.conn.commit()
            
            # Schedule the reminder
            def reminder_alert():
                self.speak(f"Reminder: {title}. {description}", urgent=True)
            
            schedule.every().day.at(remind_time.strftime("%H:%M")).do(reminder_alert)
            
            self.speak(f"Reminder set for {remind_time.strftime('%B %d at %I:%M %p')}: {title}")
            return True
            
        except Exception as e:
            print(f"Error creating reminder: {e}")
            self.speak("Sorry, I couldn't create the reminder")
            return False
    
    def get_reminders(self):
        """Get all active reminders"""
        try:
            self.cursor.execute("SELECT * FROM reminders WHERE completed = 0 ORDER BY datetime")
            reminders = self.cursor.fetchall()
            
            if reminders:
                self.speak(f"You have {len(reminders)} active reminders:")
                for reminder in reminders:
                    remind_time = datetime.datetime.fromisoformat(reminder[3])
                    self.speak(f"{reminder[1]} on {remind_time.strftime('%B %d at %I:%M %p')}")
            else:
                self.speak("You have no active reminders")
                
            return reminders
            
        except Exception as e:
            print(f"Error getting reminders: {e}")
            self.speak("Sorry, I couldn't get your reminders")
            return []
    
    def create_note(self, title, content):
        """Create a note"""
        try:
            current_time = datetime.datetime.now().isoformat()
            self.cursor.execute(
                "INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)",
                (title, content, current_time)
            )
            self.conn.commit()
            
            self.speak(f"Note '{title}' created successfully")
            return True
            
        except Exception as e:
            print(f"Error creating note: {e}")
            self.speak("Sorry, I couldn't create the note")
            return False
    
    def get_notes(self):
        """Get all notes"""
        try:
            self.cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
            notes = self.cursor.fetchall()
            
            if notes:
                self.speak(f"You have {len(notes)} notes:")
                for note in notes[:5]:  # Show first 5 notes
                    self.speak(f"{note[1]}: {note[2][:50]}...")
            else:
                self.speak("You have no notes")
                
            return notes
            
        except Exception as e:
            print(f"Error getting notes: {e}")
            self.speak("Sorry, I couldn't get your notes")
            return []
    
    def tell_joke(self):
        """Tell a random joke"""
        try:
            joke = pyjokes.get_joke()
            self.speak(joke)
            return joke
        except Exception as e:
            print(f"Error getting joke: {e}")
            self.speak("Sorry, I couldn't think of a joke right now")
            return None
    
    def generate_qr_code(self, text, filename=None):
        """Generate QR code for given text"""
        try:
            if not filename:
                filename = f"qr_code_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            
            self.speak(f"QR code generated and saved as {filename}")
            return filename
            
        except Exception as e:
            print(f"Error generating QR code: {e}")
            self.speak("Sorry, I couldn't generate the QR code")
            return None
    
    def send_email(self, to_email, subject, body):
        """Send email"""
        if not self.email_address or not self.email_password:
            self.speak("Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your environment.")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            
            self.speak(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            self.speak("Sorry, I couldn't send the email")
            return False
    
    def get_ai_response(self, prompt, context=None):
        """Enhanced AI response with context"""
        if not self.model:
            return "AI service is not available."
        
        try:
            # Add user preferences to context
            user_context = f"User preferences: {self.user_preferences}. "
            if context:
                full_context = user_context + context + " "
            else:
                full_context = user_context
            
            full_prompt = f"{full_context}You are {self.assistant_name}, a helpful voice assistant. Respond naturally: {prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"✗ Error with Gemini AI: {e}")
            return "I'm having trouble processing your request right now."
    
    def process_enhanced_command(self, command):
        """Process enhanced voice commands"""
        if not command:
            return True
        
        command = command.lower().strip()
        self.command_history.append(command)
        
        # Weather commands
        if any(word in command for word in ['weather', 'temperature', 'forecast']):
            if 'in' in command:
                city = command.split('in')[-1].strip()
                self.get_weather(city)
            else:
                self.get_weather()
        
        # News commands
        elif 'news' in command:
            category = 'general'
            if 'sports' in command:
                category = 'sports'
            elif 'technology' in command or 'tech' in command:
                category = 'technology'
            elif 'business' in command:
                category = 'business'
            elif 'health' in command:
                category = 'health'
            elif 'entertainment' in command:
                category = 'entertainment'
            
            self.get_news(category)
        
        # Reminder commands
        elif 'remind me' in command or 'reminder' in command:
            if 'show' in command or 'list' in command:
                self.get_reminders()
            else:
                self.speak("What would you like me to remind you about?")
                title = input("Reminder title: ")
                description = input("Description (optional): ")
                time_str = input("When? (HH:MM format): ")
                
                try:
                    hour, minute = map(int, time_str.split(':'))
                    remind_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
                    if remind_time < datetime.datetime.now():
                        remind_time += timedelta(days=1)
                    
                    self.create_reminder(title, description, remind_time)
                except ValueError:
                    self.speak("Invalid time format. Please use HH:MM format.")
        
        # Note commands
        elif 'note' in command:
            if 'show' in command or 'list' in command:
                self.get_notes()
            else:
                self.speak("What's the title of your note?")
                title = input("Note title: ")
                self.speak("What's the content?")
                content = input("Note content: ")
                self.create_note(title, content)
        
        # Joke command
        elif 'joke' in command:
            self.tell_joke()
        
        # QR code command
        elif 'qr code' in command:
            self.speak("What text would you like to encode in the QR code?")
            text = input("QR code text: ")
            self.generate_qr_code(text)
        
        # Email command
        elif 'email' in command or 'send email' in command:
            self.speak("What's the recipient's email address?")
            to_email = input("To: ")
            self.speak("What's the subject?")
            subject = input("Subject: ")
            self.speak("What's the message?")
            body = input("Message: ")
            self.send_email(to_email, subject, body)
        
        # User preference commands
        elif 'set preference' in command or 'configure' in command:
            self.speak("What preference would you like to set?")
            key = input("Preference key: ")
            self.speak("What value?")
            value = input("Value: ")
            self.save_user_preference(key, value)
        
        # Exit command
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # Default: use AI for other commands
        else:
            response = self.get_ai_response(command)
            self.speak(response)
        
        return True
    
    def run(self):
        """Main enhanced loop"""
        print("🚀 Starting Enhanced Voice Assistant...")
        print("=" * 50)
        
        # Enhanced greeting
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        
        welcome_message = f"{greeting} I'm your enhanced {self.assistant_name}. I can help you with weather, news, reminders, notes, and much more!"
        self.speak(welcome_message)
        
        # Main loop
        while True:
            try:
                command = self.listen()
                
                if command:
                    should_continue = self.process_enhanced_command(command)
                    if not should_continue:
                        break
                else:
                    print("\n💬 Type a command (or 'voice' to continue using voice input, 'quit' to exit):")
                    text_input = input("You: ").strip()
                    
                    if text_input.lower() == 'voice':
                        continue
                    elif text_input.lower() in ['quit', 'exit']:
                        self.speak("Goodbye!")
                        break
                    elif text_input:
                        should_continue = self.process_enhanced_command(text_input)
                        if not should_continue:
                            break
                            
            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                self.speak("I encountered an unexpected error. Please try again.")
    
    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    """Main function"""
    try:
        assistant = EnhancedVoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Failed to start enhanced voice assistant: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
