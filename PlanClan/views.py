from django.shortcuts import render
from django.contrib.postgres.search import SearchVector
from blog.models import Post
from blog.forms import SearchForm


def about(request):

    #search
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'), ).filter(search=query)

    return render(request, 'about.html', {'form': form, 'query': query, 'results': results})
