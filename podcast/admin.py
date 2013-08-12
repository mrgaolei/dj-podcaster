# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple
from models import *

class FeedAdmin(admin.ModelAdmin):
	date_hierarchy = 'updated'
	list_display = ('title','feed_url','feed_path','updated')
	#list_filter = ['online']
	actions = ['make_build']

	def queryset(self, request):
		qs = super(FeedAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			return qs.filter(admins=request.user)

	def make_build(self, request, queryset):
		from django.template.loader import render_to_string
		from datetime import datetime
		for feed in queryset:
			podcasts = Podcast.objects.filter(feeds=feed)[:100]
			rss = render_to_string("podcast/feed.html", {'feed':feed,'podcasts':podcasts,'now':datetime.now()})
			f = open(feed.feed_path(), 'w')
			f.write(rss.encode('utf-8'))
			f.close()
	make_build.short_description="重新生成所选的 Feed"

class PodcastAdmin(admin.ModelAdmin):
	date_hierarchy = 'pubdate'
	list_display = ('title', 'active', 'pubdate')
	list_filter = ['active','feeds']
	exclude = ['creator']

	def get_form(self, request, obj=None, **kwargs):
		canChange = True
		if obj:
			canChange = False
			for feed in obj.feeds.all():
				for admin in feed.admins.all():
					if admin == request.user:
						canChange = True
		if not canChange:
			raise Exception("Permission Denied!")
		form = super(PodcastAdmin, self).get_form(request, obj, **kwargs)
		form.base_fields["feeds"].widget = CheckboxSelectMultiple()
		if not request.user.is_superuser:
			form.base_fields["feeds"].queryset = Feed.objects.filter(admins=request.user)

		print form.base_fields["feeds"]
		return form

	def queryset(self, request):
		qs = super(PodcastAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			return qs
			return qs.filter(feeds__admins=request.user)

	def save_model(self, request, obj, form, change):
		obj.creator = request.user
		obj.save()

admin.site.register(Feed, FeedAdmin)
admin.site.register(Podcast, PodcastAdmin)