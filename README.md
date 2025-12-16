# FairPlay ⚽ – Intelligent Football Team Generator

## 🎯 Project Overview
FairPlay is a Django-based web application that solves the common problem of creating balanced teams for casual football matches. Using a sophisticated **Snake Draft Algorithm**, FairPlay automatically generates fair teams based on player skill levels and positions, ensuring competitive and enjoyable matches every time.

## 🚀 Features

### ✅ Completed Features

#### 1. **Player Management System**
- Add players with name, position (Striker/Defender/Midfielder/Goalkeeper), and skill rating (1-5)
- View all registered players in an organized table
- Edit player details (name, position, rating)
- Delete players from the system
- Bootstrap-styled responsive UI

#### 2. **Intelligent Team Generation**
- **Snake Draft Algorithm** for balanced team distribution
- Players sorted by rating (highest to lowest) before distribution
- Alternating pick order ensures fair team composition
- Support for 2-10 teams
- Automatic team rating calculations

#### 3. **Team Display & Analytics**
- Beautiful card-based team display with dark theme
- Individual player cards showing position and rating
- Team statistics: total rating and average rating per team
- Balance summary table comparing all teams
- Responsive design for all screen sizes

#### 4. **User Interface**
- Clean, modern landing page
- Intuitive navigation throughout the app
- Success/error message notifications
- Dark theme with white cards for team display
- Mobile-responsive Bootstrap 5 design

#### 5. **Reset Functionality**
- Reset all players and start fresh
- Confirmation page to prevent accidental deletions

#### 6. **Django Admin Integration**
- Custom admin panels for Player, Team, and Match models
- Enhanced admin views with player counts and team ratings
- Easy data management for testing and debugging

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
│   │   ├── models.py          # Player, Team, Match models
│   │   ├── forms.py           # PlayerCreationForm, TeamForm
│   │   ├── views.py           # All views including team generation
│   │   ├── urls.py            # App URL configurations
│   │   ├── admin.py           # Custom admin configurations
│   │   ├── migrations/        # Database migrations
│   │   └── templates/         # HTML templates
│   │       ├── index.html              # Landing page
│   │       ├── playeradd.html          # Add player form
│   │       ├── playerslist.html        # List all players
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

### Player Model
- `name`: CharField - Player's name
- `position`: CharField with choices (Striker, Defender, Midfielder, Goalkeeper)
- `rating`: IntegerField (1-5) - Skill level
- `team`: ForeignKey to Team (nullable)

### Team Model
- `name`: CharField - Team name
- `created_at`: DateTimeField - Auto-generated timestamp

### Match Model
- `date_created`: DateTimeField - Match creation time
- `team_A`: ForeignKey to Team
- `team_B`: ForeignKey to Team

## 🌐 URL Endpoints

| URL | View | Description |
|-----|------|-------------|
| `/` | index | Landing page |
| `/player/add/` | CreatePlayerView | Add new player |
| `/players/` | PlayerListView | View all players |
| `/player/<id>/update/` | UpdatePlayerView | Edit player details |
| `/player/<id>/delete/` | DeletePlayerView | Delete player |
| `/reset/` | reset_players | Reset all players |
| `/teams/generate/` | team_form_view | Team generation form |
| `/teams/create/` | generate_teams_view | Process team generation |
| `/teams/` | teams_display_view | Display generated teams |
| `/admin/` | Django Admin | Admin panel |


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

1. **Add Players**: Click "Continue" → "Add Player" and enter player details
2. **View Players**: Navigate to "All Players" to see your roster
3. **Generate Teams**: 
   - Click "Generate Teams" from the players list
   - Enter number of teams (2-10)
   - Provide team names
   - Click "Generate Teams"
4. **View Results**: See balanced teams with statistics and player assignments

## 🔮 Future Enhancements

### Planned Features
- [ ] Player availability toggle for each match
- [ ] Match history and statistics tracking
- [ ] Export teams to PDF
- [ ] Share team compositions via link
- [ ] User authentication and multi-user support
- [ ] Player performance tracking over time
- [ ] Advanced filtering (by position, rating)
- [ ] Team comparison analytics
- [ ] Match scheduling system
- [ ] Email notifications for team assignments

## 🧪 Testing

Run tests with:
```bash
cd fairplay
python manage.py test
```

CI/CD pipeline runs automatically on push to main branch via GitHub Actions.

## 👨‍💻 Development Status
**Current Phase**: Core Features Complete ✅  
**Status**: Production Ready 🚀  
**Version**: 1.0.0

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
This project is open source and available for educational purposes.

## 👤 Author
**Stephen Kinyua**
- GitHub: [@Stembetevo](https://github.com/Stembetevo)

---

⚽ Built with Django | Balanced with Logic | Powered by Fair Play



