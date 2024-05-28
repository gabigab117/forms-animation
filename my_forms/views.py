from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import ArticleForm
from .models import Article


def index_view(request):
    return render(request, 'my_forms/index.html')


@login_required
def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return render(request, 'my_forms/index.html')
    else:
        form = ArticleForm()
    return render(request, 'my_forms/create_article.html', context={"form": form})


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'my_forms/create_article_class.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
