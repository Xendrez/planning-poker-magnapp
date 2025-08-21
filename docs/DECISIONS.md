# Technology Stack Decisions

## Date: 2025-08-21

## Frontend
**Choice: React with TypeScript**
- **Rationale**: 
  - Mature ecosystem with excellent WebSocket support via socket.io-client
  - Strong typing with TypeScript for better maintainability
  - Rich component libraries for building interactive UI (virtual boardroom, cards)
  - Excellent tooling and community support
  - React's component model fits well with our avatar/user card system

## Backend  
**Choice: Python with FastAPI**
- **Rationale**:
  - Async/await support for handling concurrent WebSocket connections
  - Type hints and automatic API documentation via OpenAPI
  - Excellent performance for our scale (48 concurrent users max)
  - Clean, maintainable code with Pydantic models
  - Built-in validation and serialization

## Real-time Communication
**Choice: Socket.io** (python-socketio backend, socket.io-client frontend)
- **Rationale**:
  - Built-in automatic reconnection with exponential backoff (PRD requirement)
  - Room management perfect for session-based architecture (16 users/session)
  - Message acknowledgments ensure reliable delivery
  - Fallback transports if WebSockets unavailable
  - Handles connection state management automatically

## State Management
**Frontend: Zustand** (lightweight state management)
- **Rationale**:
  - Simpler than Redux for our moderate complexity
  - TypeScript first
  - Works well with React and Socket.io
  - Small bundle size

**Backend: In-memory storage**
- Using Python dictionaries with session cleanup timers
- No database needed per PRD

## Testing Strategy
**Choice: Comprehensive Testing**
- **Backend**: pytest + pytest-asyncio for async FastAPI endpoints and WebSocket handlers
- **Frontend**: Jest + React Testing Library for components, Playwright for E2E
- **Rationale**: 
  - PRD requires >95% session completion rate
  - >98% reconnection success rate requires robust testing
  - Real-time features need integration testing
  - E2E tests ensure complete user journeys work

## Styling Solution
**Choice: Tailwind CSS + CSS Modules**
- **Rationale**:
  - Tailwind for rapid prototyping and responsive design
  - CSS Modules for component-specific styles (boardroom, cards)
  - Supports light/dark mode requirement

## Build Tools
- **Frontend**: Vite (faster than Create React App, better HMR)
- **Backend**: Poetry for Python dependency management
- **Monorepo**: Separate folders with independent builds

## Deployment Target
- Docker containers for both frontend and backend
- Nginx for serving frontend and reverse proxy
- Environment variables for configuration