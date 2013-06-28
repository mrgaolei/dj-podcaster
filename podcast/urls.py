from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^feed/(?P<filename>.*)\.xml$', 'podcast.views.showfeed'),
)