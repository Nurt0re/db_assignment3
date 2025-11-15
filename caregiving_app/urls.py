"""
URL Configuration for Caregiving App
"""
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    
    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    
    # Caregivers
    path('caregivers/', views.caregiver_list, name='caregiver_list'),
    path('caregivers/<int:caregiver_id>/', views.caregiver_detail, name='caregiver_detail'),
    path('caregivers/create/', views.caregiver_create, name='caregiver_create'),
    path('caregivers/<int:caregiver_id>/update/', views.caregiver_update, name='caregiver_update'),
    path('caregivers/<int:caregiver_id>/delete/', views.caregiver_delete, name='caregiver_delete'),
    
    # Members
    path('members/', views.member_list, name='member_list'),
    path('members/<int:member_id>/', views.member_detail, name='member_detail'),
    path('members/create/', views.member_create, name='member_create'),
    path('members/<int:member_id>/update/', views.member_update, name='member_update'),
    path('members/<int:member_id>/delete/', views.member_delete, name='member_delete'),
    
    # Jobs
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:job_id>/update/', views.job_update, name='job_update'),
    path('jobs/<int:job_id>/delete/', views.job_delete, name='job_delete'),
    
    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:appointment_id>/update/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:appointment_id>/delete/', views.appointment_delete, name='appointment_delete'),
]
