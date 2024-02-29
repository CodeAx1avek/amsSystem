from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core.cache import cache
from datetime import date
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Subject,Student
from .models import Attendance
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            pass
    return render(request, 'login.html')


@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    faculties = teacher.faculties.all()  # Assuming faculties is a ManyToManyField in the Teacher model
    return render(request, 'teacher_dashboard.html', {'teacher': teacher, 'faculties': faculties})

@login_required
def faculty_subjects(request, faculty_id):
    teacher = request.user.teacher
    faculty = teacher.faculties.get(id=faculty_id)
    subjects = Subject.objects.filter(faculty=faculty, teacher=teacher)
    return render(request, 'faculty_subjects.html', {'faculty': faculty, 'subjects': subjects})

@login_required
def subject_students(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    students = Student.objects.filter(section__subjects=subject)
    return render(request, 'subject_students.html', {'subject': subject, 'students': students})

@login_required
def mark_attendance(request, subject_id):
    if request.method == 'POST':
        subject = get_object_or_404(Subject, id=subject_id)
        
        # Check if attendance is already submitted for today
        existing_attendance = Attendance.objects.filter(subject=subject, date=timezone.now().date()).exists()
        if existing_attendance:
            messages.warning(request, 'Attendance already submitted for today.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        students = Student.objects.filter(section__subjects=subject)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['Present', 'Absent']:
                # Create or update attendance record
                attendance, _ = Attendance.objects.get_or_create(
                    student=student,
                    subject=subject,
                    defaults={'status': status, 'date': timezone.now()}  # Set the date field
                )
                attendance.status = status
                attendance.save()
        
        messages.success(request, 'Attendance saved successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # If the request method is not POST, redirect to subject_students view
    return redirect('subject_students', subject_id=subject_id)