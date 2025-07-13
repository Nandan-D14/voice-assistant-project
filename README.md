
# Advanced Voice Assistant with Gemini AI

A comprehensive voice assistant built with Python that integrates Google's Gemini AI for intelligent conversations and responses.

---

## 🚀 Features

- 🎤 **Voice Recognition** – Advanced speech-to-text using Google Speech Recognition  
- 🔊 **Text-to-Speech** – Natural voice responses with customizable voice settings  
- 🧠 **AI Integration** – Powered by Google's Gemini AI for intelligent responses  
- 🌐 **Web Browsing** – Open websites and search the web with voice commands  
- 💻 **System Control** – Shutdown, restart, take screenshots, and more  
- 📊 **System Information** – Battery, memory, CPU status reporting  
- 🎬 **Media Control** – Play YouTube videos and search content  
- 📚 **Wikipedia Integration** – Fetch information via voice  
- 🖥️ **Cross-Platform** – Works on Windows (others with customization)

---

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Microphone and speaker/headphones
- Stable internet connection
- Google Gemini AI API key

---

### 2. Installation

1. **Clone the project**  
   ```
   git clone https://github.com/Nandan-D14/voice-assistant-project.git
   cd voice-assistant-project
   ```

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Configure API Key**

   * Create a `.env` file in the root directory
   * Add your Gemini API key like so:

     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

   👉 Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)

---

### 3. Running the Assistant

#### 🔹 Option 1: Use the Launcher (Windows)

Double-click `start_assistant.bat`

#### 🔹 Option 2: Manual Run

```
# Activate virtual environment
venv\Scripts\activate

# Run the assistant
python voice_assistant.py
```

---

## 🎙️ Voice Commands

### 📌 Basic Commands

* “Hello” – Get a greeting
* “What time is it?” – Current time
* “What’s the date?” – Current date
* “Exit” / “Quit” – Close the assistant

### 🌐 Web Commands

* “Open YouTube” / “Open Google”
* “Open GitHub” / “Open \[site]”
* “Search for \[query]” – Google
* “Search YouTube for \[query]”
* “Play \[song or video name]”

### 📚 Wikipedia & Info

* “Wikipedia \[topic]” – Get summary
* “Tell me about \[topic]”

### ⚙️ System Control

* “Take a screenshot”
* “System info”
* “Shutdown in 10 seconds”
* “Restart”

### 🤖 AI Chat with Gemini

Ask anything and get intelligent responses:

* “What’s the weather like?”
* “Explain quantum computing”
* “Tell me a joke”
* “Write a short poem”

---

## ⚙️ Configuration

### `.env` File Example

```env
GEMINI_API_KEY=your_api_key_here
ASSISTANT_NAME=Jarvis
VOICE_RATE=200
VOICE_VOLUME=0.9
MUSIC_DIR=C:\Music
DOWNLOADS_DIR=C:\Users\nanda\Downloads
DOCUMENTS_DIR=C:\Users\nanda\Documents
```

---

## 🧩 Dependencies

* `google-generativeai` – Gemini API
* `speechrecognition` – Voice input
* `pyttsx3` – Text-to-speech
* `wikipedia` – Wikipedia search
* `pywhatkit` – YouTube and search
* `pyautogui` – Screenshot and GUI automation
* `psutil` – System status
* `python-dotenv` – Load `.env` variables

---

## 🧰 Troubleshooting

### Microphone Not Working

* Check microphone hardware
* Run as administrator
* Check privacy settings in Windows

### Speech Not Detected

* Ensure internet connection
* Speak clearly
* Test mic in other apps

### Gemini API Errors

* Check API key in `.env`
* Ensure key is valid and active

### Audio Output Issues

* Verify speaker/headphone connection
* Test with `pyttsx3` alone

---

## 🆕 Enhanced Version Available! 🚀

We’ve built a **feature-rich enhanced version** with:

* 🌤️ Weather & 📰 News integration
* 📝 Voice-activated Notes
* ⏰ Reminders & Task management
* 📧 Email support
* 🔗 QR Code generation
* 🎭 Entertainment & jokes
* 🎛️ User preferences
* 💾 Persistent data storage

### 👉 To Run:

```
start_enhanced_assistant.bat
# or
python enhanced_voice_assistant.py
```

📖 Full docs: `ENHANCED_FEATURES.md`

---

## 📜 Version History

| Version | Features                               |
| ------- | -------------------------------------- |
| `v1.0`  | Initial release with voice recognition |
| `v2.0`  | Gemini AI integration                  |
| `v2.1`  | Improved error handling                |
| `v3.0`  | Enhanced version with smart features   |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

We welcome contributions!
Feel free to:

* Report bugs
* Suggest features
* Submit pull requests
* Improve documentation

---

**🔒 Note:** Never share your API key publicly!

````

---

### ✅ Next Step

After saving this as `README.md` in your project:

```
git add README.md
git commit -m "Add complete project README"
git push -u origin main   # Or use --force if required
````
