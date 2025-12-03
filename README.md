# Fiber Arts Forum — Hobbyist Community

A lightweight Flask-based forum for fiber arts enthusiasts: spinning, knitting, crochet, weaving, and felting.

## User Stories 
User Story 1 — Account Creation

- As a new user, I want to create an account so that I can participate in fiber-arts discussions.

User Story 2 — Starting a Discussion

- As a spinner, knitter, or crocheter, I want to create new discussion threads so that I can ask questions or share projects with the community.

User Story 3 — Posting Replies

- As a community member, I want to reply to threads so that I can contribute to discussions.

User Story 4 — Editing & Deleting Content

- As a content creator, I want to edit or delete my own threads and posts so that I can correct mistakes or remove outdated information.

User Story 5 — Searching for Topics

- As a user, I want to search for threads by title or craft category so that I can quickly find discussions relevant to my interests.

User Story 6 — User Profiles

- As a returning user, I want to customize my profile with an avatar and basic details so that others can recognize me in the forum.

User Story 7 — File Attachments (Optional Enhancement)

- As a fiber artist, I want to attach images or documents to my posts so that I can share patterns, yarn samples, or project photos.

## Features
- User registration and login
- Create discussion threads and posts (topics & replies)
- Basic tagging (craft types)
- Simple HTML/CSS frontend (Bootstrap)
- Dockerfile and docker-compose for deployment
- Unit (white-box) and functional (black-box) tests
- Scrum templates and UML placeholder

## Quick start (local)
```bash
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=src.wsgi:app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000
```

## Run with Docker Compose
```bash
cp .env.example .env
docker-compose up --build
# app will be at http://localhost:8000
```

## Tests & Coverage
```bash
pytest -q
coverage run -m pytest && coverage html
# open htmlcov/index.html
```



## New features added
- Edit/Delete threads and posts (owner-only)
- User profiles with avatar uploads
- Search by title and filter by craft
- File attachments for posts/threads
- JWT-based API endpoints (/auth/api/*, /api/*)
- PostgreSQL support and Flask-Migrate (Alembic) scaffold
- GitHub Actions CI workflow to run tests and coverage
