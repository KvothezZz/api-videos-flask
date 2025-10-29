# Flask Video Processing API

## Overview
A Python Flask API with MoviePy integration for video processing. Created on October 29, 2025.

## Purpose
Provides a simple REST API for video processing operations using the MoviePy library.

## Architecture

### Stack
- Python 3.11
- Flask web framework
- MoviePy for video processing
- Werkzeug for secure file handling

### Project Structure
```
.
├── main.py           # Flask application with API endpoints
├── requirements.txt  # Python dependencies
└── .gitignore       # Python-specific ignore patterns
```

### Endpoints
- `GET /health` - Health check endpoint returning API status
- `POST /render` - Video processing endpoint that accepts video file uploads

### Features
- Video file upload with validation (mp4, avi, mov, mkv, flv, wmv)
- MoviePy integration for video processing
- Temporary file handling for safe processing
- Error handling with descriptive JSON responses
- Demo processing: extracts first 5 seconds of uploaded video

## Recent Changes
- **2025-10-29**: Initial project setup with Flask and MoviePy
  - Created health check endpoint
  - Implemented video render endpoint with file upload
  - Added video format validation
  - Configured for deployment on port 5000

## Dependencies
- Flask 3.0.0
- moviepy 1.0.3
- Werkzeug 3.0.1

## User Preferences
None specified yet.
