from django import forms
from purf_app.models import Professor, Student, Rating, Project, User
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm

class EditStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('name','department','year','research_interests',)
        
class EditProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = ('name','office','phone','website_link','description','research_areas','research_topics','full',)
        
class StudentForm(ModelForm):
    class Meta:
        model = Student
        #fields = '__all__'

class ProfessorForm(BaseModeratedObjectForm):
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

class MessageForm(forms.Form):
        message = forms.CharField(max_length=20000,widget=forms.Textarea(attrs={'rows':6,'cols':80}))
		
class RatingForm(ModelForm):
	class Meta:
		model = Rating