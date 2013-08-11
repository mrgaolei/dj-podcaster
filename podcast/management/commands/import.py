from datetime import datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from podcast.models import *

class Command(BaseCommand):
    args = 'None'
    help = 'trans data from tangsuanradio from dj-podcast'

    def handle(self, *args, **options):
        feed_ts = Feed.objects.get(pk=1)
        posts = Posts.objects.using('ts').all()
        for post in posts:
            podcast = Podcast()
            podcast.title = post.post_title
            podcast.description = post.post_content[0:254]
            podcast.duration = 300
            try:
                podcast.enclosure_url = post.enclosure()
            except:
                continue
            podcast.enclosure_len = 10240
            podcast.enclosure_type = Podcast.PODCAST_ENCLOSURE_TYPE_MP3
            podcast.its_image = ''
            podcast.its_subtitle = post.post_content[0:254]
            podcast.its_summary = post.post_content
            podcast.its_author = 'www.tangsuanradio.com'
            podcast.its_explicit = Podcast.PODCAST_EXPLICIT_YES
            
            podcast.creator_id = 1
            podcast.pubdate = post.post_date
            try:
                podcast.save()
                podcast.feeds.add(feed_ts)
                # import all category
                #print post
                for rel in post.termrelationships_set.all():
                    if rel.term_taxonomy.taxonomy == 'category':
                        if rel.term_taxonomy.term_id == 1:
                            continue
                        try:
                            feed_tmp = Feed.objects.get(pk=rel.term_taxonomy.term_id)
                            podcast.feeds.add(feed_tmp)
                        except Exception as e:
                            print e
                        #print rel.term_taxonomy.term_id, rel.term_taxonomy.term
            except Exception as e:
                print e
            
    	self.stdout.write("success")