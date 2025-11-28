from litellm import completion
import os
from config import settings

def test_connection():
    try:
        print("Testing Azure OpenAI connection...")
        response = completion(
            model="azure/gpt-5-mini",
            messages=[{"role": "user", "content": "Hello, are you working?"}]
        )
        print("Connection successful!")
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
