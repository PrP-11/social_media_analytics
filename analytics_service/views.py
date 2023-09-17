# from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from .tasks import analyze_post
from django.core.cache import cache


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        # Trigger the Celery task asynchronously when creating a post
        instance = serializer.save()
        analyze_post.apply_async(args=[instance.id])

class PostAnalysisView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        cache_key = f'post_analysis_{instance.id}'
        analysis = cache.get(cache_key)

        if analysis is None:
            # If not found in cache, trigger Celery task
            analyze_post.delay(instance.id)
            # Return a placeholder response or status indicating that analysis is in progress
            return Response({'status': 'analysis in progress'})

        return Response(analysis)
