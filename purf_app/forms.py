from django import forms
from purf_app.models import Professor, Student, Rating, Project, User
from django.forms import ModelForm

class EditStudentForm(ModelForm):
	class Meta:
		model = Student
		fields = {'certificates', 'research_interests','year','department','email','name',}
		
class EditProfessorForm(ModelForm):
	class Meta:
		model = Professor
		fields = {'full', 'research_links', 'research_topics','research_areas','description','website_link','phone','office','email','department','title','name',}
		
class StudentForm(ModelForm):
    class Meta:
        model = Student
        #fields = '__all__'

class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        #fields = '__all__'

class ShortStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('department','year')
        hidden_fields = ('netid','name','email')

class ShortProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = ('department','research_areas')
        hidden_fields = ('netid', 'name', 'email')

