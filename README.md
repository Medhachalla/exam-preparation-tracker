# Exam Preparation Tracker

A full-stack web application for tracking exam preparation progress. Organize subjects into units and topics, track completion status, and maintain notes for each unit. Built with React, Flask, and PostgreSQL.

## Features

- **User Authentication**: Secure signup and login with JWT-based authentication
- **Subject Management**: Create and organize subjects for different exams
- **Unit & Topic Organization**: Break down subjects into units and topics for structured learning
- **Progress Tracking**: Visual progress bars for units and subjects based on topic completion
- **Status Management**: Mark topics as "Not Started", "In Progress", or "Completed"
- **Unit Notebooks**: Add and manage notes, links, and resources for each unit
- **User-Specific Data**: Each user has their own subjects and progress

## Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API requests
- **Tailwind CSS** - Utility-first CSS framework

### Backend
- **Flask** - Python web framework
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **Passlib (bcrypt)** - Password hashing
- **psycopg2** - PostgreSQL adapter
- **python-dotenv** - Environment variable management

### Database
- **PostgreSQL 15** - Relational database (runs in Docker)

## Project Structure

```
exam-prep-tracker/
├── backend/
│   ├── db/
│   │   └── schema.sql           # Database schema
│   ├── docker-compose.yml       # Docker config for PostgreSQL
│   ├── requirements.txt         # Python dependencies
│   ├── pyproject.toml          # Python project config
│   └── src/
│       └── exam-prep-tracker/
│           ├── app.py           # Flask application & routes
│           ├── auth.py          # Authentication handlers
│           └── db.py            # Database connection
├── frontend/
│   └── Exam-prep-tracker/
│       ├── src/
│       │   ├── App.jsx          # Main app component
│       │   ├── lib/
│       │   │   ├── api.js       # API client configuration
│       │   │   └── RequireAuth.jsx  # Auth route guard
│       │   └── pages/
│       │       ├── Login.jsx    # Login page
│       │       └── Signup.jsx   # Signup page
│       ├── package.json         # Node.js dependencies
│       └── vite.config.js       # Vite configuration
└── README.md
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose** - For running PostgreSQL
- **Python 3.12+** - For the Flask backend
- **Node.js 18+** and **npm** or **pnpm** - For the React frontend

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd exam-prep-tracker
```

### 2. Database Setup (PostgreSQL with Docker)

#### Configure Environment Variables

Create a `.env` file in the `backend/` directory for Docker Compose and backend configuration:

```bash
cd backend
cp .env.example .env  # Copy the example file (if it exists)
# Or create it manually
touch .env
```

Add the following environment variables to `.env`:

```env
# Database Configuration (used by Docker Compose)
POSTGRES_DB=exam_prep_db
POSTGRES_USER=exam_prep_user
POSTGRES_PASSWORD=exam_prep_password
POSTGRES_PORT=5435

# Backend Application Environment Variables
# The DATABASE_URL should match the values above
DATABASE_URL=postgresql://exam_prep_user:exam_prep_password@localhost:5435/exam_prep_db

# JWT secret key (generate a strong random string)
JWT_SECRET_KEY=your-secret-key-here-change-this-in-production
```

**Note:** You can customize these values. The Docker Compose file uses environment variable substitution, so any values you set in `.env` will be used. If you don't set them, it will use the defaults shown above.

**To generate a secure JWT secret key:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Start the PostgreSQL Container

Navigate to the backend directory and start the PostgreSQL container:

```bash
cd backend
docker-compose up -d
```

This will:
- Start a PostgreSQL 15 container
- Create a database using the `POSTGRES_DB` value from `.env` (default: `exam_prep_db`)
- Expose PostgreSQL on the port specified in `POSTGRES_PORT` (default: `5435`)
- Automatically run the schema.sql to create tables

**Default Database Credentials (if using defaults):**
- Host: `localhost`
- Port: `5435`
- Database: `exam_prep_db`
- User: `exam_prep_user`
- Password: `exam_prep_password`

To stop the database:
```bash
docker-compose down
```

To view database logs:
```bash
docker-compose logs -f postgres
```

### 3. Backend Setup

#### Create a Virtual Environment

```bash
cd backend
python3 -m venv venv
```

#### Activate the Virtual Environment

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Environment Variables

**Note:** If you already created the `.env` file in step 2 (Database Setup), you can skip this section. The `.env` file should already contain all required variables.

If you haven't created it yet, create a `.env` file in the `backend/` directory:

```bash
cd backend
touch .env
```

The `.env` file should contain:
- `DATABASE_URL` - PostgreSQL connection string (must match Docker Compose credentials)
- `JWT_SECRET_KEY` - Secret key for JWT token signing

See the [Database Setup](#2-database-setup-postgresql-with-docker) section for the complete `.env` file template.

#### Run the Flask Server

```bash
cd src
python -m exam-prep-tracker.app
```

Or from the backend directory:
```bash
python -m src.exam-prep-tracker.app
```

The Flask server will run on `http://127.0.0.1:5000`

### 4. Frontend Setup

#### Navigate to Frontend Directory

```bash
cd frontend/Exam-prep-tracker
```

#### Install Dependencies

If using **npm**:
```bash
npm install
```

If using **pnpm** (recommended):
```bash
pnpm install
```

#### Run the Development Server

```bash
npm run dev
# or
pnpm dev
```

The frontend will run on `http://localhost:5173`

## Running the Application

1. **Start PostgreSQL** (if not already running):
   ```bash
   cd backend
   docker-compose up -d
   ```

2. **Start the Backend Server**:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m src.exam-prep-tracker.app
   ```

3. **Start the Frontend Server** (in a new terminal):
   ```bash
   cd frontend/Exam-prep-tracker
   npm run dev  # or pnpm dev
   ```

4. **Open your browser** and navigate to `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Login and receive JWT token

### Subjects (Protected - Requires JWT)
- `GET /subjects` - Get all subjects for the current user
- `POST /subjects` - Create a new subject
- `DELETE /subjects/<id>` - Delete a subject

### Units (Protected)
- `GET /subjects/<id>/units` - Get all units for a subject
- `POST /subjects/<id>/units` - Create a new unit
- `DELETE /units/<id>` - Delete a unit

### Topics (Protected)
- `GET /units/<id>/topics` - Get all topics for a unit
- `POST /units/<id>/topics` - Create a new topic
- `PUT /topics/<id>/status` - Update topic status
- `DELETE /topics/<id>` - Delete a topic

### Notes (Protected)
- `GET /units/<id>/notes` - Get all notes for a unit
- `POST /units/<id>/notes` - Create a new note
- `DELETE /notes/<id>` - Delete a note

### Progress (Protected)
- `GET /units/<id>/progress` - Get progress percentage for a unit
- `GET /subjects/<id>/progress` - Get progress percentage for a subject

## Database Schema

The application uses the following tables:

- **users** - User accounts with email and password hash
- **subjects** - Exam subjects, linked to users
- **units** - Units within subjects
- **topics** - Individual topics within units, with completion status
- **notes** - Notes and resources for units

## Development

### Backend Development

- The Flask server runs in debug mode by default
- API routes are defined in `backend/src/exam-prep-tracker/app.py`
- Authentication logic is in `backend/src/exam-prep-tracker/auth.py`
- Database schema is defined in `backend/db/schema.sql`

### Frontend Development

- The React app uses Vite for hot module replacement
- Components are in `frontend/Exam-prep-tracker/src/`
- API client is configured in `frontend/Exam-prep-tracker/src/lib/api.js`
- Protected routes use `RequireAuth` component

### Common Issues

1. **Port already in use**: Change the port in `docker-compose.yml` or ensure no other PostgreSQL instance is running
2. **Module not found errors**: Ensure virtual environment is activated and dependencies are installed
3. **Database connection errors**: Verify Docker container is running and DATABASE_URL is correct
4. **CORS errors**: Ensure backend CORS is configured for your frontend URL (default: `http://localhost:5173`)

## Environment Variables Reference

### Backend (.env file in backend/)

All environment variables should be set in a `.env` file in the `backend/` directory.

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `POSTGRES_DB` | PostgreSQL database name | `exam_prep_db` | `exam_prep_db` |
| `POSTGRES_USER` | PostgreSQL username | `exam_prep_user` | `exam_prep_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `exam_prep_password` | `your-secure-password` |
| `POSTGRES_PORT` | PostgreSQL container port mapping (host:container) | `5435` | `5435` |
| `DATABASE_URL` | PostgreSQL connection string (must match above values) | - | `postgresql://exam_prep_user:exam_prep_password@localhost:5435/exam_prep_db` |
| `JWT_SECRET_KEY` | Secret key for JWT token signing | - | `your-secret-key-here` |

**Important:** The `DATABASE_URL` must match the `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`, and `POSTGRES_DB` values you set. If you change the database credentials, update `DATABASE_URL` accordingly.

