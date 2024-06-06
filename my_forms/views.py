from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ArticleForm
from .models import Article


def index_view(request):
    articles = Article.objects.all()
    return render(request, 'my_forms/index.html', context={"articles": articles})


def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("index")
    else:
        form = ArticleForm()
    return render(request, 'my_forms/form_article.html', context={"form": form, "title": "Create func"})


class CreateArticleView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'my_forms/form_article.html'
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Class"
        return context


def formset_view(request):
    my_articles = Article.objects.filter(author=request.user)
    ArticleFormSet = modelformset_factory(Article, form=ArticleForm, extra=0)
    formset =ArticleFormSet(queryset=my_articles)

    if request.method == 'POST':
        formset = ArticleFormSet(request.POST, queryset=my_articles)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.path)
    return render(request, 'my_forms/formset.html', context={'forms': formset})


def update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = ArticleForm(instance=article)
    return render(request, "my_forms/form_article.html", context={"form": form, "title": "Update func"})


class UpdateArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'my_forms/form_article.html'
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Class"
        return context
