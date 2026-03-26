# Quick Start Guide - FairPlay SPA Frontend

## TL;DR - 3 Steps to Get Running

### Step 1: Start Django Backend
```bash
cd fairplay/fairplay
python manage.py runserver 8000
```

### Step 2: Start Frontend (New Terminal)
```bash
cd fairplay/frontend
npm run dev
```

### Step 3: Open Browser
Visit `http://localhost:5173`

---

## What You'll See

A login page with options to:
- Register a new account (username, email, password, preferred position)
- Login if you already have an account

---

## ⚠️ Important: You Still Need to Implement the Django REST API

The frontend is **100% complete and ready**, but it expects Django REST API endpoints that don't exist yet in your current codebase.

**Current state:**
- ✅ Django: Standard Template-based views
- ✅ Frontend: Complete Vite React SPA
- ❌ Django REST API: NOT YET IMPLEMENTED

**To make them work together:**

Read **[FRONTEND_MIGRATION.md](./FRONTEND_MIGRATION.md)** for step-by-step instructions to:
1. Install Django REST Framework
2. Create serializers
3. Convert template views → REST API endpoints
4. Wire up authentication
5. Test everything

---

## File Structure

```
fairplay/
├── fairplay/                    # Django project (existing)
│   ├── manage.py
│   ├── fair_play/              # App with models, views, etc.
│   └── fairplay/               # Project settings
├── frontend/                    # NEW: Vite React SPA
│   ├── src/
│   │   ├── api/               # API client layer
│   │   ├── pages/             # Page components
│   │   ├── components/        # Shared components
│   │   ├── context/           # React Context (auth)
│   │   ├── types.ts           # Shared types
│   │   └── App.tsx            # Router + entry
│   ├── package.json
│   └── vite.config.ts
├── FRONTEND_SETUP_COMPLETE.md  # Detailed setup overview
├── FRONTEND_MIGRATION.md       # How to implement Django REST API
└── README.md                   # Original FairPlay docs
```

---

## Frontend Tech Stack

- **React 19** - UI library with hooks
- **React Router v6** - Client-side routing
- **TypeScript** - Type safety throughout
- **Vite** - Fast dev server & optimized builds
- **Dark Theme CSS** - Professional styling

---

## API Contract (What the Frontend Expects)

The frontend calls these endpoints (implement in Django):

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/me` | Get current user |
| GET | `/api/players` | List players |
| POST | `/api/players` | Create player |
| PATCH | `/api/players/:id` | Update player |
| DELETE | `/api/players/:id` | Delete player |
| POST | `/api/players/reset` | Reset all players |
| GET | `/api/teams` | List teams (owned + member) |
| POST | `/api/teams/generate` | Generate teams |
| GET | `/api/teams/:id/history` | Team stats/history |
| GET | `/api/matches` | List matches |
| POST | `/api/matches` | Create match |
| GET | `/api/matches/:id` | Match details |
| PATCH | `/api/matches/:id/result` | Record result |
| GET | `/api/history/me` | Personal history |

See endpoint definitions in `frontend/README.md` section "API Contract".

---

## Key Features Built

### Authentication
- Register with username, email, password, preferred position
- Login/logout with session auth
- Protected routes (auto-redirect to login)

### Players
- Add players by searching usernames
- Update position/rating
- Delete players
- Reset all at once

### Teams
- Generate balanced teams using snake draft algorithm
- View team rosters with stats
- View team history

### Matches
- Create matches between teams
- Schedule with date/location
- Record results
- View match details and rosters

### Personal Stats
- Track W/L/D record
- Goals and assists
- Team membership history
- Match participation log

---

## Development Workflow

**Make frontend changes:**
- Edit files in `frontend/src/`
- Vite auto-reloads (HMR)
- TypeScript catches errors

**Make backend changes:**
- Edit files in `fairplay/fair_play/`
- Django auto-reloads
- Serialize models to JSON

**Add new feature:**
1. Add API endpoint in Django
2. Add client method in `frontend/src/api/`
3. Create page component in `frontend/src/pages/`
4. Add route in `frontend/src/App.tsx`

---

## Next Actions

### Immediate (Make it work)
1. Read [FRONTEND_MIGRATION.md](./FRONTEND_MIGRATION.md)
2. Install `djangorestframework` and `django-cors-headers`
3. Create serializers for your models
4. Convert views to REST API endpoints
5. Test with frontend

### Short term (Polish)
- Write tests for API endpoints
- Improve error handling
- Add form validation
- Optimize performance

### Long term (Deploy)
- Set up production database (PostgreSQL recommended)
- Deploy Django backend (Heroku, Railway, AWS, etc.)
- Build frontend: `npm run build` → deploy `dist/` to Vercel, Netlify, or serve from Django
- Configure CORS for production domain
- Set up CI/CD pipeline

---

## Common Issues & Solutions

### "Cannot connect to API"
**Cause:** Django backend not running  
**Fix:** Start Django: `cd fairplay/fairplay && python manage.py runserver 8000`

### "404 on /api/players"
**Cause:** API endpoints not implemented yet  
**Fix:** Follow [FRONTEND_MIGRATION.md](./FRONTEND_MIGRATION.md) to create REST views

### "CSRF token errors"
**Cause:** Frontend-backend mismatch in CSRF handling  
**Fix:** Ensure CORS and CSRF middleware are configured correctly (see migration guide)

### "Login doesn't work"
**Cause:** Auth API endpoint returns wrong format  
**Fix:** Check serializer returns `{id, username, email}` not full User object

---

## Docs & Resources

- **Frontend README:** `frontend/README.md`
- **Migration Guide:** `FRONTEND_MIGRATION.md`
- **Setup Details:** `FRONTEND_SETUP_COMPLETE.md`
- **Django REST Framework:** https://www.django-rest-framework.org/
- **React Docs:** https://react.dev/
- **Vite Docs:** https://vite.dev/

---

## Project Stats

**Frontend Implementation:**
- 10 page components (login, register, players, teams, matches, history, etc.)
- 5 API client modules (auth, players, teams, matches, history)
- 1 auth context for state management
- Type-safe throughout with TypeScript
- 600+ lines of React components
- Dark theme responsive CSS

**Architecture:**
- Fully decoupled frontend & backend
- REST API communication
- Session-based auth with CSRF protection
- Type definitions matching Django models

---

## Questions?

The codebase is heavily commented. Check:
- `frontend/src/App.tsx` - Router setup
- `frontend/src/api/client.ts` - HTTP client implementation
- `frontend/src/context/AuthContext.tsx` - Auth state management
- Any page component for UI patterns

Let me know if you need clarification on any part! 🚀
