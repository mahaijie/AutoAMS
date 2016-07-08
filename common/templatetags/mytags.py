# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django import template

register = template.Library()

@register.filter(name='key')
def key(d, key_name):
    if key_name != None:
        return d[key_name]


@register.filter(name='MB_to_GB')
def MB_to_GB(MB):
    GB = int(MB)/1024
    GB = round(float(GB), 0)
    return int(GB)
