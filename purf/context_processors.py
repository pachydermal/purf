def getStudent(request):
    from purf_app.models import Student
    try:
        student = Student.objects.get(netid=request.user.username)
    except:
        student = None

    return { 'student': student}