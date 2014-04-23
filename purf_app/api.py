from tastypie.resources import ModelResource
from django.db.models import Q
from purf_app.models import Professor, Student
import operator

class ProfessorResource(ModelResource): 
	class Meta: 
		queryset = Professor.objects.all()
		resource_name = "professor"
        # allowed_methods = ['post', 'get', 'patch', 'delete']
        allowed_methods = ['get']
        always_return_data = True

class SearchProfessorResource(ModelResource):
    class Meta:
        queryset = Professor.objects.all()
        filtering = {
            "department": ('exact'),
            "name": ('exact', 'startswith',),
            "research_areas": ('exact'),
        }
        resource_name = "search"
        allowed_methods = ['get']
        always_return_data = True

    # def obj_create(self, bundle, request=None, **kwargs):
    #     bundle = super(GoalResource, self).obj_create(
    #         bundle, request, user=request.user)
    #
    #     search_type = bundle.data["type"]
    #     name = bundle.data["name"]
    #     department = bundle.data["department"]


    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(SearchProfessorResource, self).build_filters(filters)
        filters_dict = dict(filters.iterlists())
        if('query' in filters_dict.keys()):
            query = filters_dict['query']
            qsets = []
            filtList = [] 
            for q in query:
                qset = (
                    Q(name__icontains=q) |
                    Q(department__iexact=q) |
                    Q(email__icontains=q) |
                    Q(research_areas__icontains=q)
                    )
                qsets.append(qset)
                filtList.append(set(Professor.objects.filter(qset)))

            orm_filters.update({'custom': qsets})
        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(SearchProfessorResource, self).apply_filters(request, applicable_filters)

        if custom:
            for i in custom:
                print i
                semi_filtered = semi_filtered.filter(i)

        return semi_filtered
