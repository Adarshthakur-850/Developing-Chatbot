import sys
import os
import random

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import extract_entities
from nlp.embeddings import find_best_match
from memory import chat_memory

class ChatBotEngine:
    def __init__(self):
        self.classifier = IntentClassifier()
        # Simple Knowledge Base
        self.kb = {
            "python": "Python is a high-level, interpreted programming language known for its easy syntax.",
            "java": "Java is a popular, class-based, object-oriented programming language.",
            "ml": "Machine Learning is a field of AI focused on building systems that learn from data."
        }
        self.kb_sentences = list(self.kb.values())
        
        # Responses
        self.responses = {
            "greeting": ["Hello!", "Hi there!", "Greetings! How can I help?"],
            "farewell": ["Goodbye!", "See you later!", "Have a great day!"],
            "thanks": ["You're welcome!", "Happy to help!", "No problem."],
            "identity": ["I am a Context-Aware Chatbot built with Python.", "I'm your AI assistant."],
            "help": ["I can answer questions, chat with you, and remember our conversation."]
        }

    def generate_response(self, session_id, user_message):
        # 1. Save User Message
        chat_memory.add_message(session_id, "user", user_message)
        
        # 2. Extract Info
        intent, conf = self.classifier.predict(user_message)
        entities = extract_entities(user_message)
        
        print(f"DEBUG: Intent={intent} ({conf:.2f}), Entities={entities}")
        
        response_text = ""
        
        # 3. Logic
        if intent == "knowledge" or conf < 0.5:
            # Fallback to KB search if intent is knowledge or low confidence
            best_match, score = find_best_match(user_message, self.kb_sentences)
            if score > 0.3:
                response_text = f"Here's what I found: {best_match}"
            else:
                response_text = "I'm not sure about that. Could you rephrase?"
        elif intent in self.responses:
            response_text = random.choice(self.responses[intent])
        else:
            response_text = "I understand you, but I don't have a specific response for that yet."

        # Add entity info if available
        if entities:
            # Simple entity acknowledgement
            # response_text += f" (I noticed you mentioned: {', '.join([f'{k}: {v}' for k, v in entities.items()])})"
            pass

        # 4. Save Bot Response
        chat_memory.add_message(session_id, "bot", response_text)
        
        return {
            "response": response_text,
            "intent": intent,
            "entities": entities
        }
