# FairPlay – A Football Team Generator Web App

## 🎯 Project Overview
FairPlay is a Django-based web application that solves the common problem of creating balanced teams for casual football matches. Instead of dealing with arguments and unfair team selections, FairPlay automatically generates balanced teams based on player skill levels and positions.

## 🚀 What I'm Building
A web application that allows users to:
- Register players with their name, position, and skill rating (1-5)
- Automatically generate balanced teams based on skill distribution
- View team compositions with fair position assignments
- Manage players and create multiple match sessions

## 📊 Current Progress

### ✅ Completed Features
1. **Project Setup**
   - Django project structure initialized
   - Database models created (Player, Team, Match)
   - Initial migrations completed

2. **Player Management System**
   - Player model with fields: name, position (Striker/Defender/Midfielder/Goalkeeper), rating (1-5)
   - Player creation form with Django ModelForm
   - Add player functionality with form validation
   - Player list view to display all registered players
   - Bootstrap-styled UI for player forms

3. **User Interface**
   - Clean, centered landing page with "Continue" button
   - Responsive design using Bootstrap 5
   - Player addition page with form styling
   - Player list page with table display

### 🔨 Currently Working On
- Team generation algorithm
- Match session management
- Balancing logic based on ratings and positions

3. Main Features
1. Player Management
Add player details (name, skill level, preferred position)


Mark players as available/unavailable for a match


View all registered players


2. Match Session Setup
Create a new match session


Select players participating in the match


Define number of players per team


3. Team Generation
Automatically generate balanced teams based on:


Skill level distribution


Position distribution (Goalkeeper, Defender, Midfielder, Striker)


Randomization logic for fairness


Option to reshuffle teams


4. Team View Page
Display Team A vs Team B


Show positions and assigned players for each team



4. API Use (Optional)
This project does not require an external API to function.
5. Django Project Structure
Django Apps

A. players App
Handles everything related to player data.
Models:
Player


name – CharField


position – ChoiceField (GK, DEF, MID, ST)


skill_level – IntegerField (1–5)


is_available – BooleanField


Core Endpoints:
/players/ – List all players


/players/add/ – Add a player


/players/<id>/edit/ – Edit player details



B. matches App
Handles match creation and team generation.
Models:
Match


date_created


Team


match – ForeignKey


name – CharField


TeamPlayer


team – ForeignKey


player – ForeignKey


position_assigned – CharField


Core Endpoints:
/matches/create/ – Create a match


/matches/<id>/generate-teams/ – Generate balanced teams


/matches/<id>/teams/ – View teams



6. Database Schema Overview
Player Table
Field
Type
Description
id
PK
Auto-generated
name
varchar
Player name
position
choice
Preferred playing role(1-11)






is_available
boolean
Availability

Match Table
Field
Type
id
PK
date_created
datetime

Team Table
Field
Type
id
PK
match_id
FK to Match
name
varchar

TeamPlayer Table
Field
Type
id
PK
team_id
FK to Team
player_id
FK to Player
position_assigned
varchar


## 🔮 Future Developments

### Phase 1: Core Team Generation (Next Steps)
- [ ] Implement team balancing algorithm
- [ ] Create match session management
- [ ] Build team display page
- [ ] Add ability to shuffle/regenerate teams

### Phase 2: Enhanced Features
- [ ] Player availability tracking
- [ ] Match history tracking
- [ ] Edit/delete player functionality
- [ ] Team statistics (average rating per team)
- [ ] Export teams to PDF or share via link

### Phase 3: Advanced Features
- [ ] User authentication system
- [ ] Save multiple match configurations
- [ ] Player performance tracking
- [ ] Email notifications for match assignments
- [ ] Mobile-responsive optimization
- [ ] Dark mode toggle

## 🛠️ Tech Stack
- **Backend**: Django 4.2
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite (development)
- **Python Version**: 3.x

## 📁 Project Structure
```
fairplay/
├── fair_play/              # Main app
│   ├── models.py          # Player, Team, Match models
│   ├── forms.py           # PlayerCreationForm
│   ├── views.py           # CreatePlayerView, PlayerListView
│   ├── urls.py            # App URL configurations
│   └── templates/         # HTML templates
│       ├── index.html     # Landing page
│       ├── playeradd.html # Add player form
│       └── playerslist.html # List all players
├── fairplay/              # Project settings
│   ├── settings.py
│   └── urls.py
└── manage.py
```

## 🚦 Getting Started
1. Clone the repository
2. Install dependencies: `pip install django`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`
5. Visit: `http://127.0.0.1:8000/`

## 👨‍💻 Development Status
**Current Phase**: Player Management Complete ✅  
**Next Milestone**: Team Generation Algorithm 🎯  
**Estimated Completion**: Week 3



