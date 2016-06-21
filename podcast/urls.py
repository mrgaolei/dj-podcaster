from django.conf.urls import url
from podcast import views

urlpatterns = [
    url(r'^feed/(?P<filename>.*)\.xml$', views.showfeed),
]
