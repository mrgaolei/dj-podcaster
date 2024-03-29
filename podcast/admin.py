# -*- coding: utf-8 -*-
import requests

from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin import register
from django.forms.widgets import CheckboxSelectMultiple, URLInput
from django.shortcuts import render
from django.db import models
from .models import CloudStorage, Feed, Podcast


@register(CloudStorage)
class CloudStorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'type', 'bucket', 'domain']
    list_filter = ['type']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()


@register(Feed)
class FeedAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('title', 'feed_url', 'feed_path', 'updated')
    # list_filter = ['online']
    actions = ['make_build']
    autocomplete_fields = ['admins']

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
            podcasts = Podcast.objects.filter(feeds=feed)[:feed.display_num]
            rss = render_to_string("podcast/feed.html", {'feed': feed, 'podcasts': podcasts, 'now': datetime.now()})
            f = open(feed.feed_path(), 'wb')
            f.write(rss.encode('utf-8'))
            f.close()

    make_build.short_description = u"重新生成所选的 Feed"


class DJURLInput(URLInput):

    def render(self, name, value, attrs=None, renderer=None):
        html = super(DJURLInput, self).render(name, value, attrs, renderer)
        html += u' <button type="button" onclick="window.open(\'/admin/podcast/podcast/upload/#%s\')">直接上传(beta)</button>' % name
        return html


@register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    date_hierarchy = 'pubdate'
    list_display = ('title', 'creator', 'active', 'pubdate')
    list_filter = ['active', 'feeds']
    exclude = ['creator', 'enclosure_len']
    search_fields = ['title']
    formfield_overrides = {
        models.URLField: {'widget': DJURLInput},
    }

    def get_readonly_fields(self, request, obj=None):
        canChange = True
        if obj:
            canChange = False
            for feed in obj.feeds.all():
                for admin in feed.admins.all():
                    if admin == request.user:
                        canChange = True
        if canChange:
            return self.readonly_fields
        else:
            return [f.name for f in self.model._meta.fields]

    def get_form(self, request, obj=None, **kwargs):
        form = super(PodcastAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["feeds"].widget = CheckboxSelectMultiple()
        if not request.user.is_superuser:
            form.base_fields["feeds"].queryset = Feed.objects.filter(admins=request.user)

        print(form.base_fields["feeds"])
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)\
            .select_related('creator')\
            .prefetch_related('feeds')
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(feeds__admins=request.user)

    def save_model(self, request, obj, form, change):
        resp = requests.head(obj.enclosure_url)
        if resp.status_code == 200:
            obj.enclosure_len = int(resp.headers['Content-Length'])
        else:
            raise Exception(u"节目URL错误，请上传完节目再发布。")
        if not change:
            obj.creator = request.user
        obj.save()
        self.message_user(request, "发布/更新节目后，请记得去“播客”列表重新生成feed", level=messages.WARNING)

    def get_urls(self):
        urls = super(PodcastAdmin, self).get_urls()
        my_urls = [
            url(r'^upload/$', self.upload),
        ]
        return my_urls + urls

    def upload(self, request):
        import hashlib
        from django.core.files.uploadedfile import InMemoryUploadedFile
        from django.http import JsonResponse
        from qiniu import Auth, put_file, etag, put_data
        if request.method == 'POST':
            uploaded = request.FILES['file']
            filename_group = uploaded.name.split('.')
            file_ext = ''
            if len(filename_group) >= 2:
                file_ext = '.%s' % filename_group[-1]
            file_data = uploaded.read()
            hash = hashlib.md5(file_data).hexdigest()

            storage = CloudStorage.objects.filter(owner=request.user)[0]

            q = Auth(storage.access_key, storage.secret_key)
            domain = storage.domain
            bucket_name = storage.bucket
            key = '%s%s' % (hash, file_ext)
            token = q.upload_token(bucket_name, key)
            print(type(uploaded))
            if isinstance(uploaded, InMemoryUploadedFile):
                ret, info = put_data(token, key, file_data)
            else:
                ret, info = put_file(token, key, uploaded.temporary_file_path())

            if info.status_code == 200:
                assert ret['key'] == key
                # assert ret['hash'] == etag(uploaded.temporary_file_path())
                return JsonResponse({
                    'key': key,
                    'domain': domain,
                    'url': '%s%s' % (domain, key),
                    # 'bucket': bucket_name,
                    # 'path': '%s/%s' % (bucket_name, key),
                })
            else:
                print(ret, info)
                return JsonResponse({
                    'error': 'error',
                }, status=info.status_code)

        return render(request, 'podcast/upload.html', {'storages': CloudStorage.objects.filter(owner=request.user)})
