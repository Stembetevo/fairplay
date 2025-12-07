Capstone Project – Part 1: Project Idea & Planning Document
1. Project Title
FairPlay – A Football Team Generator Web App

2. Project Idea
When organizing casual football matches with friends, team selection is usually stressful. Often, one team ends up too strong, or many players share the same position, leading to unbalanced teams and a less enjoyable game.
FairPlay solves this by allowing players to register their details (name, skill level, preferred position, availability), and then automatically generating balanced teams based on defined criteria.
This ensures fair play, reduced arguments, and a smoother match setup experience.

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


7. Project Development Timeline
Week 1: Planning & Setup
Finalize idea and features


Create Django project


Build players app


Implement player model and CRUD views


Week 2: Match & Team Logic
Create matches app


Implement match and team models


Build team generation algorithm


Create endpoints for generating and displaying teams


Week 3: UI, Testing, Documentation
Build simple templates/UI pages


Add optional features (match history, reshuffle)


Test all endpoints


Write final documentation


Prepare for presentation/demo



