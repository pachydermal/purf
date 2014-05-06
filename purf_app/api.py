from tastypie.resources import ModelResource, ALL
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
        qsets = []

        if('query' in filters_dict.keys()):
            query = filters_dict['query']
            for q in query:
                qset = (
                    Q(name__icontains=q) |
                    Q(department__icontains=q) |
                    Q(email__icontains=q) |
                    Q(research_areas__icontains=q)
                    )
                qsets.append(qset)
        orm_filters.update({'custom': qsets})


        rasets = []
        if('research_areas' in filters_dict.keys()):
            research_areas = filters_dict['research_areas']
            for ra in research_areas:
                raset = (
                    Q(research_areas__icontains=ra) |
                    Q(research_areas__iexact=ra)
                    )
                rasets.append(raset)
        orm_filters.update({'ras': rasets})
        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'research_areas__exact' in applicable_filters:
            applicable_filters.pop('research_areas__exact')

        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        if 'ras' in applicable_filters:
            ras = applicable_filters.pop('ras')
        else:
            ras = None


        semi_filtered = super(SearchProfessorResource, self).apply_filters(request, applicable_filters)
        if custom:
            query = custom.pop()
            for i in custom:
                query |= i
            semi_filtered = semi_filtered.filter(query)

        if ras:
            ra = ras.pop()
            for i in ras:
                ra |= i
            semi_filtered = semi_filtered.filter(ra)

        return semi_filtered
