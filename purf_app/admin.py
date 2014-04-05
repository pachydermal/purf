from django.contrib import admin
from purf_app.models import Student, Professor

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class ProfAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')

admin.site.register(Professor, ProfAdmin)
admin.site.register(Student, StudentAdmin)
