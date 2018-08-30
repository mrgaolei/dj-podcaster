from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from podcast import views as podcast_views

admin.autodiscover()

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
               ]
