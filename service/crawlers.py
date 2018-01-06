import requests
import json
import os
import sys
from unipath import Path 

from django.core.wsgi import get_wsgi_application
PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_crawler.settings'
application = get_wsgi_application()

from django.utils import timezone
from service.models import Service, ServiceUpdate, Article, ArticleUpdate, TagsEntry

class AbstractBaseCrawler(object):
    def __init__(self, slug):
        self.service = Service.objects.get(slug=slug)
        print (self.service)

    def run(self):
        try:
            last_run = timezone.now()
            self.service.service_update(status=ServiceUpdate.CRAWLING, last_run=last_run)
            self.update_top_acticles()
            self.serviceupdate = ServiceUpdate.objects.get(last_run=last_run)
            self.serviceupdate.status = ServiceUpdate.GOOD
            self.serviceupdate.save()
        except:
            service = Service.objects.get(slug=self.slug)
            self.service.service_update(status=ServiceUpdate.ERROR, last_run=timezone.now())
        

class MediumCrawler(AbstractBaseCrawler):
    def __init__(self):
        super(MediumCrawler, self).__init__('medium')
    
    def fetch_articles(self):
        crawl_url = self.service.crawl_url
        r = requests.get(crawl_url)
        text_data = r.text[16:] # remove ])}while(1);</x>
        json_data = json.loads(text_data)
        return json_data['payload']['value']['posts']

    def update_top_acticles(self):
        articles = self.fetch_articles()
        today = timezone.now()
        
        for article_data in articles:
            article, created = Article.objects.get_or_create(service=self.service, article_code=article_data['id'])
            if created:
                article.date_created = timezone.datetime(today.year, today.month, today.day, tzinfo=timezone.get_current_timezone())
                article.article_url = '{0}/@{1}/{2}'.format(self.service.base_url, article_data['creator']['username'], article_data['id'])
                article.likes = int(article_data['virtuals']['totalClapCount'])
                article.comments = int(article_data['virtuals']['responsesCreatedCount'])
            
            tag_list = article_data['virtuals']['tags']
            for tag in tag_list:
                tag_name = tag['name']
                tag_entry, created = TagsEntry.objects.get_or_create(tags=tag_name.lower())
                article.tag.add(tag_entry)

            article.title = article_data['title']           
            article.content = article_data['virtuals']['metaDescription']

            likes = int(article_data['virtuals']['totalClapCount'])
            comments = int(article_data['virtuals']['responsesCreatedCount'])
            has_changes = (likes != article.likes or comments != article.comments)

            if created is False and has_changes:
                update = ArticleUpdate(article=article)
                update.comments_change = comments - int(article.comments)
                update.likes_change = likes - int(article.likes)
                update.save()
            

            article.likes = likes
            article.comments = comments
            article.save()
        print ('Articles Saved')

class RedditCrawler(AbstractBaseCrawler):

    def __init__(self):
        super(RedditCrawler, self).__init__('reddit')
    
    def fetch_articles(self):
        url = 'https://www.reddit.com/top/.json'
        articles = list()
        try:
            
            r = requests.get(url, headers= { 'user-agent': 'woid/1.0' })
            result = r.json()
            articles = result['data']['children']
            
        except:
            pass
            
        return articles

    def update_top_acticles(self):
        articles = self.fetch_articles()
        try:
            for story in articles:
                article_data = story['data']
                article, created = Article.objects.get_or_create(service=self.service, article_code=article_data.get('permalink'))            
                
                if created:
                    article.data_created = timezone.datetime.fromtimestamp(article_data.get('created_utc'), timezone.get_current_timezone())
                    article.article_url = '{0}{1}'.format(self.service.base_url, article_data.get('permalink'))
                    article.likes = article_data.get('score')
                    article.comments = article_data.get('num_comments')
                                
                article.title = article_data.get('title', '')
                likes = article_data.get('score')
                comments = article_data.get('num_comments')
                has_changes = (likes != article.likes or comments != article.comments)
                
                if created is False and has_changes:
                    update = ArticleUpdate(article=article)
                    update.comments_change = comments - int(article.comments)
                    update.likes_change = likes - int(article.likes)
                    update.save()

                article.likes = article_data.get('score')
                article.comments = article_data.get('num_comments')
                article.save()
        except:
            pass
        print ('Articles Saved')

r = RedditCrawler().run()
m = MediumCrawler().run()
 