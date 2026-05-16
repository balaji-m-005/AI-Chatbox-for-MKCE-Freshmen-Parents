#!/usr/bin/env python
"""Add proper MKCE information to database"""

from app import app
from models import db, FAQ

def add_proper_mkce_data():
    with app.app_context():
        # Clear old FAQs and add proper ones
        FAQ.query.delete()
        db.session.commit()
        
        proper_faqs = [
            {
                "question": "What is MKCE? Tell me about your organization",
                "answer": "MKCE stands for M. Kumarasamy College of Engineering. It is an autonomous engineering college located in Karur, Tamil Nadu. Established in 2000, it offers undergraduate and postgraduate programs in engineering and technology. The college is affiliated to Anna University and approved by AICTE."
            },
            {
                "question": "Who is the principal of MKCE?",
                "answer": "The Principal of MKCE is Dr. P. Kumarasamy. He is a highly experienced academician with expertise in engineering education and administration. You can contact the principal's office at principal@mkce.ac.in or visit the administrative block during working hours."
            },
            {
                "question": "Tell me about canteen facilities at MKCE",
                "answer": "MKCE has a spacious and hygienic canteen facility that provides nutritious food to students and staff. The canteen serves breakfast, lunch, and snacks at affordable prices. It offers both vegetarian and non-vegetarian options. The canteen is located near the main academic block and operates from 8:00 AM to 6:00 PM on all working days."
            },
            {
                "question": "What are the college timings?",
                "answer": "College timings are 8:45 AM to 4:40 PM on working days."
            },
            {
                "question": "What courses are offered at MKCE?",
                "answer": "MKCE offers B.E. programs in Computer Science and Engineering, Electronics and Communication Engineering, Electrical and Electronics Engineering, Mechanical Engineering, Civil Engineering, and Information Technology. It also offers M.E. programs in various specializations including VLSI Design, Computer Science, and Structural Engineering."
            },
            {
                "question": "Where is MKCE located?",
                "answer": "MKCE is located at Thalavapalayam, Karur District, Tamil Nadu, India - 639001. The campus is spread over 50 acres with modern infrastructure. It is easily accessible by road from Karur bus stand (about 8 km) and Karur railway station (about 6 km)."
            },
            {
                "question": "How can I contact MKCE?",
                "answer": "You can contact MKCE at: Phone: 04324-250222, Email: principal@mkce.ac.in, Website: www.mkce.ac.in. For admissions: admission@mkce.ac.in. The college office is open from 9:00 AM to 5:00 PM on working days."
            },
            {
                "question": "Tell me about library facilities at MKCE",
                "answer": "MKCE has a well-stocked central library with over 50,000 books, journals, and digital resources. The library provides access to IEEE, Springer, and other online databases. It has a digital library section, reading halls, and a book bank scheme for economically disadvantaged students. Library hours: 8:00 AM to 8:00 PM on working days."
            },
            {
                "question": "What are the hostel facilities at MKCE?",
                "answer": "MKCE provides separate hostel facilities for boys and girls with well-furnished rooms, Wi-Fi connectivity, 24/7 security, and mess facilities. The hostels have common rooms, gyms, and recreational areas. Wardens are available round the clock for student safety and discipline."
            },
            {
                "question": "Tell me about placement cell at MKCE",
                "answer": "MKCE has an active placement cell that organizes campus recruitment drives, training programs, and career guidance sessions. Top companies like TCS, Infosys, Wipro, Cognizant, and many core companies visit the campus for recruitment. The placement cell also provides soft skills training and interview preparation workshops."
            }
        ]
        
        for faq_data in proper_faqs:
            faq = FAQ(question=faq_data['question'], answer=faq_data['answer'])
            db.session.add(faq)
        
        db.session.commit()
        print(f"✅ Added {len(proper_faqs)} proper MKCE FAQs successfully!")
        
        # Verify
        faqs = FAQ.query.all()
        print(f"\n📋 Current FAQs in database:")
        for i, faq in enumerate(faqs, 1):
            print(f"   {i}. {faq.question}")

if __name__ == "__main__":
    add_proper_mkce_data()
