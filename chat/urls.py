from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('conversation/<int:conversation_id>/', views.conversation_view, name='conversation'),
    path('api/send/', views.send_message, name='send_message'),
    path('api/history/<int:conversation_id>/', views.get_chat_history, name='get_chat_history'),
    path('api/conversation/create/', views.create_conversation, name='create_conversation'),
    path('api/conversation/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
]
