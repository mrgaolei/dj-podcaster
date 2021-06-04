from django.conf.urls import include, url, re_path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles import views
from podcast import views as podcast_views

admin.autodiscover()

admin.site.site_header = "Apple Podcast Feed 管理器"

urlpatterns = [
               # Examples:
               # url(r'^$', 'djpodcaster.views.home', name='home'),
               url(r'^tinymce/', include('tinymce.urls')),
               url(r'^$', podcast_views.home),
               url(r'^podcast/', include('podcast.urls')),

               # Uncomment the admin/doc line below to enable admin documentation:
               # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

               # Uncomment the next line to enable the admin:
               url(r'^admin/', admin.site.urls),
               re_path(r'^static/(?P<path>.*)$', views.serve),
               ]
