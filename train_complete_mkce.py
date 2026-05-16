#!/usr/bin/env python
"""Add comprehensive MKCE data from complete knowledge base"""

from app import app
from models import db, FAQ, Document

def add_comprehensive_mkce_knowledge():
    with app.app_context():
        print("🚀 Adding comprehensive MKCE knowledge base...")
        
        # Comprehensive FAQs covering all chapters
        comprehensive_faqs = [
            # Chapter 1 - College Overview
            {
                "question": "What is MKCE? Tell me about college overview",
                "answer": """🏫 M. Kumarasamy College of Engineering (MKCE)

📍 Location: Karur, Tamil Nadu, India
📍 GPS: Lat 11.055287
📅 Established: 2000
🏛️ Type: Autonomous Engineering Institution
🏛️ Affiliation: Anna University, Chennai
✅ Approval: AICTE, New Delhi
🏛️ Trust: M. Kumarasamy Health and Educational Trust
🎓 TNEA Code: 2608
🌐 Website: https://www.mkce.ac.in
🏷️ Tagline: "The Best Engineering College With 25 Years of Excellence"
🔧 Maintained By: Technology Innovation Hub–MKCE
📊 Years of Excellence: 25 Years (as of 2025)"""
            },
            {
                "question": "What is KR Connect?",
                "answer": """🔗 KR CONNECT - Main ERP Portal of MKCE

🌐 URL: https://krconnect.mkce.ac.in/

Features:
• Academic and administrative management
• Students can check attendance and marks
• Shows mentor (faculty) details
• Used for bus fee payment
• Allows feedback submission (course/faculty)
• Provides student services (STC) and requests
• Displays academic updates, timetable, and notifications
• Helps faculty track student performance
• Acts as a centralized digital system for the college"""
            },
            # Chapter 2 - Management & Leadership
            {
                "question": "Who is the founder of MKCE?",
                "answer": """👨‍💼 Founder — Thiru. M. Kumarasamy

• Philanthropist; popularly known as "Maniyakar" in the Karur region
• Former Munisif (Village Head) of Thalavapalayam Village for over 20 years
• Founded MKCE in 2000 to provide affordable engineering education to rural students
• Other interests: Agriculture, Transport Operations, Poultry Farming
• MKCE is his dream project for rural upliftment through technical education"""
            },
            {
                "question": "Who is the chairman of MKCE?",
                "answer": """👨‍💼 Chairman & Secretary — Dr. K. Ramakrishnan

• Son of Founder Thiru M. Kumarasamy
• B.E. Production Engineering, Annamalai University, Tamil Nadu
• Champion of TIES during college days; passionate about sports
• Part of Anna University study team that visited Canadian Universities (2006)
• Signed MOU with Infosys Technologies Ltd, Bangalore through Campus Connect Program
• College accredited by TCS under his administration
• Elevated MKCE to a leading position among Tamil Nadu engineering colleges"""
            },
            {
                "question": "Who is the executive director of MKCE?",
                "answer": """👨‍💼 Executive Director — Dr. S. Kuppusamy

• B.Sc. Electronics, Erode Arts College, Erode
• MBA, Kongu Engineering College, Perundurai
• Ph.D. in Management, Bharathiar University, Coimbatore
• Cleared NET and SLET; qualified ISO Certification Auditor
• Prior: Lecturer to Professor & HOD at Kongu Arts and Science College, Erode
• Member of Board of Studies, Senate, and Inspection Commission at Bharathiar University
• Offered ISO Certification consultancy to various organizations"""
            },
            {
                "question": "Who is the principal of MKCE?",
                "answer": """👨‍🏫 Principal — Dr. B. S. Murugan (M.E., Ph.D.)

• Also serves as Professor in CSE Department
• Promotes collaborative, interactive learning
• Committed to inclusive, diverse campus community
• Supports co-curricular and extracurricular development alongside academics"""
            },
            # Chapter 3 - Vision, Mission & Quality Policy
            {
                "question": "What is the vision of MKCE?",
                "answer": """🎯 College Vision:

"To emerge as a leader among the top institutions in the field of technical education."""
            },
            {
                "question": "What is the mission of MKCE?",
                "answer": """🎯 College Mission:

1. Produce smart technocrats with empirical knowledge who can surmount global challenges.
2. Create a diverse, fully-engaged, learner-centric campus environment to provide quality education.
3. Maintain mutually beneficial partnerships with alumni, industry, and professional associations."""
            },
            {
                "question": "What is the quality policy of MKCE?",
                "answer": """📜 Quality Policy:

"We, at M/s. M. Kumarasamy College of Engineering are committed to the Society in making our Students to live a purpose as responsible citizens with Ethical Values through provision of Quality Technical Education and continually improve to become a World Class Technological University."""
            },
            {
                "question": "Why choose MKCE?",
                "answer": """✨ Why MKCE?

• Nurtures Creativity & Innovation
• Student-Centric Campus
• Experiential Learning (real-world application-based)
• Comprehensive Teaching (well-rounded curriculum)"""
            },
            # Chapter 4 - Key Statistics
            {
                "question": "What are the key statistics of MKCE?",
                "answer": """📊 MKCE Key Statistics:

• Proud Alumni: 15,100+
• Current Students: 4,150+
• Placed Students: 830+
• Total Faculty: 280+
• SCIE/Scopus/WoS Publications: 2,673+
• UGC Care Journal Publications: 302
• Book / Book Chapter Publications: 125
• h-Index (Google Scholar / Scopus): 61 / 53
• Patents (Published / Registered): 715 / 120
• Student Publications: 645
• Conference Publications: 2,530
• Total Citations (Scopus): 18,090+"""
            },
            # Chapter 5 - Contact Information
            {
                "question": "What is the contact information of MKCE?",
                "answer": """📞 MKCE Contact Information:

📞 Administration Phone: 04324-272155 / 04324-270755
📠 Administration Fax: 04324-272457
📞 Admission Helpline: 9750356377 / 8754022577
📧 Admission Email: admission@mkce.ac.in
📞 Placement & Training: 04324-272155 / 04324-270755
📧 Placement Email: placement@mkce.ac.in
📞 EEE HOD Direct: eee@mkce.ac.in / 8754015677
👨‍💼 Dean of Admissions: Dr. K. Sundararaju — +91 9750356377 / 7540046077"""
            },
            # Chapter 6 - Accreditation & Rankings
            {
                "question": "What are the accreditations and rankings of MKCE?",
                "answer": """🏆 MKCE Accreditations & Rankings:

• NAAC: "A" Grade – Cycle 2
• NBA: Accredited (select programmes, including CSE– Washington Accord / TIER-I)
• AICTE: Approved, New Delhi
• Anna University: Affiliated (Autonomous Status)
• TCS: Accredited
• NIRF: Ranked (https://mkce.ac.in/nirf.php)
• ARIIA: Ranked (https://mkce.ac.in/files/ariia.pdf)
• MBA: IIRF Ranked
• Teaching Award: CSE Dept., 2015 by Staffordshire University
• Research Centres: 6 Departments recognized by Anna University"""
            },
            # Chapter 7 - Programmes & Intake
            {
                "question": "What UG programmes are offered at MKCE?",
                "answer": """🎓 UG Programmes at MKCE:

1. B.Tech AI & Data Science — 180 seats (NRI: Yes)
2. B.E. CSE (AI & ML) — 60 seats (NRI: Yes)
3. B.E. Civil Engineering — 30 seats (NRI: Yes)
4. B.Tech CS & Business Systems — 60 seats (NRI: Yes)
5. B.E. Computer Science & Engineering — 180 seats (NRI: Yes)
6. B.E. Electrical & Electronics Engineering — 120 seats (NRI: Yes)
7. B.E. Electronics & Communication Engineering — 300 seats (NRI: Yes)
8. B.Tech Information Technology — 120 seats (NRI: Yes)
9. B.E. Mechanical Engineering — 90 seats (NRI: Yes)
10. B.E. Electronics Engg. (VLSI Design & Technology) — 60 seats (NRI: Yes)
11. B.E. CSE (Cyber Security) — 60 seats (NRI: Yes)

🎓 PG Programmes:
• Master of Business Administration (MBA) — 120 seats
• Master of Computer Applications (MCA) — 60 seats
• M.E. CSE — 12 seats
• M.E. Communication Systems — 12 seats
• M.E. Power Systems Engineering — 12 seats
• M.E. Manufacturing Engineering — 12 seats"""
            },
            # Student Portals
            {
                "question": "What are the student portals at MKCE?",
                "answer": """🌐 MKCE Student Portals & Links:

• CAMS (Exam & Curriculum): http://www.camsmkce.in
• KR Connect (Academic): http://krconnect.mkce.ac.in/
• Smart Hostel: http://hostel.mkce.ac.in/
• Teaching Learning Centre: http://tlc.krgi.in
• Library OPAC: http://10.0.7.150/impreserp/OPAC/Default.aspx
• Certificate Verification: https://mkce.directverify.in/student/index.html
• Blog: http://mkce.ac.in/blog
• Alumni Portal: http://alumni.mkce.ac.in/
• Online Grievance: Google Form on college website

💳 Fee Payment:
• New Students: https://easypay.axis.bank.in (mid=NDg0MjY%3D)
• Existing Students: https://easypay.axis.bank.in (mid=NDg0NDY%3D)

📝 Admission:
• Apply: https://forms.gle/EGoB193DkB9tu3ts8
• TNEA Code: 2608"""
            },
            # Placement
            {
                "question": "Tell me about placement at MKCE",
                "answer": """💼 MKCE Placement & Training:

Training Modules (CSD–Career Skill Development):
• Aptitude Test Skills
• Group Discussion (GD) Handling Techniques
• Professional Development
• Interview Handling Skills
• Personality Development

Placement Infrastructure:
• Testing Halls | Conference & PPT Halls | Written & Online Test Centres
• Group Discussion Hall | Interview Panel Rooms | Video Conference Facility | Placement Lounge

Recent Recruiters (2024-26):
Infosys | LTIMindtree | Hexaware | ZOHO | TCS | IndiaMart | SkipperX | Technosafe Trading | MCoreta | Hitachi Japan | OSG Japan | HashedIn | NXT SYNC | EEE PROMHO | Capgemini | Accenture | Wipro | IBM | CTS | Inautix | PurpleSlate | Infoview | Odessa | Fujitsu | Kawasaki Heavy Industries | Nissan | Mitsubishi Hitachi | NGK Spark Plug | Toyota

Japan Placements:
MKCE students have been placed in Japan-based companies and also pursued higher studies at Shizuoka University on scholarships through the Sakura Science Program (JST)."""
            },
            # Research
            {
                "question": "Tell me about research at MKCE",
                "answer": """🔬 MKCE Research & Development:

• R&D Cell Established: 2012 (Governing Council decision)
• 6 Departments recognized as Anna University Research Centres
• Ph.D. Fellowship: ₹10,000/month for full-time scholars
• Research Progress Review: Every 6 months before review committee

Funded Projects:
• SERB CRG: ₹13.07 Lakh (Dr. S. Geeitha, IT)
• SERB TARE: ₹18.30 Lakh (Dr. V. Sivakumar)
• MSME Grant: ₹28 Lakh (2023-24), ₹48 Lakh (2024-25)
• TNSCST: ₹60,000 (5 projects, 2023-24)
• Naan Mudhalvan State Govt: ₹30,000 (3 projects)

Publication Incentives:
• Q4: ₹5,000
• Q3: ₹7,500
• Q2: ₹10,000
• Q1: ₹15,000
• Q1 (Impact Factor > 10): ₹20,000"""
            },
            # Campus Facilities
            {
                "question": "What are the campus facilities at MKCE?",
                "answer": """🏫 MKCE Campus Facilities:

Academic:
• Smart Classrooms (ICT-enabled) | Drawing Hall | IT Labs | Multiple Engineering Labs
• Technology Learning Centre (TLC) | Media Centre

Library:
• Physical + Digital Library | Reading Section | Study Cubicles | Automatic Book Issue
• OPAC: http://10.0.7.150/impreserp/OPAC/Default.aspx

Auditoriums & Halls:
• Valluvar Hall | G.D. Naidu Hall | Media Centre | Conference Halls

Sports:
• Basketball Court | Tennis Court | Volleyball Court | 3 Fitness Centres / Gyms

Hostel:
• Smart Hostel portal: http://hostel.mkce.ac.in/

Transport:
• Fleet of buses; city-wide coverage; experienced drivers; speed control; first aid boxes
• Bus Route PDF: https://www.mkce.ac.in/hostel/bus_route.pdf"""
            },
            # Foreign Languages
            {
                "question": "Tell me about foreign languages at MKCE",
                "answer": """🌍 Center for Foreign Languages (CFL):

• Language Taught: Japanese (Nihongo)
• Levels: N5/Q5 | N4/Q4 | N3/Q3
• MKCE is an approved JLPT exam centre
• Prepares students for JLPT and NAT certifications

JLPT Certificate Holders:
• 2013-2017: N5: 9
• 2014-2018: N5: 90, N4: 9
• 2015-2019: N5: 45, N4: 19
• 2016-2020: N5: 42, N4: 26, N3: 11, N2: 1
• 2017-2021: N5: 49, N4: 6, N3: 6
• 2020-2024: N5: 40, N4: 3"""
            },
            # Quick FAQs
            {
                "question": "What is the TNEA code for MKCE?",
                "answer": "🎓 TNEA Code: 2608"
            },
            {
                "question": "Does MKCE have NBA accreditation?",
                "answer": "✅ Yes, MKCE has NBA accreditation for select programmes, including CSE under Washington Accord / TIER-I."
            },
            {
                "question": "Does MKCE have NAAC accreditation?",
                "answer": "✅ Yes, MKCE has NAAC 'A' Grade – Cycle 2 accreditation."
            },
            {
                "question": "When was MKCE established?",
                "answer": "📅 MKCE was established in 2000."
            },
            {
                "question": "How many students are currently studying at MKCE?",
                "answer": "👨‍🎓 Current Students: 4,150+"
            },
            {
                "question": "How many alumni does MKCE have?",
                "answer": "🎓 Proud Alumni: 15,100+"
            },
            {
                "question": "How many faculty members are there at MKCE?",
                "answer": "👨‍🏫 Total Faculty: 280+"
            },
            {
                "question": "What is the Ph.D. stipend at MKCE?",
                "answer": "💰 Ph.D. Fellowship: ₹10,000 per month for full-time scholars."
            },
            {
                "question": "Does MKCE have research centres?",
                "answer": "🔬 Yes, 6 Departments are recognized as Anna University Research Centres."
            },
            {
                "question": "What is the internet speed at MKCE?",
                "answer": "🌐 Internet: 24-hour Wi-Fi, 1 Gbps speed in CSE, EEE labs."
            }
        ]
        
        # Add all comprehensive FAQs
        added_count = 0
        for faq_data in comprehensive_faqs:
            faq = FAQ(question=faq_data['question'], answer=faq_data['answer'])
            db.session.add(faq)
            added_count += 1
        
        db.session.commit()
        
        # Add department-wise detailed documents
        dept_documents = [
            {
                "title": "ECE Department - Complete Details",
                "content": """🔌 Electronics & Communication Engineering (ECE)

📊 Established: 2000 | Intake: 300 (UG), 12 (PG– M.E. Communication Systems)
🔬 Research Centre: Recognized by Anna University since 2017
📅 PG Since: 2011 | Regulations: UG 2023, UG 2018, PG 2019

🎯 Vision:
To empower ECE students with emerging technologies, professionalism, innovative research and social responsibility.

🎯 Mission:
• M1 – Academic excellence through innovative teaching & research
• M2 – Problem-solving & lifelong learning
• M3 – Entrepreneurial skills & leadership
• M4 – Faculty technical knowledge

👨‍🏫 HOD: Dr. N. Mahendran, M.E., Ph.D. (Professor & HOD)

🧪 Laboratories (12 Labs):
• Digital Signal Processing Lab
• Electronic Circuits Lab
• Electronics & Microprocessor Lab
• Engineering Practice Lab
• Linear Integrated Circuits Lab
• Microwave & Optical Lab
• Networks Lab
• Project Lab
• Analog & Digital Communication Lab
• Embedded System Design Lab
• Research Lab
• PCB Design Lab

🏛️ Professional Bodies:
• Eminence Association (ECE Dept. Technical Body)
• IEEE ComSoc (Communications Society Student Chapter)
• IETE (Institution of Electronics & Telecommunication Engineers)"""
            },
            {
                "title": "CSE Department - Complete Details",
                "content": """💻 Computer Science & Engineering (CSE)

📊 Established: 2000 | Intake: 180 (UG) + 12 (PG– M.E. CSE)
🏆 NBA Accredited: Yes — Engineering TIER-I, Washington Accord
🏆 Award: Teaching Award in Engineering by Staffordshire University, 2015
🌐 Internet: 24-hour Wi-Fi, 1 Gbps speed

🎯 Vision:
To achieve education and research excellence in Computer Science and Engineering.

🎯 Mission:
• M1 – Excellence in teaching-learning
• M2 – Research & innovation
• M3 – Technically competent professionals with social & ethical responsibility

👨‍🏫 HOD: Dr. D. Pradeep, M.E., Ph.D. (Professor & Head)
👨‍🏫 Principal: Dr. B. S. Murugan (also Professor in CSE)

💼 Known Recruiters: TCS, Wipro, IBM, CTS, Accenture, Infosys, Inautix, PurpleSlate, Infoview, Odessa, Zoho"""
            },
            {
                "title": "IT Department - Complete Details",
                "content": """🖥️ Information Technology (IT)

📊 Established: 2001 | Intake: 120
🎯 Specialization Areas: Network Security, Data Mining, Cloud Computing, Mobile Computing, Computer Networks, Soft Computing, Evolutionary Computing, Cyber Security, Big Data Analytics, Image Processing

🎯 Vision:
To Create Technically Skilled IT Professionals to meet Corporate Expectations and to Address Societal Concerns.

🎯 Mission:
• M1 – Competency in advanced computing & project-based learning
• M2 – Industry collaboration for research & consultancy
• M3 – Entrepreneurial skills for societal benefit

👨‍🏫 HOD: Dr. K. Ravikumar, M.E., Ph.D. (Professor & HOD)

🔬 Research Project:
Dr. S. Geeitha (IT) holds an active SERB CRG-funded research project (₹13.07 Lakh)"""
            },
            {
                "title": "EEE Department - Complete Details",
                "content": """⚡ Electrical & Electronics Engineering (EEE)

📊 Established: 2001–2002 | Intake: 120 (UG), PG– M.E. Power Systems (since 2012–13)
🔬 Research Centre: Recognized by Anna University since 2017–18
🧪 Labs: 8 laboratory venues
💻 Software: MATLAB, Mi-Power, AU Power, ICT Circuit Tool, Labview
📚 Department Library: 2,226 books + 100 E-journals
📖 Books Published: 12 by faculty members

🎯 Vision:
To produce smart and dynamic professionals with profound theoretical and practical knowledge comparable with the best in the field.

👨‍🏫 HOD: Dr. J. Uma, M.E., Ph.D. (Professor & Head)
📞 Contact: 8754015677 | Email: eee@mkce.ac.in

🔬 Research Project:
Dr. V. Sivakumar (EEE) holds SERB TARE project worth ₹18.30 Lakh

🏛️ Professional Bodies: ISTE and IEEE Student Chapter"""
            },
            {
                "title": "MBA Department - Complete Details",
                "content": """📊 Master of Business Administration (MBA)

📊 Established: 2007 | Intake: 120
📜 Regulations: 2015, 2018, 2023
🎯 Electives: Finance, Marketing, Human Resource, Entrepreneurship
🎉 Events: JANANAN and IPSUM management meets
🏢 Infrastructure: Air-conditioned flipped smart classes, separate library & computer centre
🤝 MoUs: EKARUP, IIMBx, NSE, PUPA, VANAPRASTHA, RJS, EPC

🎯 Vision:
To provide excellent management education and produce dynamic, innovative, and creative global executives.

👨‍🏫 HOD: Dr. P. Vanitha, M.Com., MBA, Ph.D. (Associate Professor & HOD)"""
            },
            {
                "title": "MCA Department - Complete Details",
                "content": """💾 Master of Computer Applications (MCA)

📊 Established: 2001 | Intake: 60
📜 Regulations: 2015, 2018, 2023
📚 Department Magazine: KOLOZ
💼 Placements: HashedIn, ZOHO, NXTSYNC (recent 2025 placements)

🎯 Vision:
To meet technology and evolve innovative applications for the software industry and promote technological advancement through knowledge dissemination.

👨‍🏫 HOD: Dr. S. Vanithamani, M.C.A., M.Phil., Ph.D. (Associate Professor & HOD)"""
            },
            {
                "title": "Mechanical Department - Complete Details",
                "content": """⚙️ Mechanical Engineering (MECH)

📊 Established: 2000 | Intake: 90
🤝 MoUs: NITT-Siemens, TVS Upasana, Roots Industries
🌍 International Collaboration: UTP Universiti Teknologi PETRONAS (Malaysia), Miami University (USA)

🎯 Vision:
To create globally recognized competent Mechanical Engineers to work in multicultural environments.

👨‍🏫 HOD: Dr. M. Loganathan, M.E., Ph.D. (Professor & HOD)"""
            },
            {
                "title": "Civil Department - Complete Details",
                "content": """🏗️ Civil Engineering

📊 Established: 2009 | Intake: 30
🏛️ Professional Body Members: IV, IE, IEEE, ISTE
🎯 Activities: Consultancy projects, industrial/construction site visits, conferences, workshops, seminars

🎯 Vision:
To nurture Civil Engineering professionals with strong technical competence and moral integrity to serve the society and nation.

👨‍🏫 HOD: Dr. Balaji G, M.E., Ph.D. (Associate Professor & Head)"""
            }
        ]
        
        # Add department documents
        for doc_data in dept_documents:
            doc = Document(title=doc_data['title'], content=doc_data['content'])
            db.session.add(doc)
            added_count += 1
        
        db.session.commit()
        
        # Count total
        faq_count = FAQ.query.count()
        doc_count = Document.query.count()
        
        print(f"✅ Successfully added comprehensive MKCE knowledge base!")
        print(f"📋 Total FAQs: {faq_count}")
        print(f"📄 Total Documents: {doc_count}")
        print(f"🎯 Total Items Added: {added_count}")
        print(f"\n🚀 Chatbot is now fully trained with complete MKCE information!")
        print(f"\nTopics covered:")
        print(f"  • College overview & management")
        print(f"  • Vision, mission, quality policy")
        print(f"  • Key statistics & contact info")
        print(f"  • All departments with faculty & labs")
        print(f"  • Research & development")
        print(f"  • Placement & training")
        print(f"  • Campus facilities & student portals")

if __name__ == "__main__":
    add_comprehensive_mkce_knowledge()
