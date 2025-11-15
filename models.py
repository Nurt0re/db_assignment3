"""
SQLAlchemy ORM Models for Caregiving Database
Maps to existing PostgreSQL tables created via schema.sql
"""
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Date, Time, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100))
    phone_number = Column(String(20))
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.user_id}, name='{self.given_name} {self.surname}', email='{self.email}')>"
    
    @property
    def full_name(self):
        return f"{self.given_name} {self.surname}"


class Caregiver(Base):
    __tablename__ = 'caregiver'
    
    caregiver_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    photo = Column(String(255))
    gender = Column(String(50), CheckConstraint("gender IN ('Male', 'Female', 'Other', 'Prefer not to say')"))
    caregiving_type = Column(String(100), nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="caregiver", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Caregiver(id={self.caregiver_user_id}, type='{self.caregiving_type}', rate={self.hourly_rate})>"


class Member(Base):
    __tablename__ = 'member'
    
    member_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="member")
    addresses = relationship("Address", back_populates="member", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="member", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Member(id={self.member_user_id})>"


class Address(Base):
    __tablename__ = 'address'
    
    address_id = Column(Integer, primary_key=True)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    house_number = Column(String(20), nullable=False)
    street = Column(String(255), nullable=False)
    town = Column(String(100), nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(id={self.address_id}, address='{self.house_number} {self.street}, {self.town}')>"
    
    @property
    def full_address(self):
        return f"{self.house_number} {self.street}, {self.town}"


class Job(Base):
    __tablename__ = 'job'
    
    job_id = Column(Integer, primary_key=True)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(String(100), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job(id={self.job_id}, type='{self.required_caregiving_type}', posted={self.date_posted})>"


class JobApplication(Base):
    __tablename__ = 'job_application'
    
    application_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    job_id = Column(Integer, ForeignKey('job.job_id', ondelete='CASCADE'), nullable=False)
    date_applied = Column(Date, nullable=False)
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")
    
    def __repr__(self):
        return f"<JobApplication(id={self.application_id}, caregiver={self.caregiver_user_id}, job={self.job_id})>"


class Appointment(Base):
    __tablename__ = 'appointment'
    
    appointment_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(DECIMAL(5, 2), nullable=False)
    status = Column(String(20), CheckConstraint("status IN ('Scheduled', 'Confirmed', 'Completed', 'Cancelled')"), 
                   server_default='Scheduled')
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")
    
    def __repr__(self):
        return f"<Appointment(id={self.appointment_id}, date={self.appointment_date}, status='{self.status}')>"
    
    @property
    def total_cost(self):
        """Calculate total cost based on work hours and caregiver hourly rate"""
        if self.caregiver and self.caregiver.hourly_rate:
            return float(self.work_hours) * float(self.caregiver.hourly_rate)
        return 0.0
