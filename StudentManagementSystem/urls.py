from django.urls import path
from django.contrib import admin
from .views import login_view,teacher_dashboard,faculty_subjects,subject_students,mark_attendance
urlpatterns = [
    path('', login_view, name='login'),  # Login page
    path('dashboard/', teacher_dashboard, name='teacher_dashboard'),  # Teacher dashboard
    path('faculty/<int:faculty_id>/', faculty_subjects, name='faculty_subjects'),
    path('subject/<int:subject_id>/', subject_students, name='subject_students'),
    path('subject/<int:subject_id>/mark-attendance/', mark_attendance, name='mark_attendance'),
]
