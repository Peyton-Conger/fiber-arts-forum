# Fiber Arts Forum — Hobbyist Community

A lightweight Flask-based forum for fiber arts enthusiasts: spinning, knitting, crochet, weaving, and felting.

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
