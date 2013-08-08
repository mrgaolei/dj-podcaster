# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'podcast_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subText', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'podcast', ['Category'])

        # Adding model 'Feed'
        db.create_table(u'podcast_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('domain', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('its_summary', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('its_author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('its_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('its_owner_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('its_owner_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('its_subtitle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('its_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('its_category', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('its_subcategory', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'podcast', ['Feed'])

        # Adding M2M table for field admins on 'Feed'
        m2m_table_name = db.shorten_name(u'podcast_feed_admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm[u'podcast.feed'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feed_id', 'user_id'])

        # Adding model 'Podcast'
        db.create_table(u'podcast_podcast', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('enclosure_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('enclosure_len', self.gf('django.db.models.fields.IntegerField')()),
            ('enclosure_type', self.gf('django.db.models.fields.SmallIntegerField')(default=2)),
            ('its_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('its_subtitle', self.gf('django.db.models.fields.TextField')()),
            ('its_summary', self.gf('django.db.models.fields.TextField')()),
            ('its_author', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('its_explicit', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('pubdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 8, 0, 0))),
        ))
        db.send_create_signal(u'podcast', ['Podcast'])

        # Adding M2M table for field feeds on 'Podcast'
        m2m_table_name = db.shorten_name(u'podcast_podcast_feeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('podcast', models.ForeignKey(orm[u'podcast.podcast'], null=False)),
            ('feed', models.ForeignKey(orm[u'podcast.feed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['podcast_id', 'feed_id'])

        # Adding model 'Terms'
        db.create_table('ts_terms', (
            ('term_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'podcast', ['Terms'])

        # Adding model 'Posts'
        db.create_table('ts_posts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_content', self.gf('django.db.models.fields.TextField')()),
            ('post_title', self.gf('django.db.models.fields.TextField')()),
            ('post_status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'podcast', ['Posts'])

        # Adding model 'Postmeta'
        db.create_table('ts_postmeta', (
            ('meta_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['podcast.Posts'])),
            ('meta_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'podcast', ['Postmeta'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'podcast_category')

        # Deleting model 'Feed'
        db.delete_table(u'podcast_feed')

        # Removing M2M table for field admins on 'Feed'
        db.delete_table(db.shorten_name(u'podcast_feed_admins'))

        # Deleting model 'Podcast'
        db.delete_table(u'podcast_podcast')

        # Removing M2M table for field feeds on 'Podcast'
        db.delete_table(db.shorten_name(u'podcast_podcast_feeds'))

        # Deleting model 'Terms'
        db.delete_table('ts_terms')

        # Deleting model 'Posts'
        db.delete_table('ts_posts')

        # Deleting model 'Postmeta'
        db.delete_table('ts_postmeta')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'podcast.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subText': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'podcast.feed': {
            'Meta': {'object_name': 'Feed'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'domain': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'its_author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'its_category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'its_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'its_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'its_owner_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'its_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'its_subcategory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'its_subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'its_summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'podcast.podcast': {
            'Meta': {'ordering': "['-pubdate']", 'object_name': 'Podcast'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'enclosure_len': ('django.db.models.fields.IntegerField', [], {}),
            'enclosure_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '2'}),
            'enclosure_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['podcast.Feed']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'its_author': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'its_explicit': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'its_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'its_subtitle': ('django.db.models.fields.TextField', [], {}),
            'its_summary': ('django.db.models.fields.TextField', [], {}),
            'pubdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 8, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'podcast.postmeta': {
            'Meta': {'object_name': 'Postmeta', 'db_table': "'ts_postmeta'"},
            'meta_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'meta_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_value': ('django.db.models.fields.TextField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['podcast.Posts']"})
        },
        u'podcast.posts': {
            'Meta': {'object_name': 'Posts', 'db_table': "'ts_posts'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_content': ('django.db.models.fields.TextField', [], {}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'post_status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post_title': ('django.db.models.fields.TextField', [], {})
        },
        u'podcast.terms': {
            'Meta': {'object_name': 'Terms', 'db_table': "'ts_terms'"},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'term_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['podcast']