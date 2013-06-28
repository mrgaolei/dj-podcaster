# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	creator = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class Feed(models.Model):
	filename = models.CharField("文件名", max_length=50, unique=True, help_text="%s*.xml"%settings.FEED_URL)
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	its_summary = models.CharField(max_length=255)
	its_author = models.CharField(max_length=255)
	its_image = models.URLField()
	its_subtitle = models.CharField(max_length=255)
	its_keywords = models.CharField(max_length=255)
	its_category = models.CharField(max_length=255)
	copyright = models.CharField(max_length=255)
	tags = models.ManyToManyField(Tag)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def feed_url(self):
		return "%s%s.xml" % (settings.FEED_URL, self.filename)

	def feed_path(self):
		return "%s%s.xml" % (settings.FEED_PATH, self.filename)

	def build(self):
		pass

	def __unicode__(self):
		return self.title

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

	title = models.CharField("标题", max_length=255)
	duration = models.IntegerField("时长", help_text="单位：秒")
	enclosure_url = models.URLField("节目URL")
	enclosure_len = models.IntegerField("文件大小")
	enclosure_type = models.SmallIntegerField(choices=PODCAST_ENCLOSURE_TYPE,default=PODCAST_ENCLOSURE_TYPE_M4A)
	subtitle = models.TextField("子标题")
	summary = models.TextField("描述")
	author = models.CharField("艺人", max_length=100)
	explicit = models.SmallIntegerField(choices=PODCAST_EXPLICIT,default=PODCAST_EXPLICIT_CLEAN)
	tags = models.ManyToManyField(Tag)
	creator = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = '节目'
		verbose_name_plural = verbose_name