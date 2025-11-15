#!/usr/bin/env python3
"""
Demo Script for Caregiving Management System
Demonstrates SQLAlchemy CRUD operations
"""

from database import SessionLocal, test_connection
from models import User, Caregiver, Member, Job, Appointment
from sqlalchemy.orm import joinedload
from datetime import date, time
from decimal import Decimal

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def demo_create_operations():
    """Demonstrate CREATE operations"""
    print_section("CREATE OPERATIONS")
    
    db = SessionLocal()
    try:
        # Create a new user
        print("\n1. Creating new user...")
        new_user = User(
            email="demo@example.com",
            given_name="Demo",
            surname="User",
            city="Almaty",
            phone_number="+77771234567",
            profile_description="This is a demo user created via SQLAlchemy",
            password="demo_password"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"   ✓ Created user: {new_user.full_name} (ID: {new_user.user_id})")
        
        # Create a caregiver for this user
        print("\n2. Creating caregiver profile...")
        new_caregiver = Caregiver(
            caregiver_user_id=new_user.user_id,
            photo="photos/demo_user.jpg",
            gender="Other",
            caregiving_type="Elderly Care",
            hourly_rate=Decimal("2500.00")
        )
        db.add(new_caregiver)
        db.commit()
        print(f"   ✓ Created caregiver with rate ${new_caregiver.hourly_rate}/hour")
        
        return new_user.user_id
        
    except Exception as e:
        db.rollback()
        print(f"   ✗ Error: {e}")
        return None
    finally:
        db.close()

def demo_read_operations():
    """Demonstrate READ operations"""
    print_section("READ OPERATIONS")
    
    db = SessionLocal()
    try:
        # Simple query - count users
        print("\n1. Counting total users...")
        user_count = db.query(User).count()
        print(f"   ✓ Total users: {user_count}")
        
        # Query with filter
        print("\n2. Finding users in Almaty...")
        almaty_users = db.query(User).filter(User.city == "Almaty").all()
        print(f"   ✓ Found {len(almaty_users)} users in Almaty")
        for user in almaty_users[:3]:  # Show first 3
            print(f"     - {user.full_name}")
        
        # Query with join (eager loading)
        print("\n3. Getting caregivers with user info (eager loading)...")
        caregivers = db.query(Caregiver).options(
            joinedload(Caregiver.user)
        ).limit(5).all()
        print(f"   ✓ Found {len(caregivers)} caregivers:")
        for cg in caregivers:
            print(f"     - {cg.user.full_name}: {cg.caregiving_type} (${cg.hourly_rate}/hr)")
        
        # Complex query with multiple joins
        print("\n4. Getting appointments with all related data...")
        appointments = db.query(Appointment).options(
            joinedload(Appointment.caregiver).joinedload(Caregiver.user),
            joinedload(Appointment.member).joinedload(Member.user)
        ).filter(Appointment.status == "Confirmed").all()
        print(f"   ✓ Found {len(appointments)} confirmed appointments:")
        for apt in appointments[:3]:  # Show first 3
            print(f"     - {apt.caregiver.user.full_name} → {apt.member.user.full_name}")
            print(f"       Date: {apt.appointment_date}, Cost: ${apt.total_cost}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    finally:
        db.close()

def demo_update_operations(user_id):
    """Demonstrate UPDATE operations"""
    print_section("UPDATE OPERATIONS")
    
    if not user_id:
        print("   ⚠ No user ID provided, skipping...")
        return
    
    db = SessionLocal()
    try:
        # Update user
        print(f"\n1. Updating user {user_id}...")
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            old_city = user.city
            user.city = "Astana"
            user.profile_description = "Updated via demo script"
            db.commit()
            print(f"   ✓ Updated user city: {old_city} → {user.city}")
        else:
            print(f"   ✗ User {user_id} not found")
        
        # Update caregiver
        print(f"\n2. Updating caregiver hourly rate...")
        caregiver = db.query(Caregiver).filter(
            Caregiver.caregiver_user_id == user_id
        ).first()
        if caregiver:
            old_rate = caregiver.hourly_rate
            caregiver.hourly_rate = Decimal("2800.00")
            db.commit()
            print(f"   ✓ Updated rate: ${old_rate} → ${caregiver.hourly_rate}")
        
    except Exception as e:
        db.rollback()
        print(f"   ✗ Error: {e}")
    finally:
        db.close()

def demo_delete_operations(user_id):
    """Demonstrate DELETE operations"""
    print_section("DELETE OPERATIONS")
    
    if not user_id:
        print("   ⚠ No user ID provided, skipping...")
        return
    
    db = SessionLocal()
    try:
        # Delete user (cascade will delete caregiver)
        print(f"\n1. Deleting user {user_id} (with cascade)...")
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            print(f"   - User: {user.full_name}")
            if user.caregiver:
                print(f"   - Caregiver profile will be deleted (cascade)")
            
            db.delete(user)
            db.commit()
            print(f"   ✓ Successfully deleted user and related records")
        else:
            print(f"   ✗ User {user_id} not found")
        
    except Exception as e:
        db.rollback()
        print(f"   ✗ Error: {e}")
    finally:
        db.close()

def demo_statistics():
    """Display database statistics"""
    print_section("DATABASE STATISTICS")
    
    db = SessionLocal()
    try:
        stats = {
            'Users': db.query(User).count(),
            'Caregivers': db.query(Caregiver).count(),
            'Members': db.query(Member).count(),
            'Jobs': db.query(Job).count(),
            'Appointments': db.query(Appointment).count(),
        }
        
        print("\n   Current Database Contents:")
        for entity, count in stats.items():
            print(f"   - {entity}: {count}")
        
        # Show caregiving types distribution
        print("\n   Caregiving Types:")
        from sqlalchemy import func
        types = db.query(
            Caregiver.caregiving_type,
            func.count(Caregiver.caregiver_user_id)
        ).group_by(Caregiver.caregiving_type).all()
        
        for care_type, count in types:
            print(f"   - {care_type}: {count}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    finally:
        db.close()

def main():
    """Main demo function"""
    print("\n" + "🏥 "*20)
    print("   CAREGIVING MANAGEMENT SYSTEM - SQLAlchemy Demo")
    print("🏥 "*20)
    
    # Test connection
    print_section("DATABASE CONNECTION")
    if not test_connection():
        print("\n❌ Database connection failed. Please ensure:")
        print("  1. Docker container is running (make up)")
        print("  2. Database exists (make migrate)")
        print("  3. .env file has correct credentials")
        return
    
    # Show initial statistics
    demo_statistics()
    
    # Demonstrate CRUD operations
    user_id = demo_create_operations()
    demo_read_operations()
    demo_update_operations(user_id)
    
    # Show final statistics
    demo_statistics()
    
    # Clean up demo data
    demo_delete_operations(user_id)
    
    print_section("DEMO COMPLETE")
    print("\n✅ All SQLAlchemy operations demonstrated successfully!")
    print("\n📖 Next steps:")
    print("   1. Run web server: make runserver")
    print("   2. Visit: http://127.0.0.1:8000/")
    print("   3. Try CRUD operations in the web interface")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
