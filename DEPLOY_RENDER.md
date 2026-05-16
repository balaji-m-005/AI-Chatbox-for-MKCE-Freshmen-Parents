# Render Deployment Guide (Flask)

## 1. Prerequisites
- A Render account.
- Your project pushed to GitHub.
- A valid GEMINI_API_KEY.

## 2. Deploy Using render.yaml (Recommended)
1. In Render dashboard, click New + and select Blueprint.
2. Connect your GitHub repo.
3. Select this project.
4. Render will detect render.yaml automatically.
5. Add GEMINI_API_KEY in environment variables when prompted.
6. Click Apply.

## 3. Manual Deploy (Without Blueprint)
1. New + -> Web Service.
2. Connect GitHub repo.
3. Settings:
- Environment: Python
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn --bind 0.0.0.0:$PORT app:app

4. Environment Variables:
- GEMINI_API_KEY = your_key
- SECRET_KEY = any strong random value
- FLASK_DEBUG = 0
- DATABASE_URL = sqlite:///instance/chatbot.db

## 4. Important Production Notes
- SQLite on Render free web service is ephemeral.
- If you need persistent data, use Render Postgres and set DATABASE_URL from the Postgres service.
- The app supports postgres:// to postgresql:// conversion automatically.

## 5. Verify After Deploy
- Open deployed URL and check /login.
- Test API with a known DB query:
  - Who is the principal of MKCE?
- Test a general query:
  - who is arun

## 6. Optional: Persistent Postgres
1. Create Render Postgres service.
2. Copy Internal Database URL.
3. Set DATABASE_URL in web service env vars.
4. Redeploy service.
