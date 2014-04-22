from django.contrib import admin
from purf_app.models import Student, Professor, Rating, Project

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class ProfAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')

#class UserProfileAdmin(admin.ModelAdmin):
#    list_display = ('name', 'image')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('professor', 'overall')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('professor', 'student_name', 'project_title')

admin.site.register(Professor, ProfAdmin)
admin.site.register(Student, StudentAdmin)
#admin.site.register(User, UserAdmin)
admin.site.register(Rating, RatingAdmin)
#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Project, ProjectAdmin)
