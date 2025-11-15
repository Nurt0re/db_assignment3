# Caregiving Management System - Django + SQLAlchemy

A full-stack web application for managing caregiving services with complete CRUD operations, built using Django web framework and SQLAlchemy ORM with PostgreSQL database.

## Features

✅ **Full CRUD Operations** for all entities:
- Users
- Caregivers  
- Members
- Jobs
- Appointments

✅ **Technology Stack**:
- **Backend**: Django 4.2.7
- **ORM**: SQLAlchemy 2.0.23
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3 (embedded in templates)
- **Python**: 3.x

✅ **Key Highlights**:
- SQLAlchemy ORM models with relationships
- Django views using SQLAlchemy sessions
- Responsive web interface
- Database connection pooling
- Error handling and user feedback

## Project Structure

```
db_assignment3/
├── caregiving_project/        # Django project settings
│   ├── settings.py           # Configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py
├── caregiving_app/           # Main application
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── users/
│   │   ├── caregivers/
│   │   ├── members/
│   │   ├── jobs/
│   │   └── appointments/
│   ├── static/               # Static files (CSS, JS)
│   ├── views.py              # View functions (CRUD operations)
│   └── urls.py               # App URL routing
├── database.py               # SQLAlchemy database connection
├── models.py                 # SQLAlchemy ORM models
├── schema.sql                # Database schema
├── queries/                  # SQL query files
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── manage.py                 # Django management script
└── README_DJANGO.md          # This file
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Start Database

```bash
make up
```

### 3. Create Database Schema

```bash
make migrate
```

### 4. Insert Sample Data

```bash
make insert
```

### 5. Run Django Development Server

```bash
python3 manage.py runserver
```

Or use the Makefile:
```bash
make runserver
```

### 6. Access the Application

Open your browser and visit:
- **Home**: http://127.0.0.1:8000/
- **Users**: http://127.0.0.1:8000/users/
- **Caregivers**: http://127.0.0.1:8000/caregivers/
- **Members**: http://127.0.0.1:8000/members/
- **Jobs**: http://127.0.0.1:8000/jobs/
- **Appointments**: http://127.0.0.1:8000/appointments/

## Database Configuration

The application connects to PostgreSQL database using settings from `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=caregiving_db
DB_USER=postgres
DB_PASSWORD=postgres
```

## SQLAlchemy Models

### User
Base user model with personal information

### Caregiver
Extends User with caregiving-specific fields:
- caregiving_type
- hourly_rate
- gender

### Member
Extends User with member-specific fields:
- house_rules
- dependent_description

### Job
Job postings by members:
- required_caregiving_type
- other_requirements
- date_posted

### Appointment
Scheduled caregiving appointments:
- appointment_date
- appointment_time
- work_hours
- status

### JobApplication
Tracks caregiver applications to jobs

### Address
Member addresses

## CRUD Operations

Each entity supports complete CRUD operations:

### Create
- Forms with validation
- SQLAlchemy session management
- Success/error messages

### Read
- List all records
- View individual record details
- Related data loading (eager loading with joinedload)

### Update
- Pre-populated forms
- Field validation
- Transaction management

### Delete
- Confirmation prompts
- Cascade deletes for related records
- Error handling

## SQLAlchemy Features Used

1. **ORM Models**: Declarative base classes
2. **Relationships**: One-to-one, one-to-many with cascade deletes
3. **Eager Loading**: `joinedload()` for optimizing queries
4. **Session Management**: Scoped sessions with proper cleanup
5. **Connection Pooling**: Configured engine with pool settings
6. **Transactions**: Automatic commit/rollback

## Development

### Running Queries

```bash
# Simple queries
make simple

# Complex queries
make complex

# Derived attribute query
make derived

# View operation
make view
```

### Database Management

```bash
# Connect to database
make connect

# Run updates
make update

# Run deletes
make delete

# Reset database
make clean
```

## API Endpoints

### Users
- `GET /users/` - List all users
- `GET /users/<id>/` - View user details
- `GET /users/create/` - Create user form
- `POST /users/create/` - Create user
- `GET /users/<id>/update/` - Update user form
- `POST /users/<id>/update/` - Update user
- `POST /users/<id>/delete/` - Delete user

### Caregivers
- `GET /caregivers/` - List all caregivers
- `GET /caregivers/<id>/` - View caregiver details
- `GET /caregivers/create/` - Create caregiver form
- `POST /caregivers/create/` - Create caregiver
- `GET /caregivers/<id>/update/` - Update caregiver form
- `POST /caregivers/<id>/update/` - Update caregiver
- `POST /caregivers/<id>/delete/` - Delete caregiver

(Similar patterns for Members, Jobs, and Appointments)

## Security Notes

⚠️ **For Production**:
- Hash passwords (currently stored as plain text)
- Use environment variables for sensitive data
- Enable CSRF protection
- Add authentication and authorization
- Use HTTPS
- Set DEBUG=False
- Configure allowed hosts

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
python3 database.py
```

### Port Already in Use
```bash
# Run on different port
python3 manage.py runserver 8001
```

### Migration Issues
```bash
# Reset database
make clean
make up
make migrate
make insert
```

## Assignment Requirements Fulfilled

✅ **CRUD Functionality**: Complete Create, Read, Update, Delete for all tables

✅ **Django Framework**: Used Django 4.2.7 for web application

✅ **SQLAlchemy ORM**: All database operations use SQLAlchemy ORM

✅ **PostgreSQL**: Connected to existing PostgreSQL database

✅ **Full-Stack**: Backend (Django + SQLAlchemy) + Frontend (HTML/CSS templates)

## Author

Database Assignment 3 - Caregiving Management System

## License

Educational Project
