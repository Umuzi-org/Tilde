from .theme import styles


def theme_context(request):
    return {
        "styles": styles,
    }
