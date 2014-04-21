from django import forms
from purf_app.models import Professor, Student, Rating, Project, User
from django.forms import ModelForm
'''
class StudentForm(forms.Form):
    name = forms.CharField(max_length=200)

'''
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'
