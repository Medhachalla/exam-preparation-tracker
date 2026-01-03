# Exam Preparation Tracker

A full stack web application to help students systematically track exam preparation across subjects, units, and topics with progress tracking, notes, and Dockerized setup.


## Features

### Academic Structure
- Create and manage Subjects
- Each subject contains multiple Units
- Each unit contains multiple Topics

### Progress Tracking
- Mark topics as completed or not started
- Automatic unit completion when all topics are completed
- Visual progress bar per unit
- Checkbox based interaction for fast updates

### Notes and Resources
- Notebook style notes section per unit
- Add free form notes, links, and study resources
- Notes persist per unit and reload correctly

### UI and UX
- Responsive and clean UI built using Tailwind CSS
- Blue themed gradient layout for visual clarity
- Clear separation of subjects, units, topics, and notes
- Interactive selection and highlighting

### Data Persistence
- PostgreSQL database with relational structure
- Notes, progress, and hierarchy persist across reloads

### Containerized Setup
- Fully Dockerized frontend, backend, and database
- Single command setup using Docker Compose
- No local environment conflicts



## Tech Stack

### Frontend
- React with Vite
- Tailwind CSS
- Axios for API communication

### Backend
- Python Flask
- RESTful API design
- psycopg2 for PostgreSQL connectivity

### Database
- PostgreSQL
- Relational schema for subjects, units, topics, and notes

### DevOps
- Docker
- Docker Compose
- Named volumes for database persistence




## Prerequisites

Ensure the following are installed on your system:

- Docker  
- Docker Compose (v2)  
- Git  

No local installation of Node.js, Python, or PostgreSQL is required when using Docker.



## Environment Variables

Create a `.env` file in the project root with the following values:

```env
DB_NAME=exam_tracker
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```


