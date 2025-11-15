"""
Django Views using SQLAlchemy ORM for CRUD operations
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from sqlalchemy.orm import joinedload
from datetime import datetime, date

from database import SessionLocal
from models import User, Caregiver, Member, Address, Job, JobApplication, Appointment


# ============ Home and Dashboard Views ============

def index(request):
    """Home page with overview statistics"""
    db = SessionLocal()
    try:
        stats = {
            'total_users': db.query(User).count(),
            'total_caregivers': db.query(Caregiver).count(),
            'total_members': db.query(Member).count(),
            'total_jobs': db.query(Job).count(),
            'total_appointments': db.query(Appointment).count(),
        }
        return render(request, 'index.html', {'stats': stats})
    finally:
        db.close()


# ============ User CRUD Operations ============

def user_list(request):
    """List all users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return render(request, 'users/user_list.html', {'users': users})
    finally:
        db.close()


def user_detail(request, user_id):
    """View user details"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise Http404("User not found")
        return render(request, 'users/user_detail.html', {'user': user})
    finally:
        db.close()


def user_create(request):
    """Create new user"""
    if request.method == 'POST':
        db = SessionLocal()
        try:
            user = User(
                email=request.POST.get('email'),
                given_name=request.POST.get('given_name'),
                surname=request.POST.get('surname'),
                city=request.POST.get('city'),
                phone_number=request.POST.get('phone_number'),
                profile_description=request.POST.get('profile_description'),
                password=request.POST.get('password')  # In production, hash this!
            )
            db.add(user)
            db.commit()
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
        except Exception as e:
            db.rollback()
            messages.error(request, f'Error creating user: {str(e)}')
        finally:
            db.close()
    
    return render(request, 'users/user_form.html', {'action': 'Create'})


def user_update(request, user_id):
    """Update existing user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise Http404("User not found")
        
        if request.method == 'POST':
            user.email = request.POST.get('email')
            user.given_name = request.POST.get('given_name')
            user.surname = request.POST.get('surname')
            user.city = request.POST.get('city')
            user.phone_number = request.POST.get('phone_number')
            user.profile_description = request.POST.get('profile_description')
            if request.POST.get('password'):
                user.password = request.POST.get('password')
            
            db.commit()
            messages.success(request, 'User updated successfully!')
            return redirect('user_detail', user_id=user_id)
        
        return render(request, 'users/user_form.html', {'user': user, 'action': 'Update'})
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error updating user: {str(e)}')
        return redirect('user_list')
    finally:
        db.close()


def user_delete(request, user_id):
    """Delete user"""
    if request.method == 'POST':
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if user:
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


# ============ Caregiver CRUD Operations ============

def caregiver_list(request):
    """List all caregivers"""
    db = SessionLocal()
    try:
        caregivers = db.query(Caregiver).options(joinedload(Caregiver.user)).all()
        return render(request, 'caregivers/caregiver_list.html', {'caregivers': caregivers})
    finally:
        db.close()


def caregiver_detail(request, caregiver_id):
    """View caregiver details"""
    db = SessionLocal()
    try:
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


def caregiver_create(request):
    """Create new caregiver"""
    db = SessionLocal()
    try:
        # Get users who are not already caregivers or members
        caregiver_ids = [c.caregiver_user_id for c in db.query(Caregiver).all()]
        member_ids = [m.member_user_id for m in db.query(Member).all()]
        used_ids = set(caregiver_ids + member_ids)
        available_users = db.query(User).filter(~User.user_id.in_(used_ids)).all()
        
        if request.method == 'POST':
            caregiver = Caregiver(
                caregiver_user_id=request.POST.get('user_id'),
                photo=request.POST.get('photo'),
                gender=request.POST.get('gender'),
                caregiving_type=request.POST.get('caregiving_type'),
                hourly_rate=request.POST.get('hourly_rate')
            )
            db.add(caregiver)
            db.commit()
            messages.success(request, 'Caregiver created successfully!')
            return redirect('caregiver_list')
        
        return render(request, 'caregivers/caregiver_form.html', {
            'action': 'Create',
            'available_users': available_users
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error creating caregiver: {str(e)}')
        return redirect('caregiver_list')
    finally:
        db.close()


def caregiver_update(request, caregiver_id):
    """Update existing caregiver"""
    db = SessionLocal()
    try:
        caregiver = db.query(Caregiver).options(joinedload(Caregiver.user)).filter(
            Caregiver.caregiver_user_id == caregiver_id
        ).first()
        
        if not caregiver:
            raise Http404("Caregiver not found")
        
        if request.method == 'POST':
            caregiver.photo = request.POST.get('photo')
            caregiver.gender = request.POST.get('gender')
            caregiver.caregiving_type = request.POST.get('caregiving_type')
            caregiver.hourly_rate = request.POST.get('hourly_rate')
            
            db.commit()
            messages.success(request, 'Caregiver updated successfully!')
            return redirect('caregiver_detail', caregiver_id=caregiver_id)
        
        return render(request, 'caregivers/caregiver_form.html', {
            'caregiver': caregiver,
            'action': 'Update'
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error updating caregiver: {str(e)}')
        return redirect('caregiver_list')
    finally:
        db.close()


def caregiver_delete(request, caregiver_id):
    """Delete caregiver"""
    if request.method == 'POST':
        db = SessionLocal()
        try:
            caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_id).first()
            if caregiver:
                db.delete(caregiver)
                db.commit()
                messages.success(request, 'Caregiver deleted successfully!')
            else:
                messages.error(request, 'Caregiver not found')
        except Exception as e:
            db.rollback()
            messages.error(request, f'Error deleting caregiver: {str(e)}')
        finally:
            db.close()
    
    return redirect('caregiver_list')


# ============ Member CRUD Operations ============

def member_list(request):
    """List all members"""
    db = SessionLocal()
    try:
        members = db.query(Member).options(joinedload(Member.user)).all()
        return render(request, 'members/member_list.html', {'members': members})
    finally:
        db.close()


def member_detail(request, member_id):
    """View member details"""
    db = SessionLocal()
    try:
        member = db.query(Member).options(
            joinedload(Member.user),
            joinedload(Member.addresses),
            joinedload(Member.jobs),
            joinedload(Member.appointments)
        ).filter(Member.member_user_id == member_id).first()
        
        if not member:
            raise Http404("Member not found")
        
        return render(request, 'members/member_detail.html', {'member': member})
    finally:
        db.close()


def member_create(request):
    """Create new member"""
    db = SessionLocal()
    try:
        # Get users who are not already caregivers or members
        caregiver_ids = [c.caregiver_user_id for c in db.query(Caregiver).all()]
        member_ids = [m.member_user_id for m in db.query(Member).all()]
        used_ids = set(caregiver_ids + member_ids)
        available_users = db.query(User).filter(~User.user_id.in_(used_ids)).all()
        
        if request.method == 'POST':
            member = Member(
                member_user_id=request.POST.get('user_id'),
                house_rules=request.POST.get('house_rules'),
                dependent_description=request.POST.get('dependent_description')
            )
            db.add(member)
            db.commit()
            messages.success(request, 'Member created successfully!')
            return redirect('member_list')
        
        return render(request, 'members/member_form.html', {
            'action': 'Create',
            'available_users': available_users
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error creating member: {str(e)}')
        return redirect('member_list')
    finally:
        db.close()


def member_update(request, member_id):
    """Update existing member"""
    db = SessionLocal()
    try:
        member = db.query(Member).options(joinedload(Member.user)).filter(
            Member.member_user_id == member_id
        ).first()
        
        if not member:
            raise Http404("Member not found")
        
        if request.method == 'POST':
            member.house_rules = request.POST.get('house_rules')
            member.dependent_description = request.POST.get('dependent_description')
            
            db.commit()
            messages.success(request, 'Member updated successfully!')
            return redirect('member_detail', member_id=member_id)
        
        return render(request, 'members/member_form.html', {
            'member': member,
            'action': 'Update'
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error updating member: {str(e)}')
        return redirect('member_list')
    finally:
        db.close()


def member_delete(request, member_id):
    """Delete member"""
    if request.method == 'POST':
        db = SessionLocal()
        try:
            member = db.query(Member).filter(Member.member_user_id == member_id).first()
            if member:
                db.delete(member)
                db.commit()
                messages.success(request, 'Member deleted successfully!')
            else:
                messages.error(request, 'Member not found')
        except Exception as e:
            db.rollback()
            messages.error(request, f'Error deleting member: {str(e)}')
        finally:
            db.close()
    
    return redirect('member_list')


# ============ Job CRUD Operations ============

def job_list(request):
    """List all jobs"""
    db = SessionLocal()
    try:
        jobs = db.query(Job).options(joinedload(Job.member).joinedload(Member.user)).all()
        return render(request, 'jobs/job_list.html', {'jobs': jobs})
    finally:
        db.close()


def job_detail(request, job_id):
    """View job details"""
    db = SessionLocal()
    try:
        job = db.query(Job).options(
            joinedload(Job.member).joinedload(Member.user),
            joinedload(Job.applications).joinedload(JobApplication.caregiver).joinedload(Caregiver.user)
        ).filter(Job.job_id == job_id).first()
        
        if not job:
            raise Http404("Job not found")
        
        return render(request, 'jobs/job_detail.html', {'job': job})
    finally:
        db.close()


def job_create(request):
    """Create new job"""
    db = SessionLocal()
    try:
        members = db.query(Member).options(joinedload(Member.user)).all()
        
        if request.method == 'POST':
            job = Job(
                member_user_id=request.POST.get('member_user_id'),
                required_caregiving_type=request.POST.get('required_caregiving_type'),
                other_requirements=request.POST.get('other_requirements'),
                date_posted=datetime.strptime(request.POST.get('date_posted'), '%Y-%m-%d').date()
            )
            db.add(job)
            db.commit()
            messages.success(request, 'Job created successfully!')
            return redirect('job_list')
        
        return render(request, 'jobs/job_form.html', {
            'action': 'Create',
            'members': members
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error creating job: {str(e)}')
        return redirect('job_list')
    finally:
        db.close()


def job_update(request, job_id):
    """Update existing job"""
    db = SessionLocal()
    try:
        job = db.query(Job).options(joinedload(Job.member).joinedload(Member.user)).filter(
            Job.job_id == job_id
        ).first()
        
        if not job:
            raise Http404("Job not found")
        
        members = db.query(Member).options(joinedload(Member.user)).all()
        
        if request.method == 'POST':
            job.member_user_id = request.POST.get('member_user_id')
            job.required_caregiving_type = request.POST.get('required_caregiving_type')
            job.other_requirements = request.POST.get('other_requirements')
            job.date_posted = datetime.strptime(request.POST.get('date_posted'), '%Y-%m-%d').date()
            
            db.commit()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', job_id=job_id)
        
        return render(request, 'jobs/job_form.html', {
            'job': job,
            'members': members,
            'action': 'Update'
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error updating job: {str(e)}')
        return redirect('job_list')
    finally:
        db.close()


def job_delete(request, job_id):
    """Delete job"""
    if request.method == 'POST':
        db = SessionLocal()
        try:
            job = db.query(Job).filter(Job.job_id == job_id).first()
            if job:
                db.delete(job)
                db.commit()
                messages.success(request, 'Job deleted successfully!')
            else:
                messages.error(request, 'Job not found')
        except Exception as e:
            db.rollback()
            messages.error(request, f'Error deleting job: {str(e)}')
        finally:
            db.close()
    
    return redirect('job_list')


# ============ Appointment CRUD Operations ============

def appointment_list(request):
    """List all appointments"""
    db = SessionLocal()
    try:
        appointments = db.query(Appointment).options(
            joinedload(Appointment.caregiver).joinedload(Caregiver.user),
            joinedload(Appointment.member).joinedload(Member.user)
        ).all()
        return render(request, 'appointments/appointment_list.html', {'appointments': appointments})
    finally:
        db.close()


def appointment_detail(request, appointment_id):
    """View appointment details"""
    db = SessionLocal()
    try:
        appointment = db.query(Appointment).options(
            joinedload(Appointment.caregiver).joinedload(Caregiver.user),
            joinedload(Appointment.member).joinedload(Member.user)
        ).filter(Appointment.appointment_id == appointment_id).first()
        
        if not appointment:
            raise Http404("Appointment not found")
        
        return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})
    finally:
        db.close()


def appointment_create(request):
    """Create new appointment"""
    db = SessionLocal()
    try:
        caregivers = db.query(Caregiver).options(joinedload(Caregiver.user)).all()
        members = db.query(Member).options(joinedload(Member.user)).all()
        
        if request.method == 'POST':
            appointment = Appointment(
                caregiver_user_id=request.POST.get('caregiver_user_id'),
                member_user_id=request.POST.get('member_user_id'),
                appointment_date=datetime.strptime(request.POST.get('appointment_date'), '%Y-%m-%d').date(),
                appointment_time=datetime.strptime(request.POST.get('appointment_time'), '%H:%M').time(),
                work_hours=request.POST.get('work_hours'),
                status=request.POST.get('status', 'Scheduled')
            )
            db.add(appointment)
            db.commit()
            messages.success(request, 'Appointment created successfully!')
            return redirect('appointment_list')
        
        return render(request, 'appointments/appointment_form.html', {
            'action': 'Create',
            'caregivers': caregivers,
            'members': members
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error creating appointment: {str(e)}')
        return redirect('appointment_list')
    finally:
        db.close()


def appointment_update(request, appointment_id):
    """Update existing appointment"""
    db = SessionLocal()
    try:
        appointment = db.query(Appointment).options(
            joinedload(Appointment.caregiver).joinedload(Caregiver.user),
            joinedload(Appointment.member).joinedload(Member.user)
        ).filter(Appointment.appointment_id == appointment_id).first()
        
        if not appointment:
            raise Http404("Appointment not found")
        
        caregivers = db.query(Caregiver).options(joinedload(Caregiver.user)).all()
        members = db.query(Member).options(joinedload(Member.user)).all()
        
        if request.method == 'POST':
            appointment.caregiver_user_id = request.POST.get('caregiver_user_id')
            appointment.member_user_id = request.POST.get('member_user_id')
            appointment.appointment_date = datetime.strptime(request.POST.get('appointment_date'), '%Y-%m-%d').date()
            appointment.appointment_time = datetime.strptime(request.POST.get('appointment_time'), '%H:%M').time()
            appointment.work_hours = request.POST.get('work_hours')
            appointment.status = request.POST.get('status')
            
            db.commit()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_detail', appointment_id=appointment_id)
        
        return render(request, 'appointments/appointment_form.html', {
            'appointment': appointment,
            'caregivers': caregivers,
            'members': members,
            'action': 'Update'
        })
    except Exception as e:
        db.rollback()
        messages.error(request, f'Error updating appointment: {str(e)}')
        return redirect('appointment_list')
    finally:
        db.close()


def appointment_delete(request, appointment_id):
    """Delete appointment"""
    if request.method == 'POST':
        db = SessionLocal()
        try:
            appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
            if appointment:
                db.delete(appointment)
                db.commit()
                messages.success(request, 'Appointment deleted successfully!')
            else:
                messages.error(request, 'Appointment not found')
        except Exception as e:
            db.rollback()
            messages.error(request, f'Error deleting appointment: {str(e)}')
        finally:
            db.close()
    
    return redirect('appointment_list')
