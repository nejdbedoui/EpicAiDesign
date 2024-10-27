import base64
import io

from PIL import Image
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def music_to_base64(music):
    try:
        encoded_string = base64.b64encode(music.read()).decode('utf-8')
        base64_audio = f"data:audio/mp3;base64,{encoded_string}"
        return mark_safe(base64_audio)
    except Exception as e:
        print(f"Error encoding audio to Base64: {e}")
        return ""