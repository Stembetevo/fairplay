# FairPlay ⚽ – Multi-User Intelligent Football Team Generator

## 🎯 Project Overview
FairPlay is a full-stack Django web application that enables users to build and manage balanced football teams with their friends. Each user can register, create their own player roster by adding registered users, and generate fair teams using a sophisticated **Snake Draft Algorithm**. With user authentication and data isolation, every user has their own personalized team management experience.

## 🚀 Features

### ✅ Completed Features

#### 1. **User Authentication System** 🔐
- User registration with username, email, password, and preferred position
- Secure login/logout functionality
- User profile creation with preferred playing position
- Password validation and email uniqueness checks
- Session management and authentication state tracking
- Login-required protection for player/team management

#### 2. **Multi-User Player Management** 👥
- Search and add registered users as players to your roster
- Each user manages their own private player list
- View player's username, position, and skill rating
- Override user's preferred position when adding them
- Edit player ratings and positions (only your own players)
- Delete players from your roster
- Data isolation - users only see their own players

#### 3. **User Profile System**
- Automatic profile creation on registration
- Preferred position selection (Striker/Defender/Midfielder/Goalkeeper)
- Profile linked to user account via signal
- Default position used when adding user as player

#### 4. **Player Management System**
- Add players by searching registered usernames
- View all your players in an organized table
- Edit player details (position, rating) - only your own
- Delete players from your roster
- Skill rating system (50-100 scale)
- Bootstrap-styled responsive UI with dark theme

#### 2. **Intelligent Team Generation**
- **Snake Draft Algorithm** for balanced team distribution
- Players sorted by rating (highest to lowest) before distribution
- Alternating pick order ensures fair team composition
- Support for 2-10 teams per user
- Automatic team rating calculations
- **User-specific teams** - only uses your players
- Teams owned by individual users (private)

#### 3. **Team Display & Analytics**
- Beautiful card-based team display with dark theme
- Individual player cards showing position and rating
- Team statistics: total rating and average rating per team
- Balance summary table comparing all teams
- Responsive design for all screen sizes

#### 4. **User Interface**
- Modern landing page with authentication options
- User-aware navigation (login status displayed)
- Welcome messages with username
- Intuitive navigation throughout the app
- Success/error message notifications
- Dark theme with consistent styling
- Mobile-responsive Bootstrap 5 design
- Separate login and registration pages

#### 5. **Security & Data Isolation** 🔒
- Login required for all player/team operations
- Users can only view/edit/delete their own data
- Reset function only deletes current user's players
- Team generation uses only user's own players
- Ownership validation on all CRUD operations
- Protection against unauthorized access

#### 6. **Django Admin Integration**
- Custom admin panels for Player, Team, Match, and UserProfile models
- Enhanced admin views with user filtering
- Easy data management for testing and debugging

## 👤 User Workflow

### New User Journey
1. **Register**: Create account with username, email, password, and preferred position
2. **Login**: Access your personal dashboard
3. **Add Players**: Search for other registered users and add them to your roster
4. **Set Ratings**: Assign skill ratings (50-100) to each player
5. **Generate Teams**: Create balanced teams from your player roster
6. **View Teams**: See team compositions with statistics
7. **Manage**: Edit ratings, remove players, or reset your roster

### Key Concepts
- **User**: Registered account holder who manages their own players/teams
- **Player**: A registered user added to someone's roster with a rating
- **Owner**: The user who added a player to their roster
- **Preferred Position**: Default position set during registration
- **Position Override**: Ability to assign different position when adding player

## 🧮 Snake Draft Algorithm

The heart of FairPlay is its intelligent team balancing algorithm:

1. **Sort Players**: All players are sorted by rating (descending) and then by position
2. **Snake Pattern Distribution**: Players are distributed in a snake/zigzag pattern:
   - Round 1: Team A → Team B → Team C (forward)
   - Round 2: Team C → Team B → Team A (backward)
   - Round 3: Team A → Team B → Team C (forward)
   - And so on...
3. **Result**: Ensures the highest-rated players are evenly distributed across teams

### Example:
If you have 9 players with ratings [5, 5, 4, 4, 3, 3, 2, 2, 1] for 3 teams:
- **Team A**: Players rated [5, 4, 2] = Total: 11
- **Team B**: Players rated [5, 3, 2] = Total: 10  
- **Team C**: Players rated [4, 3, 1] = Total: 8

This creates much more balanced teams than random assignment!

## 🛠️ Tech Stack
- **Backend**: Django 4.2.11
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3, JavaScript
- **Database**: SQLite (development)
- **Python Version**: 3.9+
- **CI/CD**: GitHub Actions


## 📁 Project Structure
```
fairplay/
├── .github/
│   └── workflows/
│       └── django.yml         # CI/CD pipeline
├── fairplay/                   # Django project root
│   ├── fair_play/              # Main app
│   │   ├── models.py          # Player, Team, Match, UserProfile models
│   │   ├── forms.py           # PlayerSearchForm, CustomUserCreationForm, TeamForm
│   │   ├── views.py           # All views including auth and team generation
│   │   ├── urls.py            # App URL configurations
│   │   ├── admin.py           # Custom admin configurations
│   │   ├── migrations/        # Database migrations
│   │   └── templates/         # HTML templates
│   │       ├── index.html              # Landing page
│   │       ├── navbar.html             # Reusable navbar component
│   │       ├── registration/           # Authentication templates
│   │       │   ├── register.html       # User registration
│   │       │   └── login.html          # User login
│   │       ├── playeradd.html          # Add player by username
│   │       ├── playerslist.html        # List user's players
│   │       ├── playerupdate.html       # Edit player
│   │       ├── playerdelete.html       # Delete confirmation
│   │       ├── reset_confirm.html      # Reset confirmation
│   │       ├── team_form.html          # Team generation form
│   │       └── teams_display.html      # Display generated teams
│   ├── fairplay/              # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── db.sqlite3
├── requirements.txt           # Python dependencies
└── README.md
```

## 📊 Database Models

### User Model (Django's built-in)
- `username`: Unique username
- `email`: User's email address
- `password`: Hashed password

### UserProfile Model
- `user`: OneToOneField to User
- `preferred_position`: CharField - Default playing position
- `bio`: TextField - Optional user biography

### Player Model
- `user`: ForeignKey to User - The registered user being added as player
- `owner`: ForeignKey to User - The user who added this player
- `position`: CharField with choices (Striker, Defender, Midfielder, Goalkeeper)
- `rating`: IntegerField (50-100) - Skill level assigned by owner
- `team`: ForeignKey to Team (nullable) - Assigned during team generation

### Team Model
- `name`: CharField - Team name
- `created_at`: DateTimeField - Auto-generated timestamp
- `owner`: ForeignKey to User - User who created the team

### Match Model
- `date_created`: DateTimeField - Match creation time
- `team_A`: ForeignKey to Team
- `team_B`: ForeignKey to Team

## 🌐 URL Endpoints

| URL | View | Description | Auth Required |
|-----|------|-------------|---------------|
| `/` | index | Landing page (redirects to players if authenticated) | No |
| `/register/` | register_view | User registration | No |
| `/login/` | login_view | User login | No |
| `/logout/` | logout_view | User logout | Yes |
| `/player/add/` | add_player_view | Add player by username search | Yes |
| `/players/` | PlayerListView | View your players (filtered by owner) | Yes |
| `/player/<id>/update/` | UpdatePlayerView | Edit player details (position, rating) | Yes |
| `/player/<id>/delete/` | DeletePlayerView | Delete player from your roster | Yes |
| `/reset/` | reset_players | Reset your players only | Yes |
| `/teams/generate/` | team_form_view | Team generation form | Yes |
| `/teams/create/` | generate_teams_view | Process team generation | Yes |
| `/teams/` | teams_display_view | Display your generated teams | Yes |
| `/admin/` | Django Admin | Admin panel | Superuser |


## 🚦 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Stembetevo/fairplay.git
   cd fairplay
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Navigate to project directory**
   ```bash
   cd fairplay
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   - Main app: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 🎮 Usage Guide

### First Time Setup
1. **Register Account**: 
   - Navigate to the homepage
   - Click "Create Account" or "Register"
   - Fill in username, email, password, and preferred position
   - Click "Create Account"

2. **Add Friends as Players**:
   - Ask friends to register on the platform
   - Once logged in, go to "Add Player"
   - Search for friend's username
   - Optionally override their preferred position
   - Set their skill rating (50-100)
   - Click "Add Player"

3. **Build Your Roster**:
   - Continue adding registered users as players
   - View all your players in "My Players"
   - Edit ratings or positions as needed

4. **Generate Teams**: 
   - Once you have at least 2 players, click "Generate Teams"
   - Enter number of teams (2-10)
   - Provide team names
   - Click "Generate Teams"

5. **View Results**: 
   - See balanced teams with statistics
   - View player assignments and team ratings
   - Generate new teams anytime with different configurations

### Managing Your Data
- **Edit Players**: Click "Edit" on any player in your list to update rating/position
- **Remove Players**: Click "Remove" to delete a player from your roster
- **Reset**: Use "Reset All" to clear all your players and start fresh
- **Logout**: Click "Logout" in the navbar when done

## 🔮 Future Enhancements

### Planned Features
- [ ] Public player profiles with statistics
- [ ] Friend system and invitations
- [ ] Team sharing between users
- [ ] Match history and statistics tracking
- [ ] Export teams to PDF
- [ ] Share team compositions via link
- [ ] Player performance tracking over time
- [ ] Advanced filtering (by position, rating, availability)
- [ ] Team comparison analytics across users
- [ ] Match scheduling system
- [ ] Email notifications for team assignments
- [ ] Player availability toggle for each match
- [ ] Social features (comments, likes on teams)
- [ ] Leaderboards and rankings
- [ ] Mobile app version

## 🧪 Testing

Run tests with:
```bash
cd fairplay
python manage.py test
```

CI/CD pipeline runs automatically on push to main branch via GitHub Actions.

## 👨‍💻 Development Status
**Current Phase**: Multi-User System Complete ✅  
**Status**: Production Ready 🚀  
**Version**: 2.0.0

### Recent Updates (v2.0.0)
- ✅ Complete user authentication system
- ✅ User registration with preferred position
- ✅ Multi-user support with data isolation
- ✅ Username-based player search
- ✅ User profile system
- ✅ Ownership-based access control
- ✅ Updated UI with authentication state
- ✅ Secure login/logout functionality

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
This project is open source and available for educational purposes.

## 👤 Author
**Stephen Kinyua**
- GitHub: [@Stembetevo](https://github.com/Stembetevo)

---

⚽ Built with Django | Balanced with Logic | Powered by Fair Play | Secured for Users

