from models import db, FAQ
from app import app

def add_initial_faqs():
    """Add some initial FAQ data for testing"""
    
    initial_faqs = [
        {
            "question": "What is MKCE?",
            "answer": "MKCE stands for M. Kumarasamy College of Engineering. It is an engineering college located in Karur, Tamil Nadu, offering various undergraduate and postgraduate programs in engineering and technology."
        },
        {
            "question": "What courses are offered at MKCE?",
            "answer": "MKCE offers B.E. programs in Computer Science, Electronics, Mechanical, Civil, and other engineering branches, along with M.E. programs in various specializations."
        },
        {
            "question": "Where is MKCE located?",
            "answer": "MKCE is located in Thalavapalayam, Karur District, Tamil Nadu, India. The campus is spread over 50 acres with modern facilities."
        },
        {
            "question": "How can I contact MKCE?",
            "answer": "You can contact MKCE at: Phone: 04324-250222, Email: principal@mkce.ac.in, Website: www.mkce.ac.in"
        },
        {
            "question": "What are the college timings?",
            "answer": "College timings are 8:45 AM to 4:40 PM on working days."
        }
    ]
    
    with app.app_context():
        # Check if FAQs already exist
        if FAQ.query.first():
            print("❌ FAQs already exist. Skipping initial data creation.")
            return
        
        # Add FAQs
        for faq_data in initial_faqs:
            faq = FAQ(question=faq_data['question'], answer=faq_data['answer'])
            db.session.add(faq)
        
        db.session.commit()
        print(f"✅ Added {len(initial_faqs)} initial FAQs successfully!")

if __name__ == "__main__":
    add_initial_faqs()
