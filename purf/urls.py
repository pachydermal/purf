from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('purf_app.urls')),
    url(r'^accounts/login/$', include('django_cas.views.login')),
	url(r'^accounts/logout/$', include('django_cas.views.logout')),
)
