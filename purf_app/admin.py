from django.contrib import admin
from purf_app.models import Student, Professor

class ChoiceInline(admin.ModelAdmin):
    list_display = ('name', 'email')

class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')

admin.site.register(Professor, PollAdmin)
admin.site.register(Student, ChoiceInline)