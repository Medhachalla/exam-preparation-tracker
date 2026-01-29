# Exam Preparation Tracker

## Project Overview

Exam Preparation Tracker is a full-stack web application for managing exam study plans. Users can create subjects, organize them into units and topics, track completion status, and maintain notes for each unit.

The application provides a structured approach to exam preparation with progress tracking at both the unit and subject levels. The backend is a Flask REST API with PostgreSQL, and the frontend is a React single-page application built with Vite.

## Tech Stack

### Backend
- Python 3.12
- Flask (web framework)
- Flask-CORS (cross-origin resource sharing)
- Flask-JWT-Extended (JWT authentication)
- bcrypt (password hashing)
- PostgreSQL (via psycopg2)
- Python package: `exam_prep_tracker` (src layout)

### Frontend
- React 18
- Vite (build tool and dev server)
- Axios (HTTP client)
- React Router (client-side routing)
- Tailwind CSS (styling)

### Database
- PostgreSQL 15 (runs in Docker)

### Tooling
- **uv**: Python dependency and virtual environment management
- **mise**: Runtime version manager for Python and Node.js

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **mise**: Runtime version manager
- **uv**: Python package and environment manager
- **Docker** and **Docker Compose**: For running PostgreSQL
- **Node.js 18+**: Installed via mise (not manually)

Verify installation:
```bash
mise --version
uv --version
docker --version
docker compose version
```

## Runtime Setup with mise

The project uses mise to manage Python and Node.js versions. This ensures consistent runtimes across different development environments.

From the repository root, run:

```bash
mise install
```

This command reads the project's mise configuration and installs the required versions of Python (3.12) and Node.js (18+). These runtimes are automatically used when running commands within the project directory.

## Backend Setup (uv-based)

The backend uses uv for dependency management and virtual environment creation. All Python operations are performed through uv commands.

### Step 1: Navigate to backend directory

```bash
cd backend
```

### Step 2: Create virtual environment

```bash
uv venv
```

This creates a virtual environment managed by uv. You do not need to activate it manually.

### Step 3: Install backend package and dependencies

```bash
uv pip install -e .
```

This installs the `exam_prep_tracker` package in editable mode along with all dependencies specified in `pyproject.toml`.

**Important notes:**
- Do not use `pip install` directly
- Do not manually activate the virtual environment with `source venv/bin/activate`
- The project does not use `requirements.txt`
- All Python dependencies are managed through `pyproject.toml` and uv

### Step 4: Run the backend server

```bash
uv run python -m exam_prep_tracker.app
```

This starts the Flask development server. The backend will be available at `http://127.0.0.1:5000`.

The `uv run` command automatically uses the virtual environment created by uv, so no manual activation is required.

## Database Setup (PostgreSQL via Docker)

The application uses PostgreSQL exclusively. The database runs in a Docker container for easy setup and consistency.

### Start PostgreSQL

From the `backend/` directory:

```bash
docker compose up -d
```

This starts the PostgreSQL container in detached mode. The database will be initialized with the schema defined in `backend/db/schema.sql`.

### Verify PostgreSQL is running

```bash
docker compose ps
```

You should see the PostgreSQL container with a status of "running".

### View database logs

```bash
docker compose logs -f postgres
```

### Stop PostgreSQL

```bash
docker compose down
```

## Environment Variables

The backend reads configuration from a `.env` file in the `backend/` directory. Create this file if it does not exist.

Required environment variables:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5435/database_name
```

### Variable descriptions

- **FLASK_ENV**: Flask environment mode (`development` or `production`)
- **SECRET_KEY**: Flask secret key for session management
- **JWT_SECRET_KEY**: Secret key for signing JWT tokens (use a strong random string)
- **DATABASE_URL**: PostgreSQL connection string in the format `postgresql://user:password@host:port/database`

**Note**: After modifying `.env`, restart the backend server for changes to take effect.

## Frontend Setup

The frontend is a React application built with Vite.

### Step 1: Navigate to frontend directory

```bash
cd frontend
```

### Step 2: Install dependencies

```bash
npm install
```

### Step 3: Start development server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`. The development server includes hot module replacement for fast development.

## Authentication Overview

The application uses a two-part authentication system:

**Password Hashing**: User passwords are hashed using bcrypt. To handle bcrypt's 72-byte input limitation, passwords are first hashed with SHA-256, then the resulting digest is hashed with bcrypt. This approach allows passwords of any length while maintaining security.

**JWT Authentication**: After successful login, the backend issues a JSON Web Token (JWT) containing the user's ID. The frontend stores this token and includes it in the `Authorization` header for authenticated API requests. Protected backend routes verify the JWT token before processing requests.

## Troubleshooting

### CORS errors often indicate backend issues

If you see CORS errors in the browser console, especially on authentication endpoints, check the backend terminal output. CORS errors frequently mask underlying 500 Internal Server Errors. Fix the backend error first, and the CORS error will typically resolve.

### Backend must be running before frontend

The React frontend expects the Flask backend to be available at `http://127.0.0.1:5000`. Start services in this order:

1. PostgreSQL: `docker compose up -d` (from `backend/`)
2. Backend: `uv run python -m exam_prep_tracker.app` (from `backend/`)
3. Frontend: `npm run dev` (from `frontend/`)

### Do not mix uv with manual virtual environments

Do not create virtual environments using `python -m venv` or `virtualenv`. Always use `uv venv` to create environments. Mixing different environment management tools can cause dependency conflicts and version mismatches.

### Run uv commands from backend directory

All `uv` commands (`uv venv`, `uv pip install -e .`, `uv run`) must be executed from the `backend/` directory. Running these commands from other directories may fail to locate `pyproject.toml` or create environments in unexpected locations.

## Development Philosophy

### Why uv instead of pip

uv provides a unified interface for virtual environment creation, dependency installation, and command execution. It eliminates the need for separate `pip` and `venv` commands while ensuring consistent dependency resolution. The `uv pip install -e .` command installs the package in editable mode with all dependencies, matching the production deployment environment.

### Why mise for runtimes

mise ensures all developers use identical Python and Node.js versions, preventing version-related bugs and inconsistencies. A single `mise install` command sets up the required runtimes, making onboarding faster and more reliable.

### Why src layout

The backend uses a src layout with the `exam_prep_tracker` package located in `backend/src/exam_prep_tracker/`. This structure prevents accidental imports from the project root and ensures all imports go through the installed package, matching production behavior. It works seamlessly with editable installs via `uv pip install -e .`.

## License

This project is for educational and learning purposes.
