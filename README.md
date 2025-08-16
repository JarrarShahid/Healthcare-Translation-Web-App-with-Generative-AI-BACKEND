# Healthcare Translator Backend

A FastAPI backend service that provides AI-powered medical translation using Groq's Mixtral-8x7B model through LangChain.

## Features

- **Medical Translation**: Specialized AI translation for healthcare terminology
- **Multi-language Support**: Supports 12 languages including English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, and Hindi
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **LangChain Integration**: Leverages LangChain for structured AI interactions
- **Groq LLM**: Uses Groq's Mixtral-8x7B model for high-quality translations
- **CORS Support**: Configured for frontend integration
- **Error Handling**: Comprehensive error handling with meaningful messages

## Prerequisites

- Python 3.8 or higher
- Groq API key (get one at [https://console.groq.com/](https://console.groq.com/))

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd voice-med-speak-backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Running the Server

### Development Mode
```bash
uvicorn main:app --reload --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using Python directly
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### 1. Health Check
- **GET** `/` - Basic health check
- **GET** `/health` - Health status

### 2. Translation
- **POST** `/translate` - Translate medical text

#### Request Body:
```json
{
  "text": "I have diabetes and chest pain",
  "source_lang": "en",
  "target_lang": "es"
}
```

#### Response:
```json
{
  "translated_text": "Tengo diabetes y dolor en el pecho"
}
```

### 3. Languages
- **GET** `/languages` - Get supported languages

## Testing the API

### Using curl

1. **Health check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Translation**:
   ```bash
   curl -X POST http://localhost:8000/translate \
     -H "Content-Type: application/json" \
     -d '{"text": "I have diabetes", "source_lang": "en", "target_lang": "es"}'
   ```

3. **Get languages**:
   ```bash
   curl http://localhost:8000/languages
   ```

### Using the Interactive API Docs

1. Start the server
2. Open your browser to `http://localhost:8000/docs`
3. Use the interactive Swagger UI to test endpoints

### Frontend Integration

The backend is configured with CORS to work with the React frontend running on:
- `http://localhost:3000` (Create React App)
- `http://localhost:5173` (Vite)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | Required |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Model Configuration

The backend uses Groq's Mixtral-8x7B model with:
- **Temperature**: 0.1 (low for consistent medical translations)
- **Model**: `mixtral-8x7b-32768` (high-quality, fast inference)

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Successful translation
- **400**: Bad request (missing text, languages)
- **500**: Server error (API key issues, translation failures)

Error responses include descriptive messages:
```json
{
  "error": "Translation failed, please try again."
}
```

## Deployment

### Local Development
- Perfect for development and testing
- Uses `--reload` flag for automatic restarts

### Production Deployment

#### Railway
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

#### Render
1. Connect your GitHub repository
2. Set environment variables
3. Choose Python runtime
4. Deploy

#### Docker (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Groq API      │
│   (React)       │───▶│   Backend       │───▶│   (Mixtral)     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   LangChain     │
                       │   (Prompts)     │
                       └─────────────────┘
```

## Security & Privacy

- **No Data Storage**: Translations are not stored or logged
- **API Key Security**: Store your Groq API key in environment variables
- **CORS Configuration**: Only allows specified frontend origins
- **Input Validation**: All inputs are validated using Pydantic models

## Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not configured"**
   - Ensure your `.env` file exists and contains the API key
   - Check that `python-dotenv` is installed

2. **"Translation failed"**
   - Verify your Groq API key is valid
   - Check Groq service status
   - Ensure you have sufficient API credits

3. **CORS errors**
   - Verify the frontend URL is in the allowed origins
   - Check that the backend is running on the expected port

4. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

### Logs

The server provides detailed logging. Check the console output for:
- Translation requests and responses
- Error details
- API call information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Voice-Med-Speak healthcare translation application.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Check the logs for detailed error information

