from tastypie.resources import ModelResource, ALL
from django.db.models import Q
from purf_app.models import Professor, Student
from django.db import connection, transaction
from moderation import moderation
import operator
import ast

class ProfessorResource(ModelResource): 
    class Meta:
        queryset = Professor.objects.all()

        # exclude unmoderated professors
        cursor = connection.cursor()
        cursor.execute('SELECT object_pk FROM moderation_moderatedobject WHERE moderation_status=2')
        for prof in cursor.fetchall():
            queryset = queryset.exclude(pk=str(prof)[1:-2])

        resource_name = "professor"
        allowed_methods = ['get']
        always_return_data = True

class SearchProfessorResource(ModelResource):
    class Meta:
        queryset = Professor.objects.all()

        # exclude unmoderated professors
        cursor = connection.cursor()
        cursor.execute('SELECT object_pk FROM moderation_moderatedobject WHERE moderation_status=2')
        for prof in cursor.fetchall():
            queryset = queryset.exclude(pk=str(prof)[1:-2])

        # allowed fields in query url
        filtering = {
            "department": ('exact'),
            "name": ('exact', 'startswith',),
            "research_areas": ('exact'),
        }
        resource_name = "search"
        allowed_methods = ['get']
        always_return_data = True

    # build filters for selecting over professors
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(SearchProfessorResource, self).build_filters(filters)
        filters_dict = dict(filters.iterlists())
        qsets = []

        # build filters for search box terms
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

        # build filters for refine research area checkboxes
        rasets = []
        if('research_areas' in filters_dict.keys()):
            research_areas = filters_dict['research_areas']
            for ra in research_areas:
                raset = (
                    Q(research_areas__icontains=ra) |
                    Q(department__icontains=ra)
                    )
                rasets.append(raset)
        orm_filters.update({'ras': rasets})
        return orm_filters

    # apply filters over professor data
    def apply_filters(self, request, applicable_filters):
        # ignore default research_areas tastypie filtering
        if 'research_areas__exact' in applicable_filters:
            applicable_filters.pop('research_areas__exact')

        # grab search term related filters
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        # grab refine research area related filters
        if 'ras' in applicable_filters:
            ras = applicable_filters.pop('ras')
        else:
            ras = None

        
        semi_filtered = super(SearchProfessorResource, self).apply_filters(request, applicable_filters)

        # apply search term filters
        if custom:
            query = custom.pop()
            for i in custom:
                query |= i
            semi_filtered = semi_filtered.filter(query)

        # apply refine research area filters
        if ras:
            ra = ras.pop()
            for i in ras:
                ra |= i
            semi_filtered = semi_filtered.filter(ra)

        return semi_filtered
