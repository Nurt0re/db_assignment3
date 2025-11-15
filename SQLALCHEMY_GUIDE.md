# SQLAlchemy Implementation Guide

## Overview
This document explains how SQLAlchemy ORM is used throughout the application.

## Database Connection (database.py)

### Engine Configuration
```python
engine = create_engine(
    DATABASE_URL,
    echo=True,              # Log SQL statements
    pool_pre_ping=True,     # Verify connections
    pool_size=10,           # Connection pool size
    max_overflow=20         # Max overflow connections
)
```

### Session Management
```python
# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session for thread-safety
db_session = scoped_session(SessionLocal)

# Usage in views
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## ORM Models (models.py)

### Base Model
```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

### User Model
```python
class User(Base):
    __tablename__ = 'user'
    
    # Primary Key
    user_id = Column(Integer, primary_key=True)
    
    # Required Fields
    email = Column(String(255), nullable=False, unique=True)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    
    # Optional Fields
    city = Column(String(100))
    phone_number = Column(String(20))
    profile_description = Column(Text)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), 
                       onupdate=func.current_timestamp())
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="user", 
                            uselist=False, cascade="all, delete-orphan")
    member = relationship("Member", back_populates="user", 
                         uselist=False, cascade="all, delete-orphan")
    
    # Properties
    @property
    def full_name(self):
        return f"{self.given_name} {self.surname}"
```

### Caregiver Model (with Foreign Key)
```python
class Caregiver(Base):
    __tablename__ = 'caregiver'
    
    # Foreign Key as Primary Key
    caregiver_user_id = Column(Integer, 
                               ForeignKey('user.user_id', ondelete='CASCADE'), 
                               primary_key=True)
    
    # Fields with constraints
    gender = Column(String(50), 
                   CheckConstraint("gender IN ('Male', 'Female', 'Other', 'Prefer not to say')"))
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver", 
                                   cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="caregiver", 
                               cascade="all, delete-orphan")
```

### Appointment Model (with Multiple Foreign Keys)
```python
class Appointment(Base):
    __tablename__ = 'appointment'
    
    appointment_id = Column(Integer, primary_key=True)
    
    # Multiple Foreign Keys
    caregiver_user_id = Column(Integer, 
                               ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), 
                               nullable=False)
    member_user_id = Column(Integer, 
                           ForeignKey('member.member_user_id', ondelete='CASCADE'), 
                           nullable=False)
    
    # Date/Time Fields
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    
    # Numeric Field
    work_hours = Column(DECIMAL(5, 2), nullable=False)
    
    # Enum-like Field with Check Constraint
    status = Column(String(20), 
                   CheckConstraint("status IN ('Scheduled', 'Confirmed', 'Completed', 'Cancelled')"),
                   server_default='Scheduled')
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")
    
    # Computed Property
    @property
    def total_cost(self):
        if self.caregiver and self.caregiver.hourly_rate:
            return float(self.work_hours) * float(self.caregiver.hourly_rate)
        return 0.0
```

---

## CRUD Operations in Views

### CREATE Operation
```python
def user_create(request):
    if request.method == 'POST':
        db = SessionLocal()
        try:
            # Create new instance
            user = User(
                email=request.POST.get('email'),
                given_name=request.POST.get('given_name'),
                surname=request.POST.get('surname'),
                city=request.POST.get('city'),
                phone_number=request.POST.get('phone_number'),
                profile_description=request.POST.get('profile_description'),
                password=request.POST.get('password')
            )
            
            # Add to session and commit
            db.add(user)
            db.commit()
            
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
        except Exception as e:
            db.rollback()  # Rollback on error
            messages.error(request, f'Error creating user: {str(e)}')
        finally:
            db.close()  # Always close session
```

### READ Operations

#### List All (Basic Query)
```python
def user_list(request):
    db = SessionLocal()
    try:
        # Simple query
        users = db.query(User).all()
        return render(request, 'users/user_list.html', {'users': users})
    finally:
        db.close()
```

#### Get One (Filter Query)
```python
def user_detail(request, user_id):
    db = SessionLocal()
    try:
        # Filter query
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise Http404("User not found")
        return render(request, 'users/user_detail.html', {'user': user})
    finally:
        db.close()
```

#### Eager Loading (Join Query)
```python
def caregiver_detail(request, caregiver_id):
    db = SessionLocal()
    try:
        # Eager load related data
        caregiver = db.query(Caregiver).options(
            joinedload(Caregiver.user),
            joinedload(Caregiver.appointments),
            joinedload(Caregiver.job_applications)
        ).filter(Caregiver.caregiver_user_id == caregiver_id).first()
        
        if not caregiver:
            raise Http404("Caregiver not found")
        
        return render(request, 'caregivers/caregiver_detail.html', {'caregiver': caregiver})
    finally:
        db.close()
```

#### Complex Query with Multiple Joins
```python
def appointment_list(request):
    db = SessionLocal()
    try:
        # Multiple eager loads with nested relationships
        appointments = db.query(Appointment).options(
            joinedload(Appointment.caregiver).joinedload(Caregiver.user),
            joinedload(Appointment.member).joinedload(Member.user)
        ).all()
        
        return render(request, 'appointments/appointment_list.html', 
                     {'appointments': appointments})
    finally:
        db.close()
```

### UPDATE Operation
```python
def user_update(request, user_id):
    db = SessionLocal()
    try:
        # Get existing record
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise Http404("User not found")
        
        if request.method == 'POST':
            # Update fields
            user.email = request.POST.get('email')
            user.given_name = request.POST.get('given_name')
            user.surname = request.POST.get('surname')
            user.city = request.POST.get('city')
            user.phone_number = request.POST.get('phone_number')
            user.profile_description = request.POST.get('profile_description')
            
            # Conditional update
            if request.POST.get('password'):
                user.password = request.POST.get('password')
            
            # Commit changes
            db.commit()
            
            messages.success(request, 'User updated successfully!')
            return redirect('user_detail', user_id=user_id)
        
        return render(request, 'users/user_form.html', 
                     {'user': user, 'action': 'Update'})
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error updating user: {str(e)}')
        return redirect('user_list')
    finally:
        db.close()
```

### DELETE Operation
```python
def user_delete(request, user_id):
    if request.method == 'POST':
        db = SessionLocal()
        try:
            # Get record
            user = db.query(User).filter(User.user_id == user_id).first()
            if user:
                # Delete with cascade (related records deleted automatically)
                db.delete(user)
                db.commit()
                messages.success(request, 'User deleted successfully!')
            else:
                messages.error(request, 'User not found')
        except Exception as e:
            db.rollback()
            messages.error(request, f'Error deleting user: {str(e)}')
        finally:
            db.close()
    
    return redirect('user_list')
```

---

## Advanced SQLAlchemy Features Used

### 1. Relationships

#### One-to-One
```python
class User(Base):
    caregiver = relationship("Caregiver", back_populates="user", uselist=False)

class Caregiver(Base):
    user = relationship("User", back_populates="caregiver")
```

#### One-to-Many
```python
class Member(Base):
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")

class Job(Base):
    member = relationship("Member", back_populates="jobs")
```

### 2. Cascade Deletes
```python
# When User is deleted, Caregiver is automatically deleted
caregiver = relationship("Caregiver", cascade="all, delete-orphan")
```

### 3. Eager Loading (N+1 Query Prevention)
```python
# Bad: N+1 queries (1 for caregivers + N for users)
caregivers = db.query(Caregiver).all()
for c in caregivers:
    print(c.user.full_name)  # Separate query each time

# Good: 1 query with join
caregivers = db.query(Caregiver).options(joinedload(Caregiver.user)).all()
for c in caregivers:
    print(c.user.full_name)  # No additional query
```

### 4. Filtering and Exclusions
```python
# Get available users (not already caregivers or members)
caregiver_ids = [c.caregiver_user_id for c in db.query(Caregiver).all()]
member_ids = [m.member_user_id for m in db.query(Member).all()]
used_ids = set(caregiver_ids + member_ids)

available_users = db.query(User).filter(~User.user_id.in_(used_ids)).all()
```

### 5. Check Constraints
```python
status = Column(String(20), 
               CheckConstraint("status IN ('Scheduled', 'Confirmed', 'Completed', 'Cancelled')"))
```

### 6. Server Defaults
```python
created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
status = Column(String(20), server_default='Scheduled')
```

### 7. Auto-updating Timestamps
```python
updated_at = Column(TIMESTAMP, 
                   server_default=func.current_timestamp(),
                   onupdate=func.current_timestamp())
```

---

## Transaction Management

### Manual Transaction Control
```python
db = SessionLocal()
try:
    # Multiple operations in single transaction
    user = User(email="test@example.com", ...)
    db.add(user)
    db.flush()  # Get user_id without committing
    
    caregiver = Caregiver(caregiver_user_id=user.user_id, ...)
    db.add(caregiver)
    
    db.commit()  # Commit all changes
except Exception as e:
    db.rollback()  # Rollback on error
finally:
    db.close()
```

---

## Query Examples

### Simple Queries
```python
# All records
users = db.query(User).all()

# First record
user = db.query(User).first()

# Filter
user = db.query(User).filter(User.user_id == 1).first()

# Multiple filters
users = db.query(User).filter(User.city == 'Astana', User.email.like('%@gmail.com')).all()

# Count
count = db.query(User).count()
```

### Complex Queries
```python
# Join with filter
caregivers = db.query(Caregiver).join(User).filter(User.city == 'Almaty').all()

# Subquery
from sqlalchemy import func
avg_rate = db.query(func.avg(Caregiver.hourly_rate)).scalar()
above_avg = db.query(Caregiver).filter(Caregiver.hourly_rate > avg_rate).all()

# Order by
caregivers = db.query(Caregiver).order_by(Caregiver.hourly_rate.desc()).all()

# Limit
top_5 = db.query(Caregiver).order_by(Caregiver.hourly_rate.desc()).limit(5).all()
```

---

## Best Practices Used

1. **Always close sessions**: Using try-finally blocks
2. **Error handling**: Rollback on exceptions
3. **Eager loading**: Prevent N+1 queries
4. **Transaction management**: Explicit commits and rollbacks
5. **Connection pooling**: Reuse database connections
6. **Cascade deletes**: Maintain referential integrity
7. **Constraints**: Database-level validation

---

## Testing Database Connection

```python
# Test in Python
python3 -c "from database import test_connection; test_connection()"

# Or use Makefile
make test-db
```

---

This implementation demonstrates professional-grade SQLAlchemy usage suitable for production applications!
