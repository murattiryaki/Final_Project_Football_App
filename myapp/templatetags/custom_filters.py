from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, args):
    search, replace = args.split(',')
    return value.replace(search, replace)
