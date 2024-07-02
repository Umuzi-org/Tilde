from django import template

from markdown import markdown

register = template.Library()

@register.inclusion_tag("frontend/partial_user_avatar.html")
def user_avatar(user, size="default"):
    size_css_classes = {
        "default": "w-[30px] h-[30px]",
        "small": "w-[15px] h-[15px] text-xs",
    }
    initial = user.email[0].upper()
    return {"initial": initial, "size": size_css_classes[size]}


@register.filter(name='markdownify')
def markdownify(raw_text):
    return markdown(raw_text, safe_mode='escape', extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'pymdownx.inlinehilite'
    ], ).strip()

