# 🏗️ AI Chatbot - System Architecture Visual Guide

## Complete System Overview

This document provides visual diagrams and flowcharts to understand the complete AI chatbot system architecture.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Student │  │  Admin   │  │  Mobile  │  │  Desktop │        │
│  │  Browser │  │  Browser │  │  Device  │  │  Device  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
│       └─────────────┴─────────────┴─────────────┘               │
│                          ↓                                       │
│                   HTTPS / HTTP                                   │
└──────────────────────────┼──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    APPLICATION LAYER (Flask)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              app.py (Main Application)                 │    │
│  │  ┌──────────────────────────────────────────────────┐ │    │
│  │  │  Route Handlers                                   │ │    │
│  │  │  • /login, /signup                                │ │    │
│  │  │  • /chat                                          │ │    │
│  │  │  • /admin/*                                       │ │    │
│  │  │  • /api/*                                         │ │    │
│  │  └──────────────────────────────────────────────────┘ │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Authentication & Security                             │    │
│  │  • Session Management                                  │    │
│  │  • Password Hashing                                    │    │
│  │  • Route Protection                                    │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────┐         ┌────────────────────┐         │
│  │   ai.py            │         │   models.py        │         │
│  │   (NLP Engine)     │         │   (Data Models)    │         │
│  │  ┌──────────────┐ │         │  ┌──────────────┐ │         │
│  │  │ SentenceBERT │ │         │  │ User Model   │ │         │
│  │  │ Embeddings   │ │         │  │ Admin Model  │ │         │
│  │  └──────────────┘ │         │  │ FAQ Model    │ │         │
│  │  ┌──────────────┐ │         │  │ Document     │ │         │
│  │  │ FAISS Index  │ │         │  │ ChatLog      │ │         │
│  │  │ Search       │ │         │  └──────────────┘ │         │
│  │  └──────────────┘ │         │                   │         │
│  └────────────────────┘         └────────────────────┘         │
│                                                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    DATA ACCESS LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────┐         ┌────────────────────┐         │
│  │   SQLAlchemy ORM   │         │   File System      │         │
│  │  ┌──────────────┐ │         │  ┌──────────────┐ │         │
│  │  │ Query Builder│ │         │  │ Uploads/     │ │         │
│  │  │ Transactions │ │         │  │ Documents    │ │         │
│  │  │ Connections  │ │         │  └──────────────┘ │         │
│  │  └──────────────┘ │         │                   │         │
│  └────────────────────┘         └────────────────────┘         │
│                                                                  │
└──────────┬──────────────────────────────────────────┬───────────┘
           │                                          │
┌──────────▼───────────┐                  ┌──────────▼───────────┐
│   DATABASE LAYER     │                  │   EXTERNAL APIs      │
├──────────────────────┤                  ├──────────────────────┤
│  ┌────────────────┐ │                  │  ┌────────────────┐ │
│  │ SQLite / MySQL │ │                  │  │ Google Gemini  │ │
│  │                │ │                  │  │ AI API         │ │
│  │ • Users        │ │                  │  └────────────────┘ │
│  │ • FAQs         │ │                  │                     │
│  │ • Documents    │ │                  │  ┌────────────────┐ │
│  │ • Chat Logs    │ │                  │  │ Web Speech     │ │
│  └────────────────┘ │                  │  │ API (Voice)    │ │
│                     │                  │  └────────────────┘ │
└─────────────────────┘                  └──────────────────────┘
```

---

## 🔄 Request Flow Diagram

### Complete Journey of a User Query

```
┌──────────┐
│  User    │
│  Types:  │
│ "What    │
│ are      │
│ library  │
│ hours?"  │
└────┬─────┘
     │
     │ 1. HTTP POST /api/chat
     ▼
┌─────────────────────────────────────────┐
│  Flask App (app.py)                     │
│  ┌─────────────────────────────────┐   │
│  │ 2. Authenticate User            │   │
│  │    ✓ Check session              │   │
│  │    ✓ Validate input             │   │
│  └─────────────────────────────────┘   │
└────┬────────────────────────────────────┘
     │
     │ 3. Preprocess Query
     ▼
┌─────────────────────────────────────────┐
│  NLP Engine (ai.py)                     │
│  ┌─────────────────────────────────┐   │
│  │ 4. Generate Embedding           │   │
│  │    - SentenceTransformer        │   │
│  │    - 384-dimensional vector     │   │
│  └─────────────────────────────────┘   │
│           │                             │
│           │ 5. Search FAISS Index       │
│           ▼                             │
│  ┌─────────────────────────────────┐   │
│  │ 6. Find Similar Content         │   │
│  │    - Cosine similarity          │   │
│  │    - Score ranking              │   │
│  │    - Threshold filtering        │   │
│  └─────────────────────────────────┘   │
└────┬────────────────────────────────────┘
     │
     │ 7a. High Score (≥0.25)?
     ├──────────────YES──────────────┐
     │                               │
     ▼                               ▼
┌─────────┐                   ┌──────────┐
│ FAQ/Doc │                   │ No Match │
│ Match   │                   │ Found    │
└────┬────┘                   └────┬─────┘
     │                             │
     │ 8a. Return DB Answer        │ 7b. Low Score (<0.25)?
     │    (Instant)                ├──────────────YES──────────────┐
     │                             │                               │
     ▼                             ▼                               ▼
┌─────────────────┐         ┌──────────┐                   ┌────────────┐
│ Format Response │         │ Check AI │                   │ Call       │
│ with Source     │         │ Fallback │                   │ Gemini API │
└────┬────────────┘         └────┬─────┘                   └─────┬──────┘
     │                           │                               │
     │                           │ 8b. Generate AI Response      │
     │                           │    (2-5 seconds)              │
     │                           ▼                               │
     │                    ┌──────────────┐                      │
     │                    │ Personality  │                      │
     │                    │ & Context    │                      │
     │                    └──────┬───────┘                      │
     │                           │                               │
     └───────────────┬───────────┴───────────────────────────────┘
                     │
                     │ 9. Combine Results
                     ▼
┌─────────────────────────────────────────┐
│  Response Assembly                      │
│  ┌─────────────────────────────────┐   │
│  │ • Select best answer            │   │
│  │ • Apply language translation    │   │
│  │ • Format for display            │   │
│  └─────────────────────────────────┘   │
└────┬────────────────────────────────────┘
     │
     │ 10. Log Conversation
     ▼
┌─────────────────────────────────────────┐
│  Database (ChatLog Table)               │
│  • Save user message                    │
│  • Save bot response                    │
│  • Timestamp                            │
└────┬────────────────────────────────────┘
     │
     │ 11. Return JSON Response
     ▼
┌─────────────────────────────────────────┐
│  {                                      │
│    "response": "Library operates..."    │
│  }                                      │
└────┬────────────────────────────────────┘
     │
     │ 12. Display to User
     ▼
┌──────────┐
│  User    │
│  Sees:   │
│ "Library │
│ operates │
│ 8AM-8PM" │
└──────────┘
```

---

## 🎯 Response Priority Decision Tree

```
                         User Query
                             │
                    ┌────────▼────────┐
                    │ Normalize Text  │
                    │ Lowercase, trim │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Is Greeting?    │
                    │ (hi, hello, etc)│
                    └────────┬────────┘
                         Yes │ No
                    ┌────────┴─────────┐
                    │                  │
              ┌─────▼─────┐    ┌──────▼──────┐
              │ Return    │    │ Generate    │
              │ Greeting  │    │ Embedding   │
              └───────────┘    └──────┬──────┘
                                     │
                              ┌──────▼──────┐
                              │ Search      │
                              │ FAISS Index │
                              └──────┬──────┘
                                     │
                              ┌──────▼──────┐
                              │ Get Scores  │
                              │ & Rank      │
                              └──────┬──────┘
                                     │
                        ┌────────────▼────────────┐
                        │ Top Score ≥ 0.25?      │
                        └────────────┬────────────┘
                             Yes     │     No
                    ┌────────────────┴──────┐    ┌─────────────┐
                    │                       │    │             │
              ┌─────▼─────┐         ┌──────▼──────┐  │  ┌──────▼──────┐
              │ Source =  │         │ Source =    │  │  │ Call Gemini │
              │ FAQ?      │         │ Document?   │  │  │ AI API      │
              └─────┬─────┘         └──────┬──────┘  │  └──────┬──────┘
               Yes  │ No                   │ Yes    │         │
          ┌─────────┴─┐           ┌────────┴──────┐ │         │
          │           │           │               │ │         │
    ┌─────▼─────┐ ┌──▼────────┐ ┌─▼──────────┐ ┌─▼─────────┐ │
    │ Return    │ │ Check Doc │ │ Extract    │ │ Generate  │ │
    │ FAQ       │ │ Score     │ │ Context    │ │ Response  │ │
    │ Answer    │ └─────┬─────┘ └─────┬──────┘ └─────┬─────┘ │
    │ Instant   │       │ Yes         │             │       │
    └───────────┘       │             │             │       │
                        └─────────────┴─────────────┘       │
                                      │                     │
                                      └──────────┬──────────┘
                                                 │
                                        ┌────────▼────────┐
                                        │ Translate if    │
                                        │ Non-English     │
                                        └────────┬────────┘
                                                 │
                                        ┌────────▼────────┐
                                        │ Log to Database │
                                        └────────┬────────┘
                                                 │
                                        ┌────────▼────────┐
                                        │ Return to User  │
                                        └─────────────────┘
```

---

## 📦 Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  index.html  │  │  login.html  │  │  signup.html │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              chat.html (Main Interface)              │     │
│  │  ┌────────────────────────────────────────────────┐ │     │
│  │  │  JavaScript: Handle user input, AJAX calls    │ │     │
│  │  └────────────────────────────────────────────────┘ │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │         admin_dashboard.html (Admin Panel)           │     │
│  │  ┌────────────────────────────────────────────────┐ │     │
│  │  │  JavaScript: CRUD operations, file upload     │ │     │
│  │  └────────────────────────────────────────────────┘ │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────┬──────────────────────────────────────────────────┘
              │
              │ HTTP Requests (AJAX/Fetch)
              ▼
┌────────────────────────────────────────────────────────────────┐
│                        BACKEND (Flask)                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  app.py                                                │   │
│  │                                                        │   │
│  │  @app.route('/api/chat')  ← Receives user queries     │   │
│  │  @app.route('/api/faqs')  ← FAQ management            │   │
│  │  @app.route('/api/documents') ← Document handling     │   │
│  │                                                        │   │
│  │  Calls: ai.py functions                                │   │
│  │  Queries: models.py tables                             │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  ai.py                                                 │   │
│  │                                                        │   │
│  │  build_knowledge_embeddings()                          │   │
│  │    ↓ Loads FAQs + Documents                            │   │
│  │    ↓ Creates Sentence-BERT embeddings                  │   │
│  │    ↓ Builds FAISS index                                │   │
│  │                                                        │   │
│  │  find_relevant_context(query)                          │   │
│  │    ↓ Encodes query                                     │   │
│  │    ↓ Searches FAISS index                              │   │
│  │    ↓ Returns ranked results                            │   │
│  │                                                        │   │
│  │  get_local_answer(query)                               │   │
│  │    ↓ Returns best DB match                             │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  models.py                                             │   │
│  │                                                        │   │
│  │  class Admin(db.Model)                                 │   │
│  │  class User(db.Model)                                  │   │
│  │  class FAQ(db.Model)                                   │   │
│  │  class Document(db.Model)                              │   │
│  │  class ChatLog(db.Model)                               │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────┬──────────────────────────────────────────────────┘
              │
              │ SQL Queries
              ▼
┌────────────────────────────────────────────────────────────────┐
│                        DATABASE                                 │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Admin   │  │  User    │  │  FAQ     │  │ Document │      │
│  │  Table   │  │  Table   │  │  Table   │  │  Table   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐         │
│  │              ChatLog Table                       │         │
│  │  (Stores all conversations for analytics)        │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔀 Data Flow: Admin Uploads Document

```
┌──────────┐
│  Admin   │
│  Login   │
└────┬─────┘
     │
     │ 1. Navigate to Dashboard
     ▼
┌─────────────────────────────────────────┐
│  Admin Dashboard                        │
│  ┌─────────────────────────────────┐   │
│  │ Click "Upload Document"         │   │
│  └─────────────────────────────────┘   │
└────┬────────────────────────────────────┘
     │
     │ 2. Select File (PDF/DOCX/TXT/Image)
     ▼
┌─────────────────────────────────────────┐
│  File Upload Form                       │
│  • Choose file                          │
│  • Enter title                          │
│  • Submit                               │
└────┬────────────────────────────────────┘
     │
     │ 3. POST /api/documents
     ▼
┌─────────────────────────────────────────┐
│  Flask Backend                          │
│  ┌─────────────────────────────────┐   │
│  │ Validate file type & size       │   │
│  │ Save to static/uploads/         │   │
│  └─────────────────────────────────┘   │
└────┬────────────────────────────────────┘
     │
     │ 4. Extract Text
     ▼
┌─────────────────────────────────────────┐
│  Text Extraction Pipeline               │
│                                         │
│  If PDF → pdfplumber.extract_text()    │
│  If DOCX → python-docx.paragraphs      │
│  If TXT → open().read()                │
│  If Image → easyocr.readtext()         │
└────┬────────────────────────────────────┘
     │
     │ 5. Store in Database
     ▼
┌─────────────────────────────────────────┐
│  Document Table                         │
│  • title: "Employee Handbook"           │
│  • content: [extracted text]            │
│  • filename: "handbook.pdf"             │
│  • uploaded_at: timestamp               │
└────┬────────────────────────────────────┘
     │
     │ 6. Trigger Rebuild
     ▼
┌─────────────────────────────────────────┐
│  ai.py: build_knowledge_embeddings()    │
│  ┌─────────────────────────────────┐   │
│  │ Load ALL FAQs + Documents       │   │
│  │ Generate embeddings             │   │
│  │ Update FAISS index              │   │
│  │ Cache in memory                 │   │
│  └─────────────────────────────────┘   │
└────┬────────────────────────────────────┘
     │
     │ 7. Confirmation
     ▼
┌─────────────────────────────────────────┐
│  Success Message                        │
│  "Document uploaded and indexed!"       │
└────┬────────────────────────────────────┘
     │
     │ Now searchable by students!
     ▼
┌──────────┐
│  Ready   │
│  for     │
│  Queries │
└──────────┘
```

---

## 🌐 Multi-Language Support Flow

```
User selects language: Tamil
     │
     │ Query in Tamil: "நூலகம் எங்கே உள்ளது?"
     ▼
┌─────────────────────────────────────────┐
│  Backend Processing                     │
│                                         │
│  1. Detect language = 'tamil'           │
│  2. Generate embedding for Tamil query  │
│  3. Search FAISS index (English DB)     │
│     Note: Embeddings are language-      │
│           agnostic at semantic level    │
│  4. Find matching English content       │
└────┬────────────────────────────────────┘
     │
     │ Match found in English:
     │ "The library is located in Building A"
     │
     ▼
┌─────────────────────────────────────────┐
│  Translation Decision                   │
│                                         │
│  Option A: Database Match               │
│  → Send to Gemini API:                  │
│     "Translate to Tamil: [content]"     │
│                                         │
│  Option B: AI Fallback                  │
│  → Prompt: "Respond in Tamil only"      │
│  → Gemini generates native Tamil        │
└────┬────────────────────────────────────┘
     │
     │ Translated to Tamil:
     │ "நூலகம் கட்டிடம் A-இல் உள்ளது"
     │
     ▼
┌─────────────────────────────────────────┐
│  Return Tamil Response                  │
│  Display to user in Tamil script        │
└─────────────────────────────────────────┘
```

---

## 📊 Technology Stack Layers

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
├─────────────────────────────────────────────────────────┤
│  HTML5     │  Structure & Content                      │
│  CSS3      │  Styling & Layout                         │
│  Bootstrap5│  Responsive Components                    │
│  Font      │  Icons & Visual Elements                  │
│  Awesome   │                                           │
│  JavaScript│  Client-side Logic & AJAX                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                    │
├─────────────────────────────────────────────────────────┤
│  Flask      │  Web Framework (Python)                  │
│  Werkzeug   │  WSGI Utilities & Security               │
│  Sessions   │  User State Management                   │
│  Jinja2     │  Template Rendering                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                  │
├─────────────────────────────────────────────────────────┤
│  Sentence    │  NLP Embeddings                          │
│  Transformers│                                           │
│  FAISS       │  Semantic Search Engine                  │
│  NumPy       │  Numerical Computing                     │
│  google-     │  Generative AI Integration               │
│  generativeai│                                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     DATA ACCESS LAYER                    │
├─────────────────────────────────────────────────────────┤
│  SQLAlchemy  │  ORM (Object-Relational Mapping)         │
│  pdfplumber  │  PDF Text Extraction                     │
│  python-docx │  Word Document Parsing                   │
│  EasyOCR     │  Image Text Recognition                  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                       DATA LAYER                         │
├─────────────────────────────────────────────────────────┤
│  SQLite      │  Primary Database (Dev)                  │
│  MySQL       │  Production Database                     │
│  File System │  Uploaded Documents Storage              │
└─────────────────────────────────────────────────────────┘
```

---

## 🎭 User Journey Map

```
Day in the Life of a Student Using Chatbot

┌─────────────────────────────────────────────────────────┐
│  MORNING: Need Information                              │
│                                                         │
│  8:30 AM  → Opens browser                              │
│           → Goes to college chatbot portal             │
│           → Logs in with credentials                   │
│                                                         │
│  8:31 AM  → Types: "When do exams start?"              │
│           → Bot instantly matches FAQ                  │
│           → Returns: "Exams begin April 15th"          │
│           ✅ Fast, accurate answer                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  AFTERNOON: Document Search                             │
│                                                         │
│  2:00 PM  → Needs syllabus details                     │
│         → Asks: "What's in CS301 syllabus?"            │
│         → Bot searches uploaded documents              │
│         → Finds excerpt from PDF                       │
│         → Returns relevant section                     │
│         ✅ Saved time searching manually                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  EVENING: General Question                              │
│                                                         │
│  7:00 PM  → Career curiosity                            │
│         → Asks: "How to prepare for FAANG interviews?"  │
│         → No database match                            │
│         → AI generates comprehensive guide             │
│         → Lists study plan, resources, tips            │
│         ✅ Valuable AI-powered advice                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  RESULT: Happy Student                                  │
│                                                         │
│  • Got instant answers to factual questions            │
│  • Found document information quickly                  │
│  • Received personalized career advice                 │
│  • Will recommend to friends                           │
│                                                         │
│  Admin Benefits:                                       │
│  • 50+ repetitive questions avoided                    │
│  • Students satisfied with 24/7 access                 │
│  • Staff can focus on complex queries                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Success Metrics Dashboard

```
┌─────────────────────────────────────────────────────────┐
│              CHATBOT ANALYTICS DASHBOARD                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TODAY'S STATS                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Total Queries│  │ Unique Users │  │ Avg Response │ │
│  │     342      │  │     127      │  │    0.8s      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  RESPONSE BREAKDOWN                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ FAQ Matches       ████████████████░░  65% ⚡    │   │
│  │ Document Matches  █████████░░░░░░░░░  20% 📚    │   │
│  │ AI Responses      ████░░░░░░░░░░░░░░  15% 🤖    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  LANGUAGE DISTRIBUTION                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ English         ██████████████████    78%       │   │
│  │ Tamil           ██████░░░░░░░░░░░░    15%       │   │
│  │ Hindi           ██░░░░░░░░░░░░░░░░     7%       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  TOP QUERIES TODAY                                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1. "Library hours"                (42 times)    │   │
│  │ 2. "Exam schedule"                (38 times)    │   │
│  │ 3. "Fee payment deadline"         (31 times)    │   │
│  │ 4. "Lab location"                 (27 times)    │   │
│  │ 5. "Holiday list"                 (24 times)    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  PERFORMANCE METRICS                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Uptime        │  │ Error Rate   │  │ API Cost     │   │
│  │  99.8%       │  │  0.2%        │  │  $0.45/day   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  COST SAVINGS                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Without DB Priority: $2.50/day (100% AI)        │   │
│  │ With DB Priority:  $0.45/day (15% AI)           │   │
│  │ 💰 Daily Savings: $2.05 (82% reduction)         │   │
│  │ 💰 Monthly Savings: ~$61.50                     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 System Scalability Model

```
GROWTH TRAJECTORY

Phase 1: PILOT (Current)
┌──────────────────────────────────────┐
│ Users: 50-100                        │
│ FAQs: 50                             │
│ Documents: 20                        │
│ Response Time: <1s                   │
│ Infrastructure: Single server        │
└──────────────────────────────────────┘
              │
              │ Growth
              ▼
Phase 2: DEPARTMENT (3 months)
┌──────────────────────────────────────┐
│ Users: 500-1000                      │
│ FAQs: 200                            │
│ Documents: 100                       │
│ Response Time: <1.5s                 │
│ Infrastructure: Load balancer + 2x   │
└──────────────────────────────────────┘
              │
              │ Expansion
              ▼
Phase 3: COLLEGE (6 months)
┌──────────────────────────────────────┐
│ Users: 2000-5000                     │
│ FAQs: 500                            │
│ Documents: 300                       │
│ Response Time: <2s                   │
│ Infrastructure: Cluster + Redis      │
└──────────────────────────────────────┘
              │
              │ Scale
              ▼
Phase 4: MULTI-COLLEGE (1 year)
┌──────────────────────────────────────┐
│ Users: 10,000+                       │
│ FAQs: 2000+                          │
│ Documents: 1000+                     │
│ Response Time: <2.5s                 │
│ Infrastructure: Cloud + CDN          │
└──────────────────────────────────────┘
```

---

**This visual guide provides a complete understanding of how all components work together!** 🎨📊

*Last Updated: April 2026*
