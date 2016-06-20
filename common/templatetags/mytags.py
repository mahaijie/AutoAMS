from django import template

register = template.Library()

@register.filter(name='key')
def key(d, key_name):
    return d[key_name]
key = register.filter('key', key)