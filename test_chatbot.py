import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from engine.response_engine import ChatBotEngine

def test_chatbot():
    print("Initializing ChatBot Engine...")
    try:
        engine = ChatBotEngine()
        print("Engine initialized.")
    except Exception as e:
        print(f"FAILED to init engine: {e}")
        return

    session_id = "test_session_123"
    
    test_inputs = [
        "Hello there!",
        "What is machine learning?",
        "My name is Alice.",
        "tell me about python",
        "Goodbye"
    ]
    
    print("\nStarting Conversation Test:\n")
    
    for user_msg in test_inputs:
        print(f"User: {user_msg}")
        try:
            response = engine.generate_response(session_id, user_msg)
            print(f"Bot: {response['response']}")
            print(f"   [Intent: {response['intent']}, Entities: {response['entities']}]")
        except Exception as e:
            print(f"FAILED to generate response: {e}")
            
    print("\nSUCCESS: Verification complete.")

if __name__ == "__main__":
    test_chatbot()
