from posthog.ai.openai import OpenAI
from posthog import Posthog
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

posthog = Posthog(settings.POSTHOG_API_KEY, host="https://us.i.posthog.com")

class OpenAIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
        
        if not self.api_key:
            logger.warning("OpenAI API key not found in environment variables")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key, posthog_client=posthog) if self.api_key else None
        
        logger.info(f"OpenAI service initialized with model: {self.model}")
    
    def get_chat_response(self, messages, model=None, posthog_trace_id=None, ai_span_name=None):
        """
        Get a response from OpenAI chat completion API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: OpenAI model to use (defaults to settings.OPENAI_MODEL)
            posthog_trace_id: Optional trace ID for PostHog tracking
            ai_span_name: Optional trace name for PostHog tracking (will be sent as $ai_span_name)
        
        Returns:
            str: The AI response content
        """
        if not self.api_key or not self.client:
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        # Use provided model or default from settings
        model_to_use = model or self.model
        
        try:
            logger.info(f"Making OpenAI API call with model: {model_to_use}")
            
            # Prepare completion parameters
            completion_params = {
                "model": model_to_use,
                "messages": messages
            }
            
            # Add posthog_trace_id if provided
            if posthog_trace_id:
                completion_params["posthog_trace_id"] = posthog_trace_id
            
            # Add ai_span_name if provided (PostHog will receive this as $ai_span_name)
            if ai_span_name:
                completion_params["posthog_properties"] = {
                    "$ai_span_name": ai_span_name
                }
            
            response = self.client.chat.completions.create(**completion_params)
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"An error occurred: {str(e)}"
    
    def format_messages_for_api(self, conversation_messages):
        """
        Format conversation messages for OpenAI API
        
        Args:
            conversation_messages: QuerySet of ChatMessage objects
        
        Returns:
            list: List of message dictionaries for OpenAI API
        """
        messages = []
        
        # Add system message for context
        messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
        })
        
        # Add conversation history
        for message in conversation_messages:
            messages.append({
                "role": message.role,
                "content": message.content
            })
        
        return messages
