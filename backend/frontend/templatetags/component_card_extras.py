from django import template

register = template.Library()

def convert_git_url(repo_name, owner):
    return f"https://github.com/{owner.replace('.','-')}/{repo_name}"



register.filter("convert_git_url",convert_git_url)