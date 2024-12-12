__all__ = ()

import django.template


register = django.template.Library()


@register.inclusion_tag("includes/infinite_scroll.html")
def infinite_scroll():
    return {}
