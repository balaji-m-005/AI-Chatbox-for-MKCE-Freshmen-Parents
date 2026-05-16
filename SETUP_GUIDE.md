# AI Chatbot Setup Guide

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key (get from https://makersuite.google.com/app/apikey)
- 4GB RAM minimum (for ML models)
- 2GB free disk space

### Step-by-Step Installation

#### 1. Clone/Navigate to Project Directory

```bash
cd c:\CHATBOT
```

#### 2. Create Virtual Environment (Recommended)

**Windows**:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask web framework
- SQLAlchemy ORM
- SentenceTransformers for NLP
- FAISS for semantic search
- Google Generative AI
- PDF/DOCX/Image processing libraries
- And more...

**Note**: Installation may take 5-10 minutes due to ML packages.

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google Gemini API Key (REQUIRED)
GEMINI_API_KEY=your_actual_api_key_here

# Flask Secret Key (change for production)
SECRET_KEY=your-secret-key-change-this

# Database URL (SQLite default)
DATABASE_URL=sqlite:///instance/chatbot.db

# For MySQL (optional):
# DATABASE_URL=mysql://username:password@localhost/dbname
```

**Get Gemini API Key**:
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

#### 5. Initialize Database

```bash
python setup_db.py
```

This creates:
- SQLite database file
- All required tables
- Default admin account

**Default Admin Credentials**:
- Username: `927623bec200`
- Password: `senthil@2006`

#### 6. Add Initial FAQs (Optional)

```bash
python add_initial_faqs.py
```

Populates database with sample FAQ entries for testing.

#### 7. Run the Application

```bash
python app.py
```

Or use Flask CLI:
```bash
flask run
```

Server starts at: `http://127.0.0.1:5000/`

---

## 🌐 Accessing the Application

### User Interface

1. Open browser: `http://127.0.0.1:5000/`
2. Login or Signup
3. Start chatting!

### Admin Dashboard

1. Visit: `http://127.0.0.1:5000/admin/login`
2. Login with admin credentials
3. Manage FAQs, Documents, and view chat logs

---

## 📁 Project Structure

```
CHATBOT/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── ai.py                       # NLP & semantic search
├── setup_db.py                 # Database initialization
├── add_initial_faqs.py         # Sample data seeder
├── test_chat_flow.py           # Test suite
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
│
├── templates/                  # HTML templates
│   ├── login.html
│   ├── signup.html
│   ├── chat.html
│   ├── admin_login.html
│   └── admin_dashboard.html
│
├── static/
│   ├── uploads/               # User uploaded files
│   ├── css/                   # Stylesheets
│   └── js/                    # JavaScript
│
└── instance/
    └── chatbot.db             # SQLite database
```

---

## 🔧 Configuration Options

### Database Selection

**SQLite (Default)**:
```env
DATABASE_URL=sqlite:///instance/chatbot.db
```

**MySQL**:
```env
DATABASE_URL=mysql://username:password@localhost/chatbot_db
```

Install MySQL connector:
```bash
pip install mysql-connector-python==8.1.0
```

### File Upload Limits

Edit `app.py` to change max upload size:
```python
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB
```

### Upload Folder Location

```python
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
```

---

## 🧪 Testing the System

### 1. Test User Authentication

```
1. Visit http://127.0.0.1:5000/
2. Click "Sign Up"
3. Create new account
4. Login with credentials
```

### 2. Test Chat Functionality

```
1. Login as user
2. Go to chat page
3. Try greetings: "hi", "hello"
4. Ask campus questions
5. Check response quality
```

### 3. Test Admin Features

```
1. Visit /admin/login
2. Login as admin
3. Add new FAQ
4. Upload a PDF document
5. View chat logs
```

### 4. Test Multi-Language

```
1. In chat interface
2. Select Tamil or Hindi
3. Ask question in selected language
4. Verify translation quality
```

### 5. Test File Uploads

Supported formats:
- PDF documents
- Word (.docx)
- Text files (.txt)
- Images with OCR (.png, .jpg)

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError

**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: GEMINI_API_KEY not found

**Solution**:
1. Check `.env` file exists
2. Verify API key is correct
3. Restart Flask server

### Issue: Database errors

**Solution**:
```bash
# Delete old database
rm instance/chatbot.db  # Linux/Mac
del instance\chatbot.db  # Windows

# Recreate
python setup_db.py
```

### Issue: Port already in use

**Solution**:
```bash
# Kill process on port 5000
# Windows PowerShell:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or change port in app.py:
app.run(port=5001)
```

### Issue: Slow first query

**Normal**: First query loads ML models (~10-30 seconds)
**Solution**: Warm up the system by asking a test question first

### Issue: OCR not working

**Windows**: Install Tesseract
- Download: https://github.com/UB-Mannheim/tesseract/wiki

**Linux**:
```bash
sudo apt-get install tesseract-ocr
```

---

## 🚀 Production Deployment

### Using Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Windows Alternative

```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Environment Variables for Production

```env
FLASK_ENV=production
SECRET_KEY=<strong-random-string>
DATABASE_URL=<production-database>
GEMINI_API_KEY=<your-api-key>
```

### HTTPS Requirement

For Web Speech API (voice input), HTTPS is required in production.

---

## 📊 Monitoring & Maintenance

### Check Database Size

```bash
# SQLite
du -h instance/chatbot.db

# Or query from Python
python -c "import os; print(os.path.getsize('instance/chatbot.db'))"
```

### View Logs

Flask debug mode shows console logs. For production:

```python
import logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO)
```

### Backup Database

```bash
# Copy database file
cp instance/chatbot.db backup_$(date +%Y%m%d).db
```

### Clear Old Chat Logs

Add this route temporarily to `app.py`:

```python
@app.route('/clear_logs')
def clear_logs():
    ChatLog.query.delete()
    db.session.commit()
    return "Logs cleared"
```

---

## 🎓 Learning Resources

### Flask Documentation
- Official Docs: https://flask.palletsprojects.com/
- Tutorial: https://flask.palletsprojects.com/en/2.3.x/tutorial/

### Machine Learning Models
- Sentence Transformers: https://www.sbert.net/
- FAISS: https://github.com/facebookresearch/faiss

### Google Gemini AI
- Documentation: https://ai.google.dev/
- Python SDK: https://github.com/google/generative-ai-python

### Web Development
- Bootstrap 5: https://getbootstrap.com/docs/5.0/
- Font Awesome: https://fontawesome.com/icons

---

## ✅ System Requirements Checklist

- [ ] Python 3.8+ installed
- [ ] pip package manager working
- [ ] 4GB+ RAM available
- [ ] 2GB+ free disk space
- [ ] Google Gemini API key obtained
- [ ] Virtual environment created (recommended)
- [ ] All dependencies installed
- [ ] .env file configured
- [ ] Database initialized
- [ ] Port 5000 available
- [ ] Browser accessible

---

## 🎉 Next Steps

After successful setup:

1. **Customize Content**
   - Add your institution's FAQs
   - Upload relevant documents
   - Customize chatbot personality

2. **Test Thoroughly**
   - Run test scripts
   - Verify all features
   - Check edge cases

3. **Deploy**
   - Choose hosting platform
   - Configure production settings
   - Set up domain name

4. **Monitor & Improve**
   - Review chat logs
   - Add missing information
   - Optimize responses

---

## 📞 Support

For issues or questions:
1. Check ARCHITECTURE.md for technical details
2. Review troubleshooting section above
3. Examine console logs for errors
4. Test individual components

Happy chatting! 🤖💬
