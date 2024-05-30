from django.contrib import admin
from django.urls import path
from my_forms.views import index_view, create_article_view, CreateArticleView, formset_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('create-article-func/', create_article_view, name='create-article-func'),
    path('create-article-class/', CreateArticleView.as_view(), name='create-article-class'),
    path('formset/', formset_view, name='formset')
]
