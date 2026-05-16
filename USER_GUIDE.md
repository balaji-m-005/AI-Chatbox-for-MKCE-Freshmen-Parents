# AI Chatbot User Guide

## 📖 Table of Contents

1. [Getting Started](#getting-started)
2. [User Features](#user-features)
3. [Admin Features](#admin-features)
4. [Best Practices](#best-practices)
5. [FAQs](#faqs)

---

## 🎯 Getting Started

### For Students/Users

#### Step 1: Access the Chatbot

Open your web browser and go to:
```
http://127.0.0.1:5000/
```

#### Step 2: Create Account (First Time)

1. Click **"Sign Up"** button
2. Enter desired username
3. Create a secure password
4. Click **"Register"**
5. You'll be redirected to login

#### Step 3: Login

1. Enter your username
2. Enter your password
3. Click **"Login"**
4. You'll enter the chat interface!

---

## 💬 User Features

### 1. Chat Interface

![Chat Interface](assets/chat-interface.png)

**Components**:
- **Message Area**: Your conversation history
- **Input Box**: Type your questions here
- **Send Button**: Submit your message
- **Language Selector**: Choose English/Tamil/Hindi
- **Voice Input**: Speak your question (if supported)
- **Logout**: Exit your session

### 2. Asking Questions

#### Types of Questions You Can Ask:

**Greetings**:
- "Hi" / "Hello" / "Hey"
- "Good morning" / "Good afternoon"
- "How are you?"

**Campus Information**:
- "What are the library hours?"
- "Where is the computer lab located?"
- "Tell me about the cafeteria"
- "What are the college timings?"

**Academic Queries**:
- "When are the exams scheduled?"
- "What is the fee structure?"
- "How do I apply for leave?"
- "Tell me about the attendance policy"

**Technical Questions**:
- "Explain machine learning"
- "How to create a website?"
- "What is Python used for?"
- "Help me debug this code"

**General Knowledge**:
- "Who invented the computer?"
- "What is artificial intelligence?"
- "Tell me about space exploration"

### 3. Multi-Language Support

#### How to Change Language:

1. Look for language dropdown in chat interface
2. Select your preferred language:
   - **English** - Default
   - **Tamil** (தமிழ்)
   - **Hindi** (हिन्दी)
3. Continue chatting in selected language

#### Examples:

**English**:
```
Q: What are the library hours?
A: Library operates from 8 AM to 8 PM on weekdays.
```

**Tamil**:
```
Q: நூலகம் எப்போது திறந்திருக்கும்?
A: நூலகம் காலை 8 மணி முதல் மாலை 8 மணி வரை திறந்திருக்கும்.
```

**Hindi**:
```
Q: पुस्तकालय कब खुलता है?
A: पुस्तकालय सुबह 8 बजे से शाम 8 बजे तक खुलता है।
```

### 4. Voice Input (If Supported)

#### Requirements:
- Modern browser (Chrome, Firefox, Edge)
- Microphone access granted
- HTTPS connection (in production)

#### How to Use:

1. Click **microphone icon**
2. Allow microphone access if prompted
3. Speak your question clearly
4. Wait for text to appear
5. Edit if needed
6. Press Send

#### Tips:
- Speak clearly and at normal pace
- Minimize background noise
- Works best in quiet environment

### 5. Chat History

Your last 50 conversations are saved automatically.

#### To View History:
- Scroll up in chat window
- Previous messages load automatically
- Each message shows timestamp

#### To Clear History:
History is personal and persistent. Contact admin if you need deletion.

---

## 👨‍💼 Admin Features

### Accessing Admin Panel

1. Visit: `http://127.0.0.1:5000/admin/login`
2. Login with admin credentials:
   - Username: `927623bec200`
   - Password: `senthil@2006`
3. You'll see the admin dashboard

### Dashboard Overview

The admin panel has several sections:

#### 1. FAQ Management

**Purpose**: Add/Edit/Delete frequently asked questions

**Add New FAQ**:
1. Click **"Add FAQ"** button
2. Enter question (e.g., "What is the exam fee?")
3. Enter answer (e.g., "The exam fee is $50")
4. Click **"Save"**

**Edit Existing FAQ**:
1. Find FAQ in the list
2. Click **"Edit"** button
3. Modify question or answer
4. Click **"Update"**

**Delete FAQ**:
1. Find FAQ in the list
2. Click **"Delete"** button
3. Confirm deletion

**Tips for Good FAQs**:
- Use clear, specific questions
- Provide complete answers
- Include relevant details
- Update regularly

#### 2. Document Management

**Purpose**: Upload campus documents, brochures, guidelines

**Upload Document**:
1. Click **"Upload Document"**
2. Choose file from your computer
3. Enter document title
4. Click **"Upload"**

**Supported Formats**:
- ✅ PDF files (.pdf)
- ✅ Word documents (.docx, .doc)
- ✅ Text files (.txt)
- ✅ Images with text (.png, .jpg, .jpeg)

**File Size Limit**: 20 MB per file

**How It Works**:
1. System extracts text from file
2. Creates semantic embeddings
3. Makes content searchable
4. Returns relevant excerpts when queried

**Example Workflow**:

```
Step 1: Upload "Library_Rules.pdf"
Step 2: Student asks "What are the library rules?"
Step 3: Bot returns excerpt from uploaded PDF
```

**Edit Document Info**:
1. Find document in list
2. Click **"Edit"**
3. Change title or content
4. Save changes

**Delete Document**:
1. Click **"Delete"** next to document
2. Confirm deletion
3. File removed from system

#### 3. Chat Logs Monitoring

**Purpose**: View all conversations users have had with bot

**Access Logs**:
1. Go to "Chat Logs" section
2. See list of recent conversations
3. Includes: User, Question, Answer, Timestamp

**Use Cases**:
- Monitor bot performance
- Identify common questions
- Find missing information
- Improve response quality

**Export Logs** (Manual):
1. Select logs you need
2. Copy/paste to spreadsheet
3. Analyze patterns

---

## 🎯 Best Practices

### For Users

#### Asking Effective Questions:

✅ **DO**:
- Be specific: "What time does the library close?"
- Use proper spelling
- Include context when needed
- Check previous messages first

❌ **DON'T**:
- Ask multiple questions at once
- Use excessive slang or abbreviations
- Ask ambiguous questions
- Spam repetitive queries

#### Examples:

**Good Questions**:
```
✓ "When is the last date to register for courses?"
✓ "Where can I find the syllabus for CS301?"
✓ "How do I apply for a transcript?"
```

**Vague Questions** (avoid):
```
✗ "info about exam"
✗ "tell me everything"
✗ "help me"
```

### For Admins

#### Managing Content Effectively:

1. **Regular Updates**
   - Review FAQs monthly
   - Update outdated information
   - Add seasonal notices (exam schedules, holidays)

2. **Document Organization**
   - Use descriptive filenames
   - Group related documents
   - Remove obsolete files

3. **Quality Control**
   - Test bot responses regularly
   - Review chat logs weekly
   - Identify knowledge gaps

4. **Content Strategy**
   - Start with top 20 common questions
   - Expand based on user queries
   - Prioritize high-impact information

#### Sample Content Plan:

**Week 1**: Basic FAQs (admissions, fees, timings)
**Week 2**: Academic policies (attendance, exams, grading)
**Week 3**: Campus facilities (library, labs, sports)
**Week 4**: Student services (counseling, placement, clubs)

---

## ❓ Frequently Asked Questions (FAQs)

### General Questions

**Q: Is the chatbot available 24/7?**
A: Yes! The AI chatbot works round the clock.

**Q: Can I access chatbot from mobile?**
A: Absolutely! The interface is mobile-responsive.

**Q: Are my conversations private?**
A: Your chats are logged but only visible to admins for improvement purposes.

**Q: Can I use chatbot in regional languages?**
A: Currently supports English, Tamil, and Hindi.

### Technical Questions

**Q: Why is the first response slow?**
A: Initial ML model loading takes time (~10-30 seconds). Subsequent queries are fast.

**Q: Voice input not working?**
A: Ensure browser supports Web Speech API and microphone permission is granted.

**Q: Can I download my chat history?**
A: Currently not available. Contact admin for data requests.

### Admin-Specific

**Q: How many FAQs can I add?**
A: No hard limit, but keep it manageable (50-100 recommended).

**Q: Can I edit uploaded documents?**
A: You must delete and re-upload to change file content.

**Q: How to backup database?**
A: Copy the `instance/chatbot.db` file regularly.

---

## 🔧 Troubleshooting for Users

### Common Issues & Solutions

#### Issue: Cannot login
**Solutions**:
- Check username/password spelling
- Ensure caps lock is off
- Try password reset via admin
- Clear browser cache

#### Issue: Chatbot not responding
**Solutions**:
- Refresh the page
- Check internet connection
- Wait a few seconds (AI processing)
- Try simpler question

#### Issue: Wrong answers
**Solutions**:
- Rephrase your question
- Be more specific
- Check if admin has uploaded relevant info
- Provide feedback to admin

#### Issue: Language not changing
**Solutions**:
- Refresh page after selection
- Ensure proper encoding (UTF-8)
- Try different browser

---

## 📊 Understanding Response Types

### 1. Database Answers (Fastest)

When your question matches existing content:

```
Q: "What are the library hours?"
→ Bot finds exact FAQ match
→ Returns stored answer instantly
→ Label: "According to campus records..."
```

**Characteristics**:
- ⚡ Very fast (<1 second)
- 📚 Accurate, official information
- ✅ High confidence

### 2. AI-Generated Answers (Slower)

When question needs general knowledge:

```
Q: "How do I improve coding skills?"
→ No database match found
→ Gemini AI generates response
→ Personalized advice
```

**Characteristics**:
- ⏱️ Takes 2-5 seconds
- 🤖 Creative, contextual
- 💡 Educational content

### 3. Translation Layer

For non-English queries:

```
Q (Tamil): "நூலகம் எங்கே உள்ளது?"
→ Bot searches database
→ Finds English answer
→ AI translates to Tamil
→ Returns: "நூலகம் கட்டிடம் A-இல் உள்ளது"
```

**Characteristics**:
- 🌐 Maintains meaning
- 📝 Natural phrasing
- 🎯 Context-appropriate

---

## 🎓 Tips for Best Results

### 1. Start Simple
Begin with basic questions to understand bot capabilities.

### 2. Be Specific
Instead of "tell me about exams", ask "when are mid-semester exams?"

### 3. Use Keywords
Include important terms: "library", "fees", "exam", "lab", etc.

### 4. Check Admin Updates
New documents and FAQs improve bot knowledge.

### 5. Provide Feedback
If bot gives wrong answer, inform admin to update content.

---

## 📈 Usage Statistics (For Admins)

Track these metrics:

- **Daily Active Users**: How many unique users daily
- **Most Asked Questions**: Identify trends
- **Unanswered Queries**: Find knowledge gaps
- **Response Times**: Monitor performance
- **Language Preferences**: Serve users better

---

## 🆘 Getting Help

### If You're Stuck:

1. **Check Documentation**
   - Read this user guide
   - Review ARCHITECTURE.md for technical details

2. **Contact Admin**
   - Report bugs or issues
   - Suggest improvements
   - Request features

3. **Technical Support**
   - Check SETUP_GUIDE.md
   - Review error logs
   - Test components individually

---

## 🎉 Making the Most of Your Chatbot

### Success Stories

**Scenario 1: Quick Information**
```
Student: "When is the next holiday?"
Bot: "Next holiday is on April 14 for Tamil New Year."
Result: Instant answer, no searching needed
```

**Scenario 2: Study Help**
```
Student: "Explain neural networks simply"
Bot: Provides clear explanation with examples
Result: Learning aid available 24/7
```

**Scenario 3: Administrative Query**
```
Student: "How to get transfer certificate?"
Bot: Lists step-by-step procedure from admin docs
Result: Saves admin office time
```

### Pro Tips:

1. **Bookmark the chatbot** for quick access
2. **Use voice input** when typing is inconvenient
3. **Save useful responses** for future reference
4. **Share feedback** to improve the system
5. **Explore different topics** - bot knows more than you think!

---

## 🌟 What's New

### Recent Enhancements:

✅ Improved semantic search accuracy
✅ Faster response times
✅ Better multi-language support
✅ Document chunking for large files
✅ Enhanced OCR for images
✅ Conversation history per user
✅ Mobile-responsive design
✅ Dark mode support

### Coming Soon:

- 📊 Analytics dashboard
- 📱 Mobile app
- 🔔 Notifications
- 📥 Export chat history
- 🎨 Customizable themes
- 📈 Performance metrics

---

## 📞 Contact & Support

For technical issues or questions:
- Email: admin@mkce.edu
- Office Hours: 9 AM - 5 PM (Mon-Fri)
- Location: Computer Science Dept.

Remember: This chatbot is continuously improving thanks to your feedback and usage!

Happy Chatting! 🤖💬✨
