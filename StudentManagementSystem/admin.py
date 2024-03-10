from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models import Subject, Attendance, Teacher, Class, Student

class DateListFilter(admin.DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = _('Date')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'date', 'status']  # Display these fields in the admin list view
    list_filter = [
        ('date', DateListFilter),  # Filter by date using custom DateListFilter
        'status',
        'subject',
        'student'
    ]  

    def year(self, obj):
        return obj.date.year

    def month(self, obj):
        return obj.date.strftime('%B')  # Month name

    def day(self, obj):
        return obj.date.strftime('%d')  # Day of the month

    year.short_description = 'Year'
    month.short_description = 'Month'
    day.short_description = 'Day'

admin.site.register(Student)
admin.site.register(Attendance, AttendanceAdmin)  # Register Attendance model with custom admin class
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Teacher)
