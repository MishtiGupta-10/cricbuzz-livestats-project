# API Design

## Overview
The API layer acts as a gateway to the Cricbuzz RapidAPI. It ensures that the application only ever interacts with strictly-typed domain models rather than raw JSON data.

## Components

### Cricbuzz Client
- **File**: `backend/clients/cricbuzz.py`
- **Class**: `CricbuzzClient`
- **Description**: Handles all HTTP communication with the Cricbuzz RapidAPI.
- **Responsibilities**:
  - Request construction and header management (`_build_headers`).
  - Network retries and timeouts via `urllib3.util.retry.Retry` and `requests.adapters.HTTPAdapter`.
  - HTTP error validation (`_validate_response`).
  - Delegates response payloads to the parser layer.
  - Implements lightweight `@ttl_cache` to reduce API calls.

### Parsers
- **Files**: `backend/parsers/common.py`, `backend/parsers/live_matches.py`, `backend/parsers/match_info.py`
- **Description**: Responsible for mapping raw, unstructured JSON dictionaries into validated Pydantic models.
- **Responsibilities**:
  - Safely extracts nested fields using `.get()` to avoid `KeyError`.
  - Raises `CricbuzzParseError` if critical parsing fails.
  - Modularized by domain concept.

### Domain Models (Schemas)
- **File**: `backend/schemas/cricbuzz.py`
- **Description**: Pydantic models acting as the internal source of truth for the application's data structures.
- **Models**:
  - `Team`
  - `Venue`
  - `Player`
  - `LiveMatch`
  - `MatchInfo`
- **Note**: Scorecard domain models are deferred until subsequent phases.

### Error Handling
- **File**: `backend/core/exceptions.py`
- **Description**: Standardizes errors thrown by the client and parsers.
- **Exceptions**:
  - `CricInsightError`: Base error.
  - `CricbuzzClientError`: Network and connection issues.
  - `CricbuzzAPIError`: Non-2xx HTTP responses from Cricbuzz.
  - `CricbuzzParseError`: Issues encountered while parsing JSON into models.
