# Catan: Corporate Intelligent Search & Analysis Engine

A modern web application for intelligent document search and analysis, built with FastAPI and React.

## Features

- Advanced document search with AI-powered analysis
- Real-time search results with instant feedback
- Modern, responsive user interface
- Secure document handling and processing
- Integration with Google's Gemini AI for intelligent insights

## Tech Stack

### Backend
- FastAPI (Python)
- Google Gemini AI API
- Docker for containerization

### Frontend
- React with TypeScript
- Modern UI components
- Responsive design

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js (for frontend development)
- Python 3.8+ (for backend development)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd catan
```

2. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
GOOGLE_API_KEY=your_gemini_api_key
```

3. Start the application using Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 