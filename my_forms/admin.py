from django.contrib import admin

from my_forms.models import Article, Comment

admin.site.register(Comment)
admin.site.register(Article)
