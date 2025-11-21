from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.SubjectListAPIView.as_view()),
    path('posts/', views.PostListAPIView.as_view()),
    path('posts/<int:post_id>/', views.PostDetailAPIView.as_view()),
    
    path('ai/summarize/', views.AISummarizeView.as_view()),
    path('ai/chat/', views.AIChatView.as_view()),
]