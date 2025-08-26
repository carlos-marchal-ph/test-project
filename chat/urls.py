from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/send/', views.send_message, name='send_message'),
    path('api/history/<str:session_id>/', views.get_chat_history, name='get_chat_history'),
]
