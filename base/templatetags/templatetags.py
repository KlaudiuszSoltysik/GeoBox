from django import template

from colorthief import ColorThief

register = template.Library()

def stars(value):
    return ''.join('★' for _ in range(value))

register.filter('stars', stars)

def getDominantColor(path):
    color_thief = ColorThief(path) 
    color = color_thief.get_color(quality=1000)
    return f'rgba({color[0]}, {color[1]}, {color[2]}, 0.7)'

register.filter('getDominantColor', getDominantColor)