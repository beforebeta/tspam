from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tspam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/admin', permanent=False)),
    url(r'^inspiration/$', view="inspiration.views.home"),
    url(r'^plant/(?P<plant_id>[0-9]+)/$', view="inspiration.views.plant_popup"),
    url(r'^admin/', include(admin.site.urls)),

)

admin.site.site_header = 'Taunton Spam Scanner'