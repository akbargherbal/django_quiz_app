from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def divide(value, arg):
    if arg != 0:
        return value / arg
    return 0

@register.filter
def subtract(value, arg):
    return value - arg