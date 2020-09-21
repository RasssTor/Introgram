from django import template

register = template.Library()

@register.filter
def count(value):
    return len(eval(value))