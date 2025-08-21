# MagnaPP - Planning Poker Application

A real-time web-based Planning Poker application for distributed agile teams, supporting collaborative estimation sessions through an intuitive virtual boardroom interface.

## Features

- 🎯 Real-time collaborative estimation sessions
- 👥 Support for up to 16 participants per session
- 🎴 Fibonacci sequence voting cards (1, 2, 3, 5, 8, 13, 21) plus Coffee break
- 🔄 Automatic session management with 10-minute timeout
- 📱 Responsive design for desktop, tablet, and mobile
- 🔌 Automatic reconnection support
- 📊 Vote statistics and distribution visualization
- 🎭 Custom avatars and user preferences

## Tech Stack

- **Frontend**: React with TypeScript, Vite, Tailwind CSS
- **Backend**: Python FastAPI with Socket.io
- **Real-time**: Socket.io for WebSocket communication
- **State Management**: Zustand (frontend), In-memory storage (backend)
- **Testing**: Jest, React Testing Library, Playwright, pytest

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Poetry (Python dependency management)

## Quick Start

### Backend Setup

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173`

## Development

### Running Tests

```bash
# Backend tests
cd backend
poetry run pytest

# Frontend tests
cd frontend
npm test
npm run test:e2e
```

### Code Quality

```bash
# Backend
poetry run black .
poetry run isort .
poetry run flake8

# Frontend  
npm run lint
npm run format
```

## Project Structure

```
magna-pp/
├── backend/          # FastAPI backend service
│   ├── app/         # Application code
│   ├── tests/       # Backend tests
│   └── pyproject.toml
├── frontend/         # React frontend application
│   ├── src/         # Source code
│   ├── tests/       # Frontend tests
│   └── package.json
├── docs/            # Documentation
├── plans/           # Development plans
└── docker-compose.yml
```

## Configuration

See `.env.example` for required environment variables:

- `VITE_API_URL`: Backend API URL
- `VITE_WS_URL`: WebSocket server URL
- `SESSION_TIMEOUT_MINUTES`: Session inactivity timeout
- `MAX_SESSIONS`: Maximum concurrent sessions
- `MAX_USERS_PER_SESSION`: Maximum users per session

## Contributing

Please read our contributing guidelines before submitting PRs.

## License

MIT License - see LICENSE file for details