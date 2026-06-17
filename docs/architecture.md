# Architecture

## System Overview

ScoreMorph-AI היא מערכת המרת אודיו לנוטות מוזיקליות.

### Components

```
Frontend (React)
    ↓
Backend (Flask)
    ├── API Routes
    ├── Services
    ├── Models
    └── Utils
    ↓
Data Layer
    ├── uploads/
    ├── separated/
    ├── midi/
    ├── scores/
    └── temp/
```

### Data Flow

1. **Upload** → User uploads audio file
2. **Analysis** → Backend analyzes the audio
3. **Separation** → Source separation (vocals/instruments)
4. **Transcription** → Convert to notes
5. **MIDI Processing** → Create MIDI representation
6. **Score Generation** → Generate musical score
7. **Export** → Download in various formats (PDF, MusicXML, MIDI, PNG)

### Architecture Layers

#### Frontend
- React components
- User interface for uploading and viewing scores
- Service layer for API communication

#### Backend
- Flask web server
- REST API endpoints
- Business logic services
- Data models

#### Data Storage
- File system for audio files
- Output directory for generated files
- Temporary directory for intermediate files

## API Architecture

### RESTful Endpoints

- `POST /api/upload/audio` - Upload audio file
- `POST /api/score/generate` - Generate score from audio
- `GET /api/score/list` - List all scores
- `GET /api/export/score/<id>` - Export score
- `GET /api/export/score/<id>/formats` - Get available formats
