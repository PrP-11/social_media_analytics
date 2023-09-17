from django.urls import path
from .views import PostCreateView, PostAnalysisView

urlpatterns = [
    path('api/v1/posts', PostCreateView.as_view(), name='post-create'),
    path('api/v1/posts/<uuid:pk>/analysis', PostAnalysisView.as_view(), name='post-analysis'),
]
