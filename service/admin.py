from django.contrib import admin

from .models import Article, ArticleUpdate, TagsEntry, Service, ServiceUpdate

admin.site.register(Article)
admin.site.register(ArticleUpdate)
admin.site.register(Service)
admin.site.register(ServiceUpdate)
admin.site.register(TagsEntry)
