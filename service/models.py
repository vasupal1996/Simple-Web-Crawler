from django.db import models
from tagging.fields import TagField
from tagging.utils import parse_tag_input
from django.utils.translation import ugettext_lazy as _

class Service(models.Model):
    name = models.CharField(max_length=255)
    base_url = models.URLField()
    slug = models.SlugField()
    crawl_url = models.URLField()

    def __str__(self):
        return self.name

    def service_update(self, status, last_run):
        update = ServiceUpdate.objects.create(service=self, status=status, last_run=last_run)
        update.save()

class ServiceUpdate(models.Model):
    GOOD = 'G'
    ERROR = 'E'
    CRAWLING = 'C'
    CURRENT_STATUS = (
        (GOOD, u'✓ good'),
        (ERROR, u'× error'),
        (CRAWLING, u'~ running')
        )

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    last_run = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, default=GOOD, choices=CURRENT_STATUS)

    def __str__(self):
        return self.service.name + " -last run- " + str(self.last_run) + self.status

class TagsEntry(models.Model):
    tags = TagField(_('tags'))

    def __str__(self):
        return self.tags

    @property
    def tags_list(self):

        return parse_tag_input(self.tags)

    # def create_tags(self, raw_input): 
    #     return (SlugToTagGenerator.parse_to_tags(raw_input))

class Article(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    article_url = models.URLField(null=True, blank=True)
    article_code = models.CharField(max_length=255)
    date_created = models.DateTimeField(null=True, blank=True)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    tag = models.ManyToManyField(TagsEntry, blank=True)

    def __str__(self):
        return  self.title + ' - ' +str(self.service.name)

class ArticleUpdate(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now_add=True, editable=True)
    comments_change = models.IntegerField(default=0)
    likes_change = models.IntegerField(default=0)
    dislikes_change = models.IntegerField(default=0)
    shares_change = models.IntegerField(default=0)

    def __str__(self):
        return self.article.title + ' - ' + self.article.service.name


# class SlugToTagGenerator:
#     NonDescriptiveWordsList = [
#         'this', 'is', 'what', 'why', 'where', 'how', 'to', 'your', 'and', 'we', 'have', '\'ve', 
#         'every', 'all', 'so', 'they', 'can', 'us', 'a', 'just', 'got', 'these', 'you', 'are', 
#         'when', 'for', 'more', 
#     ]

#     def parse_to_tags(raw_input):
        
