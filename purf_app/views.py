from django.shortcuts import render, render_to_response
from purf_app.models import Professor, Student, User, Rating, Project
from purf_app.forms import StudentForm
from django.http import HttpResponseRedirect
#from perf_app import models

def index(request):
    return render(request, 'index.html')

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

def student(request):
    try:   
        print 'try'
        student = Student.objects.get(user=request.user.id)
    except Student.DoesNotExist:
        print 'except'
        student = None
    
    if request.method == 'POST':
        print request.POST.get('name', '')
        form = StudentForm(request.POST)
        print 'if'
        if form.is_valid():
            print 'valid'
            temp_post = form.save(commit=False)
            temp_post.user = request.user
            temp_post.save()
            return HttpResponseRedirect('/account/')
    else:
        print 'else'
        form = StudentForm()
    
    
    context ={'form': form, 'student':student}
    
    return render(request, 'student.html', context)
    


