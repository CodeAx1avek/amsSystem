from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Subject,Student
from django.http import HttpResponseRedirect
from django.urls import reverse
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
    faculties = teacher.faculties.all()

    # Fetch attendance report for all subjects taught by the teacher
    attendance_report = Subject.objects.filter(teacher=teacher).annotate(total_attendance=Count('attendance'))

    # Fetch present students for all subjects taught by the teacher
    present_students = Student.objects.filter(
        section__subjects__in=Subject.objects.filter(teacher=teacher),
        attendance__status='Present'
    ).distinct()

    # Fetch absent students for all subjects taught by the teacher
    absent_students = Student.objects.filter(
        section__subjects__in=Subject.objects.filter(teacher=teacher),
        attendance__status='Absent'
    ).distinct()

    return render(request, 'teacher_dashboard.html', {
        'teacher': teacher,
        'faculties': faculties,
        'attendance_report': attendance_report,
        'present_students': present_students,
        'absent_students': absent_students
    })


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
            return HttpResponseRedirect(reverse('subject_students', args=[subject_id]))

        students = Student.objects.filter(section__subjects=subject)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['Present', 'Absent']:
                # Create attendance record
                Attendance.objects.create(
                    student=student,
                    subject=subject,
                    status=status,
                    date=timezone.now()  # Save the current date
                )
        
        messages.success(request, 'Attendance saved successfully.')
        return HttpResponseRedirect(reverse('subject_students', args=[subject_id]))

    # If the request method is not POST, redirect to subject_students view
    return redirect('subject_students', subject_id=subject_id)