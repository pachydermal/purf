from django.conf.urls import patterns, include, url
from tastypie.api import Api
from purf_app.api import ProfessorResource, SearchProfessorResource

from purf_app import views


v1_api = Api(api_name='v1')
v1_api.register(ProfessorResource())
v1_api.register(SearchProfessorResource())

urlpatterns = patterns('',
	url(r'^$', 'django_cas.views.login')
    (r'^$', views.index, name='index'),
	(r'^logout/$', 'django_cas.views.logout'),
    (r'^api/', include(v1_api.urls)),
    url(r'^profile/(?P<id>.+)', views.profile, name='profile'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media'}),
	url(r'^account/', views.student, name='student'),
    url(r'^del_prof/(?P<id>.+)/$', views.del_prof, name='del_prof'),
    url(r'^fav_prof/(?P<id>.+)/$', views.fav_prof, name='fav_prof'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media'}),
)
