from django.conf.urls import patterns, include, url

from purf_app import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	# (r'^login/$', 'django_cas.views.login'),
	# (r'^logout/$', 'django_cas.views.logout'),
)