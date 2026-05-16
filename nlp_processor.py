import re
from difflib import SequenceMatcher

def extract_keywords(text):
    """Extract important keywords from user query"""
    # Remove common stop words
    stop_words = {'what', 'is', 'are', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'how', 'can', 'you', 'tell', 'me', 'about', 'i', 'want', 'know'}
    
    # Clean and split text
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts using SequenceMatcher"""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def find_best_match(query, database_items, threshold=0.3):
    """Find best matching item from database using fuzzy matching"""
    query_keywords = extract_keywords(query)
    
    best_match = None
    best_score = 0
    
    for item in database_items:
        # Check question/title match
        if hasattr(item, 'question'):
            item_text = item.question + " " + item.answer
        else:
            item_text = item.title + " " + item.content
        
        # Calculate similarity score
        score = calculate_similarity(query, item_text)
        
        # Bonus for keyword matches
        item_keywords = extract_keywords(item_text)
        keyword_matches = len(set(query_keywords) & set(item_keywords))
        score += keyword_matches * 0.1
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = item
    
    return best_match, best_score

def process_user_query(query, language='english'):
    """Process user query and extract intent"""
    query_lower = query.lower().strip()
    
    # Intent detection
    intents = {
        'greeting': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'vanakkam', 'namaste'],
        'farewell': ['bye', 'goodbye', 'see you', 'take care'],
        'thanks': ['thank', 'thanks', 'thank you', 'nandri', 'dhanyavad'],
        'help': ['help', 'assist', 'support'],
        'about': ['what is', 'tell me about', 'information', 'details'],
        'location': ['where', 'location', 'address', 'place', ' situated'],
        'contact': ['contact', 'phone', 'email', 'call', 'reach'],
        'courses': ['course', 'program', 'branch', 'department', 'study', 'be', 'b.e', 'me', 'm.e'],
        'admission': ['admission', 'apply', 'join', 'enroll', 'eligibility'],
        'fees': ['fee', 'cost', 'price', 'payment', 'money', 'scholarship']
    }
    
    detected_intent = 'general'
    for intent, keywords in intents.items():
        if any(keyword in query_lower for keyword in keywords):
            detected_intent = intent
            break
    
    return {
        'original_query': query,
        'keywords': extract_keywords(query),
        'intent': detected_intent,
        'language': language
    }
