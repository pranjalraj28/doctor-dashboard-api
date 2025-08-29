# Healthcare API

This is a FastAPI-based backend for a healthcare application. It provides functionalities for doctor registration, authentication, and profile management.

## Features

- Doctor registration and authentication
- JWT-based access and refresh tokens
- Password hashing
- Database migrations with Alembic
- Centralized configuration managem1ent

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (with SQLAlchemy and asyncpg)
- **Migrations:** Alembic
- **Authentication:** JWT (pyjwt), passlib
- **Configuration:** pydantic-settings
- **Testing:** pytest, pytest-asyncio

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Healthcare
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the project root by copying the example:
    ```bash
    cp .env.example .env
    ```

2.  Update the `.env` file with your configuration. You'll need to provide values for the following variables:

    ```env
    # Application settings
    APP_NAME="Healthcare API"
    APP_VERSION="0.1.0"
    DEBUG=True
    API_V1_STR="/api/v1"

    # Database
    DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname"

    # JWT settings
    SECRET_KEY="your-super-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_DAYS=7
    ALGORITHM="HS256"
    JWT_SECRET_KEY="your-jwt-secret-key"
    JWT_REFRESH_SECRET_KEY="your-jwt-refresh-secret-key"
    ```

### Database Migration

Run the following command to apply database migrations:

```bash
alembic upgrade head
```

## Running the Application

To start the development server, run:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

The following endpoints are available under the `/api/v1` prefix:

-   **`POST /auth/register`**: Register a new doctor.
-   **`POST /auth/login`**: Log in and receive access/refresh tokens.
-   **`POST /auth/refresh`**: Refresh an access token.
-   **`GET /auth/profile`**: Get the profile of the currently authenticated doctor.
-   **`GET /health`**: Health check endpoint.

## Project Structure

```
Healthcare/
├── app/                # Main application folder
│   ├── api/            # API endpoint definitions
│   ├── core/           # Core components (config, dependencies)
│   ├── db/             # Database connection and session management
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   └── services/       # Business logic
├── alembic/            # Alembic migration scripts
├── .env                # Environment variables
├── alembic.ini         # Alembic configuration
├── main.py             # Application entry point
├── requirements.txt    # Project dependencies
└── README.md           # This file
```
