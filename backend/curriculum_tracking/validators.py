from django.core.exceptions import ValidationError


def validate_content_item_url(url):

    if not url.endswith(".md"):

        raise ValidationError(_("url"), code="Invalid url")
