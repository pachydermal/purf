from django.shortcuts import render, render_to_response
from purf_app.models import Professor
from purf_app.models import Student, User
#from perf_app import models

def index(request):
    return render_to_response('index.html')

def profile(request, id):
    prof = Professor.objects.get(pk=id)
    context ={'prof': prof}
    return render(request, 'profile.html', context)

def student(request, id):
	student = Student.objects.get(pk=id)
	user = User.objects.get(student=id)
	favorited_professors = user.favorited_professors
	context ={'student':student, 'favorited_professors':favorited_professors}
	return render(request, 'student.html', context)


# Create your views here.
