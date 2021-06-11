from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail




def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': page})

@login_required(login_url="/accounts/login")
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day, )
    return render(request, 'blog/detail.html', {'post': post})

def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id,status='published')
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
            send_mail(subject, message, "mysite@info.com", [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'form': form, 'post': post, 'sent': sent})
