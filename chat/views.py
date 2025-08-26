from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from .models import ChatMessage, Conversation
from .services import OpenAIService

def chat_view(request):
    """Main chat interface view - shows conversation list"""
    conversations = Conversation.objects.all()
    return render(request, 'chat/chat.html', {'conversations': conversations})

def conversation_view(request, conversation_id):
    """View for a specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    return render(request, 'chat/conversation.html', {
        'conversation': conversation,
        'messages': messages
    })

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """API endpoint to send a message and get a response"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            conversation = Conversation.objects.create(session_id=session_id)
            # Set title based on first message
            conversation.title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            conversation.save()
        
        # Save user message
        user_chat_message = ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Get AI response using OpenAI
        openai_service = OpenAIService()
        
        # Get conversation history for context
        conversation_messages = conversation.messages.all()
        messages_for_api = openai_service.format_messages_for_api(conversation_messages)
        
        # Create posthog trace ID for tracking
        posthog_trace_id = f"convo-{conversation.id}"
        
        # Calculate message index (this will be the AI response message index)
        user_message_count = conversation.messages.filter(role='user').count()
        
        # Create ai trace name: conversation title + message index
        conversation_title = conversation.title or f"Conversation {conversation.id}"
        ai_span_name = f"{conversation_title} - Message {user_message_count}"
        
        # Get AI response
        ai_response = openai_service.get_chat_response(
            messages_for_api, 
            posthog_trace_id=posthog_trace_id,
            ai_span_name=ai_span_name
        )
        
        # Save AI response
        ai_chat_message = ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_response
        )
        
        # Update conversation timestamp
        conversation.save()  # This will update the updated_at field
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'conversation_id': conversation.id,
            'session_id': conversation.session_id,
            'user_message_id': user_chat_message.id,
            'ai_message_id': ai_chat_message.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_chat_history(request, conversation_id):
    """Get chat history for a specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    chat_history = []
    
    for message in messages:
        chat_history.append({
            'role': message.role,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
        })
    
    return JsonResponse({'messages': chat_history})

@csrf_exempt
@require_http_methods(["POST"])
def create_conversation(request):
    """Create a new conversation"""
    try:
        data = json.loads(request.body)
        title = data.get('title', 'New Conversation')
        session_id = str(uuid.uuid4())
        
        conversation = Conversation.objects.create(
            title=title,
            session_id=session_id
        )
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation.id,
            'session_id': conversation.session_id,
            'title': conversation.title
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        conversation.delete()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
