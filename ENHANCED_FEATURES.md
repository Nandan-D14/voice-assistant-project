# Enhanced Voice Assistant Features

## 🚀 New Features Added

### 1. **Weather Integration**
- Get current weather for any city
- Voice commands: "What's the weather?", "Weather in London"
- Requires: OpenWeatherMap API key

### 2. **News Integration**
- Get latest news headlines by category
- Voice commands: "Give me news", "Sports news", "Tech news"
- Requires: NewsAPI key

### 3. **Smart Reminders**
- Create, list, and manage reminders
- Automatic scheduling with background alerts
- Voice commands: "Remind me to...", "Show my reminders"
- Persistent storage in SQLite database

### 4. **Note-Taking System**
- Create and manage notes with voice commands
- Voice commands: "Create a note", "Show my notes"
- Persistent storage in SQLite database

### 5. **Email Integration**
- Send emails using voice commands
- Voice commands: "Send email"
- Requires: Gmail credentials

### 6. **QR Code Generation**
- Generate QR codes for text, URLs, etc.
- Voice commands: "Generate QR code"
- Saves QR codes as PNG files

### 7. **Enhanced AI Responses**
- Context-aware responses using user preferences
- Improved conversation flow
- Better error handling

### 8. **User Preferences System**
- Save and load user preferences
- Customize voice settings, default city, etc.
- Voice commands: "Set preference"

### 9. **Jokes and Entertainment**
- Tell random programming jokes
- Voice commands: "Tell me a joke"

### 10. **Background Scheduler**
- Automatic reminder notifications
- Runs in background thread
- Smart scheduling system

## 🛠️ Setup Instructions

### 1. Install Enhanced Dependencies

```bash
pip install -r requirements.txt
```

### 2. API Keys Setup

Create a `.env` file based on `.env.example`:

#### Weather API (OpenWeatherMap)
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key
4. Add to `.env`: `WEATHER_API_KEY=your_key_here`

#### News API
1. Go to https://newsapi.org/
2. Sign up for a free account
3. Get your API key
4. Add to `.env`: `NEWS_API_KEY=your_key_here`

#### Email (Gmail)
1. Enable 2-factor authentication on Gmail
2. Generate an app password
3. Add to `.env`: 
   ```
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

### 3. Run Enhanced Assistant

```bash
# Using the launcher
start_enhanced_assistant.bat

# Or directly
python enhanced_voice_assistant.py
```

## 🎯 Voice Commands Reference

### Weather Commands
- "What's the weather?"
- "Weather in [city name]"
- "What's the temperature?"
- "Weather forecast"

### News Commands
- "Give me news"
- "Latest news"
- "Sports news"
- "Technology news"
- "Business news"
- "Health news"
- "Entertainment news"

### Reminder Commands
- "Remind me to [task]"
- "Create a reminder"
- "Show my reminders"
- "List reminders"

### Note Commands
- "Create a note"
- "Take a note"
- "Show my notes"
- "List notes"

### Email Commands
- "Send email"
- "Send an email"

### QR Code Commands
- "Generate QR code"
- "Create QR code"

### Preference Commands
- "Set preference"
- "Configure settings"

### Entertainment Commands
- "Tell me a joke"
- "Make me laugh"

### System Commands (Original)
- "What time is it?"
- "What's the date?"
- "Take a screenshot"
- "System info"
- "Open [website]"
- "Search for [query]"
- "Play [song/video]"
- "Wikipedia [topic]"

## 📊 Database Schema

The enhanced assistant uses SQLite for persistent storage:

### Reminders Table
- id (PRIMARY KEY)
- title (TEXT)
- description (TEXT)
- datetime (TEXT - ISO format)
- completed (INTEGER - 0/1)

### Notes Table
- id (PRIMARY KEY)
- title (TEXT)
- content (TEXT)
- created_at (TEXT - ISO format)
- updated_at (TEXT - ISO format)

### User Preferences Table
- key (PRIMARY KEY)
- value (TEXT)

## 🔧 Configuration Options

### Voice Settings
- `VOICE_RATE`: Speech rate (default: 200)
- `VOICE_VOLUME`: Volume level (default: 0.9)
- `ASSISTANT_NAME`: Assistant name (default: Jarvis)

### Enhanced Settings
- `WEATHER_API_KEY`: OpenWeatherMap API key
- `NEWS_API_KEY`: NewsAPI key
- `EMAIL_ADDRESS`: Gmail address
- `EMAIL_PASSWORD`: Gmail app password

### User Preferences (Stored in Database)
- `voice_gender`: "male" or "female"
- `voice_rate`: Speech rate
- `voice_volume`: Volume level
- `default_city`: Default city for weather

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify API keys are correctly set in `.env`
   - Check API key validity and quotas

2. **Database Errors**
   - Ensure write permissions in project directory
   - Delete `assistant_data.db` to reset database

3. **Email Errors**
   - Use Gmail app password, not regular password
   - Enable 2-factor authentication first

4. **Voice Recognition Issues**
   - Check microphone permissions
   - Ensure stable internet connection
   - Speak clearly and at normal pace

### Performance Tips

1. **Background Scheduler**
   - Runs in separate thread for better performance
   - Automatically handles reminder notifications

2. **Database Optimization**
   - SQLite database is lightweight and fast
   - Indexes on datetime columns for better query performance

3. **Error Handling**
   - Graceful fallbacks for API failures
   - User-friendly error messages

## 🔮 Future Enhancements

### Planned Features
- Calendar integration
- Smart home device control
- Voice-activated file management
- Language translation
- Task automation
- Machine learning for better command recognition
- Multi-language support
- Plugin system for custom commands

### Potential Integrations
- Google Calendar
- Spotify API
- Smart home devices (Philips Hue, etc.)
- File system operations
- Browser automation
- Social media posting
- Stock market data
- Cryptocurrency prices

## 📝 Contributing

Feel free to contribute by:
- Adding new voice commands
- Integrating new APIs
- Improving error handling
- Adding new features
- Optimizing performance
- Writing tests
- Improving documentation

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: Always keep your API keys secure and never commit them to version control!
