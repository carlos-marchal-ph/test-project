from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from .models import ChatMessage

def chat_view(request):
    """Main chat interface view"""
    return render(request, 'chat/chat.html')

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """API endpoint to send a message and get a response"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Save user message
        user_chat_message = ChatMessage.objects.create(
            role='user',
            content=user_message,
            session_id=session_id
        )
        
        # Generate AI response (simple echo for now, you can integrate with actual LLM here)
        ai_response = f"I received your message: '{user_message}'. This is a placeholder response. In a real implementation, you would integrate with an LLM API here."
        
        # Save AI response
        ai_chat_message = ChatMessage.objects.create(
            role='assistant',
            content=ai_response,
            session_id=session_id
        )
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'session_id': session_id,
            'user_message_id': user_chat_message.id,
            'ai_message_id': ai_chat_message.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_chat_history(request, session_id):
    """Get chat history for a specific session"""
    messages = ChatMessage.objects.filter(session_id=session_id)
    chat_history = []
    
    for message in messages:
        chat_history.append({
            'role': message.role,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
        })
    
    return JsonResponse({'messages': chat_history})
