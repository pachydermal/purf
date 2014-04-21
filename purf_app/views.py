from django.shortcuts import render, render_to_response
from purf_app.models import Professor, Student, User, Rating, Project
from purf_app.forms import StudentForm, ProfessorForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
#from perf_app import models

def index(request):
    results = [{'name':'Ira Banks', 'id':1}, {'name':'Lassy Delomina', 'id':2}]
    research_areas = ['Bleh', 'Blah', 'Blu', 'Blo', 'Blei', 'Blee', 'Blar', 'Blair', 'Blaf', 'Blaz', 'Blarf']

    context = {'results':results, 'research_areas':research_areas, }
    return render(request, 'index.html', context)

def profile(request, id):
    print id
    prof = Professor.objects.get(pk=id)

    try:
        myProfId = Professor.objects.get(user=request.user.id).id
    except:
        myProfId = -1
    print id
    rating = Rating.objects.filter(professor=id)
    project = Project.objects.filter(professor=id)
    if prof.research_links: research = prof.research_links.split(';')
    else: research = []
    if prof.research_areas: areas = prof.research_areas.split(';')
    else: areas = []
    if prof.research_topics: topics = prof.research_topics.split(';')
    else: topics = []
    if prof.department: department = prof.department.split(';')
    else: department = []

    '''try:
        student = Student.objects.get(user=request.user.id)
        isFavorited = student.favorited_professors.filter(pk=id).count()
    except Student.DoesNotExist:
        isFavorited = '-1'
        try:
            student = Professor.objects.get(user=request.user.id)
        except Professor.DoesNotExist:
            student = None'''
    isFavorited = '-1'
    context ={'prof': prof, 'department': department, 'rating': rating, 'project': project, 'research': research, 'areas': areas, 'topics': topics, 'isFavorited' : isFavorited, 'myProfId' : myProfId}
    return render(request, 'profile.html', context)

def del_prof(request,id):
    prof = Professor.objects.get(pk =id )
    student = Student.objects.get(user=request.user.id)
    student.favorited_professors.remove(prof)
    return HttpResponseRedirect('/account/')
    
def fav_prof(request,id):
    prof = Professor.objects.get(pk =id )
    try:
        student = Student.objects.get(user=request.user.id)
        student.favorited_professors.add(prof)
    except:
        print 'hi'
    return HttpResponseRedirect('/profile/'+str(id))

def new_prof(request):
    try:
        student = Student.objects.get(user=request.user.id)
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':
        profForm = ProfessorForm(request.POST)
        if profForm.is_valid():
            temp_post = profForm.save(commit=False)
            temp_post.user = request.user
            temp_post.save()
            return HttpResponseRedirect('/account/')
    else:
        profForm = ProfessorForm()

    form = StudentForm()

    context = {'form':form, 'profForm':profForm}
    return render(request, 'student.html', context)


def student(request):
    try:   
        student = Student.objects.get(user=request.user.id)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(user=request.user.id)
        except Professor.DoesNotExist:
            student = None

    if request.method == 'POST':
        form = StudentForm(request.POST)
        profForm = ProfessorForm(request.POST)
        if 'student' in request.POST:
            if form.is_valid():
                temp_post = form.save(commit=False)
                temp_post.user = request.user
                temp_post.save()
                form.save_m2m()
                return HttpResponseRedirect('/account/')
        elif 'professor' in request.POST:
            if profForm.is_valid():
                temp_post = profForm.save(commit=False)
                temp_post.user = request.user
                temp_post.save()
                profForm.save_m2m()
                me = Professor.objects.get(user=request.user.id)
                return HttpResponseRedirect('/profile/' + str(me.id))
    else:
        form = StudentForm()
        profForm = ProfessorForm()


    context ={'form': form, 'profForm': profForm, 'student': student}
    
    return render(request, 'student.html', context)
    


