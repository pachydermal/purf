from django.shortcuts import render, render_to_response
from purf_app.models import Professor, Student, User, Rating, Project, Department
from purf_app.forms import StudentForm, ShortProfessorForm, MessageForm,ShortStudentForm, ProfessorForm, EditProfessorForm, EditStudentForm, RatingForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import random

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

    research_areas = ['CHM', 'COS', 'ELE', 'MOL']
    try:
        if student and student.department:
            department = Department.objects.get(name=student.department)
        else:
            department = Department.objects.get(name='COS')
        research_areas = department.research_areas.split(';')
    except Department.DoesNotExist:
        print 'Department does not exist'
    try:
        mod = Professor.unmoderated_objects.get(netid=request.user.username)
        context = {'results':results, 'research_areas':research_areas, 'new':new, 'sForm': sForm, 'pForm':pForm, 'student':student}
        return render_to_response('mod.html', context, context_instance=RequestContext(request))
    except:
        context = {'results':results, 'research_areas':research_areas, 'new':new, 'sForm': sForm, 'pForm':pForm, 'student':student}

        return render_to_response('index.html', context, context_instance=RequestContext(request))
    context = {'results':results, 'research_areas':research_areas, 'new':new, 'sForm': sForm, 'pForm':pForm, 'student':student}
    return render_to_response('index.html', context, context_instance=RequestContext(request))


def department_text (dept):
    if dept == 'COS':
        return "Computer Science"
    elif dept == 'ELE':
        return "Electrical Engineering"
    elif dept == 'MOL':
        return "Molecular Biology"
    elif dept == 'CHM':
        return "Chemistry"
    else:
        return "Princeton Undergraduate Research Finder"


@login_required
def search (request, query):
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

    results = []

    research_areas = []
    try:
        if student and student.department:
            department = Department.objects.get(name=student.department)
        else:
            department = Department.objects.get(name='COS')
        research_areas = department.research_areas.split(';')
    except Department.DoesNotExist:
        print 'Department does not exist'

    department = department_text(student.department)

    context = {'results':results, 'department': department, 'research_areas':research_areas, 'student':student}
    return render(request, 'search.html', context)

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

    rating = {
        "responsive": 0,
        "frequency": 0,
        "idea_input": 0,
        # starting error value is 30 percent of the bar
        "error1": 15,
        "error2": 15,
        "error3": 15,
    }
    comments = []

    length = 0.0
    for item in Rating.objects.filter(professor=prof.id):
        # The times 10 is to convert the 1-5 scale to a 10-50 scale
        rating["responsive"] += float(item.responsive) * 10
        rating["frequency"] += float(item.frequency) * 10
        rating["idea_input"] += float(item.idea_input) * 10
        comments.append(item.comments)
        length += 1

    if (length > 0):
        random.seed(rating["responsive"])
        rating["error1"] = (rating["error1"] + random.randint(-5, 5)) / (float (length + 1) / 3);
        random.seed(rating["frequency"])
        rating["error2"] = (rating["error2"] + random.randint(-5, 5)) / (float (length + 1) / 3);
        random.seed(rating["idea_input"])
        rating["error3"] = (rating["error3"] + random.randint(-5, 5)) / (float (length + 1) / 3);

    if length > 0:
        # the minus error is so the error affects both sides of the bar
        random.seed(rating["responsive"])
        rating["responsive"] = rating["responsive"]/length - (rating["error1"] / 2) + random.randint(-2, 2)
        random.seed(rating["frequency"])
        rating["frequency"] = rating["frequency"]/length - (rating["error2"] / 2) + random.randint(-2, 2)
        random.seed(rating["idea_input"])
        rating["idea_input"] = rating["idea_input"]/length - (rating["error3"] / 2) + random.randint(-2, 2)

        rating["responsive"] = 49 if rating["responsive"] > 49 else rating["responsive"]
        rating["frequency"] = 49 if rating["frequency"] > 49 else rating["frequency"]
        rating["idea_input"] = 49 if rating["idea_input"] > 49 else rating["idea_input"]
    else:
        rating = None

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
    formInvalid = False
    #ALLOW EDITING
    eForm = EditProfessorForm(instance=myProf)
    if request.method == 'POST':
        eForm = EditProfessorForm(request.POST, instance=myProf)
        if eForm.is_valid():
            eForm.save()
            myProf.moderated_object.approve(reason='Professor already exists, editing profile') #CHANGE MODERATED_BY PERSON!!
            return HttpResponseRedirect('/profile/'+str(request.user.username))
        else:
            formInvalid = True
    #else:
    #    eForm = EditProfessorForm(instance=myProf)
    messageForm = MessageForm()
    context ={'prof': prof, 'messageForm':messageForm, 'department': department, 'rating': rating, 'comments': comments, 'project': project, 'research': research, 'areas': areas, 'topics': topics, 'isFavorited': isFavorited, 'eForm': eForm, 'url':url, 'formInvalid':formInvalid}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

@login_required
def message(request,id):
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
    print id
    prof = Professor.objects.get(netid=id)

    if request.method == 'POST':
        send_mail('PURF - IW Request from ' + student.name, request.POST.__getitem__('message') + '\n \n This is an automated message from PURF: Princeton Undergraduate Research Finder, sent by ' + student.netid + '@princeton.edu . \n purf.herokuapp.com \n Please delete PURF from your email chain for further correspondence.', 'from@example.com', [prof.email, student.email], fail_silently=False)
    return HttpResponseRedirect('/profile/' + prof.netid)
    
@login_required
def rating(request):
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
        print "IN POST!"
        rForm = RatingForm(request.POST)
        if rForm.is_valid():
            rForm.save()
            return HttpResponseRedirect('/')
    else:
        rForm = RatingForm()

    context = {'rForm':rForm}
    return render(request, 'rating.html', context)
    
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
def del_prof2(request,id):
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
    return HttpResponseRedirect('/profile/'+str(id))

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
    isProfessor = False
    try:
        student = Student.objects.get(netid=request.user.username)
    except Student.DoesNotExist:
        try:
            student = Professor.objects.get(netid=request.user.username)
            isProfessor = True
        except Professor.DoesNotExist:
            student = None
    if student == None:
        return HttpResponseRedirect('/')
    formInvalid = False
    if isProfessor:
        return HttpResponseRedirect('/profile/'+str(request.user.username))
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
                formInvalid = True
    else:
        form = StudentForm()
        profForm = ProfessorForm()
        eForm = EditStudentForm(instance=student)
    context ={'form': form, 'profForm': profForm, 'eForm': eForm, 'student': student, 'formInvalid': formInvalid}
    return render(request, 'student.html', context)
