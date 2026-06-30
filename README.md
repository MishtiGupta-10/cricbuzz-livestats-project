# CricInsight

CricInsight is a cricket analytics platform evolving from the original Cricbuzz LiveStats Streamlit prototype. The project is being refactored incrementally into a clean, interview-ready architecture with Streamlit, FastAPI, a service layer, Cricbuzz API integration, and MySQL.

## Current Phase

Phase 1: project foundation and architecture setup.

## Architecture

```text
Streamlit UI
   |
   v
FastAPI Routes
   |
   v
Services
   |
   +--> MySQL Repository
   |
   +--> Cricbuzz Client
          |
          v
       Parsers
```

During Phase 1, existing Streamlit pages are preserved so the original live match, match details, and scorecard flows keep working. FastAPI foundation, configuration, logging, and project structure are added beside the existing app.

## Project Structure

```text
backend/              FastAPI backend package
backend/api/routes/   HTTP route modules
backend/core/         Configuration, logging, and cache utilities
backend/services/     Business logic layer
database/             Simple SQL and query boundary
pages/                Existing Streamlit pages
utils/                Existing utility modules retained during incremental refactor
tests/                Test package placeholder
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your RapidAPI key.

## Run Streamlit

```bash
streamlit run Home.py
```

## Run FastAPI

```bash
uvicorn backend.main:app --reload
```

Health check:

```text
GET /api/v1/health
```

## Phase 1 Scope

- Preserve existing Streamlit functionality.
- Add FastAPI application foundation.
- Add centralized environment configuration.
- Add logging setup.
- Add lightweight in-memory TTL cache utility for development.
- Keep database versioning simple with `schema.sql`, `seed.sql`, and `queries.py`.
