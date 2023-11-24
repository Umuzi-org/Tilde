# Custom template filters according to the docs here: https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/

from django import template

register = template.Library()


@register.filter(name="convert_git_url")
def convert_git_url(repo_name, owner):
    """
    Converts a git repo's ssh url to a normal github repo url because we are already storing the ssh format.
    """
    return f"https://github.com/{owner.replace('.','-')}/{repo_name}"
