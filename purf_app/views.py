from django.shortcuts import render, render_to_response
from purf_app.models import Professor, Student, User, Rating, Project
from purf_app.forms import StudentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
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
    
    student = Student.objects.get(user=request.user.id)
    #print student.favorited_professors.filter(pk=id).exists()
    isFavorited = student.favorited_professors.filter(pk=id).exists()
    context ={'prof': prof, 'rating': rating, 'project': project, 'research': research, 'areas': areas, 'topics': topics, 'isFavorited' : isFavorited}
    return render(request, 'profile.html', context)

def del_prof(request,id):
    prof = Professor.objects.get(pk =id )
    student = Student.objects.get(user=request.user.id)
    student.favorited_professors.remove(prof)
    return HttpResponseRedirect('/account/')
    
def fav_prof(request,id):
    prof = Professor.objects.get(pk =id )
    student = Student.objects.get(user=request.user.id)
    student.favorited_professors.add(prof)
    return HttpResponseRedirect('/profile/'+str(id))
    
def student(request):
    try:   
        student = Student.objects.get(user=request.user.id)
    except Student.DoesNotExist:
        student = None
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            temp_post = form.save(commit=False)
            temp_post.user = request.user
            temp_post.save()
            form.save_m2m()
            return HttpResponseRedirect('/account/')
    else:
        form = StudentForm()
    
    
    context ={'form': form, 'student':student}
    
    return render(request, 'student.html', context)
    


