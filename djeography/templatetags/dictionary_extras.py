from django import template

register = template.Library()


@register.simple_tag(takes_context=False)
def get_from_dict(dictionary, key):
    return dictionary.get(key, None)
