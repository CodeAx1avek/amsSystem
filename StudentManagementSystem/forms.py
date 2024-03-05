from django.contrib.auth.models import User
from django import forms
from .models import Teacher,Faculty

class TeacherForm(forms.ModelForm):
    faculties = forms.ModelMultipleChoiceField(queryset=Faculty.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Teacher
        fields = ['user', 'faculties']
from .models import Attendance

