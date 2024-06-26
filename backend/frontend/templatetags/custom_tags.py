from django import template

from markdown import markdown

register = template.Library()


@register.inclusion_tag("frontend/partial_user_avatar.html")
def user_avatar(user):
    initial = user.email[0].upper()
    return {"initial": initial}


@register.filter(name='markdownify')
def markdownify(raw_text):
    return markdown(raw_text, safe_mode='escape', extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'pymdownx.inlinehilite'
    ], ).strip()
