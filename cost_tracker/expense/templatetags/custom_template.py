from django import template
from datetime import datetime

register = template.Library()


@register.filter
def to(value):
    if isinstance(value, int):
        return range(value, datetime.now().year + 1)  # for years, range until the current year
    return range(1, value + 1)  # for months, range from 1 to the value provided (like 12)
