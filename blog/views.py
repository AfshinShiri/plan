from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    latest_post = Post.published.all().order_by('-publish')[:4]
    get_most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:4]
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
 #search
    formSearch = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        formSearch = SearchForm(request.GET)
        if formSearch.is_valid():
            query = formSearch.cleaned_data['query']

            search_query = SearchQuery(query)
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            # similarity = TrigramSimilarity('title', 'query').filter(similarity__gt=0.1).order_by('-similarity')
            # result = Post.published.annotate(similarity=TrigramSimilarity('title', query), ).filter(
            #     similarity__gt=0.1).order_by('-similarity')
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query),) \
                .filter(search=search_query).order_by('-rank')


    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': page, 'tag': tag,
                                                   'latest_post': latest_post,
                                                   'get_most_commented_posts': get_most_commented_posts,
                                                   'formSearch': formSearch, 'query': query, 'results': results})


@login_required(login_url="/accounts/login")
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day, )
    latest_post = Post.published.all().order_by('-publish')[:4]
    get_most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:4]

    # similar post
    post_tag_id = post.tags.values_list('id', flat=True)
    similar_post = Post.published.filter(tags__in=post_tag_id).distinct().exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    # comment
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

        # search
    formSearch = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        formSearch = SearchForm(request.GET)
        if formSearch.is_valid():
            query = formSearch.cleaned_data['query']

            search_query = SearchQuery(query)
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            # similarity = TrigramSimilarity('title', 'query').filter(similarity__gt=0.1).order_by('-similarity')
            # result = Post.published.annotate(similarity=TrigramSimilarity('title', query), ).filter(
            #     similarity__gt=0.1).order_by('-similarity')
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query), ) \
                .filter(search=search_query).order_by('-rank')
    return render(request, 'blog/detail.html', {'post': post, 'comment_form': comment_form,
                                                'comments': comments, 'new_comment': new_comment,
                                                'similar_post': similar_post,
                                                'latest_post': latest_post,
                                                'get_most_commented_posts': get_most_commented_posts,
                                                'formSearch': formSearch, 'query': query, 'results': results})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommend you read {post.title}"

            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']} comments:{cd['comments']}"
            send_mail(subject, message, "https://planclan.ir", [cd['to']])
            sent = True

    else:
        form = EmailPostForm()

    # search
    formSearch = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        formSearch = SearchForm(request.GET)
        if formSearch.is_valid():
            query = formSearch.cleaned_data['query']

            search_query = SearchQuery(query)
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                # similarity = TrigramSimilarity('title', 'query').filter(similarity__gt=0.1).order_by('-similarity')
                # result = Post.published.annotate(similarity=TrigramSimilarity('title', query), ).filter(
                #     similarity__gt=0.1).order_by('-similarity')
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query), ) \
                            .filter(search=search_query).order_by('-rank')
    return render(request, 'blog/share.html', {'form': form, 'post': post, 'sent': sent,
                                               'formSearch': formSearch, 'query': query, 'results': results})

# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.published.annotate(search=SearchVector('title', 'body'), ).filter(search=query)
#     return render(request, 'blog/search.html', {'form': form,
#                                          'query': query,
#                                          'results': results})
