from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'serial_configuration.views.port_configuration', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
