from fastapi.testclient import TestClient
import sys
import os
import traceback
import sentence_transformers
import transformers

# Add project root
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

print(f"DEBUG: sentence-transformers version: {sentence_transformers.__version__}")
print(f"DEBUG: transformers version: {transformers.__version__}")

try:
    from api.app import app
    client = TestClient(app)
except Exception:
    traceback.print_exc()
    sys.exit(1)

def test_api():
    print("Testing Chatbot API...")
    
    # Test 1: Chat Endpoint
    print("1. Testing 'POST /chat'...")
    payload = {
        "session_id": "test_api_session",
        "message": "Hello, how are you?"
    }
    
    try:
        response = client.post("/chat", json=payload)
        if response.status_code != 200:
            print(f"   FAILED: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
        data = response.json()
        assert "response" in data
        assert "intent" in data
        print(f"   SUCCESS: Response='{data['response']}', Intent='{data['intent']}'")
    except Exception as e:
        print("   FAILED with Exception:")
        traceback.print_exc()
        return

    # Test 2: History Endpoint
    print("2. Testing 'GET /history'...")
    try:
        response = client.get("/history/test_api_session")
        if response.status_code != 200:
            print(f"   FAILED: Status {response.status_code}")
            return
            
        history = response.json()
        print(f"   SUCCESS: Retrieved {len(history)} messages from history.")
    except Exception as e:
        traceback.print_exc()
        return

    print("API Verification Complete.")

if __name__ == "__main__":
    test_api()
