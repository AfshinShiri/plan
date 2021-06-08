from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required



def post_list(request):
    object_list = Post.published.all()
    return render(request, 'blog/post_list.html', {'object_list': object_list})

@login_required(login_url="/accounts/login")
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day, )
    return render(request, 'blog/detail.html', {'post': post})
