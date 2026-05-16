#!/usr/bin/env python
"""Test database search functionality"""

from app import app
from models import FAQ, Document

def test_database_search():
    with app.app_context():
        # Check if data exists
        faqs = FAQ.query.all()
        docs = Document.query.all()
        
        print(f'📊 Database Status:')
        print(f'   FAQs: {len(faqs)}')
        print(f'   Documents: {len(docs)}')
        
        if faqs:
            print(f'\n📋 First FAQ:')
            print(f'   Q: {faqs[0].question}')
            print(f'   A: {faqs[0].answer[:100]}...')
        
        # Test search function
        from app import search_database
        
        test_queries = [
            'What is MKCE?',
            'courses offered',
            'college location'
        ]
        
        print(f'\n🔍 Testing Search Function:')
        for query in test_queries:
            result = search_database(query)
            status = '✅ FOUND' if result['found'] else '❌ NOT FOUND'
            print(f'   {status}: "{query}"')
            if result['found']:
                print(f'      Source: {result["source"]}, Score: {result.get("score", "N/A"):.2f}')

if __name__ == "__main__":
    test_database_search()
