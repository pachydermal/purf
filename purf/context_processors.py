def getStudent(request):
#	global myStudent
#	global myProfessor
	from purf_app.models import Student, Professor
	try:
		student = Student.objects.get(netid=request.user.username)
	except Student.DoesNotExist:
		student = None
		try:
			professor = Professor.objects.get(netid=request.user.username)
		except Professor.DoesNotExist:
			professor = None
	if student != None:
		professor = None

	return { 'student': student, 'professor': professor,}