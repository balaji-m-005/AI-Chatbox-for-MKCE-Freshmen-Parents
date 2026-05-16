# AI Chatbot System - Architecture Documentation

## 📋 Overview

This is a Flask-based AI chatbot system with **database priority architecture**: it first searches the local knowledge base (FAQs, documents), then falls back to Gemini AI when no match is found.

## 🏗️ System Architecture

```
User Query → NLP Processing → Semantic Search → Database Match? → Yes → Return DB Answer
                                              ↓
                                            No → Gemini AI → Return AI Response
```

---

## 📥 A) DATA COLLECTION

### Admin Capabilities

1. **FAQ Management**
   - Add/Edit/Delete FAQ entries (Question-Answer pairs)
   - Structured format for quick retrieval
   - Automatic embedding updates

2. **Document Upload**
   - **Supported Formats:**
     - PDF (using `pdfplumber`)
     - Word documents (.docx using `python-docx`)
     - Text files (.txt)
     - Images with OCR (.png, .jpg, .jpeg, .gif, .bmp using EasyOCR/Tesseract)
   
3. **File Processing Pipeline**
   ```
   Upload → Text Extraction → Chunking (>1000 chars) → Embedding → FAISS Index
   ```

### File Processing Details

#### PDF Extraction
```python
with pdfplumber.open(file_path) as pdf:
    content = '\n'.join(page.extract_text() or '' for page in pdf.pages)
```

#### DOCX Extraction
```python
docx_file = DocxDocument(file_path)
content = '\n'.join(paragraph.text for paragraph in docx_file.paragraphs)
```

#### Image OCR
```python
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
ocr_lines = reader.readtext(file_path, detail=0)
```

---

## 💾 B) DATABASE STORAGE

### Technology Stack

- **Primary**: SQLite (default, file-based)
- **Alternative**: MySQL (via environment configuration)
- **Future**: Firebase integration possible

### Database Schema

#### 1. Admin Table
```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL  -- Hashed with werkzeug
);
```

#### 2. User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL  -- Hashed
);
```

#### 3. FAQ Table
```sql
CREATE TABLE faq (
    id INTEGER PRIMARY KEY,
    question VARCHAR(500) NOT NULL,
    answer TEXT NOT NULL
);
```

#### 4. Document Table
```sql
CREATE TABLE document (
    id INTEGER PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    content TEXT NOT NULL,
    filename VARCHAR(250),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. ChatLog Table
```sql
CREATE TABLE chat_log (
    id INTEGER PRIMARY KEY,
    user VARCHAR(100),
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Optimization Strategies

1. **FAISS Vector Index**
   - Facebook AI Similarity Search for fast nearest-neighbor lookup
   - Uses Inner Product (IndexFlatIP) with normalized vectors
   - Cosine similarity computation

2. **Sentence-BERT Embeddings**
   - Model: `all-MiniLM-L6-v2` (384 dimensions)
   - Normalized embeddings for cosine similarity
   - Cached in memory for performance

3. **Chunking Strategy**
   - Documents >1000 characters split into chunks
   - Each chunk indexed separately
   - Better retrieval precision

4. **In-Memory Caching**
   ```python
   cached_embeddings = {
       'index': FAISS index,
       'embedder': SentenceTransformer model,
       'texts': List of text chunks,
       'metas': List of metadata dicts
   }
   ```

---

## 🔍 C) QUERY PROCESSING

### NLP Pipeline

```
1. Input Preprocessing
   ↓
2. Embedding Generation
   ↓
3. FAISS Similarity Search
   ↓
4. Score Filtering (min_score: 0.20-0.25)
   ↓
5. Top-K Results (k=3-5)
   ↓
6. Context Aggregation
```

### Step-by-Step Implementation

#### 1. Input Preprocessing
```python
normalized = user_message.lower().strip(' .!?,')
```

#### 2. Semantic Embedding
```python
query_vec = embedder.encode([query], 
                           convert_to_numpy=True, 
                           normalize_embeddings=True)
```

#### 3. FAISS Search
```python
distances, indices = index.search(query_vec, top_k)
```

#### 4. Similarity Scoring
- **Cosine similarity** via inner product (normalized vectors)
- **Threshold filtering**: min_score = 0.20-0.25
- **Ranking**: Higher scores = better matches

#### 5. Multi-Source Matching
- FAQs prioritized (direct Q&A format)
- Document content
- Uploaded file content

### Semantic Matching Algorithm

```python
def find_relevant_context(query, top_k=4, min_score=0.20):
    # Encode query
    query_vec = embedder.encode([query], normalize=True)
    
    # Search FAISS index
    distances, indices = index.search(query_vec, top_k)
    
    # Filter by score
    results = []
    for score, idx in zip(distances[0], indices[0]):
        if score >= min_score and idx >= 0:
            results.append({
                'score': float(score),
                'text': texts[idx],
                'meta': metas[idx]
            })
    
    return results
```

---

## 🤖 D) RESPONSE GENERATION

### Priority-Based Architecture

#### Level 1: Direct FAQ Match (Highest Priority)
**Trigger**: FAQ source with score ≥ 0.25

**Process**:
1. Extract exact answer from database
2. For non-English: AI translation only
3. Return structured response

**Example**:
```
Q: "What are the library hours?"
→ FAQ match found (score: 0.92)
→ Return: "Library operates 8 AM to 8 PM on weekdays"
```

#### Level 2: Document Content Match
**Trigger**: Document/Upload source with score ≥ 0.25

**Process**:
1. Extract relevant context (800 char preview)
2. Format: "According to campus records: [context]"
3. For non-English: AI translation

**Example**:
```
Q: "Tell me about the computer lab"
→ Document match (score: 0.78)
→ Return: "According to campus records: The computer lab has 50 workstations..."
```

#### Level 3: AI Fallback (Lowest Priority)
**Trigger**: No database match (all scores < threshold)

**Process**:
1. Call Gemini API with personality prompt
2. Generate contextual response
3. Multi-language native generation

**Example**:
```
Q: "How do I improve my coding skills?"
→ No database match
→ Gemini generates personalized advice
```

### Response Flow Diagram

```
User Query
    ↓
[Check Greetings] → Match → Return greeting
    ↓ No match
[Search Database] → FAQ match → Return FAQ answer
    ↓ No match  
[Search Documents] → Document match → Return document excerpt
    ↓ No match
[Gemini AI] → Generate creative response
    ↓
[Log Conversation] → Save to ChatLog
    ↓
[Return Response] → Send to user
```

### Multi-Language Support

**Supported Languages**: English, Tamil, Hindi

**Translation Strategy**:
1. **Database content**: AI translates stored answer
2. **AI responses**: Native generation in target language

**Implementation**:
```python
if language != 'english':
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemma-3-4b-it')
    
    prompt = f"Translate this to {language}: {answer}"
    response = model.generate_content(prompt)
```

---

## 🎨 E) USER INTERFACE

### User Features

1. **Authentication**
   - Login/Signup system
   - Session management
   - Password hashing

2. **Chat Interface**
   - Modern Copilot-inspired design
   - Real-time conversation bubbles
   - Typing indicators
   - Message history

3. **Multi-Language Selection**
   - Dropdown for English/Tamil/Hindi
   - Persistent across session

4. **Voice Input**
   - Web Speech API integration
   - Hands-free queries
   - Browser support required

5. **Responsive Design**
   - Mobile-first approach
   - Bootstrap 5 components
   - Touch-friendly interface

### Admin Features

1. **Dashboard**
   - Content management overview
   - Quick stats (FAQs, Documents, Users)

2. **FAQ Management**
   - Add new FAQs
   - Edit existing entries
   - Delete outdated content

3. **Document Management**
   - Upload files (PDF, DOCX, TXT, Images)
   - View uploaded documents
   - Delete files

4. **Chat Logs**
   - View all user conversations
   - Monitor chatbot performance
   - Analytics potential

### UI Components

#### Homepage
- Centered input box
- Suggestion buttons
- Clean, modern design

#### Chat Page
- Message bubbles (user/AI)
- Timestamp display
- Scroll-to-bottom auto
- Loading animations

#### Admin Dashboard
- Tabbed interface
- CRUD modals
- File upload form
- Data tables

---

## 🔧 Technical Implementation

### Key Files Structure

```
CHATBOT/
├── app.py                  # Main Flask application (756 lines)
├── models.py               # SQLAlchemy database models
├── ai.py                   # NLP & semantic search logic
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
│
├── templates/              # HTML templates
│   ├── login.html
│   ├── signup.html
│   ├── chat.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── index.html
│
├── static/
│   ├── uploads/           # Uploaded documents
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript files
│
└── instance/
    └── chatbot.db         # SQLite database
```

### Dependencies

**Core Framework**:
- Flask==2.3.3
- Flask-SQLAlchemy==3.0.5
- Flask-Session==0.5.0

**NLP & AI**:
- sentence-transformers==2.2.2
- faiss-cpu==1.7.4
- google-generativeai==0.8.3

**File Processing**:
- pdfplumber==0.10.3
- python-docx==1.1.0
- Pillow==10.1.0
- easyocr==1.7.0
- pytesseract==0.3.10

**Utilities**:
- numpy==1.24.3
- requests==2.31.0
- python-dotenv==1.0.1
- werkzeug==2.3.7

### Environment Setup

**.env file**:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SECRET_KEY=your_flask_secret_key
DATABASE_URL=sqlite:///instance/chatbot.db
```

For MySQL:
```env
DATABASE_URL=mysql://username:password@localhost/dbname
```

---

## 🚀 API Endpoints

### Public Endpoints

#### POST /api/chat
```json
Request:
{
  "message": "What are the library hours?",
  "language": "english"
}

Response:
{
  "response": "Library operates 8 AM to 8 PM..."
}
```

### User Endpoints

#### GET /api/chat_logs
Returns user's last 50 conversations

#### DELETE /api/chat_logs/<id>
Delete specific chat log

### Admin Endpoints

All require `session['admin']` authentication

#### GET /api/faqs
List all FAQs

#### POST /api/faqs
Add new FAQ
```json
{
  "question": "What is the fee structure?",
  "answer": "The annual fee is..."
}
```

#### PUT /api/faqs/<id>
Update FAQ

#### DELETE /api/faqs/<id>
Delete FAQ

#### GET /api/documents
List all documents

#### POST /api/documents
Upload document (multipart/form-data)

#### PUT /api/documents/<id>
Update document

#### DELETE /api/documents/<id>
Delete document

#### GET /api/admin/chat_logs
View all chat logs (200 recent)

---

## 📊 Performance Optimization

### 1. Embedding Caching
- Load once at startup
- Rebuild only on data changes
- In-memory FAISS index

### 2. Chunking Benefits
- Faster retrieval (smaller vectors)
- Better precision (focused context)
- Reduced memory per query

### 3. Database Priority
- Instant answers for known questions
- No AI API call latency
- Cost reduction

### 4. Lazy Loading
- Only load AI model when needed
- Fallback to local answers
- Graceful degradation

---

## 🔒 Security Features

1. **Password Hashing**
   - Werkzeug's `generate_password_hash()`
   - PBKDF2 algorithm

2. **Session Management**
   - Flask sessions with SECRET_KEY
   - Server-side storage

3. **Input Validation**
   - File type checking
   - Size limits (20MB max)
   - Secure filenames

4. **Access Control**
   - Admin-only endpoints protected
   - User-specific chat logs
   - Authentication checks

---

## 🧪 Testing Strategy

### Manual Testing Checklist

1. ✅ User signup/login
2. ✅ Admin login
3. ✅ FAQ CRUD operations
4. ✅ Document upload (all formats)
5. ✅ Chat with greetings
6. ✅ Chat with FAQ match
7. ✅ Chat with document match
8. ✅ Chat with AI fallback
9. ✅ Multi-language responses
10. ✅ Chat history viewing

### Automated Tests

Located in:
- `test_chat_flow.py` - Full conversation flow
- `test_gemini_api.py` - AI integration
- `test_simple.py` - Basic functionality

---

## 📈 Future Enhancements

1. **Advanced Analytics**
   - Most asked questions
   - User engagement metrics
   - Response accuracy tracking

2. **Improved NLP**
   - Entity recognition
   - Intent classification
   - Sentiment analysis

3. **Caching Layer**
   - Redis for sessions
   - Response caching

4. **Deployment**
   - Docker containerization
   - Production server (Gunicorn)
   - Cloud hosting (AWS/GCP)

5. **Extended File Support**
   - Excel spreadsheets
   - PowerPoint presentations
   - Video transcripts

6. **API Documentation**
   - OpenAPI/Swagger specs
   - Interactive testing

---

## 🐛 Troubleshooting

### Common Issues

**1. No API Token Error**
```
Solution: Add GEMINI_API_KEY to .env file
```

**2. Import Errors**
```bash
pip install -r requirements.txt
```

**3. Database Not Found**
```bash
python setup_db.py
```

**4. OCR Not Working**
```bash
# Install Tesseract
# Windows: Download installer
# Linux: sudo apt-get install tesseract-ocr
```

**5. FAISS Import Error**
```bash
pip install faiss-cpu
```

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Generative AI](https://ai.google.dev/)
- [Hugging Face Models](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

---

## 👥 Credits

Developed as an AI-powered campus assistant chatbot with intelligent database priority architecture.

**Key Features**:
- ✅ Database-first response strategy
- ✅ Semantic search with FAISS
- ✅ Multi-language support (EN/TAM/HIN)
- ✅ Document processing with OCR
- ✅ Modern web interface
- ✅ Admin content management
- ✅ Conversation logging

**Architecture Philosophy**: Fast, accurate, cost-effective answers through intelligent caching and prioritization.
