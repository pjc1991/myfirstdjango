import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))


@register.filter
def get_query_string(query_dict: dict):
    query_string = ""
    for key in list(query_dict.keys()):
        if key == "page":
            continue
        query_string += f"&{key}={query_dict[key]}"

    return query_string
