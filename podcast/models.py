# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from datetime import datetime
# Create your models here.

class Feed(models.Model):
	filename = models.CharField("文件名", max_length=50, unique=True, help_text="%s*.xml"%settings.FEED_URL, validators=[validate_slug])
	admins = models.ManyToManyField(User, verbose_name="可发布人", help_text="管理员拥有全部Feed发布权")
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	its_summary = models.CharField(max_length=255)
	its_author = models.CharField(max_length=255)
	its_image = models.ImageField("播客封面", upload_to="feed")
	its_owner_name = models.CharField(max_length=255)
	its_owner_email = models.EmailField()
	its_subtitle = models.CharField(max_length=255)
	its_keywords = models.CharField(max_length=255)
	its_category = models.CharField(max_length=255)
	its_subcategory = models.CharField(max_length=255, blank=True)
	copyright = models.CharField(max_length=255)
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

	class Meta:
		verbose_name = '播客'
		verbose_name_plural = verbose_name

class Podcast(models.Model):
	PODCAST_ENCLOSURE_TYPE_MP3 = 1
	PODCAST_ENCLOSURE_TYPE_M4A = 2
	PODCAST_ENCLOSURE_TYPE = (
		(PODCAST_ENCLOSURE_TYPE_MP3, 'audio/mpeg'),
		(PODCAST_ENCLOSURE_TYPE_M4A, 'audio/x-m4a'),
	)
	PODCAST_EXPLICIT_CLEAN = 0
	PODCAST_EXPLICIT_YES = 1
	PODCAST_EXPLICIT_NO = 2
	PODCAST_EXPLICIT = (
		(PODCAST_EXPLICIT_CLEAN, 'clean'),
		(PODCAST_EXPLICIT_YES, 'yes'),
		(PODCAST_EXPLICIT_NO, 'no'),
	)

	title = models.CharField("标题", max_length=255)
	description = models.CharField(max_length=255)
	duration = models.IntegerField("时长", help_text="单位：秒")
	enclosure_url = models.URLField("节目URL")
	enclosure_len = models.IntegerField("文件大小",help_text="单位：字节")
	enclosure_type = models.SmallIntegerField(choices=PODCAST_ENCLOSURE_TYPE,default=PODCAST_ENCLOSURE_TYPE_M4A)
	its_image = models.ImageField("节目封面", upload_to="podcast")
	its_subtitle = models.TextField("子标题")
	its_summary = models.TextField("描述")
	its_author = models.CharField("艺人", max_length=100)
	its_explicit = models.SmallIntegerField(choices=PODCAST_EXPLICIT,default=PODCAST_EXPLICIT_CLEAN)
	feeds = models.ManyToManyField(Feed)
	creator = models.ForeignKey(User)
	active = models.BooleanField("上线",default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	pubdate = models.DateTimeField("发布时间",default=datetime.now())

	def enclosure_type_str(self):
		for r in self.PODCAST_ENCLOSURE_TYPE:
			if r[0] == self.enclosure_type:
				return r[1]

	def its_explicit_str(self):
		for r in self.PODCAST_EXPLICIT:
			if r[0] == self.its_explicit:
				return r[1]

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = '节目'
		verbose_name_plural = verbose_name