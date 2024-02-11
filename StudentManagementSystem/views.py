from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Class

def home(request):
    return render(request,"home.html")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    user_class = user.student.section
    class_schedule = user_class.time_table
    
    # Calculate attendance summary (you need to implement this logic)
    attendance_summary = calculate_attendance_summary(user)
    
    context = {
        'user': user,
        'class_schedule': class_schedule,
        'attendance_summary': attendance_summary,
    }
    return render(request, 'dashboard.html', context)

def calculate_attendance_summary(user):
    # Placeholder function to calculate attendance summary
    # You should implement the actual logic to calculate attendance summary
    return {
        'total_classes': 20,
        'classes_attended': 18,
        'attendance_percentage': 90,
    }