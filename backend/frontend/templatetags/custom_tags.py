from django import template

register = template.Library()


@register.inclusion_tag("frontend/user/board/partial_user_avatar.html")
def user_avatar(user):
    initial = user.email[0].upper()
    return {"initial": initial}
