# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class FeedAdmin(admin.ModelAdmin):
	date_hierarchy = 'updated'
	list_display = ('title','feed_url','feed_path','updated')
	list_filter = ['tags']
	actions = ['make_build']

	def make_build(self, request, queryset):
		pass
	make_build.short_description="重新生成所选的 Feed"

admin.site.register(Feed, FeedAdmin)
admin.site.register(Tag)
admin.site.register(Podcast)