from django.conf.urls import patterns, include, url
from tastypie.api import Api
from purf_app.api import ProfessorResource, SearchProfessorResource

from purf_app import views
from moderation.helpers import auto_discover
auto_discover()

v1_api = Api(api_name='v1')
v1_api.register(ProfessorResource())
v1_api.register(SearchProfessorResource())

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	(r'^login/$', 'django_cas.views.login'),
	(r'^logout/$', 'django_cas.views.logout'),
    (r'^api/', include(v1_api.urls)),
    url(r'^search/?(?P<query>.+)', views.search, name='search'),
    url(r'^profile/(?P<id>.+)', views.profile, name='profile'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media'}),
	url(r'^account/', views.student, name='student'),
    url(r'^del_prof/(?P<id>.+)/$', views.del_prof, name='del_prof'),
    url(r'^del_prof2/(?P<id>.+)/$', views.del_prof2, name='del_prof2'),
    url(r'^fav_prof/(?P<id>.+)/$', views.fav_prof, name='fav_prof'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media'}),
)
