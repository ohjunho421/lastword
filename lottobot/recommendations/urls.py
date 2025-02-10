from django.urls import path
from .views import ChatBotRecommendView

urlpatterns = [
    path('chatbot/', ChatBotRecommendView.as_view(), name='chatbot_recommend'),
]