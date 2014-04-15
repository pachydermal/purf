from django.shortcuts import render, render_to_response
from purf_app.models import Professor, Student, User, Rating, Project
#from perf_app import models

def index(request):
    return render_to_response('index.html')

def profile(request, id):
    prof = Professor.objects.get(pk=id)
    rating = Rating.objects.filter(professor=id)
    project = Project.objects.filter(professor=id)
    if prof.research_links: research = prof.research_links.split(';')
    else: research = []
    if prof.research_areas: areas = prof.research_areas.split(';')
    else: areas = []
    if prof.research_topics: topics = prof.research_topics.split(';')
    else: topics = []
    context ={'prof': prof, 'rating': rating, 'project': project, 'research': research, 'areas': areas, 'topics': topics}
    return render(request, 'profile.html', context)

def student(request, id):
	student = Student.objects.get(pk=id)
	user = User.objects.get(student=id)
	favorited_professors = user.favorited_professors
	context ={'student':student, 'favorited_professors':favorited_professors}
	return render(request, 'student.html', context)


# Create your views here.
