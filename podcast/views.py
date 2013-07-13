from django.http import HttpResponse
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from podcast.models import Feed, Podcast
from datetime import datetime

# Create your views here.
def showfeed(request, filename):
	feed = get_object_or_404(Feed, filename=filename)
	podcasts = Podcast.objects.filter(feeds=feed)
	return render_to_response("podcast/feed.html", {'feed':feed,'podcasts':podcasts,'now':datetime.now()})