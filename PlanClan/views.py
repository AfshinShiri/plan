from django.shortcuts import render
from django.contrib.postgres.search import SearchVector
from blog.models import Post
from blog.forms import SearchForm


def about(request):

    #search
    formSearch = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        formSearch = SearchForm(request.GET)
        if formSearch.is_valid():
            query = formSearch.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'), ).filter(search=query)

    return render(request, 'about.html', {'formSearch': formSearch, 'query': query, 'results': results})
