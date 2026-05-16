#!/usr/bin/env python
"""Add comprehensive MKCE college information to database"""

from app import app
from models import db, FAQ, Document

def add_comprehensive_mkce_data():
    with app.app_context():
        # Add detailed FAQs
        comprehensive_faqs = [
            {
                "question": "What is MKCE? Tell me about college basic information",
                "answer": """🏫 M. Kumarasamy College of Engineering (MKCE)

📍 Location: Karur, Tamil Nadu
📅 Established: 2000
🏛️ Affiliation: Anna University
✅ Approval: AICTE
🎓 TNEA Code: 2608
🌐 Website: https://www.mkce.ac.in

MKCE is an autonomous engineering college offering quality education in various engineering disciplines."""
            },
            {
                "question": "Where is CSE department located?",
                "answer": "CSE (Computer Science Engineering) department is located on the Ground Floor of Dr. APJ Abdul Kalam Block, Room 009."
            },
            {
                "question": "Where is ECE department?",
                "answer": "ECE (Electronics and Communication Engineering) department is located on the Second Floor of Dr. APJ Abdul Kalam Block, Rooms 239 and 301."
            },
            {
                "question": "Where is EIE department?",
                "answer": "EIE (Electronics and Instrumentation Engineering) department is located in Room 314 of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is IT department?",
                "answer": "IT (Information Technology) department is located on the Second Floor of Dr. S Radhakrishnan Block."
            },
            {
                "question": "Where is Mechanical department?",
                "answer": "Mechanical Engineering department is located on the First Floor of Dr. S Radhakrishnan Block."
            },
            {
                "question": "Where is Civil department?",
                "answer": "Civil Engineering department is located on the Ground Floor of Dr. S Radhakrishnan Block."
            },
            {
                "question": "Where is MBA department?",
                "answer": "MBA department is located on the First Floor of Dr. S Radhakrishnan Block."
            },
            {
                "question": "Where is AI and DS department?",
                "answer": "AI & DS (Artificial Intelligence and Data Science) department is located on the Third Floor of Dr. S Radhakrishnan Block."
            },
            {
                "question": "Where is library located?",
                "answer": "📚 Library is located in Room 027, Ground Floor of Dr. APJ Abdul Kalam Block. There is also a PG Library in Dr. S Radhakrishnan Block."
            },
            {
                "question": "Where is principal office?",
                "answer": "🏢 Principal Office is located on the First Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is administrative office?",
                "answer": "🏢 Administrative Office is located in Room 101 on the First Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is admission office?",
                "answer": "🏢 Admission Office is located in Room 104 on the First Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is placement cell?",
                "answer": "🏢 Placement Cell is located on the First Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is COE office?",
                "answer": "🏢 COE (Controller of Examinations) Office is located in Room 106 on the First Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is medical centre?",
                "answer": "🏥 Medical Centre is located in Room 003, Ground Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where are seminar halls?",
                "answer": """🏛️ Seminar Halls Location:
• Sir CV Raman Hall → Room 004 (Ground Floor, APJ Block)
• GD Naidu Hall → Room 005 (Ground Floor, APJ Block)
• Valluvar Hall → Room 103 (First Floor, APJ Block)
• Bharathiar Hall → Room 218 (Second Floor, APJ Block)
• Visvesvaraya Hall → Dr. S Radhakrishnan Block
• Vivekananda Hall → First Floor, Radhakrishnan Block"""
            },
            {
                "question": "Where are lecture halls?",
                "answer": """📍 Lecture Halls:
• LH 013, 014 → Right side
• LH 017, 018, 019, 024 → Left side"""
            },
            {
                "question": "Where is gents washroom?",
                "answer": "🚻 Gents Washroom is located in Room 020."
            },
            {
                "question": "Tell me about canteen menu food items prices",
                "answer": """🍽️ CANTEEN MENU (Best Canteen)

🍛 South Indian Items:
• Idly (1 set) – ₹12
• Poori – ₹15
• Pongal – ₹40
• Vadai – ₹5

🍽️ Meals & Rice:
• Meals – ₹60
• Chicken Briyani – ₹70
• Tomato Rice – ₹50
• Lemon Rice – ₹50
• Curd Rice – ₹30

🍜 Noodles:
• Veg Noodles – ₹50
• Egg Noodles – ₹55
• Chicken Noodles – ₹60
• Mushroom Noodles – ₹55

🍗 Chicken Items:
• Chilly Chicken – ₹60
• Pepper Chicken – ₹80
• Grill Chicken – ₹360
• Andhra Chicken – ₹70

🍄 Veg Items:
• Mushroom Chilly – ₹45
• Paneer Butter Masala – ₹110
• Cauliflower Manchurian – ₹55

🍳 Egg Items:
• Omelette – ₹15
• Egg Fries – ₹30"""
            },
            {
                "question": "Tell me about relax cafeteria drink menu",
                "answer": """🥤 RELAX CAFETERIA (Drink Menu)

🥛 Milkshakes (₹30):
• Chocolate
• Rosemilk
• Pista
• Strawberry
• Butterscotch
• Vanilla
• Pineapple
• Badam

☕ Beverages:
• Cold Coffee – ₹45
• Cold Boost – ₹45
• Cold Horlicks – ₹45
• Oreo Milkshake – ₹35

🍹 Fresh Juices:
• Lemon – ₹20
• Watermelon – ₹25
• Musk Melon – ₹35
• Apple – ₹50
• Pomegranate – ₹65"""
            },
            {
                "question": "What are gents hostel mess timings?",
                "answer": """🏨 GENTS HOSTEL MESS TIMING

🗓️ Working Days:
• Breakfast: 6:45 AM – 8:25 AM
• Lunch: 12:10 PM – 2:00 PM
• Snacks: 4:45 PM – 6:00 PM
• Dinner: 6:45 PM – 7:50 PM

🎉 Holidays:
• Breakfast: 6:45 AM – 9:30 AM
• Lunch: 12:10 PM – 2:30 PM
• Snacks: 4:45 PM – 6:00 PM
• Dinner: 6:45 PM – 7:50 PM"""
            },
            {
                "question": "How to get bonafide certificate?",
                "answer": """📄 BONAFIDE CERTIFICATE DETAILS

📧 Email: bonafide@mkce.ac.in

Required Details:
• Name
• Roll Number
• Father Name
• Counseling Type
• First Graduate (Yes/No)
• Hostel / Day Scholar / Bus
• Purpose of Bonafide

Scholarship Details:
• Management Scholarship
• Community Scholarship
• PMSS SC/ST
• 7.5% Govt School Quota

Loan Details (if applicable):
• Bank Name
• Branch
• IFSC Code
• District"""
            },
            {
                "question": "Where is chairman office?",
                "answer": "🏢 Chairman Office is located on the Ground Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is trust office?",
                "answer": "🏢 Trust Office is located on the Ground Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is HR office?",
                "answer": "🏢 HR Office is located on the First Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is IQAC office?",
                "answer": "🏢 IQAC Office is located in Room 105 on the First Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is CSBS department?",
                "answer": "CSBS (Computer Science and Business Systems) department is located on the Third Floor of Dr. APJ Abdul Kalam Block."
            },
            {
                "question": "Where is AI and Data Science department?",
                "answer": "AI & DS (Artificial Intelligence and Data Science) department is located on the Third Floor of Dr. S Radhakrishnan Block."
            },
            {
                "question": "Where is Science and Humanities department?",
                "answer": "S&H (Science and Humanities) department is located on the Third Floor of Dr. S Radhakrishnan Block."
            }
        ]
        
        # Add all FAQs
        for faq_data in comprehensive_faqs:
            faq = FAQ(question=faq_data['question'], answer=faq_data['answer'])
            db.session.add(faq)
        
        db.session.commit()
        
        # Add block-wise information as documents
        block_documents = [
            {
                "title": "Dr. APJ Abdul Kalam Block - Complete Information",
                "content": """🔷 Dr. APJ Abdul Kalam Block

Ground Floor:
• Chairman Office
• Trust Office
• Library (Room 027)
• Medical Centre (Room 003)
• Sir CV Raman Hall (Room 004)
• GD Naidu Hall (Room 005)
• CSE Department (Room 009)

First Floor:
• Principal Office
• Administrative Office (Room 101)
• HR Office
• Placement Cell
• Admission Office (Room 104)
• COE Office (Room 106)
• IQAC Office (Room 105)
• Valluvar Hall (Room 103)
• EEE Department

Second Floor:
• Bharathiar Hall (Room 218)
• Women Empowerment Cell
• ECE Department (Rooms 239, 301)

Third Floor:
• CSBS Department
• Technology Innovation Hub
• EIE Department (Room 314)"""
            },
            {
                "title": "Dr. S Radhakrishnan Block - Complete Information",
                "content": """🔷 Dr. S Radhakrishnan Block

Ground Floor:
• Executive Director Office
• PG Library
• Civil Department
• Visvesvaraya Hall

First Floor:
• Mechanical Department
• MBA Department
• Vivekananda Hall

Second Floor:
• IT Department
• Seminar Hall

Third Floor:
• AI & DS Department
• S&H Department (Science & Humanities)
• CSBS Department"""
            }
        ]
        
        # Add documents
        for doc_data in block_documents:
            doc = Document(title=doc_data['title'], content=doc_data['content'])
            db.session.add(doc)
        
        db.session.commit()
        
        # Count total
        faq_count = FAQ.query.count()
        doc_count = Document.query.count()
        
        print(f"✅ Successfully added comprehensive MKCE data!")
        print(f"📋 Total FAQs: {faq_count}")
        print(f"📄 Total Documents: {doc_count}")
        print(f"\n🎯 Chatbot is now trained with complete campus information!")

if __name__ == "__main__":
    add_comprehensive_mkce_data()
