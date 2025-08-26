from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('role', 'content_preview', 'session_id', 'timestamp')
    list_filter = ('role', 'timestamp', 'session_id')
    search_fields = ('content', 'session_id')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('role', 'content', 'session_id')
        }),
        ('Timing', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
