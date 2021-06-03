from django.shortcuts import render,get_object_or_404
from .models import Post

def post_list(request):
    object_list = Post.published.all()
    return render(request, 'blog/post_list.html', {'object_list': object_list})
