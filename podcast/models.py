# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from tinymce.models import HTMLField
from datetime import datetime


# Create your models here.

class Category(models.Model):
    text = models.CharField(u"类目", max_length=255)
    subText = models.CharField(u"子类目", max_length=255, blank=True)


class Feed(models.Model):
    filename = models.CharField(u"文件名", max_length=50, unique=True, help_text="%s*.xml" % settings.FEED_URL,
                                validators=[validate_slug])
    domain = models.URLField(u"自定义域名", help_text=u"自定义域名会覆盖系统默认域名", blank=True)
    display_num = models.SmallIntegerField(u"节目展示数", default=100)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u"可发布人", help_text=u"管理员拥有全部Feed发布权")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    its_summary = models.CharField(max_length=255)
    its_author = models.CharField(max_length=255)
    its_image = models.ImageField(u"播客封面", upload_to="feed")
    its_owner_name = models.CharField(max_length=255)
    its_owner_email = models.EmailField()
    its_subtitle = models.CharField(max_length=255)
    its_keywords = models.CharField(max_length=255)
    its_category = models.CharField(max_length=255)
    its_subcategory = models.CharField(max_length=255, blank=True)
    its_categories = models.TextField(u"播客分类xml", default='')
    copyright = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def feed_url(self):
        if self.domain:
            return "%s%s.xml" % (self.domain, self.filename)
        else:
            return "%s%s.xml" % (settings.FEED_URL, self.filename)

    def feed_path(self):
        return "%s%s.xml" % (settings.FEED_PATH, self.filename)

    def build(self):
        pass

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'播客'
        verbose_name_plural = verbose_name


class Podcast(models.Model):
    PODCAST_ENCLOSURE_TYPE_MP3 = 1
    PODCAST_ENCLOSURE_TYPE_M4A = 2
    PODCAST_ENCLOSURE_TYPE_MP4 = 3
    PODCAST_ENCLOSURE_TYPE_M4V = 4
    PODCAST_ENCLOSURE_TYPE_MOV = 5
    PODCAST_ENCLOSURE_TYPE = (
        (PODCAST_ENCLOSURE_TYPE_MP3, 'audio/mpeg'),
        (PODCAST_ENCLOSURE_TYPE_M4A, 'audio/x-m4a'),
        (PODCAST_ENCLOSURE_TYPE_MP4, 'video/mp4'),
        (PODCAST_ENCLOSURE_TYPE_M4V, 'video/x-m4v'),
        (PODCAST_ENCLOSURE_TYPE_MOV, 'video/quicktime'),
    )
    PODCAST_EXPLICIT_CLEAN = 0
    PODCAST_EXPLICIT_YES = 1
    PODCAST_EXPLICIT_NO = 2
    PODCAST_EXPLICIT = (
        (PODCAST_EXPLICIT_CLEAN, 'clean'),
        (PODCAST_EXPLICIT_YES, 'yes'),
        (PODCAST_EXPLICIT_NO, 'no'),
    )

    title = models.CharField(u"标题", max_length=255)
    description = models.CharField(max_length=255, blank=True)
    duration = models.DurationField(u"时长", default="01:10:10", help_text=u"请按照［01:15:21］格式输入")
    enclosure_url = models.URLField(u"节目URL")
    enclosure_len = models.IntegerField(u"文件大小", help_text=u"单位：字节")
    enclosure_type = models.SmallIntegerField(choices=PODCAST_ENCLOSURE_TYPE, default=PODCAST_ENCLOSURE_TYPE_M4A)
    its_image = models.ImageField(u"节目封面", upload_to="podcast")
    its_subtitle = models.TextField(u"子标题")
    its_summary = HTMLField(u"描述", help_text=u"从iOS 9起,描述支持简单HTML")
    its_author = models.CharField(u"艺人", max_length=100)
    its_explicit = models.SmallIntegerField(choices=PODCAST_EXPLICIT, default=PODCAST_EXPLICIT_CLEAN)
    feeds = models.ManyToManyField(Feed)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"发布人")
    active = models.BooleanField(u"上线", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pubdate = models.DateTimeField(u"发布时间", default=datetime.now())

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
        verbose_name = u'节目'
        verbose_name_plural = verbose_name
        ordering = ['-pubdate']


"""
class Terms(models.Model):
	term_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'ts_terms'

class PostsManager(models.Manager):
	def get_query_set(self):
		return super(PostsManager, self).get_query_set().filter(post_status='publish')

class Posts(models.Model):
	post_content = models.TextField()
	post_title = models.TextField()
	post_status = models.CharField(max_length=20)
	post_date = models.DateTimeField()
	
	objects = PostsManager()

	def __unicode__(self):
		return self.post_title

	def enclosure(self):
		return self.postmeta_set.get(meta_key='enclosure')

	class Meta:
		db_table = 'ts_posts'

class Postmeta(models.Model):
	meta_id = models.IntegerField(primary_key=True)
	post = models.ForeignKey(Posts)
	meta_key = models.CharField(max_length=255)
	meta_value = models.TextField()

	def __unicode__(self):
		return self.meta_value

	class Meta:
		db_table = 'ts_postmeta'

class TermTaxonomyManager(models.Manager):
	def get_query_set(self):
		return super(TermTaxonomyManager, self).get_query_set().filter(taxonomy='category')

class TermTaxonomy(models.Model):
	term_taxonomy_id = models.IntegerField(primary_key=True)
	term = models.ForeignKey(Terms)
	taxonomy = models.CharField(max_length=32)

	objects = TermTaxonomyManager()

	class Meta:
		db_table = 'ts_term_taxonomy'

class TermRelationships(models.Model):
	post = models.ForeignKey(Posts, db_column='object_id', primary_key=True)
	term_taxonomy = models.ForeignKey(TermTaxonomy)

	class Meta:
		db_table = 'ts_term_relationships'
		unique_together = (("post", "term_taxonomy"),)
		"""
