from celery import shared_task
from .models import Post

@shared_task
def analyze_post(id):
    try:
        post = Post.objects.get(id=id)
        return post.analyze_post()
    except Post.DoesNotExist:
        return None
