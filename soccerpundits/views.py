import requests
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from .models import Post
from .forms import PostForm
from django.utils import timezone


CACHE_TTL = 60 * 15


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context = {"posts": posts}
    return render(request, 'soccerpundits/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render(request, 'soccerpundits/post_detail.html', context)


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'soccerpundits/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'soccerpundits/post_edit.html', {'form': form})


@cache_page(CACHE_TTL)
def generic_news(request):
    sources = ['bbc-sport', 'the-sport-bible', 'espn', 'talksport', 'four-four-two']
    key = os.environ['newskey']
    data = list()
    for source in sources:
        url = 'https://newsapi.org/v1/articles?source=' + source + \
            '&sortBy=top&apiKey=' + key
        req = requests.get(url)
        response_news_articles = req.json()
        data.append(response_news_articles)
    return render(request, 'soccerpundits/generic_news.html', {'data': data})
