from app import app, db
from models import FAQ

LABELS = [
    "**Question:**",
    "**Answer:**",
    "**Summary:**",
    "**Explanation:**",
    "Question:",
    "Answer:",
    "Summary:",
    "Explanation:"
]

with app.app_context():
    faqs = FAQ.query.all()
    for faq in faqs:
        question = faq.question.strip()
        answer = faq.answer.strip()

        for label in LABELS:
            answer = answer.replace(label, "")

        # Remove repeated question prefix
        if question and answer.lower().startswith(question.lower()):
            answer = answer[len(question):].strip()

        faq.answer = answer

    db.session.commit()

print("All FAQ answers cleaned successfully.")
