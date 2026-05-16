from app import app
from models import FAQ, Document
import sys

def export_to_markdown(filepath):
    with app.app_context():
        faqs = FAQ.query.all()
        docs = Document.query.all()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Chatbot Knowledge Base\n\n")
            f.write("This file contains all the current information the chatbot uses to answer questions.\n")
            f.write("You can review and revise these details.\n\n")
            
            f.write("## 1. Frequently Asked Questions (FAQs)\n\n")
            if not faqs:
                f.write("*No FAQs found in the database.*\n\n")
            for faq in faqs:
                f.write(f"### Q: {faq.question}\n")
                f.write(f"**A:** {faq.answer}\n\n")
                f.write("---\n\n")
                
            f.write("## 2. Documents (Detailed Information)\n\n")
            if not docs:
                f.write("*No Documents found in the database.*\n\n")
            for doc in docs:
                f.write(f"### {doc.title}\n")
                f.write(f"{doc.content}\n\n")
                f.write("---\n\n")

if __name__ == "__main__":
    export_to_markdown("current_chatbot_knowledge.md")
