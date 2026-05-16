# Quick Reference Card - AI Chatbot

## 🚀 Quick Start (30 seconds)

```bash
# 1. Activate virtual environment
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Run the application
python app.py

# 3. Open browser
http://127.0.0.1:5000/
```

---

## 👥 Default Login Credentials

### Admin Access
```
URL: http://127.0.0.1:5000/admin/login
Username: 927623bec200
Password: senthil@2006
```

### User Access
```
URL: http://127.0.0.1:5000/
Create new account → Login → Start chatting
```

---

## 📋 API Endpoints Cheat Sheet

### Public Routes
```
POST   /api/chat              - Send message, get response
GET    /api/chat_logs         - User's chat history
DELETE /api/chat_logs/:id     - Delete specific log
```

### Admin Routes (Protected)
```
GET    /api/faqs              - List all FAQs
POST   /api/faqs              - Add new FAQ
PUT    /api/faqs/:id          - Update FAQ
DELETE /api/faqs/:id          - Remove FAQ

GET    /api/documents         - List documents
POST   /api/documents         - Upload file
PUT    /api/documents/:id     - Update document
DELETE /api/documents/:id     - Delete document

GET    /api/admin/chat_logs   - View all conversations
```

---

## 🗄️ Database Schema Quick View

```sql
-- Users
Admin(id, username, password)
User(id, username, password)

-- Knowledge Base
FAQ(id, question, answer)
Document(id, title, content, filename, uploaded_at)

-- Logs
ChatLog(id, user, user_message, bot_response, timestamp)
```

---

## 🔧 Configuration (.env)

```env
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/chatbot.db
```

---

## 💻 Common Commands

### Setup
```bash
pip install -r requirements.txt
python setup_db.py
python add_initial_faqs.py
```

### Running
```bash
python app.py
# OR
flask run
```

### Testing
```bash
python test_chat_flow.py
python test_gemini_api.py
```

### Maintenance
```bash
# Clear chat logs (add temp route)
@app.route('/clear_logs')
def clear_logs():
    ChatLog.query.delete()
    db.session.commit()
```

---

## 🎯 Query Processing Flow

```
User Input
    ↓
[1] Check Greeting? → Yes → Return greeting
    ↓ No
[2] Generate Embedding
    ↓
[3] FAISS Search
    ↓
[4] Score ≥ 0.25? → Yes → Return DB answer (FAST)
    ↓ No
[5] Gemini AI → Generate response (SLOWER)
    ↓
[6] Log conversation
    ↓
[7] Return to user
```

---

## 📊 File Format Support

| Format | Extension | Library | Use Case |
|--------|-----------|---------|----------|
| PDF | .pdf | pdfplumber | Documents, brochures |
| Word | .docx, .doc | python-docx | Guidelines, notices |
| Text | .txt | built-in | Simple notes |
| Image | .png, .jpg | EasyOCR | Posters, scanned docs |

---

## 🌐 Multi-Language Codes

```python
language_labels = {
    'english': 'English',
    'tamil': 'Tamil',
    'hindi': 'Hindi'
}

# Usage in API call
{
  "message": "Library hours?",
  "language": "english"  # or "tamil", "hindi"
}
```

---

## ⚡ Performance Tips

### Fast Response (<1s)
- ✅ FAQ matches
- ✅ Document excerpts
- ✅ Cached embeddings

### Medium Response (2-5s)
- 🤖 AI-generated answers
- 🌐 Translations
- 📚 Complex queries

### Optimization Strategies
1. Add more FAQs for common questions
2. Chunk large documents (automatic >1000 chars)
3. Keep database updated
4. Warm up ML models on startup

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| No API key | Check `.env` file |
| Port busy | Change port in `app.py` |
| DB error | Run `python setup_db.py` |
| Slow first query | Normal - ML loading |
| OCR fails | Install Tesseract |

---

## 📁 Project Structure at a Glance

```
CHATBOT/
├── app.py                 ← Main app (756 lines)
├── models.py              ← DB models (33 lines)
├── ai.py                  ← NLP logic (226 lines)
├── templates/             ← HTML files
│   ├── chat.html
│   ├── admin_dashboard.html
│   └── ...
├── static/
│   └── uploads/           ← User files
└── instance/
    └── chatbot.db         ← SQLite DB
```

---

## 🎨 UI Color Scheme

```css
Background: #faf9f6 (off-white)
Primary: #007bff (blue)
Success: #28a745 (green)
Warning: #ffc107 (amber)
Danger: #dc3545 (red)
Border-radius: 20px
```

---

## 🔒 Security Checklist

- [x] Password hashing (Werkzeug PBKDF2)
- [x] Session management (Flask sessions)
- [x] File type validation
- [x] Size limits (20MB max)
- [x] Secure filenames
- [x] Auth checks on routes
- [ ] Rate limiting (future)
- [ ] CSRF protection (future)

---

## 📈 Monitoring Metrics

Track these KPIs:
- Daily Active Users (DAU)
- Average Response Time
- FAQ Match Rate (%)
- AI Fallback Rate (%)
- Most Common Queries
- Unanswered Questions
- Language Distribution

---

## 🆘 Emergency Commands

### Reset Everything
```bash
# Windows PowerShell
Remove-Item -Recurse -Force instance
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python setup_db.py
python app.py
```

### Backup Database
```bash
cp instance/chatbot.db backup_$(date +%Y%m%d).db
```

### Check What's Running
```bash
# Find Flask process
netstat -ano | findstr :5000
```

---

## 📞 Quick Links

- **Architecture Docs**: ARCHITECTURE.md
- **Setup Guide**: SETUP_GUIDE.md
- **User Manual**: USER_GUIDE.md
- **Flask Docs**: https://flask.palletsprojects.com/
- **Gemini AI**: https://ai.google.dev/
- **FAISS**: https://github.com/facebookresearch/faiss

---

## 🎯 Success Criteria

✅ System is working when:
- User can signup/login
- Bot responds to greetings
- FAQ matches return instantly
- Documents are searchable
- AI fallback works
- Multi-language functional
- Admin can manage content

❌ Issues if:
- Database errors appear
- API key missing
- Imports failing
- Port conflicts
- Extremely slow responses

---

**Print this card and keep it handy!** 📇
