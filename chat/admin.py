from django.contrib import admin
from .models import ChatMessage, Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message_count', 'created_at', 'updated_at', 'session_id')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'session_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    
    def message_count(self, obj):
        return obj.get_message_count()
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('role', 'content_preview', 'conversation', 'timestamp')
    list_filter = ('role', 'timestamp', 'conversation')
    search_fields = ('content', 'conversation__title')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('conversation', 'role', 'content')
        }),
        ('Timing', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
