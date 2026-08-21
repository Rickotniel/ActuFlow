from django.utils.text import slugify
import uuid

def generate_slug(text):
    base = slugify(text)[:50]
    return f"{base}-{uuid.uuid4().hex[:8]}"
