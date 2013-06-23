from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feed(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	its_summary = models.CharField(max_length=255)
	its_author = models.CharField(max_length=255)
	its_image = models.URLField()
	its_subtitle = models.CharField(max_length=255)
	its_keywords = models.CharField(max_length=255)
	its_category = models.CharField(max_length=255)
	copyright = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	creator = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)

class Podcast(models.Model):
	PODCAST_ENCLOSURE_TYPE_MP3 = 1
	PODCAST_ENCLOSURE_TYPE_M4A = 2
	PODCAST_ENCLOSURE_TYPE = (
		(PODCAST_ENCLOSURE_TYPE_MP3, 'MP3'),
		(PODCAST_ENCLOSURE_TYPE_M4A, 'M4A'),
	)
	PODCAST_EXPLICIT_CLEAN = 1
	PODCAST_EXPLICIT = (
		(PODCAST_EXPLICIT_CLEAN, 'clean'),
	)

	title = models.CharField(max_length=255)
	duration = models.IntegerField()
	enclosure_url = models.URLField()
	enclosure_len = models.IntegerField()
	enclosure_type = models.SmallIntegerField(choices=PODCAST_ENCLOSURE_TYPE,default=PODCAST_ENCLOSURE_TYPE_M4A)
	subtitle = models.TextField()
	summary = models.TextField()
	author = models.CharField()
	explicit = models.SmallIntegerField(choices=PODCAST_EXPLICIT,default=PODCAST_EXPLICIT_CLEAN)
	tags = models.ManyToManyField(Tag)
	creator = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)