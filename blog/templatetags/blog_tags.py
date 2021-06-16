
from django import template
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.filter(name="markdown")
def markdown_formatted(text):
    return mark_safe(markdown.markdown(text))