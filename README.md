# 🎼 ScoreMorphAI

An AI-powered music arrangement system that transforms audio files into orchestral sheet music using deep learning.

---

## Overview

ScoreMorphAI takes an audio file (MP3/WAV), separates its stems, analyzes melody and harmony, and generates a full orchestral arrangement exported as PDF sheet music — powered by a custom Transformer model.

---

## Architecture

```
ScoreMorphAI/
├── frontend/               # React app (port 3000)
├── backend/
│   ├── core_service/       # FastAPI — auth, users, arrangements (port 8000)
│   └── ai_service/         # Flask — audio processing & AI inference (port 5000)
└── data/
    ├── ai_data/            # Temp files: uploads, separated stems, MIDI, scores
    └── app_data/           # DB migrations, user uploads
```

### Backend Layers (core_service)

```
Router → Controller → Service → Repository → Database
```

| Layer | Responsibility |
|---|---|
| Router | HTTP routing, request parsing |
| Controller | Orchestrates flow, returns responses |
| Service | Business logic (auth, JWT, bcrypt) |
| Repository | DB queries via SQLAlchemy |

### AI Pipeline (ai_service)

```
Audio Upload
    → Source Separation (Demucs)
    → Melody Extraction (Chroma CQT + Basic Pitch)
    → Accompaniment Extraction (Basic Pitch)
    → Tempo Detection (Autocorrelation)
    → Model Input Builder (one-hot encoding + normalization)
    → Orchestra Transformer (custom Transformer model)
    → MIDI Builder (MusicXML export)
    → PDF Generator (MuseScore)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Tailwind CSS, react-hook-form, react-router-dom |
| Core Backend | FastAPI, SQLAlchemy 2.x, MySQL, JWT, bcrypt |
| AI Backend | Flask, PyTorch, Demucs, Basic Pitch, librosa, music21 |
| Auth | JWT (python-jose), bcrypt (passlib) |
| DB | MySQL (`scoreMorphAI` database) |

---

## Prerequisites

- Python 3.11 (AI service) + Python 3.13 (core service)
- Node.js 18+
- MySQL Server
- MuseScore 4 (for PDF export)

---

## Setup & Installation

### 1. Database

Create the MySQL database manually:

```sql
CREATE DATABASE scoreMorphAI;
```

### 2. Core Service (FastAPI)

```bash
cd backend/core_service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in `core_service/`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=scoreMorphAI
DB_USER=root
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Run:

```bash
uvicorn main:app --reload --port 8000
```

### 3. AI Service (Flask)

```bash
cd backend/ai_service
python -m venv .venv311
.venv311\Scripts\activate
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

### 4. Frontend (React)

```bash
cd frontend
npm install
npm start
```

`.env` in `frontend/`:

```env
REACT_APP_CORE_API_URL=http://127.0.0.1:8000
REACT_APP_AI_API_URL=http://127.0.0.1:5000
```

---

## API Reference

### Core Service (port 8000)

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | Login, returns JWT | ❌ |
| GET | `/auth/me` | Validate token, get user | ✅ |
| GET | `/arrangements` | List user's arrangements | ✅ |
| POST | `/arrangements` | Create new arrangement | ✅ |

### AI Service (port 5000)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/upload/audio` | Upload audio, start processing |
| GET | `/api/score/<id>` | Get arrangement status/result |
| GET | `/api/export/<id>` | Download PDF score |

---

## Key Files

```
core_service/
├── main.py                         # App entry point, sys.path setup
├── database.py                     # SQLAlchemy engine + get_db
├── config.py                       # Pydantic Settings from .env
├── models/
│   ├── user_model.py               # User ORM model
│   └── arrangement_model.py        # Arrangement ORM model
├── schemas/
│   ├── user_schema.py              # Pydantic request/response schemas
│   └── arrangement_schema.py
├── routers/
│   ├── auth.py                     # Auth routes
│   └── arrangements.py             # Arrangement routes
├── controllers/
│   ├── auth_controller.py
│   └── arrangement_controller.py
├── services/
│   ├── auth_service.py             # JWT + bcrypt logic
│   └── arrangement_service.py
├── repositories/
│   ├── user_repository.py          # DB queries for users
│   └── arrangement_repository.py
└── middleware/
    ├── request_id_middleware.py    # Adds X-Request-ID header
    ├── logging_middleware.py       # Logs all requests
    └── rate_limit_middleware.py    # Per-IP rate limiting

ai_service/
├── app.py                          # Flask entry point
├── services/
│   ├── music_processing_service.py # Full 7-step pipeline
│   ├── source_separator.py         # Demucs stem separation
│   ├── melody_extractor.py         # Chroma CQT + key detection
│   ├── accompaniment_extractor.py  # Basic Pitch harmony/bass
│   ├── tempo_detector.py           # BPM via autocorrelation
│   ├── model_input_builder.py      # Tensor preparation
│   ├── model_runner.py             # Singleton model loader + inference
│   ├── orchestra_transformer.py    # Custom Transformer architecture
│   ├── model_output_parser.py      # Decode model output to notes
│   ├── midi_builder.py             # Build MusicXML from notes
│   └── pdf_generator.py            # MuseScore PDF export
└── models/
    └── orchestra_transformer_model.pth  # Trained model weights
```

---

## Authentication Flow

1. User registers/logs in → receives JWT
2. Token stored in `localStorage`
3. Every request attaches `Authorization: Bearer <token>` via axios interceptor
4. On app load, `GET /auth/me` validates token server-side
5. `ProtectedRoute` blocks access and redirects to `/login` if token is invalid
6. Logout clears token and navigates with `replace: true` (blocks back-navigation)

---

## Notes

- `core_service` uses flat `sys.path` injection in `main.py` — no relative imports
- Models named `user_model.py` / `arrangement_model.py` to avoid Python name collisions with schemas
- SQLAlchemy `>=2.0.36` required for Python 3.13 compatibility
- AI service requires Python 3.11 due to Demucs/torch compatibility
- MySQL database name `scoreMorphAI` is case-sensitive — must match exactly
