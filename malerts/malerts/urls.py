from django.conf.urls import patterns, include, url
# TASTYPIE API
from tastypie.api import Api
from gtfs.api import AlertResource

v1_api = Api(api_name='v1')
v1_api.register(AlertResource())

# GENERIC VIEWS
from gtfs.views import IndexView, DetailView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'malerts.views.home', name='home'),
	# url(r'^malerts/', include('malerts.foo.urls')),
	
	# url(r'^$', 'gtfs.views.alerts_html'),
	url(r'^alert.asciipb$', 'gtfs.views.alerts_ascii'),
	url(r'^api/', include(v1_api.urls)),

	url(r'^$',
		IndexView.as_view(),
		name='index'),

	url(r'^(?P<pk>\d+)/$',
		DetailView.as_view(),
		name="detail"),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# admin addons
	url(r'^grappelli/', include('grappelli.urls')),
	url(r'^ckeditor/', include('ckeditor.urls')),
	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
