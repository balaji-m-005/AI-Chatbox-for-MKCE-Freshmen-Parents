#!/usr/bin/env python
"""Test specific user queries"""

from app import app
from app import search_database

def test_specific_queries():
    with app.app_context():
        test_queries = [
            "What is MKCE?",
            "Tell me about your organization",
            "Who is the principal?",
            "Tell me about canteen",
            "principal of our college",
            "canteen details",
            "where is college located",
            "college timings",
            "courses offered",
            "placement cell"
        ]
        
        print("🔍 Testing Specific User Queries:")
        print("=" * 60)
        
        for query in test_queries:
            result = search_database(query)
            
            if result['found']:
                print(f"✅ \"{query}\"")
                print(f"   Source: {result['source']}")
                print(f"   Score: {result['score']:.2f}")
                print(f"   Answer: {result['answer'][:80]}...")
                print()
            else:
                print(f"❌ \"{query}\" - NOT FOUND (will use Gemini API)")
                print()

if __name__ == "__main__":
    test_specific_queries()
