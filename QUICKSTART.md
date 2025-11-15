# Quick Start Guide - Django + SQLAlchemy Web Application

## 🚀 Quick Start (5 Steps)

### Step 1: Install Dependencies
```bash
make install
```
Or manually:
```bash
pip3 install Django==4.2.7 SQLAlchemy==2.0.23 psycopg2-binary==2.9.9 python-dotenv==1.0.0
```

### Step 2: Start Database
```bash
make up
```

### Step 3: Create Schema & Insert Data
```bash
make migrate
make insert
```

### Step 4: Run Django Migrations
```bash
python3 manage.py migrate
```

### Step 5: Start Web Server
```bash
make runserver
```
Or:
```bash
python3 manage.py runserver
```

### Step 6: Access Application
Open your browser: **http://127.0.0.1:8000/**

---

## 📱 Application URLs

- **Home**: http://127.0.0.1:8000/
- **Users**: http://127.0.0.1:8000/users/
- **Caregivers**: http://127.0.0.1:8000/caregivers/
- **Members**: http://127.0.0.1:8000/members/
- **Jobs**: http://127.0.0.1:8000/jobs/
- **Appointments**: http://127.0.0.1:8000/appointments/

---

## 🎯 Features

### CRUD Operations for All Entities:
✅ **Users** - Manage all system users
✅ **Caregivers** - Manage caregivers with specializations
✅ **Members** - Manage members seeking care
✅ **Jobs** - Post and manage caregiving jobs
✅ **Appointments** - Schedule and track appointments

### Each Entity Supports:
- **Create**: Add new records with forms
- **Read**: List all records & view details
- **Update**: Edit existing records
- **Delete**: Remove records (with confirmation)

---

## 💻 Technology Stack

- **Backend**: Django 4.2.7
- **ORM**: SQLAlchemy 2.0.23 (NOT Django ORM!)
- **Database**: PostgreSQL
- **Frontend**: HTML5 + CSS3
- **Python**: 3.x

---

## 🔧 Makefile Commands

### Database Management
```bash
make up          # Start PostgreSQL container
make down        # Stop containers
make connect     # Connect to database
make clean       # Delete all data
```

### Data Operations
```bash
make migrate     # Create tables
make insert      # Insert sample data
make update      # Run update queries
make delete      # Run delete queries
```

### Query Operations
```bash
make simple      # Simple queries (5.1-5.4)
make complex     # Complex queries (6.1-6.4)
make derived     # Derived attribute query (7)
make view        # View operation (8)
```

### Django Application
```bash
make install     # Install dependencies
make runserver   # Start web server
make test-db     # Test database connection
```

---

## 📁 Key Files

| File | Description |
|------|-------------|
| `database.py` | SQLAlchemy connection & session management |
| `models.py` | SQLAlchemy ORM models for all tables |
| `caregiving_app/views.py` | Django views with CRUD operations |
| `caregiving_app/urls.py` | URL routing configuration |
| `caregiving_app/templates/` | HTML templates for UI |
| `requirements.txt` | Python dependencies |
| `.env` | Database configuration |

---

## 🗂️ Project Structure

```
db_assignment3/
├── caregiving_project/         # Django project
│   ├── settings.py            # Configuration
│   └── urls.py                # Main routing
├── caregiving_app/            # Main application
│   ├── views.py               # CRUD views (using SQLAlchemy!)
│   ├── urls.py                # App routing
│   └── templates/             # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── users/
│       ├── caregivers/
│       ├── members/
│       ├── jobs/
│       └── appointments/
├── database.py                # SQLAlchemy setup
├── models.py                  # SQLAlchemy models
├── manage.py                  # Django management
├── requirements.txt           # Dependencies
└── .env                       # Config
```

---

## 🔍 How It Works

### Django + SQLAlchemy Integration

This project uniquely combines:
- **Django** for web framework (views, templates, URLs)
- **SQLAlchemy** for ORM (NOT Django's ORM)

#### In views.py:
```python
from database import SessionLocal  # SQLAlchemy session
from models import User, Caregiver  # SQLAlchemy models

def user_list(request):
    db = SessionLocal()
    try:
        users = db.query(User).all()  # SQLAlchemy query
        return render(request, 'users/user_list.html', {'users': users})
    finally:
        db.close()
```

---

## 🎨 Example CRUD Flow

### Creating a User:
1. Visit: http://127.0.0.1:8000/users/create/
2. Fill form (name, email, city, etc.)
3. Click "Create User"
4. SQLAlchemy creates record in PostgreSQL
5. Redirects to user list

### Updating a Caregiver:
1. Visit: http://127.0.0.1:8000/caregivers/
2. Click "Edit" on any caregiver
3. Modify fields (hourly rate, type, etc.)
4. Click "Update Caregiver"
5. SQLAlchemy updates record
6. View updated details

---

## ⚠️ Troubleshooting

### Database Connection Failed
```bash
# Check if database is running
docker ps

# Restart database
make down
make up
```

### Port 8000 Already in Use
```bash
# Run on different port
python3 manage.py runserver 8001
```

### Template Not Found
```bash
# Check templates directory exists
ls caregiving_app/templates/
```

---

## 📊 Sample Data

After running `make insert`, you'll have:
- 10 Users
- 6 Caregivers
- 4 Members
- 5 Jobs
- 8 Appointments

---

## 🎓 Assignment Requirements

✅ **CRUD Functionality**: Complete for all tables
✅ **Django Framework**: Web application
✅ **SQLAlchemy ORM**: All database operations
✅ **PostgreSQL Database**: Connected and working
✅ **Full-Stack**: Backend + Frontend

---

## 📚 Learning Resources

- [Django Docs](https://docs.djangoproject.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## 🆘 Need Help?

1. Check server is running: Visit http://127.0.0.1:8000/
2. Check database connection: `make test-db`
3. View logs: Check terminal output
4. Reset everything:
   ```bash
   make clean
   make up
   make migrate
   make insert
   python3 manage.py migrate
   make runserver
   ```

---

**🎉 Your Caregiving Management System is ready to use!**

Start by visiting: **http://127.0.0.1:8000/**
