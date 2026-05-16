from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import uuid
import re
from datetime import datetime
from dotenv import load_dotenv
from nlp_processor import process_user_query, extract_keywords, calculate_similarity

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
instance_db_path = os.path.join(app.root_path, 'instance', 'chatbot.db')
database_url = os.environ.get('DATABASE_URL', f'sqlite:///{instance_db_path}')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print("DATABASE URI:", database_url)

os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

from models import db, Admin, User, FAQ, Alias, ChatLog, ChatSession, SharedChat, Document

try:
    from semantic_search import initialize_faq_embeddings, search_semantic
except ImportError:
    initialize_faq_embeddings = lambda faqs: None
    search_semantic = lambda query: (None, 0.0)

db.init_app(app)

ALL_FAQS = []
ALL_DOCS = []
ALL_ALIASES = []
ALIASES_BY_KEYWORD = {}

DOMAIN_KEYWORDS = {
    'mkce', 'college', 'campus', 'admission', 'tnea', 'code', 'principal', 'chairman',
    'director', 'hod', 'department', 'course', 'courses', 'programme', 'program', 'ug',
    'pg', 'cse', 'ece', 'eee', 'it', 'civil', 'mechanical', 'mba', 'mca', 'vlsi',
    'fees', 'fee', 'scholarship', 'hostel', 'transport', 'bus', 'placement', 'training',
    'faculty', 'library', 'lab', 'labs', 'research', 'naac', 'nba', 'aicte', 'anna',
    'university', 'alumni', 'portal', 'cams', 'kr', 'connect', 'grievance', 'contact',
    'canteen', 'menu', 'block', 'rk', 'radhakrishnan', 'kalam'
}


def refresh_database_cache():
    """Load FAQ and Document records into memory for faster retrieval."""
    global ALL_FAQS, ALL_DOCS, ALL_ALIASES, ALIASES_BY_KEYWORD
    ALL_FAQS = FAQ.query.order_by(FAQ.id.desc()).all()
    ALL_DOCS = Document.query.order_by(Document.id.desc()).all()
    ALL_ALIASES = Alias.query.order_by(Alias.id.desc()).all()
    ALIASES_BY_KEYWORD = {}
    for alias in ALL_ALIASES:
        key = alias.keyword.lower().strip()
        if key:
            ALIASES_BY_KEYWORD[key] = alias
    initialize_faq_embeddings(ALL_FAQS)
    print("REFRESH_DATABASE_CACHE:", len(ALL_FAQS), "FAQs loaded")

DOMAIN_PHRASES = [
    'm. kumarasamy', 'kumarasamy college', 'anna university', 'tnea code',
    'admission helpline', 'placement email', 'dean of admissions', 'research centre',
    'rk block', 'r k block', 'radhakrishnan block', 'kalam block', 'canteen menu'
]

GENERIC_QUERY_TERMS = {
    'give', 'some', 'name', 'names', 'list', 'show', 'tell', 'please', 'kindly',
    'want', 'need', 'about', 'info', 'information', 'general'
}


def _filtered_keywords(keywords):
    return {word for word in keywords if word not in GENERIC_QUERY_TERMS}


def normalize_query_text(text):
    """Normalize common abbreviations and misspellings for better FAQ retrieval."""
    normalized = (text or '').lower().strip()

    replacements = {
        'bllock': 'block',
        'mneu': 'menu',
        'cantine': 'canteen',
        'cafeteriaa': 'cafeteria',
    }

    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    normalized = re.sub(r'\br\s*k\b', 'rk', normalized)
    normalized = normalized.replace('rk block', 'radhakrishnan block')

    return normalized


def is_domain_query(query_lower, query_keywords):
    """Return True when query appears related to MKCE/campus topics."""
    if 'mkce' in query_lower:
        return True

    if any(phrase in query_lower for phrase in DOMAIN_PHRASES):
        return True

    return bool(_filtered_keywords(query_keywords) & DOMAIN_KEYWORDS)

# Create default admin
DEFAULT_ADMIN_USERNAME = '927623bec200'
DEFAULT_ADMIN_PASSWORD = 'senthil@2006'

with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(username=DEFAULT_ADMIN_USERNAME).first():
        admin = Admin(username=DEFAULT_ADMIN_USERNAME, password=generate_password_hash(DEFAULT_ADMIN_PASSWORD))
        db.session.add(admin)
        db.session.commit()
    refresh_database_cache()

# Improved database search function with better intent matching
def search_database(query, language='english'):
    """Search FAQ and Document database with intent-aware matching"""
    
    query_normalized = normalize_query_text(query)
    query_lower = query_normalized
    query_keywords = set(extract_keywords(query_normalized))
    filtered_query_keywords = _filtered_keywords(query_keywords)
    domain_query = is_domain_query(query_lower, query_keywords)

    # Alias mapping support for multilingual / campus terms
    for alias_key, alias in ALIASES_BY_KEYWORD.items():
        if alias_key in query_lower or query_lower in alias_key:
            return {
                'found': True,
                'source': 'alias',
                'answer': alias.faq.answer,
                'question': alias.faq.question,
                'score': 1.0
            }

    semantic_answer, semantic_score = search_semantic(query_normalized)
    if semantic_answer and semantic_score > 0.60:
        return {
            'found': True,
            'source': 'semantic',
            'answer': semantic_answer,
            'score': semantic_score
        }
    
    # Search FAQs with better scoring
    faqs = ALL_FAQS
    best_faq_match = None
    best_faq_score = 0
    best_faq_overlap = 0
    faq_threshold = 0.4 if domain_query else 0.95
    
    for faq in faqs:
        faq_question_lower = faq.question.lower()
        faq_answer_lower = faq.answer.lower()
        
        # Direct match check (highest priority)
        is_specific_query = len(query_lower) >= 8 and len(filtered_query_keywords) >= 2
        if is_specific_query and (query_lower in faq_question_lower or query_lower in faq_answer_lower):
            return {
                'found': True,
                'source': 'faq',
                'answer': faq.answer,
                'question': faq.question,
                'score': 1.5
            }
        
        # Calculate similarity scores
        question_sim = calculate_similarity(query_normalized, faq.question)
        answer_sim = calculate_similarity(query_normalized, faq.answer)
        
        # Weight question similarity higher (0.7) than answer (0.3)
        score = (question_sim * 0.7) + (answer_sim * 0.3)
        
        # Keyword matching bonus
        faq_keywords = set(extract_keywords(faq.question + " " + faq.answer))
        keyword_match = len(filtered_query_keywords & faq_keywords)
        score += keyword_match * 0.15
        
        # Specific intent boosts
        if 'what is' in query_lower and 'what is' in faq_question_lower:
            score += 0.2
        if 'principal' in query_lower and 'principal' in faq_question_lower:
            score += 0.3
        if 'canteen' in query_lower and 'canteen' in faq_question_lower:
            score += 0.3
        if 'organization' in query_lower or 'college' in query_lower:
            if 'mkce' in faq_answer_lower and 'stands' in faq_answer_lower:
                score += 0.25
        
        if score > best_faq_score and score >= faq_threshold:
            best_faq_score = score
            best_faq_match = faq
            best_faq_overlap = keyword_match
    
    if best_faq_match:
        if not domain_query and best_faq_overlap < 2 and best_faq_score < 1.25:
            return {'found': False}

        return {
            'found': True,
            'source': 'faq',
            'answer': best_faq_match.answer,
            'question': best_faq_match.question,
            'score': best_faq_score
        }

    # For non-domain prompts, bypass document retrieval and let chat API fallback to Gemini.
    if not domain_query:
        return {'found': False}
    
    # Search Documents
    docs = ALL_DOCS
    best_doc_match = None
    best_doc_score = 0
    
    for doc in docs:
        title_sim = calculate_similarity(query_normalized, doc.title)
        content_sim = calculate_similarity(query_normalized, doc.content)
        
        score = (title_sim * 0.8) + (content_sim * 0.2)
        
        doc_keywords = set(extract_keywords(doc.title + " " + doc.content))
        keyword_match = len(query_keywords & doc_keywords)
        score += keyword_match * 0.1
        
        if score > best_doc_score and score >= 0.3:
            best_doc_score = score
            best_doc_match = doc
    
    if best_doc_match:
        doc_content = " ".join([ln.strip() for ln in best_doc_match.content.splitlines() if ln.strip()])
        snippet = doc_content[:800].strip()
        if len(doc_content) > 800 and not snippet.endswith('...'):
            snippet = snippet.rstrip(' .') + '...'
        return {
            'found': True,
            'source': 'document',
            'answer': snippet,
            'title': best_doc_match.title,
            'score': best_doc_score
        }
    
    return {'found': False}

def translate_text(text, language):
    """Translate plain text to selected language when possible."""
    if not text or language == 'english':
        return text

    target_language = {
        'tamil': 'Tamil',
        'hindi': 'Hindi'
    }.get(language)

    target_code = {
        'tamil': 'ta',
        'hindi': 'hi'
    }.get(language)

    if not target_language:
        return text

    # First try lightweight Google Translate wrapper (no API key required).
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source='auto', target=target_code).translate(text)
        if translated and translated.strip():
            return translated.strip()
    except Exception as e:
        print(f"Deep translator error: {e}")

    try:
        import google.generativeai as genai

        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            return text

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemma-3-4b-it')

        prompt = (
            f"Translate the following text to {target_language}. "
            "Keep names, numbers, links, and formatting unchanged. "
            "Return only the translated text without extra commentary.\n\n"
            f"Text:\n{text}"
        )

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=700,
                temperature=0.2,
            )
        )

        translated = response.text.strip() if response and response.text else ''
        return translated or text

    except Exception as e:
        print(f"Translation error: {e}")
        return text

SYSTEM_PROMPT = """
You are Namma MKCE, the official AI assistant of M. Kumarasamy College of Engineering.

STRICT RESPONSE RULES:
- Reply naturally like a human assistant.
- Return ONLY the final answer.
- NEVER include:
  - Question:
  - Answer:
  - Summary:
  - Markdown
  - Bullet labels
  - JSON
  - Explanations unless asked
- Keep responses short, clean, and conversational.
- For room/location queries:
  give direct room + floor + block.
- For staff queries:
  give only relevant staff details.
- For navigation:
  give short directions.

Examples:

User: Where is DSP Lab?
Correct:
DSP Lab is located in Room 217, APJ Abdul Kalam Block, Second Floor.

Wrong:
Question: Where is DSP Lab?
Answer:
Summary:
DSP Lab...
"""

# Format database answers into the user's requested structured format
def clean_assistant_response(text):
    """Clean backend assistant text so it returns plain conversational output."""
    if not text:
        return text

    cleaned = str(text).strip()
    cleaned = re.sub(r'(?i)\*\*\s*(question|answer|summary|explanation|details)\s*\*\*:?\s*', '', cleaned)
    cleaned = re.sub(r'(?i)\b(question|answer|summary|explanation|details):\s*', '', cleaned)
    cleaned = re.sub(r'(?i)^\s*according to [^:]+:\s*', '', cleaned)
    cleaned = re.sub(r'[\*_`~>-]{1,}', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def clean_response(answer, question=None):
    """
    Clean chatbot responses and remove repeated question-style text.
    """
    if not answer:
        return "Sorry, I couldn't find that information."

    answer = str(answer).strip()
    print("DEBUG ANSWER:", answer)
    print("DEBUG QUESTION:", question)

    labels = [
        "**Question:**",
        "**Answer:**",
        "**Summary:**",
        "**Explanation:**",
        "Question:",
        "Answer:",
        "Summary:",
        "Explanation:"
    ]

    for label in labels:
        answer = answer.replace(label, "")

    answer = answer.strip()

    if question:
        q = question.lower().strip()
        a = answer.lower().strip()

        if a.startswith(q):
            answer = answer[len(question):].strip()

        patterns = [
            r"^where\s+is\s+",
            r"^what\s+is\s+",
            r"^who\s+is\s+",
            r"^how\s+to\s+",
            r"^how\s+do\s+i\s+",
        ]

        for pattern in patterns:
            answer = re.sub(pattern, "", answer, flags=re.IGNORECASE)

    answer = re.sub(r'\s+', ' ', answer)
    return answer.strip()

# Lazy Gemini API function
def get_offline_general_response(message, language='english'):
    """Provide simple offline responses for common non-campus prompts."""
    message_lower = (message or '').lower().strip()

    asks_pm_india = (
        ('india' in message_lower and (re.search(r'\bpm\b', message_lower) or 'prime minister' in message_lower))
        or 'pm of india' in message_lower
        or 'prime minister of india' in message_lower
        or 'இந்திய பிரதமர்' in message_lower
        or 'भारत के प्रधानमंत्री' in message_lower
    )

    asks_cm_tamil_nadu = (
        (
            ('tamil nadu' in message_lower or re.search(r'\btn\b', message_lower) or 'தமிழ்நாடு' in message_lower or 'तमिलनाडु' in message_lower)
            and (re.search(r'\bcm\b', message_lower) or 'chief minister' in message_lower or 'முதல்வர்' in message_lower or 'मुख्यमंत्री' in message_lower)
        )
        or 'cm of tamil nadu' in message_lower
        or 'chief minister of tamil nadu' in message_lower
    )

    if asks_pm_india:
        if language == 'tamil':
            return 'ஏப்ரல் 2026 நிலவரப்படி, இந்தியாவின் பிரதமர் நரேந்திர மோடி.'
        if language == 'hindi':
            return 'अप्रैल 2026 तक, भारत के प्रधानमंत्री नरेंद्र मोदी हैं।'
        return 'As of April 2026, the Prime Minister of India is Narendra Modi.'

    if asks_cm_tamil_nadu:
        if language == 'tamil':
            return 'ஏப்ரல் 2026 நிலவரப்படி, தமிழ்நாட்டின் முதலமைச்சர் மு.க. ஸ்டாலின்.'
        if language == 'hindi':
            return 'अप्रैल 2026 तक, तमिलनाडु के मुख्यमंत्री एम. के. स्टालिन हैं।'
        return 'As of April 2026, the Chief Minister of Tamil Nadu is M. K. Stalin.'

    fruit_terms = ['fruit', 'fruits', 'பழம்', 'பழங்கள்', 'फल', 'फलो']
    wants_five = any(token in message_lower for token in ['5', 'five', 'ஐந்து', 'पांच'])

    if any(term in message_lower for term in fruit_terms):
        english_items = ["Apple", "Banana", "Orange", "Mango", "Grapes"]
        tamil_items = ["ஆப்பிள்", "வாழைப்பழம்", "ஆரஞ்சு", "மாம்பழம்", "திராட்சை"]
        hindi_items = ["सेब", "केला", "संतरा", "आम", "अंगूर"]

        if language == 'tamil':
            items = tamil_items[:5 if wants_five else 3]
            return "சில பழங்கள்: " + ", ".join(items)

        if language == 'hindi':
            items = hindi_items[:5 if wants_five else 3]
            return "कुछ फलों के नाम: " + ", ".join(items)

        items = english_items[:5 if wants_five else 3]
        return "Some fruits are: " + ", ".join(items)

    return None


def get_gemini_response(message, language='english'):
    """Get response from Google Gemini API (lazy loading)"""
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            offline_response = get_offline_general_response(message, language)
            return offline_response or get_localized_text(language, 'no_response')
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemma-3-4b-it')
        
        language_instructions = {
            'english': '',
            'tamil': 'If the user question is in Tamil, reply in Tamil.',
            'hindi': 'If the user question is in Hindi, reply in Hindi.'
        }

        prompt = SYSTEM_PROMPT
        extra_instructions = language_instructions.get(language, '')
        if extra_instructions:
            prompt += '\n' + extra_instructions

        response = model.generate_content(
            f"{prompt}\n\nUser: {message}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500,
                temperature=0.7,
            )
        )
        
        return clean_response(response.text.strip()) if response and response.text else get_localized_text(language, 'no_response')
        
    except Exception as e:
        print(f"Gemini error: {e}")
        offline_response = get_offline_general_response(message, language)
        return offline_response or get_localized_text(language, 'no_response')

# Multi-language support
def get_localized_text(language, key):
    """Get localized text based on language"""
    texts = {
        'english': {
            'greeting': 'Hello! I am MKCE campus assistant. How can I help you?',
            'no_response': 'Sorry, I could not find that information.',
            'error': 'An error occurred. Please try again.',
            'missing_question': 'Please ask me something!',
            'ai_unavailable': 'AI service is currently unavailable. Please try again later.'
        },
        'tamil': {
            'greeting': 'வணக்கம்! நான் MKCE வளாக உதவியாளர். நான் உங்களுக்கு எப்படி உதவலாம்?',
            'no_response': 'மன்னிக்கவும், நான் அந்த தகவலைக் கண்டுபிடிக்கவில்லை.',
            'error': 'ஒரு பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.',
            'missing_question': 'தயவுசெய்து என்னிடம் ஏதேனும் கேளுங்கள்!',
            'ai_unavailable': 'AI சேவை தற்போது கிடைக்கவில்லை. தயவுசெய்து பின்னர் முயற்சிக்கவும்.'
        },
        'hindi': {
            'greeting': 'नमस्ते! मैं MKCE कैंपस सहायक हूं। मैं आपकी कैसे मदद कर सकता हूं?',
            'no_response': 'क्षमा करें, मैं वह जानकारी नहीं ढूंढ सका।',
            'error': 'एक त्रुटि हुई। कृपया फिर से कोशिश करें।',
            'missing_question': 'कृपया मुझसे कुछ पूछें!',
            'ai_unavailable': 'AI सेवा अभी उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।'
        }
    }
    
    return texts.get(language, texts['english']).get(key, texts['english'][key])

def get_active_user():
    return session.get('user') or 'test_user'

def start_new_conversation_id():
    conversation_id = f"conv-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"[:64]
    session['active_conversation_id'] = conversation_id
    return conversation_id

def resolve_conversation_id(raw_conversation_id):
    provided_conversation_id = (raw_conversation_id or '').strip()
    if provided_conversation_id:
        session['active_conversation_id'] = provided_conversation_id[:64]
        return session['active_conversation_id']

    active_conversation_id = (session.get('active_conversation_id') or '').strip()
    if active_conversation_id:
        return active_conversation_id[:64]

    return start_new_conversation_id()

def parse_transcript(raw_transcript):
    try:
        messages = json.loads(raw_transcript or '[]')
        if isinstance(messages, list):
            return messages
    except (TypeError, ValueError, json.JSONDecodeError):
        pass
    return []

def save_chat_exchange(user, conversation_id, user_message, bot_response):
    chat_log = ChatLog(user=user, user_message=user_message, bot_response=bot_response)
    db.session.add(chat_log)

    chat_session = ChatSession.query.filter_by(user=user, conversation_id=conversation_id).first()
    if not chat_session:
        chat_session = ChatSession(
            user=user,
            conversation_id=conversation_id,
            title=user_message[:200],
            transcript='[]'
        )
        db.session.add(chat_session)

    transcript = parse_transcript(chat_session.transcript)
    transcript.append({
        'user_message': user_message,
        'bot_response': bot_response,
        'timestamp': datetime.utcnow().isoformat()
    })

    chat_session.transcript = json.dumps(transcript, ensure_ascii=True)
    chat_session.updated_at = datetime.utcnow()
    if not chat_session.title:
        chat_session.title = user_message[:200]

    db.session.commit()

def build_share_url(share_id):
    return url_for('chat', share=share_id, _external=True)

# Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('User already exists.')
            return redirect(url_for('signup'))
        
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user'] = username
            session.pop('active_conversation_id', None)
            return redirect(url_for('chat'))
        
        flash('Invalid credentials.')
    
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('active_conversation_id', None)
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password, password):
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        
        flash('Invalid credentials.')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

# API Routes
@app.route('/api/chat', methods=['POST'])
def chat_api():
    # Temporarily bypass authentication for testing
    # if 'user' not in session:
    #     return jsonify({'error': 'Unauthorized'}), 401
    
    user = get_active_user()

    data = request.get_json() or {}
    user_message = data.get('message', '').strip()
    language = data.get('language', 'english').lower()
    conversation_id = resolve_conversation_id(data.get('conversation_id'))
    
    if language not in ['english', 'tamil', 'hindi']:
        language = 'english'
    
    if not user_message:
        return jsonify({'response': get_localized_text(language, 'missing_question')})
    
    # Check for greetings in multiple languages
    greetings = ['hi', 'hello', 'hey', 'how are you', 'good morning', 'good afternoon', 'good evening', 'vanakkam', 'epdi irukinga', 'எப்படி இருக்கிறீர்கள்']
    if user_message.lower() in greetings or any(greet in user_message.lower() for greet in greetings):
        bot_response = get_localized_text(language, 'greeting')
        save_chat_exchange(user, conversation_id, user_message, bot_response)
        return jsonify({'response': bot_response, 'conversation_id': conversation_id})
    
    try:
        normalized_query = normalize_query_text(user_message)
        query_keywords = set(extract_keywords(normalized_query))
        domain_query = is_domain_query(normalized_query, query_keywords)

        if not domain_query:
            # Unrelated/general prompts should go online directly.
            print("Non-campus query detected - using Gemini API")
            bot_response = get_gemini_response(user_message, language)
        else:
            db_result = search_database(user_message, language)

            if db_result['found']:
                translated = translate_text(db_result['answer'], language)
                bot_response = clean_response(translated, user_message)
                print(f"Database match found: {db_result['source']}")
                print('DEBUG: cleaned bot_response:\n' + bot_response)
            else:
                print("No database match - using Gemini API")
                bot_response = get_gemini_response(user_message, language)
        
        bot_response = clean_response(bot_response, user_message)
        # Log conversation
        save_chat_exchange(user, conversation_id, user_message, bot_response)
        
        return jsonify({'response': bot_response, 'conversation_id': conversation_id})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        bot_response = get_localized_text(language, 'error')
        return jsonify({'response': bot_response, 'conversation_id': conversation_id})

@app.route('/debug-faq', methods=['GET'])
def debug_faq():
    faq = FAQ.query.filter_by(
        question="Where is 3rd year ECE D section located?"
    ).first()
    if not faq:
        return jsonify({'error': 'FAQ not found'}), 404
    return jsonify({
        'question': faq.question,
        'answer': faq.answer,
        'faq_count': len(ALL_FAQS)
    })

@app.route('/api/chat/session/new', methods=['POST'])
def new_chat_session_api():
    return jsonify({'conversation_id': start_new_conversation_id()})

@app.route('/api/chat/share', methods=['POST'])
def share_chat_api():
    user = get_active_user()
    data = request.get_json() or {}
    conversation_id = resolve_conversation_id(data.get('conversation_id'))
    provided_messages = data.get('messages') if isinstance(data.get('messages'), list) else []

    def normalize_messages(raw_messages):
        normalized = []
        for item in raw_messages:
            if not isinstance(item, dict):
                continue
            user_message = str(item.get('user_message', '') or '').strip()
            bot_response = str(item.get('bot_response', '') or '').strip()
            timestamp = str(item.get('timestamp', '') or '').strip()
            if user_message or bot_response:
                normalized.append({
                    'user_message': user_message,
                    'bot_response': bot_response,
                    'timestamp': timestamp or datetime.utcnow().isoformat()
                })
        return normalized

    chat_session = ChatSession.query.filter_by(user=user, conversation_id=conversation_id).first()

    selected_title = None
    selected_conversation_id = conversation_id
    selected_transcript = '[]'

    if chat_session:
        selected_title = chat_session.title
        selected_transcript = chat_session.transcript or '[]'
    else:
        normalized_provided_messages = normalize_messages(provided_messages)
        if normalized_provided_messages:
            selected_title = normalized_provided_messages[0].get('user_message', 'Shared chat')[:200]
            selected_transcript = json.dumps(normalized_provided_messages, ensure_ascii=True)
        else:
            fallback_session = ChatSession.query.filter_by(user=user).order_by(ChatSession.updated_at.desc()).first()
            if fallback_session:
                selected_conversation_id = fallback_session.conversation_id
                selected_title = fallback_session.title
                selected_transcript = fallback_session.transcript or '[]'
            else:
                return jsonify({'error': 'No chat session found to share'}), 404

    share_id = uuid.uuid4().hex[:16]
    shared_chat = SharedChat(
        share_id=share_id,
        owner_user=user,
        source_conversation_id=selected_conversation_id,
        title=selected_title,
        transcript=selected_transcript
    )
    db.session.add(shared_chat)
    db.session.commit()

    return jsonify({
        'share_id': share_id,
        'share_url': build_share_url(share_id)
    })

@app.route('/api/chat/shared/<share_id>', methods=['GET'])
def get_shared_chat_api(share_id):
    shared_chat = SharedChat.query.filter_by(share_id=share_id).first()
    if not shared_chat:
        return jsonify({'error': 'Shared chat not found'}), 404

    messages = parse_transcript(shared_chat.transcript)
    return jsonify({
        'share_id': shared_chat.share_id,
        'title': shared_chat.title or 'Shared chat',
        'messages': messages,
        'created_at': shared_chat.created_at.isoformat()
    })

@app.route('/api/chat/shared/<share_id>/import', methods=['POST'])
def import_shared_chat_api(share_id):
    shared_chat = SharedChat.query.filter_by(share_id=share_id).first()
    if not shared_chat:
        return jsonify({'error': 'Shared chat not found'}), 404

    user = get_active_user()
    new_conversation_id = start_new_conversation_id()

    imported_chat_session = ChatSession(
        user=user,
        conversation_id=new_conversation_id,
        title=shared_chat.title,
        transcript=shared_chat.transcript or '[]'
    )
    db.session.add(imported_chat_session)
    db.session.commit()

    return jsonify({
        'conversation_id': new_conversation_id,
        'title': imported_chat_session.title or 'Shared chat',
        'messages': parse_transcript(imported_chat_session.transcript)
    })

@app.route('/api/chat_logs', methods=['GET', 'DELETE'])
def chat_logs_api():
    user = get_active_user()

    if request.method == 'GET':
        sessions = ChatSession.query.filter_by(user=user).order_by(ChatSession.updated_at.desc()).all()

        logs = []
        for chat_session in sessions:
            messages = parse_transcript(chat_session.transcript)
            normalized_messages = []
            for message in messages:
                user_message = (message.get('user_message') or '').strip()
                bot_response = (message.get('bot_response') or '').strip()
                timestamp = message.get('timestamp')
                if user_message or bot_response:
                    normalized_messages.append({
                        'user_message': user_message,
                        'bot_response': bot_response,
                        'timestamp': timestamp
                    })

            latest_message = normalized_messages[-1] if normalized_messages else {}
            display_title = chat_session.title or latest_message.get('user_message') or 'Chat'
            logs.append({
                'id': chat_session.id,
                'conversation_id': chat_session.conversation_id,
                'user_message': display_title,
                'bot_response': latest_message.get('bot_response', ''),
                'timestamp': latest_message.get('timestamp') or chat_session.updated_at.isoformat(),
                'messages': normalized_messages
            })

        if logs:
            return jsonify(logs)

        # Backward compatibility for older chat logs
        legacy_logs = ChatLog.query.filter_by(user=user).order_by(ChatLog.timestamp.desc()).limit(50).all()
        return jsonify([
            {
                'id': log.id,
                'conversation_id': '',
                'user_message': log.user_message,
                'bot_response': log.bot_response,
                'timestamp': log.timestamp.isoformat(),
                'messages': [
                    {
                        'user_message': log.user_message,
                        'bot_response': log.bot_response,
                        'timestamp': log.timestamp.isoformat()
                    }
                ]
            }
            for log in legacy_logs
        ])

    try:
        ChatSession.query.filter_by(user=user).delete(synchronize_session=False)
        ChatLog.query.filter_by(user=user).delete(synchronize_session=False)
        db.session.commit()
        start_new_conversation_id()
        return jsonify({'message': 'Chat history deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete chat history: {str(e)}'}), 500

@app.route('/api/chat_logs/<int:id>', methods=['DELETE'])
def delete_chat_log(id):
    user = get_active_user()

    chat_session = ChatSession.query.filter_by(id=id, user=user).first()
    if chat_session:
        db.session.delete(chat_session)
        db.session.commit()
        return jsonify({'message': 'Chat session deleted'})

    legacy_log = ChatLog.query.filter_by(id=id, user=user).first()
    if legacy_log:
        db.session.delete(legacy_log)
        db.session.commit()
        return jsonify({'message': 'Chat log deleted'})

    return jsonify({'error': 'Chat session not found'}), 404

@app.route('/api/faqs', methods=['GET', 'POST'])
def faqs_api():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        faqs = FAQ.query.order_by(FAQ.id.desc()).all()
        return jsonify([{'id': f.id, 'question': f.question, 'answer': f.answer} for f in faqs])
    
    # POST - Add new FAQ
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        if not answer:
            return jsonify({'error': 'Answer is required'}), 400
        
        # Create FAQ
        faq = FAQ(question=question, answer=answer)
        db.session.add(faq)
        db.session.commit()
        refresh_database_cache()
        
        return jsonify({'message': 'FAQ added', 'id': faq.id}), 201
        
    except Exception as e:
        print(f"Error adding FAQ: {e}")
        db.session.rollback()
        return jsonify({'error': f'Failed to add FAQ: {str(e)}'}), 500

@app.route('/api/faqs/<int:id>', methods=['PUT', 'DELETE'])
def faq_api(id):
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    faq = FAQ.query.get_or_404(id)
    
    if request.method == 'PUT':
        data = request.get_json()
        faq.question = data['question']
        faq.answer = data['answer']
        db.session.commit()
        refresh_database_cache()
        return jsonify({'message': 'FAQ updated'})
    
    db.session.delete(faq)
    db.session.commit()
    refresh_database_cache()
    return jsonify({'message': 'FAQ deleted'})

@app.route('/api/documents', methods=['GET', 'POST'])
def documents_api():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        docs = Document.query.order_by(Document.uploaded_at.desc()).all()
        return jsonify([{
            'id': d.id,
            'title': d.title,
            'content': d.content,
            'filename': d.filename,
            'uploaded_at': d.uploaded_at.isoformat()
        } for d in docs])
    
    # POST - Add new document (supports both JSON and FormData)
    try:
        title = None
        content = None
        filename = None
        
        # Check if request is FormData (file upload) or JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle FormData (file upload)
            title = request.form.get('title', '').strip()
            filename = request.form.get('filename', '').strip()
            
            # Get content from file or form
            content = request.form.get('content', '').strip()
            
            if 'file' in request.files:
                file = request.files['file']
                if file.filename:
                    filename = file.filename
                    # Read file content based on type
                    if file.content_type and 'text' in file.content_type:
                        content = file.read().decode('utf-8', errors='ignore')
                    else:
                        content = f"File uploaded: {file.filename}"
        else:
            # Handle JSON data
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()
        
        # Validate required fields
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Create document
        doc = Document(title=title, content=content, filename=filename)
        db.session.add(doc)
        db.session.commit()
        refresh_database_cache()
        
        return jsonify({'message': 'Document added', 'id': doc.id}), 201
        
    except Exception as e:
        print(f"Error adding document: {e}")
        db.session.rollback()
        return jsonify({'error': f'Failed to add document: {str(e)}'}), 500

@app.route('/api/documents/<int:id>', methods=['PUT', 'DELETE'])
def document_api(id):
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    doc = Document.query.get_or_404(id)
    
    if request.method == 'PUT':
        data = request.get_json()
        doc.title = data['title']
        doc.content = data['content']
        db.session.commit()
        refresh_database_cache()
        return jsonify({'message': 'Document updated'})
    
    db.session.delete(doc)
    db.session.commit()
    refresh_database_cache()
    return jsonify({'message': 'Document deleted'})

if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host=host, port=port, debug=debug)
