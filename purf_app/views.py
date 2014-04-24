from django.shortcuts import render, render_to_response
from purf_app.models import Professor, Student, User, Rating, Project
from purf_app.forms import StudentForm, ShortProfessorForm, ShortStudentForm, ProfessorForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail

def index(request):
    results = []
    research_areas = ['Compilers', 'Computer Security', 'Programming Languages']

    #Check if the first time they logged in
    try:
        student = Student.objects.get(netid=request.user.username)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(netid=request.user.username)
        except Professor.DoesNotExist:
            student = None
    if student == None:
        new = True
    else: new = False

    ##RECEIVE FORM DATA FOR FIRST USERS
    if request.method == 'POST':
        sForm = ShortStudentForm(request.POST)
        pForm = ShortProfessorForm(request.POST)
        if 'student' in request.POST:
            if sForm.is_valid():
                temp_post = sForm.save(commit=False)
                temp_post.netid = request.user.username
                temp_post.email = request.user.username + '@princeton.edu'
                temp_post.name = request.user.username #Fix this later
                temp_post.save()
                return HttpResponseRedirect('/')
        elif 'professor' in request.POST:
            if pForm.is_valid():
                temp_post = pForm.save(commit=False)
                temp_post.netid = request.user.username
                temp_post.email = request.user.username + '@princeton.edu'
                temp_post.name = request.user.username #Fix this later
                temp_post.save()
                return HttpResponseRedirect('/')
    else:
        sForm = ShortStudentForm()
        pForm = ShortProfessorForm()

    context = {'results':results, 'research_areas':research_areas, 'new':new, 'sForm': sForm, 'pForm':pForm, 'student':student}
    return render_to_response('major.html', context, context_instance=RequestContext(request))

def profile(request, id):
	prof = Professor.objects.get(netid=id)
    #try:
    #    myProfId = Professor.objects.get(user=request.user.id).id
    #except:
    #    myProfId = -1
	rating = Rating.objects.filter(professor=prof.id)
	project = Project.objects.filter(professor=prof.id)
	if prof.research_links: research = prof.research_links.split(';')
	else: research = []
	if prof.research_areas: areas = prof.research_areas.split(';')
	else: areas = []
	if prof.research_topics: topics = prof.research_topics.split(';')
	else: topics = []
	if prof.department: department = prof.department.split(';')
	else: department = []
	
	
	try:
		student = Student.objects.get(netid=request.user.username)
	except Student.DoesNotExist:
		student = None
	
	isFavorited = "0"
	if student != None:
		if student.favorited_professors.filter(netid=prof.netid).exists():
			isFavorited = "1"

	
	#isFavorited = '-1'
    #context ={'prof': prof, 'department': department, 'rating': rating, 'project': project, 'research': research, 'areas': areas, 'topics': topics, 'isFavorited' : isFavorited, 'myProfId' : myProfId}
	context ={'prof': prof, 'department': department, 'rating': rating, 'project': project, 'research': research, 'areas': areas, 'topics': topics, 'isFavorited': isFavorited}
	return render_to_response('profile.html', context, context_instance=RequestContext(request))

def del_prof(request,id):
    print id
    prof = Professor.objects.get(netid =id )
    student = Student.objects.get(netid=request.user.username)
    student.favorited_professors.remove(prof)
    return HttpResponseRedirect('/account/')


def fav_prof(request,id):
	prof = Professor.objects.get(netid=id)
	try:
		student = Student.objects.get(netid=request.user.username)
		student.favorited_professors.add(prof)
	except:
		print 'hi'
	return HttpResponseRedirect('/profile/'+str(id))

def new_prof(request):
    try:
        student = Student.objects.get(netid=request.user.username)
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
        student = Student.objects.get(netid=request.user.username)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(netid=request.user.username)
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
                me = Professor.objects.get(netid=request.user.username)
                return HttpResponseRedirect('/profile/' + str(me.id))
    else:
        form = StudentForm()
        profForm = ProfessorForm()


    context ={'form': form, 'profForm': profForm, 'student': student}
    
    return render(request, 'student.html', context)
    


