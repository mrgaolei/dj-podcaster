from datetime import datetime
from django.shortcuts import render, get_object_or_404
from podcast.models import Feed, Podcast

def home(request):
	return render(request, 'index.html')

def showfeed(request, filename):
	feed = get_object_or_404(Feed, filename=filename)
	podcasts = Podcast.objects.filter(feeds=feed)
	return render(request, "podcast/feed.html", {'feed':feed,'podcasts':podcasts,'now':datetime.now()})
