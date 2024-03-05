from django.contrib import admin
from .models import Faculty, Subject, Attendance, Teacher, Class, Student
from .forms import TeacherForm
from django import forms

class ClassAdminForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['branch', 'section', 'year', 'no_of_students', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple for multiple selections
        }

class ClassAdmin(admin.ModelAdmin):
    form = ClassAdminForm

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm

admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Subject)
admin.site.register(Class, ClassAdmin)
admin.site.register(Teacher, TeacherAdmin)
