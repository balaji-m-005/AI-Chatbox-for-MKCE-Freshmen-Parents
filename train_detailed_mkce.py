#!/usr/bin/env python
"""Add additional detailed MKCE data including ECE department and Q&A bank"""

from app import app
from models import db, FAQ, Document

def add_detailed_mkce_data():
    with app.app_context():
        print("🚀 Adding detailed MKCE data...")
        
        # Additional FAQs from Part C - Q&A Bank (60+ Questions)
        additional_faqs = [
            # C1. ABOUT THE COLLEGE
            {
                "question": "How old is MKCE?",
                "answer": "MKCE has 25 years of excellence, established in the year 2000."
            },
            {
                "question": "Who founded MKCE?",
                "answer": """MKCE was founded by Thiru. M. Kumarasamy, a philanthropist from Karur region, popularly known as "Maniyakar."

He was:
• Former Munisif of Thalavapalayam Village for over 20 years
• Founded MKCE in 2000 to provide technical education to rural students at affordable cost
• Primary interests: Agriculture, transport operation, poultry farming, and education"""
            },
            {
                "question": "Who is the Chairman of MKCE?",
                "answer": """👨‍💼 Chairman & Secretary — Dr. K. Ramakrishnan (Son of Founder)

• B.E. Production Engineering, Annamalai University, Tamil Nadu
• Dynamic leader and role model for students
• Part of Anna University study team that visited Canadian Universities (2006)
• Initiated MOU with Infosys Technologies Ltd, Bangalore (via Campus Connect Program)
• Champion of TIES during his college days (sports achiever)
• Secured accreditation with TCS for the institution
• Signed MOUs with prominent local industrial establishments"""
            },
            {
                "question": "Who is the Executive Director of MKCE?",
                "answer": """👨‍💼 Executive Director — Dr. S. Kuppusamy

• B.Sc. Electronics – Erode Arts College, Erode
• MBA – Kongu Engineering College, Perundurai
• Ph.D. Management – Bharathiar University, Coimbatore
• Cleared both NET and SLET
• Qualified auditor for ISO Certification
• Former Professor & Head, Dept. of Management Studies, Kongu Arts and Science College, Erode
• Member of BoS, Inspection Commission, and Senate – Bharathiar University, Coimbatore
• Provides consultancy for ISO Certification processes"""
            },
            {
                "question": "How many students are currently studying at MKCE?",
                "answer": "MKCE currently has over 4,150 students and 15,100+ proud alumni."
            },
            {
                "question": "Is MKCE autonomous?",
                "answer": "Yes, MKCE is an Autonomous Institution affiliated to Anna University and approved by AICTE, New Delhi."
            },
            {
                "question": "Is MKCE NAAC accredited?",
                "answer": "Yes, MKCE has been accredited with 'A' Grade by NAAC (Cycle 2)."
            },
            
            # C2. ADMISSIONS
            {
                "question": "How do I apply for admission to MKCE?",
                "answer": "Apply online at https://forms.gle/EGoB193DkB9tu3ts8 or call 9750356377 / 8754022577."
            },
            {
                "question": "Who is the Dean of Admissions?",
                "answer": "Dr. K. Sundararaju, M.E., Ph.D., SMIEEE – Contact: +91 9750356377 / 7540046077"
            },
            {
                "question": "What is the total ECE intake?",
                "answer": "The current intake for B.E. ECE is 300 seats."
            },
            {
                "question": "What is the eligibility for B.E. programmes?",
                "answer": "10+2 with pass in Physics, Chemistry, and Mathematics."
            },
            {
                "question": "Is lateral entry available?",
                "answer": "Yes. Lateral entry is available for diploma holders – 3 years / 6 semesters."
            },
            
            # C3. ECE DEPARTMENT
            {
                "question": "When was the ECE department started?",
                "answer": """The ECE department was established in 2000 with an initial intake of 60 students.

Intake History:
• 2000: 60 students
• 2005: 120 students
• 2011: 180 students
• 2012: 240 students
• Current: 300 students"""
            },
            {
                "question": "Is there a Research Centre in ECE?",
                "answer": "Yes, the ECE department is a recognized Research Centre by Anna University since 2017."
            },
            {
                "question": "What PG programme is offered in ECE?",
                "answer": "M.E. Communication Systems with an intake of 12 students (since 2011)."
            },
            {
                "question": "How many semesters are in B.E. ECE?",
                "answer": "8 semesters (Regular) or 6 semesters (Lateral Entry)."
            },
            {
                "question": "Can I pursue Ph.D. in ECE at MKCE?",
                "answer": "Yes. The ECE Research Centre recognized by Anna University allows Ph.D. registration. Institutional Fellowship of ₹10,000/month is available for full-time scholars."
            },
            {
                "question": "What professional clubs are in ECE?",
                "answer": """🏛️ ECE Professional Bodies & Associations:

• Eminence Association – ECE Departmental Technical Association
• IEEE ComSoc – IEEE Communications Society Student Chapter
• IETE – Institution of Electronics & Telecommunication Engineers"""
            },
            {
                "question": "Does ECE conduct hackathons?",
                "answer": """Yes! ECE conducts various technical events:
• 24-Hour Hackathons
• Make-A-Thon
• Innovators Hackathon (I2H) 2.0
• HackFest 2026
• National-level hackathons
• 24-Hour ECE Hackathon (Feb 26-27, 2026)"""
            },
            {
                "question": "What are the higher study options after B.E. ECE?",
                "answer": """After completing B.E. ECE at MKCE, students can pursue:
• M.E. / M.Tech. in ECE-related specializations
• M.B.A. – Master of Business Administration
• M.S. – Master of Science (India or Abroad)
• Competitive Exams: GATE, GRE, GMAT, TOEFL, IELTS"""
            },
            
            # C4. FACULTY
            {
                "question": "How many faculty members are in ECE?",
                "answer": "Approximately 42 faculty members including Professors, Associate Professors, and Assistant Professors."
            },
            {
                "question": "Who manages the PCB Design Lab in ECE?",
                "answer": "Dr. K. Karthikeyan, M.E., Ph.D. is the Lab In-Charge for PCB Design Laboratory."
            },
            {
                "question": "Who handles the Embedded Systems Lab in ECE?",
                "answer": "Mr. S. Mohanraj, M.E., (Ph.D.) is the Lab In-Charge for Embedded System Design Laboratory."
            },
            {
                "question": "Who is the Lab In-Charge for the Communication Lab?",
                "answer": "Dr. K. Sivanandam, M.E., Ph.D. is the Lab In-Charge for Analog and Digital Communication Laboratory."
            },
            
            # C5. RESEARCH
            {
                "question": "When was MKCE's R&D Cell established?",
                "answer": "The R&D Cell was established in 2012 by decision of the Governing Council."
            },
            {
                "question": "What is the incentive for publishing in a Q1 journal?",
                "answer": """Publication Incentives for Faculty:

• Q4: ₹5,000
• Q3: ₹7,500
• Q2: ₹10,000
• Q1: ₹15,000
• Q1 with Impact Factor above 10: ₹20,000"""
            },
            
            # C6. PLACEMENT
            {
                "question": "Has MKCE placed students in Japan?",
                "answer": "Yes. MKCE has Japan placement drives including Hitachi Japan, OSG Japan, and other Japanese companies."
            },
            {
                "question": "What is the placement email?",
                "answer": "placement@mkce.ac.in"
            },
            {
                "question": "How many students are placed from MKCE?",
                "answer": "830+ students have been placed as per latest data on the homepage."
            },
            
            # C7. CAMPUS LIFE
            {
                "question": "Is there a hostel at MKCE?",
                "answer": "Yes. MKCE has a hostel facility. Access the Smart Hostel portal at http://hostel.mkce.ac.in/"
            },
            {
                "question": "Does MKCE have bus transport?",
                "answer": """Yes. MKCE provides college bus service from various city locations.

• Coverage: Pick-up from inside and outside the city, including areas near the college
• Daily Schedule: Same pickup and drop points daily
• Safety: Experienced drivers, speed control devices, first aid box in all buses
• Bus Route PDF: https://www.mkce.ac.in/hostel/bus_route.pdf"""
            },
            {
                "question": "What are the major auditoriums at MKCE?",
                "answer": "Valluvar Hall and G.D. Naidu Hall, along with a Media Centre and Technology Learning Centre (TLC)."
            },
            {
                "question": "Does MKCE offer foreign language courses?",
                "answer": """Yes. MKCE has a Center for Foreign Languages (CFL).

• Language Taught: Japanese (Nihongo)
• Levels: N5/Q5 | N4/Q4 | N3/Q3
• MKCE is an approved JLPT exam centre
• Prepares students for JLPT and NAT certifications"""
            },
            {
                "question": "Does MKCE have an Entrepreneurship cell?",
                "answer": "Yes. MKCE has IEDC (Innovation & Entrepreneurship Development Cell) at https://www.mkce.ac.in/IEDC"
            },
            
            # C8. FEES & PORTALS
            {
                "question": "How do I pay my college fees?",
                "answer": """Fees can be paid online through Axis Bank EasyPay:

• New Students: https://easypay.axis.bank.in (mid=NDg0MjY%3D)
• Existing Students: https://easypay.axis.bank.in (mid=NDg0NDY%3D)"""
            },
            {
                "question": "Where can I check my exam schedule or results?",
                "answer": "Visit http://www.camsmkce.in (CAMS portal)."
            },
            {
                "question": "How can I verify my certificate?",
                "answer": "Visit https://mkce.directverify.in/student/index.html"
            },
            {
                "question": "How do I raise a grievance at MKCE?",
                "answer": "Use the Online Grievance Redressal form available on the MKCE website."
            },
            {
                "question": "What is the admission email?",
                "answer": "admission@mkce.ac.in"
            },
            
            # Additional detailed questions
            {
                "question": "What is KR Connect?",
                "answer": """🔗 KR CONNECT - Student Academic Portal of MKCE

🌐 URL: http://krconnect.mkce.ac.in/

Features:
• Academic and administrative management
• Check attendance and marks
• Shows mentor (faculty) details
• Bus fee payment
• Feedback submission (course/faculty)
• Student services (STC) and requests
• Academic updates, timetable, and notifications
• Faculty track student performance
• Centralized digital system for the college"""
            },
            {
                "question": "What regulations are followed in ECE?",
                "answer": "UG Regulation 2023, UG Regulation 2018, and PG Regulation 2019."
            },
            {
                "question": "What is the ECE intake history?",
                "answer": """ECE Intake History:
• 2000: 60 students
• 2005: 120 students  
• 2011: 180 students
• 2012: 240 students
• Current: 300 students (B.E. ECE)
• M.E. Communication Systems: 12 seats (since 2011)"""
            },
            
            # ECE Labs detailed
            {
                "question": "What are the 12 laboratories in ECE?",
                "answer": """🔬 ECE Laboratories (12 Labs):

1. Digital Signal Processing Laboratory (Dr. P. Jeyakumar)
2. Electronic Circuits Laboratory (Dr. R. Rajesh Kanna)
3. Electronics and Microprocessor Laboratory (Dr. C. Nandagopal)
4. Engineering Practice Laboratory (Mr. T. Sivakumar)
5. Linear Integrated Circuits Laboratory (Dr. A. Sridevi)
6. Microwave and Optical Laboratory (Dr. V. Mariselvam)
7. Networks Laboratory (Dr. A. Kavitha)
8. Project Laboratory (Dr. S. Vimalnath)
9. Analog and Digital Communication Laboratory (Dr. K. Sivanandam)
10. Embedded System Design Laboratory (Mr. S. Mohanraj)
11. Research Laboratory (Mr. S. Mohanraj)
12. PCB Design Laboratory (Dr. K. Karthikeyan)"""
            },
            
            # Recent events
            {
                "question": "What are the recent events at MKCE?",
                "answer": """📅 Recent Events at MKCE (2025-2026):

🏆 Major Events:
• Orlia 2026 (Annual Fest) – March 20, 2026
• Project Expo – March 5, 2026
• HackFest 2026 – January 30, 2026 & February 23, 2026
• ECE 24-Hour Hackathon – February 26-27, 2026
• EEE National Level 24-Hour Hackathon cum HackFest – February 6, 2026
• IQAC Day Celebration – January 27, 2026
• Republic Day Celebration – January 27, 2026
• AI in School Education Training Course – January 5, 2026
• Idea Fusion Competition – December 22, 2025
• Sports Day – April 1, 2025

📢 Placement News:
• Technosafe Trading (2025)
• PROMHO (2026)
• IndiaMart (2025)
• SkipperX (2025)
• Infosys (2025 & 2026)
• LTIMindtree (2025 & 2026)
• Hexaware (2025)
• ZOHO Drive (2025)
• Hitachi Japan (2025)
• OSG Japan (2025)"""
            }
        ]
        
        # Add all additional FAQs
        added_count = 0
        for faq_data in additional_faqs:
            faq = FAQ(question=faq_data['question'], answer=faq_data['answer'])
            db.session.add(faq)
            added_count += 1
        
        db.session.commit()
        
        # Add detailed ECE department document
        ece_detailed_doc = {
            "title": "ECE Department - Complete Detailed Information",
            "content": """🔌 ELECTRONICS & COMMUNICATION ENGINEERING (ECE) - COMPLETE DETAILS

📊 Department Overview:
• Full Name: Electronics and Communication Engineering
• Short Name: ECE
• Established: 2000
• Current UG Intake: 300 seats
• PG Programme: M.E. Communication Systems (12 seats, since 2011)
• Research Centre: Recognized by Anna University since 2017
• UG Duration: 4 years (Regular) / 3 years (Lateral Entry)
• UG Semesters: 8 (Regular) / 6 (Lateral Entry)
• Regulations: UG Regulation 2023, UG Regulation 2018, PG Regulation 2019
• NRI Quota: Available
• PIO/FN/GULF/OCI: Not Available
• HOD: Dr. N. Mahendran, M.E., Ph.D.

🎯 Vision:
To empower the Electronics and Communication Engineering students with emerging technologies, professionalism, innovative research and social responsibility.

🎯 Mission:
• M1: Attain academic excellence through innovative teaching-learning process, research areas, laboratories, and consultancy projects
• M2: Inculcate students in problem-solving and lifelong learning ability
• M3: Provide entrepreneurial skills and leadership qualities
• M4: Render the technical knowledge and skills of faculty members

📋 Program Educational Objectives (PEO):
PEO1 - Core Competence: Graduates will have a successful career in academia or industry associated with ECE
PEO2 - Professionalism: Graduates will provide feasible solutions for challenging problems through comprehensive research and innovation
PEO3 - Lifelong Learning: Graduates will contribute to social needs through lifelong learning, professional ethics, and leadership quality

📋 Program Specific Outcomes (PSO):
PSO1: Applying knowledge in Electronics, Communications, Signal Processing, VLSI, Embedded Systems in design and implementation of engineering applications
PSO2: Solving complex ECE problems with analytical and managerial skills using latest hardware and software tools, independently or in teams, to meet industrial expectations

🧪 12 Laboratories:
1. Digital Signal Processing Laboratory
2. Electronic Circuits Laboratory
3. Electronics and Microprocessor Laboratory
4. Engineering Practice Laboratory
5. Linear Integrated Circuits Laboratory
6. Microwave and Optical Laboratory
7. Networks Laboratory
8. Project Laboratory
9. Analog and Digital Communication Laboratory
10. Embedded System Design Laboratory
11. Research Laboratory
12. PCB Design Laboratory

🏛️ Professional Bodies:
• Eminence Association (ECE Departmental Technical Association)
• IEEE ComSoc (IEEE Communications Society - Student Chapter)
• IETE (Institution of Electronics & Telecommunication Engineers)

🎓 Student Activities:
• TEL Curricula (Technology Enhanced Learning)
• Minor Projects
• Industrial Visits
• Internships (including NIT-level internships)
• National/International Conferences
• Hackathons & Make-A-Thons (24-Hour Hackathon, I2H 2.0, HackFest)
• Alumni Interaction Sessions
• Web Development Workshops
• Higher Studies Awareness Programs
• NPTEL Course Enrollments
• VAC (Value Added Courses)
• ECE-JLPT (Japanese Language Proficiency Test)

📊 Intake History:
2000: 60 → 2005: 120 → 2011: 180 → 2012: 240 → Current: 300

💼 Placement Batches Available: 2012-16 through 2021-25

🏆 Achievements:
• NIT Internship achievements
• Students SCI Journal Publications
• Indian Mobile Congress (IMC) participation
• Innovators Hackathon (I2H) 2.0
• Make-A-Thon
• Internship offer from Axiscades
• TCS Digital Offer
• PEGA Best Outgoing Student Award
• Hackathon Winner & Third Place with Cash Prize
• Code Battle Winner
• Best Coding Assistant App award"""
        }
        
        # Add ECE detailed document
        doc = Document(title=ece_detailed_doc['title'], content=ece_detailed_doc['content'])
        db.session.add(doc)
        added_count += 1
        
        db.session.commit()
        
        # Count totals
        faq_count = FAQ.query.count()
        doc_count = Document.query.count()
        
        print(f"✅ Successfully added detailed MKCE data!")
        print(f"📋 Total FAQs: {faq_count}")
        print(f"📄 Total Documents: {doc_count}")
        print(f"🎯 New items added: {added_count}")
        print(f"\n🚀 Enhanced database now includes:")
        print(f"  • 60+ Q&A pairs from complete knowledge base")
        print(f"  • Detailed ECE department information")
        print(f"  • Faculty and lab details")
        print(f"  • Recent events and achievements")
        print(f"  • Student activities and clubs")

if __name__ == "__main__":
    add_detailed_mkce_data()
