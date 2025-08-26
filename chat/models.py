from django.db import models
from django.utils import timezone

# Create your models here.

class Conversation(models.Model):
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=100, unique=True, blank=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title or f"Conversation {self.id}"
    
    def get_first_message_preview(self):
        """Get a preview of the first message for the title"""
        first_message = self.messages.first()
        if first_message:
            return first_message.content[:50] + "..." if len(first_message.content) > 50 else first_message.content
        return "No messages yet"
    
    def get_message_count(self):
        """Get the total number of messages in this conversation"""
        return self.messages.count()

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
