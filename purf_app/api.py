from tastypie.resources import ModelResource
from purf_app.models import Professor, Student

class ProfessorResource(ModelResource): 
	class Meta: 
		queryset = Professor.objects.all()
		resource_name = "professor"
        allowed_methods = ['post', 'get', 'patch', 'delete']
        always_return_data = True