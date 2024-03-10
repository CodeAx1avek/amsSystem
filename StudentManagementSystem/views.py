from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Teacher, Subject, Student, Attendance

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    teacher = request.user.teacher
    subjects = Subject.objects.filter(teacher=teacher)
    
    # Retrieve students associated with the subjects taught by the teacher
    students = Student.objects.filter(section__subjects__in=subjects)
    
    # Retrieve attendance records for each student and sort them by date
    student_reports = []
    processed_combinations = set()  # Keep track of processed combinations
    
    for student in students:
        for subject in subjects:
            # Check if the combination has been processed already
            combination = (student.id, subject.id)
            if combination not in processed_combinations:
                attendance_records = Attendance.objects.filter(student=student, subject=subject).order_by('date')
                if attendance_records:
                    student_reports.append({'student': student, 'subject': subject, 'attendance_records': attendance_records})
                    processed_combinations.add(combination)
    
    return render(request, 'dashboard.html', {'subjects': subjects, 'student_reports': student_reports})


@login_required
def export_attendance(request):
    teacher = request.user.teacher
    subjects = Subject.objects.filter(teacher=teacher)
    
    # Retrieve students associated with the subjects taught by the teacher
    students = Student.objects.filter(section__subjects__in=subjects)
    
    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.append(['Student Name', 'Roll No', 'Subject', 'Date', 'Status'])
    
    # Iterate through each student and subject combination
    for student in students:
        for subject in subjects:
            # Retrieve attendance records for the current student and subject combination
            attendance_records = Attendance.objects.filter(student=student, subject=subject).order_by('date')
            
            # Write attendance records to the worksheet
            for record in attendance_records:
                ws.append([student.name, student.roll_no, subject.subject_name, record.date, record.status])
    
    # Save the workbook to a response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendance.xlsx'
    wb.save(response)
    
    return response
@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def subject_details(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    students = Student.objects.filter(section__subjects=subject)
    existing_attendance = Attendance.objects.filter(subject=subject, date=timezone.now().date()).exists()
    
    if request.method == 'POST':
        if existing_attendance:
            messages.warning(request, 'Attendance for today has already been saved.')
            return redirect('subject_details', subject_id=subject_id)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['Present', 'Absent']:
                Attendance.objects.create(
                    student=student,
                    subject=subject,
                    date=timezone.now().date(),
                    status=status
                )
        messages.success(request, 'Attendance saved successfully.')
        return redirect('subject_details', subject_id=subject_id)
    
    return render(request, 'subject_details.html', {'subject': subject, 'students': students, 'attendance_saved': existing_attendance})