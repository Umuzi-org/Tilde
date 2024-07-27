from django import template

from markdown import markdown

register = template.Library()

@register.inclusion_tag("frontend/partial_user_avatar.html")
def user_avatar(user, size="default"):
    size_css_classes = {
        "default": "w-[30px] h-[30px]",
        "small": "w-[15px] h-[15px] text-xs",
    }
    if hasattr(user, "email"):
        initial = user.email[0].upper()
    else:
        initial =  user[0].upper()
        
    return {"initial": initial, "size": size_css_classes[size]}

@register.filter(name="markdownify")
def markdownify(raw_text):
    return markdown(
        raw_text,
        safe_mode="escape",
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.tables",
            "markdown.extensions.sane_lists",
            "markdown.extensions.admonition",
            "markdown.extensions.smarty",
            "pymdownx.extra",
            "pymdownx.highlight",
            "pymdownx.tasklist",
            "pymdownx.inlinehilite",
            "pymdownx.magiclink",
            "pymdownx.superfences",
        ],
    ).strip()

@register.filter
def event_class(event_type):
    class_mapping = {
        'CARD_STARTED': 'text-green-400',
        'CARD_MOVED_TO_COMPLETE': 'text-yellow-400',
        'CARD_REVIEW_REQUESTED': 'text-orange-400',
        'CARD_REVIEW_CANCELLED': 'text-gray-400',
        'CARD_MOVED_TO_REVIEW_FEEDBACK': 'text-red-400',
        'COMPETENCE_REVIEW_DONE': 'text-blue-400',
        'PR_REVIEWED': 'text-purple-400',
        'GIT_PUSH': 'text-green-700',
    }

    for key, value in class_mapping.items():
        if key in event_type:
            return value
    return ''

@register.filter
def event_text(event_type):
    event_mapping = {
        'CARD_MOVED_TO_COMPLETE': 'card moved to complete',
        'CARD_STARTED': 'card started',
        'COMPETENCE_REVIEW_DONE': 'competence review done',
        'CARD_REVIEW_REQUESTED': 'card review requested',
        'CARD_STOPPED': 'card stopped',
        'CARD_REVIEW_REQUEST_CANCELLED': 'card review request cancelled',
        'CARD_MOVED_TO_REVIEW_FEEDBACK': 'card moved to review feedback',
        'PR_REVIEWED': 'PR reviewed',
        'GIT_PUSH': 'git push',
        'not yet competent': 'not yet competent',
        'competent': 'competent',
        'excellent': 'excellent',
        'red flag': 'red flag'
    }
    
    for key in event_mapping:
        if key in event_type:
            return event_mapping[key]
    
    return ''

@register.filter
def trusted_icon(event_type):
    if 'trusted=True' in event_type:
        return 'fa-solid fa-circle-check'
    if 'trusted=False' in event_type:
        return 'fa-regular fa-circle-check'
    return ''