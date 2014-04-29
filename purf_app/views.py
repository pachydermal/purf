from django.shortcuts import render, render_to_response
from purf_app.models import Professor, Student, User, Rating, Project, Department
from purf_app.forms import StudentForm, ShortProfessorForm, ShortStudentForm, ProfessorForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    results = []

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

    try:
        department = Department.objects.get(name=student.department)
    except Department.DoesNotExist:
        print 'Department does not exist'

    research_areas = department.research_areas.split(';')
    
    try:
        mod = Professor.unmoderated_objects.get(netid=request.user.username)
        context = {'results':results, 'research_areas':research_areas, 'new':new, 'sForm': sForm, 'pForm':pForm, 'student':student}
        return render_to_response('mod.html', context, context_instance=RequestContext(request))
    except:
        context = {'results':results, 'research_areas':research_areas, 'new':new, 'sForm': sForm, 'pForm':pForm, 'student':student}
        return render_to_response('major.html', context, context_instance=RequestContext(request))

    context = {'results':results, 'research_areas':research_areas, 'new':new, 'sForm': sForm, 'pForm':pForm, 'student':student}
    return render_to_response('major.html', context, context_instance=RequestContext(request))

@login_required
def profile(request, id):
    #Prevent unidentified user from accessing any part of the site
    try:
        student = Student.objects.get(netid=request.user.username)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(netid=request.user.username)
        except Professor.DoesNotExist:
            student = None
    if student == None:
        return HttpResponseRedirect('/')
    prof = Professor.objects.get(netid=id)

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
			
	try:
		myProf = Professor.objects.get(netid=request.user.username)
	except:
		myProf = None
	url = '/profile/'+str(request.user.username)
	
	#ALLOW EDITING
	if request.method == 'POST':
		eForm = EditProfessorForm(request.POST, instance=myProf)
		if eForm.is_valid():
			eForm.save()
			return HttpResponseRedirect('/profile/'+str(request.user.username))
	else:
		eForm = EditProfessorForm(instance=myProf)
		
		
    context ={'prof': prof, 'department': department, 'rating': rating, 'project': project, 'research': research, 'areas': areas, 'topics': topics, 'isFavorited': isFavorited, 'eForm': eForm, 'url':url}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

@login_required
def del_prof(request,id):
    #Prevent unidentified user from accessing any part of the site
    try:
        student = Student.objects.get(netid=request.user.username)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(netid=request.user.username)
        except Professor.DoesNotExist:
            student = None
    if student == None:
        return HttpResponseRedirect('/')

    prof = Professor.objects.get(netid =id )
    student = Student.objects.get(netid=request.user.username)
    student.favorited_professors.remove(prof)
    return HttpResponseRedirect('/account/')

@login_required
def fav_prof(request,id):
    #Prevent unidentified user from accessing any part of the site
    try:
        student = Student.objects.get(netid=request.user.username)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(netid=request.user.username)
        except Professor.DoesNotExist:
            student = None
    if student == None:
        return HttpResponseRedirect('/')

    prof = Professor.objects.get(netid=id)
    try:
        student = Student.objects.get(netid=request.user.username)
        student.favorited_professors.add(prof)
    except:
        print 'hi'
    return HttpResponseRedirect('/profile/'+str(id))

@login_required
def new_prof(request):
    #Prevent unidentified user from accessing any part of the site
    try:
        student = Student.objects.get(netid=request.user.username)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(netid=request.user.username)
        except Professor.DoesNotExist:
            student = None
    if student == None:
        return HttpResponseRedirect('/')

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

@login_required
def student(request):
    #Prevent unidentified user from accessing any part of the site
	try:
		student = Student.objects.get(netid=request.user.username)
	except Student.DoesNotExist:
		try:
			student = Professor.objects.get(netid=request.user.username)
		except Professor.DoesNotExist:
			student = None
	if student == None:
		return HttpResponseRedirect('/')
		
	if request.method == 'POST':
		form = StudentForm(request.POST)
		profForm = ProfessorForm(request.POST)
		eForm = EditStudentForm(request.POST, instance=student)
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
		elif 'edit' in request.POST:
			if eForm.is_valid():
				eForm.save()
				return HttpResponseRedirect('/account/')
	else:
		form = StudentForm()
		profForm = ProfessorForm()
		eForm = EditStudentForm(instance=student)
		
	context ={'form': form, 'profForm': profForm, 'eForm': eForm, 'student': student}
	return render(request, 'student.html', context)
    


