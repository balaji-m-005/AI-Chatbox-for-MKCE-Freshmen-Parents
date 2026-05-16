import requests
import json

def test_chat_api():
    """Test the chat API endpoint"""
    
    url = "http://127.0.0.1:5000/api/chat"
    
    # Test cases
    test_cases = [
        {
            "name": "English greeting",
            "data": {
                "message": "hello",
                "language": "english"
            }
        },
        {
            "name": "Tamil greeting", 
            "data": {
                "message": "வணக்கம்",
                "language": "tamil"
            }
        },
        {
            "name": "Database query",
            "data": {
                "message": "What is MKCE?",
                "language": "english"
            }
        },
        {
            "name": "Random question",
            "data": {
                "message": "Tell me about artificial intelligence",
                "language": "english"
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n🧪 Testing: {test['name']}")
        print(f"Data: {test['data']}")
        
        try:
            response = requests.post(url, json=test['data'], timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {result.get('response', 'No response')[:100]}...")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - make sure app is running")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_chat_api()
