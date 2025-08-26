from django.db import migrations, models
import uuid

def migrate_existing_messages(apps, schema_editor):
    ChatMessage = apps.get_model('chat', 'ChatMessage')
    Conversation = apps.get_model('chat', 'Conversation')
    
    # Get all messages without conversations
    messages_without_conversation = ChatMessage.objects.filter(conversation__isnull=True)
    
    if messages_without_conversation.exists():
        # Group messages by timestamp (within 1 hour) to create conversations
        from django.utils import timezone
        from datetime import timedelta
        
        # Create a default conversation for existing messages
        default_conversation = Conversation.objects.create(
            title="Migrated Conversation",
            session_id=f"migrated_{uuid.uuid4().hex[:8]}"
        )
        
        # Assign all existing messages to this conversation
        messages_without_conversation.update(conversation=default_conversation)

def reverse_migrate_existing_messages(apps, schema_editor):
    # This migration cannot be easily reversed
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_conversation_remove_chatmessage_session_id_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_existing_messages, reverse_migrate_existing_messages),
    ]
