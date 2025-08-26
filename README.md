# Django Chat Interface

A modern, responsive chat interface built with Django for interacting with Large Language Models (LLMs).

## Features

- 🎨 **Modern UI**: Beautiful, responsive design with gradient backgrounds and smooth animations
- 💬 **Real-time Chat**: Interactive chat interface with typing indicators
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- 🔄 **Session Management**: Maintains chat history with unique session IDs
- 💾 **Database Storage**: Stores all chat messages in SQLite database
- 🛠️ **Admin Interface**: Django admin panel for managing chat messages
- 🚀 **RESTful API**: Clean API endpoints for sending messages and retrieving history

## Screenshots

The interface features:
- Gradient background with modern card design
- User and AI message bubbles with distinct styling
- Typing indicators during AI responses
- Responsive design for all screen sizes

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or download the project**
   ```bash
   cd test-project
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser and navigate to**
   ```
   http://127.0.0.1:8000/
   ```

## Usage

### Chat Interface
- Type your message in the input field
- Press Enter or click Send to submit
- View AI responses in real-time
- Chat history is automatically saved

### Admin Panel
- Access at `http://127.0.0.1:8000/admin/`
- View and manage all chat messages
- Filter by role, session, or timestamp
- Search through message content

## Project Structure

```
test-project/
├── chat/                          # Chat application
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions and API endpoints
│   ├── urls.py                    # URL routing for chat app
│   ├── admin.py                   # Admin interface configuration
│   └── templates/chat/            # HTML templates
│       └── chat.html              # Main chat interface
├── chat_project/                  # Django project settings
│   ├── settings.py                # Project configuration
│   ├── urls.py                    # Main URL routing
│   └── wsgi.py                    # WSGI configuration
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## API Endpoints

### Send Message
- **URL**: `/api/send/`
- **Method**: POST
- **Body**: `{"message": "Your message", "session_id": "optional_session_id"}`
- **Response**: `{"success": true, "response": "AI response", "session_id": "session_id"}`

### Get Chat History
- **URL**: `/api/history/<session_id>/`
- **Method**: GET
- **Response**: `{"messages": [{"role": "user", "content": "...", "timestamp": "..."}]}`

## Customization

### Integrating with Real LLM APIs
To connect with actual LLM services (OpenAI, Anthropic, etc.), modify the `send_message` view in `chat/views.py`:

```python
# Example OpenAI integration
import openai

# In the send_message view, replace the placeholder response with:
openai.api_key = 'your-api-key'
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_message}]
)
ai_response = response.choices[0].message.content
```

### Styling
- Modify CSS in `chat/templates/chat/chat.html`
- Update color schemes, fonts, and layout
- Add custom animations and transitions

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes

## Deployment

### Production Settings
1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL, MySQL)
4. Set up static file serving
5. Configure HTTPS

### Environment Variables
```bash
export DJANGO_SECRET_KEY="your-secret-key"
export DJANGO_DEBUG="False"
export DATABASE_URL="your-database-url"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the Django documentation
- Review the code comments
- Open an issue in the repository

## Future Enhancements

- [ ] User authentication and user-specific chat history
- [ ] File upload support
- [ ] Real-time WebSocket communication
- [ ] Multiple AI model support
- [ ] Chat export functionality
- [ ] Advanced message formatting
- [ ] Chat analytics and insights

