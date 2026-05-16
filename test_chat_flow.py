#!/usr/bin/env python
"""Test the complete chat flow with database and Gemini API"""

from app import app, db
from models import FAQ, Document
from ai import get_context_for_query, find_relevant_context, build_knowledge_embeddings
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def test_database_content():
    """Check if database has content"""
    print("=" * 60)
    print("TESTING DATABASE CONTENT")
    print("=" * 60)
    
    with app.app_context():
        faqs = FAQ.query.all()
        docs = Document.query.all()
        
        print(f"\n✓ Found {len(faqs)} FAQs")
        print(f"✓ Found {len(docs)} Documents")
        
        if faqs:
            print(f"\nFirst FAQ:")
            print(f"  Q: {faqs[0].question}")
            print(f"  A: {faqs[0].answer[:100]}...")
        
        return len(faqs) > 0 or len(docs) > 0

def test_embedding_generation():
    """Test embedding generation"""
    print("\n" + "=" * 60)
    print("TESTING EMBEDDING GENERATION")
    print("=" * 60)
    
    with app.app_context():
        result = build_knowledge_embeddings()
        
        if result:
            print(f"\n✓ Embeddings built successfully")
            print(f"  Index type: {type(result)}")
            print(f"  Total items indexed: {result.ntotal}")
        else:
            print("\n✗ No embeddings generated (no data)")
        
        return result is not None

def test_context_retrieval():
    """Test context retrieval from database"""
    print("\n" + "=" * 60)
    print("TESTING CONTEXT RETRIEVAL")
    print("=" * 60)
    
    test_queries = [
        "What is AI?",
        "Tell me about machine learning",
        "How do I register for courses?"
    ]
    
    with app.app_context():
        # Build embeddings first
        build_knowledge_embeddings()
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            context = get_context_for_query(query, top_k=3)
            
            if context:
                print(f"  ✓ Found context ({len(context)} chars)")
                print(f"  Preview: {context[:150]}...")
            else:
                print(f"  ✗ No context found")

def test_gemini_api():
    """Test Gemini API connectivity"""
    print("\n" + "=" * 60)
    print("TESTING GEMINI API")
    print("=" * 60)
    
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    if not api_key:
        print("\n✗ No API key found!")
        return False
    
    print(f"\n✓ API key found (length: {len(api_key)})")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemma-3-4b-it')
        
        prompt = "Hello! Are you working?"
        print(f"\nSending test prompt: '{prompt}'")
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=50,
                temperature=0.7,
            )
        )
        
        if response.text:
            print(f"✓ Response received: {response.text.strip()}")
            return True
        else:
            print("✗ No response from API")
            return False
            
    except Exception as e:
        print(f"✗ API Error: {e}")
        return False

def test_full_chat_flow():
    """Test complete chat flow"""
    print("\n" + "=" * 60)
    print("TESTING FULL CHAT FLOW")
    print("=" * 60)
    
    test_message = "What is artificial intelligence?"
    
    with app.app_context():
        print(f"\nUser message: '{test_message}'")
        
        # Step 1: Get context
        context = get_context_for_query(test_message, top_k=5)
        
        if context:
            print(f"✓ Database context found")
            print(f"  Context length: {len(context)} chars")
            
            # Check if it's an FAQ match
            results = find_relevant_context(test_message, top_k=3, min_score=0.25)
            if results and results[0]['meta']['source'] == 'faq':
                print(f"  ✓ Direct FAQ match found!")
                print(f"  Answer: {results[0]['meta']['answer'][:100]}...")
            else:
                print(f"  → Document match - would use translated content")
        else:
            print(f"✗ No database context - would use Gemini API fallback")
            
            # Test API fallback
            api_key = os.environ.get("GEMINI_API_KEY", "").strip()
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemma-3-4b-it')
                    
                    system_prompt = "You are a helpful campus assistant chatbot.\nProvide clear, accurate, and student-friendly answers.\nBe polite and conversational.\nRespond in English only."
                    prompt_text = f"Question: {test_message}\n\nPlease provide a helpful, natural answer in English."
                    
                    response = model.generate_content(
                        f"{system_prompt}\n\n{prompt_text}",
                        generation_config=genai.types.GenerationConfig(
                            max_output_tokens=200,
                            temperature=0.7,
                        )
                    )
                    
                    if response.text:
                        print(f"✓ Gemini API response: {response.text.strip()[:100]}...")
                    else:
                        print(f"✗ No response from Gemini API")
                        
                except Exception as e:
                    print(f"✗ Gemini API error: {e}")
            else:
                print(f"✗ No API key available for fallback")

if __name__ == "__main__":
    print("\n🚀 COMPREHENSIVE CHATBOT DIAGNOSTIC TEST")
    print("=" * 60)
    
    tests = [
        ("Database Content", test_database_content),
        ("Embedding Generation", test_embedding_generation),
        ("Context Retrieval", test_context_retrieval),
        ("Gemini API", test_gemini_api),
        ("Full Chat Flow", test_full_chat_flow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems working correctly!")
    else:
        print("\n⚠️ Some components need attention")
