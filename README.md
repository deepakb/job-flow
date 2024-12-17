# Job Flow API

A FastAPI-based backend for a job-matching platform that enables users to upload resumes, match jobs, receive insights, and handle notifications.

## Features

- User Management with Firebase Authentication
- Resume Parsing and Enhancement using OpenAI
- Job Aggregation and Matching
- Insights and Recommendations
- Real-time Notifications

## Setup

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
poetry run uvicorn src.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
src/
├── api/             # API routes
├── core/            # Core settings, middlewares, and utilities
├── models/          # Pydantic models
├── services/        # Business logic
├── repositories/    # Firebase integration
├── tests/          # Unit and integration tests
└── main.py         # FastAPI application entry point
```

## Development

1. Run tests:
```bash
poetry run pytest
```

2. Format code:
```bash
poetry run black .
```

## License

MIT
