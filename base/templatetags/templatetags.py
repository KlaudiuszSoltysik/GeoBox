from django import template

register = template.Library()

def stars(value):
    return ''.join('★' for _ in range(value))

register.filter('stars', stars)