from django.db import models

import uuid
from django.core.cache import cache
from django.conf import settings

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()

    def __str__(self):
        return f"Post {self.id}"
    
    def analyze_post(self):
        cache_key = f'post_analysis_{self.id}'
        analysis = cache.get(cache_key)

        if analysis is None:

            words = self.content.split()
            word_count = len(words)
            total_word_length = sum(len(word) for word in words)
            average_word_length = total_word_length / word_count if word_count > 0 else 0

            analysis = {
                'word_count': word_count,
                'average_word_length': average_word_length,
            }

            # Cache the analysis result
            cache.set(cache_key, analysis, timeout=settings.CACHE_TTL)
        
        return analysis

