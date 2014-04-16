from django.conf.urls import patterns, include, url
from tastypie.api import Api
from purf_app.api import ProfessorResource

from purf_app import views


v1_api = Api(api_name='v1')
v1_api.register(ProfessorResource())

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	(r'^login/$', 'django_cas.views.login'),
	(r'^logout/$', 'django_cas.views.logout'),
    (r'^api/', include(v1_api.urls)),
    url(r'^profile/(?P<id>\d+)', views.profile, name='profile'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media'}),
	url(r'^account/', views.student, name='student'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media'}),
)
