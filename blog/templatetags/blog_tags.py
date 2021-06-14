from ..models import Post
from django import template

register = template.Library()


@register.inclusion_tag('blog/latest_post.html')
def latest_post(count=3):
    latest_post = Post.published.all().order_by('-publish')[:count]
    return {'latest_post': latest_post}