import os
import logging
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Set your HF token in .env
HF_TOKEN = os.getenv("HF_TOKEN")
# Adjust as needed
MAX_TOKENS = 500

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentProcessor:
    def __init__(self):
        if not HF_TOKEN:
            logger.warning("HF_TOKEN not set. Unauthenticated requests may fail for some models.")
        self.client = InferenceClient(token=HF_TOKEN)
        self.conversation_history = []

    def _make_api_call(self, prompt, model_name, max_tokens):
        try:
            # Build messages properly for conversational task
            messages = [{"role": "user", "content": prompt}]
            
            result = self.client.chat_completion(
                messages,
                model=model_name,
                max_tokens=max_tokens,
                temperature=0.4,
            )
            # Extract text from the chat format
            text = result.choices[0].message.content
            return text.strip()
        except Exception as error:
            logger.error(f"API call failed: {error}")
            return f"Error: {str(error)}"

    def summarize_content(self, content):
        """Generate a summary of provided text."""
        prompt = f"""
        Summarize the following text into one concise paragraph:
        {content}
        Summary:
        """
        summary = self._make_api_call(
            prompt, 
            "meta-llama/Llama-3.3-70B-Instruct",
            MAX_TOKENS
        )
        self.conversation_history.append({
            "type": "summary",
            "content": summary
        })
        return summary

    def answer_question(self, question, context):
        """Answer user question based on context."""
        prompt = f"""
        Context: {context}
        Question: {question}
        If the answer isn't in the context, respond: "I don't have enough info to answer that based on the provided context."
        Answer:
        """
        answer = self._make_api_call(
            prompt,
            "meta-llama/Llama-3.3-70B-Instruct",
            MAX_TOKENS
        )
        self.conversation_history.append({
            "type": "qa",
            "question": question,
            "answer": answer
        })
        return answer

    def get_recent_history(self):
        """Return last 5 conversation items."""
        return self.conversation_history[-5:]

    def clear_history(self):
        """Reset conversation history."""
        self.conversation_history = []