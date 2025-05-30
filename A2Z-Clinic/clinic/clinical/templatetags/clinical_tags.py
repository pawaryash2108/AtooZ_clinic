from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
    Split a string by a key and return a list of strings.
    Usage: {{ value|split:"key" }}
    """
    return value.split(key)

@register.filter
def get_item(lst, index):
    """
    Get an item from a list by index.
    Usage: {{ list|get_item:index }}
    """
    try:
        return lst[int(index)]
    except (IndexError, ValueError):
        return '' 