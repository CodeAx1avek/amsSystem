from django.urls import path
from .views import home, login, dashboard, logout, about, subject_details,export_attendance

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('export_attendance/', export_attendance, name='export_attendance'),
    path('about/', about, name='about'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),
    path('subject/<int:subject_id>/', subject_details, name='subject_details'),  # Add this line
]
