# FairPlay Frontend

A modern Vite + React + TypeScript SPA for the FairPlay football team management app.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

## Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173` and automatically proxies API calls to the Django backend at `http://localhost:8000`.

**Important**: Ensure the Django backend is running on `http://localhost:8000` before starting the frontend dev server.

## Architecture

- **src/api**: Typed API client modules for each feature (auth, players, teams, matches, history)
- **src/pages**: React components for each page/screen
- **src/components**: Shared UI components (AppLayout, ProtectedRoute)
- **src/context**: React Context for global state (AuthContext for user session)
- **src/types.ts**: Shared TypeScript type definitions matching Django models

## Building

Build for production:
```bash
npm run build
```

Output goes to the `dist/` folder, ready to be served by a static host or CDN.

## API Contract

The frontend expects the following Django REST API endpoints:

### Auth
- `GET /api/auth/csrf` - Get CSRF cookie
- `GET /api/auth/me` - Get current user
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Players
- `GET /api/players` - List user's players
- `POST /api/players` - Create player
- `PATCH /api/players/:id` - Update player
- `DELETE /api/players/:id` - Delete player
- `POST /api/players/reset` - Reset all players

### Teams
- `GET /api/teams` - List teams
- `POST /api/teams/generate` - Generate teams using snake draft
- `GET /api/teams/:id/history` - Get team history and stats

### Matches
- `GET /api/matches` - List matches
- `POST /api/matches` - Create match
- `GET /api/matches/:id` - Get match details
- `PATCH /api/matches/:id/result` - Record match result

### History
- `GET /api/history/me` - Get user's personal history and stats

## Environment Variables

- `VITE_API_BASE_URL`: Base URL for API calls (default: `/api`)

## Features Implemented

- ✅ User authentication (register/login/logout)
- ✅ Player management (add/update/delete/reset)
- ✅ Team generation with snake draft algorithm
- ✅ Team display with statistics
- ✅ Match management (create, view, record results)
- ✅ Personal history and statistics
- ✅ Responsive dark theme UI
- ✅ Protected routes with auth context
- ✅ SessionStorage-based CSRF token handling

## Development Notes

The frontend uses:
- React 19 with hooks
- React Router DOM v6 for client-side routing
- TypeScript for type safety
- Custom API client with CSRF/session auth support
- CSS Grid and Flexbox for responsive layouts
- Dark theme (Slate/Sky color scheme)
