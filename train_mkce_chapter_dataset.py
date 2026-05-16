#!/usr/bin/env python
"""Train chatbot with MKCE chapter-wise knowledge base and FAQ bank.

This script is idempotent:
- Existing FAQs are updated by question (case-insensitive)
- Existing Documents are updated by title (case-insensitive)
"""

from app import app
from models import db, FAQ, Document


CHAPTER_DOCUMENTS = [
    {
        "title": "MKCE Chapter 1 - College Overview",
        "content": """Full Name: M. Kumarasamy College of Engineering\nShort Name: MKCE\nTagline: The Best Engineering College With 25 Years of Excellence\nLocation: Karur, Tamil Nadu, India\nGPS Coordinates: Latitude 11.055287\nEstablished: 2000\nType: Autonomous Engineering Institution\nAffiliation: Anna University, Chennai\nApproval: AICTE, New Delhi\nTrust: M. Kumarasamy Health and Educational Trust\nTNEA Counselling Code: 2608\nWebsite: https://www.mkce.ac.in\nMaintained By: Technology Innovation Hub - MKCE\nYears of Excellence: 25 years as of 2025""",
    },
    {
        "title": "MKCE Chapter 2 - Management and Leadership",
        "content": """Founder: Thiru M. Kumarasamy, known as Maniyakar, former Munisif of Thalavapalayam village for 20+ years.\nChairman and Secretary: Dr. K. Ramakrishnan, B.E. Production Engineering, Annamalai University.\nExecutive Director: Dr. S. Kuppusamy, B.Sc. Electronics, MBA, Ph.D. Management, NET and SLET qualified.\nPrincipal: Dr. B. S. Murugan, M.E., Ph.D., also Professor in CSE.\nMKCE was founded in 2000 to offer affordable engineering education to rural students.""",
    },
    {
        "title": "MKCE Chapter 3 - Vision Mission Quality",
        "content": """Vision: To emerge as a leader among the top institutions in technical education.\nMission: 1) Produce smart technocrats to face global challenges. 2) Create a diverse learner-centric campus for quality education. 3) Maintain partnerships with alumni, industry and professional associations.\nQuality Policy: MKCE commits to developing responsible citizens with ethical values through quality technical education and continual improvement toward world-class technological standards.\nWhy MKCE: Creativity and innovation, student-centric campus, experiential learning, comprehensive teaching.""",
    },
    {
        "title": "MKCE Chapter 4 - Key Statistics",
        "content": """Proud Alumni: 15100+\nCurrent Students: 4150+\nPlaced Students: 830+\nTotal Faculty: 280+\nSCIE or Scopus or WoS Publications: 2673+\nUGC Care Journal Publications: 302\nBook or Book Chapter Publications: 125\nh-index: 61 on Google Scholar and 53 on Scopus\nPatents: 715 published and 120 registered\nStudent Publications: 645\nConference Publications: 2530\nTotal Citations in Scopus: 18090+""",
    },
    {
        "title": "MKCE Chapter 5 - Contact Information",
        "content": """Administration Phone: 04324-272155 / 04324-270755\nAdministration Fax: 04324-272457\nAdmission Helpline: 9750356377 / 8754022577\nAdmission Email: admission@mkce.ac.in\nPlacement and Training: 04324-272155 / 04324-270755\nPlacement Email: placement@mkce.ac.in\nEEE HOD Direct: eee@mkce.ac.in / 8754015677\nDean of Admissions: Dr. K. Sundararaju, +91 9750356377 / 7540046077""",
    },
    {
        "title": "MKCE Chapter 6 - Accreditation and Rankings",
        "content": """NAAC: A Grade, Cycle 2\nNBA: Accredited for select programmes including CSE under Washington Accord Tier-I\nAICTE: Approved, New Delhi\nAnna University: Affiliated with Autonomous status\nTCS: Accredited\nNIRF: Ranked (https://mkce.ac.in/nirf.php)\nARIIA: Ranked (https://mkce.ac.in/files/ariia.pdf)\nMBA: IIRF ranked\nStaffordshire University: Teaching Award in Engineering to CSE Department in 2015\nResearch Centres: 6 departments recognized by Anna University""",
    },
    {
        "title": "MKCE Chapter 7 - Programmes and Intake",
        "content": """UG Programmes include B.E. and B.Tech in AI and DS, CSE, CSE AI and ML, Civil, CSBS, EEE, ECE, IT, Mechanical, VLSI, and CSE Cyber Security.\nUG intake highlights: AI and DS 180, CSE 180, ECE 300, EEE 120, IT 120, Mechanical 90, Civil 30, CSE AI and ML 60, CSBS 60, VLSI 60, CSE Cyber Security 60.\nPG Programmes: MBA 120, MCA 60, M.E. CSE 12, Communication Systems 12, Power Systems Engineering 12, Manufacturing Engineering 12.""",
    },
    {
        "title": "MKCE Chapter 8 - Department Wise Overview",
        "content": """Departments covered: ECE, CSE, IT, EEE, Mechanical, Civil, VLSI, MBA, MCA, AI and DS, CSE AI and ML, CSBS, and Freshmen Engineering.\nECE established 2000 with UG intake 300 and PG Communication Systems intake 12; 12 labs and recognized research centre.\nCSE established 2000 with NBA Tier-I and Washington Accord recognition; 1 Gbps internet support.\nIT established 2001 with focus areas including Network Security, Cloud, Data Mining, Cyber Security and Big Data.\nEEE has 8 labs and uses MATLAB, Mi-Power, AU Power, ICT Circuit Tool, LabVIEW; recognized research centre.\nMechanical has industry MoUs and international collaborations.\nCivil focuses on core domain competence with professional body engagement.\nVLSI is a recent programme under Regulation 2023 with intake 60 and semiconductor focus.\nMBA and MCA include modern curriculum and placement support.""",
    },
    {
        "title": "MKCE Chapter 9 - Research and Development",
        "content": """R and D Cell established in 2012.\n6 departments are recognized as Anna University research centres.\nPh.D. Fellowship: INR 10000 per month for full-time scholars.\nResearch progress review every 6 months.\nFunded projects include SERB CRG INR 13.07 lakh, SERB TARE INR 18.30 lakh, MSME grants INR 28 lakh and INR 48 lakh, TNSCST INR 60000 for 5 projects, and Naan Mudhalvan INR 30000 for 3 projects.\nPublication incentives: Q4 INR 5000, Q3 INR 7500, Q2 INR 10000, Q1 INR 15000, Q1 with impact factor above 10 INR 20000.""",
    },
    {
        "title": "MKCE Chapter 10 - Placement and Training",
        "content": """Career Skill Development modules include aptitude, group discussion, interview handling, professional and personality development.\nPlacement infrastructure includes testing halls, conference halls, online test centres, discussion rooms, interview rooms, video conferencing and placement lounge.\nRecent recruiters include Infosys, LTIMindtree, Hexaware, Zoho, TCS, Capgemini, Accenture, Wipro, IBM, CTS and multiple Japan recruiters.\nJapan placement and higher studies opportunities are supported through Sakura Science Program pathways.""",
    },
    {
        "title": "MKCE Chapter 11 - Center for Foreign Languages",
        "content": """Language taught: Japanese (Nihongo).\nLevels: N5 or Q5, N4 or Q4, N3 or Q3.\nMKCE is an approved JLPT exam centre and prepares students for JLPT and NAT certifications.\nHistoric JLPT certification counts are available batch-wise from 2013 to 2024.""",
    },
    {
        "title": "MKCE Chapter 12 - Campus Facilities",
        "content": """Academic facilities: Smart classrooms, drawing halls, IT labs, engineering labs, Technology Learning Centre and Media Centre.\nLibrary: physical and digital resources with OPAC access at http://10.0.7.150/impreserp/OPAC/Default.aspx.\nAuditoriums and halls: Valluvar Hall, G.D. Naidu Hall, conference halls and media spaces.\nSports: Basketball, tennis, volleyball and 3 fitness centres.\nHostel portal: http://hostel.mkce.ac.in/.\nTransport: city-wide bus fleet, safety features and route file at https://www.mkce.ac.in/hostel/bus_route.pdf.""",
    },
    {
        "title": "MKCE Chapter 13 - Student Portals and Links",
        "content": """CAMS: http://www.camsmkce.in\nKR Connect: http://krconnect.mkce.ac.in/\nSmart Hostel: http://hostel.mkce.ac.in/\nTeaching Learning Centre: http://tlc.krgi.in\nLibrary OPAC: http://10.0.7.150/impreserp/OPAC/Default.aspx\nCertificate verification: https://mkce.directverify.in/student/index.html\nBlog: http://mkce.ac.in/blog\nAlumni portal: http://alumni.mkce.ac.in/\nAdmission form: https://forms.gle/EGoB193DkB9tu3ts8\nFee payment via Axis EasyPay with separate links for new and existing students.""",
    },
    {
        "title": "MKCE Chapter 14 - Alumni Testimonials",
        "content": """Alumni testimonials mention strong academic foundations, mentoring support, practical curriculum, and effective placement support.\nReferenced alumni include leaders from Oracle Cerner Healthcare, State Street Corporation, Prodrive Technologies Japan, and NASSCOM roles.""",
    },
    {
        "title": "MKCE Chapter 15 - Campus Block Layout",
        "content": """MKCE campus has two main academic blocks: Dr. APJ Abdul Kalam Block and Dr. S. Radhakrishnan Block.\n\nDr. APJ Abdul Kalam Block floors:\nGround Floor - CSE\nFirst Floor - EEE\nSecond Floor - ECE\nThird Floor - CSBS\n\nDr. S. Radhakrishnan Block floors:\nGround Floor - Civil Engineering\nFirst Floor - Mechanical Engineering and MBA\nSecond Floor - IT\nThird Floor - AIDS and AIML""",
    },
    {
        "title": "MKCE Chapter 16 - ECE Department Layout",
        "content": """ECE department is located on the Second Floor of Dr. APJ Abdul Kalam Block.\n\nClassrooms:\nRoom 202 - II ECE A\nRoom 203 - II ECE B\nRoom 204 - II ECE C\nRoom 208 - II ECE D\nRoom 209 - II VLSI\nRoom 210 - III ECE A\nRoom 211 - III ECE B\nRoom 213 - III ECE C\nRoom 214 - III ECE D\nRoom 224 - III ECE B\nRoom 225 - III ECE A\nRoom 215 - IV ECE A\nRoom 222 - IV ECE B\nRoom 232 - IV ECE C\nRoom 229 - IV ECE D\n\nStaff Rooms:\nRoom 205 - ECE Staff Room 1\nRoom 212 - ECE Staff Room 2\nRoom 230 - ECE Staff Room 3\n\nHOD Cabin:\nRoom 239 - ECE HOD Cabin\nHOD: Mr. Mahendran\n\nLaboratories:\nRoom 201 - Optical and Microwave Lab\nRoom 207 - Embedded System Design Lab\nRoom 217 - DSP Lab\nRoom 227 - Electronics and Microprocessors Lab\nRoom 228 - Electronic Circuits Lab (VLSI)\nRoom 231 - Analog and Digital Communication Lab\nRoom 233 - Electronic Circuits Laboratory\nRoom 234 - LIC Lab\nRoom 235 - Project Lab\nRoom 238 - PCB Design Lab\n\nOther facilities:\nRoom 218 - ECE Board Room\nOpposite Room 218 - RO Water Tank\nRoom 226 - ECE Record Room\nRoom 236 - Server Room\nRoom 237 - ECE Library\n\nUtilities:\nRoom 223 - Boys Washroom\nRoom 224 - Boys Common Room\nRoom 225 - Gents Staff Washroom\nOpposite Room 209 - RO Drinking Water\nOpposite Room 232 - RO Drinking Water\nOpposite Room 202 - Lift Available\nFire Extinguisher Available\n\nSpecial Cell:\nRoom 216 - Women Empowerment Cell""",
    },
]


FAQ_BANK = [
    {
        "question": "What is MKCE?",
        "answer": "M. Kumarasamy College of Engineering is an autonomous institution in Karur, Tamil Nadu, affiliated to Anna University and approved by AICTE.",
    },
    {"question": "What is the TNEA code of MKCE?", "answer": "The TNEA counselling code is 2608."},
    {"question": "When was MKCE established?", "answer": "MKCE was established in 2000."},
    {"question": "Who is the Principal of MKCE?", "answer": "Dr. B. S. Murugan, M.E., Ph.D., is the Principal and also a Professor in CSE."},
    {"question": "Who is the Chairman of MKCE?", "answer": "Dr. K. Ramakrishnan is the Chairman and Secretary of MKCE."},
    {"question": "What is MKCE NAAC grade?", "answer": "MKCE is accredited with NAAC A Grade, Cycle 2."},
    {"question": "How many alumni does MKCE have?", "answer": "MKCE has more than 15100 alumni."},
    {"question": "How many students are currently studying at MKCE?", "answer": "MKCE has more than 4150 current students."},
    {"question": "How many total faculty members are there in MKCE?", "answer": "MKCE has more than 280 faculty members."},
    {"question": "How many students are placed from MKCE?", "answer": "Latest figures report 830+ placed students."},
    {"question": "Who is the ECE HOD in MKCE?", "answer": "Dr. N. Mahendran, M.E., Ph.D., is the ECE HOD."},
    {"question": "Who is the CSE HOD in MKCE?", "answer": "Dr. D. Pradeep, M.E., Ph.D., is the CSE HOD."},
    {"question": "Who is the IT HOD in MKCE?", "answer": "Dr. K. Ravikumar, M.E., Ph.D., is the IT HOD."},
    {"question": "Who is the EEE HOD in MKCE?", "answer": "Dr. J. Uma, M.E., Ph.D., is the EEE HOD. Contact: 8754015677, eee@mkce.ac.in."},
    {"question": "Who is the Mechanical HOD in MKCE?", "answer": "Dr. M. Loganathan, M.E., Ph.D., is the Mechanical HOD."},
    {"question": "Who is the Civil HOD in MKCE?", "answer": "Dr. Balaji G, M.E., Ph.D., is the Civil HOD and Associate Professor and Head."},
    {"question": "Who is the MBA HOD in MKCE?", "answer": "Dr. P. Vanitha, M.Com., MBA, Ph.D., is the MBA HOD."},
    {"question": "Who is the MCA HOD in MKCE?", "answer": "Dr. S. Vanithamani, M.C.A., M.Phil., Ph.D., is the MCA HOD."},
    {"question": "How many laboratories are there in ECE?", "answer": "ECE has 12 laboratories."},
    {"question": "Is there a VLSI department in MKCE?", "answer": "Yes. MKCE offers B.E. Electronics Engineering (VLSI Design and Technology) with 60 seats."},
    {"question": "Does EEE have a PG programme?", "answer": "Yes. EEE offers M.E. Power Systems Engineering with 12 seats."},
    {"question": "What are recent placement companies for MCA students?", "answer": "Recent MCA placements include HashedIn, ZOHO, and NXTSYNC."},
    {"question": "What language does the CFL teach at MKCE?", "answer": "The Center for Foreign Languages teaches Japanese."},
    {"question": "Is MKCE an approved JLPT exam centre?", "answer": "Yes, MKCE is an approved JLPT exam centre."},
    {"question": "What is the internet speed in MKCE labs?", "answer": "1 Gbps Wi-Fi is available, including 24-hour internet availability in key departments."},
    {"question": "Does Mechanical department have international collaborations?", "answer": "Yes, collaborations include UTP Malaysia and Miami University USA."},
    {"question": "What software tools are used in EEE?", "answer": "EEE uses MATLAB, Mi-Power, AU Power, ICT Circuit Tool, and LabVIEW."},
    {"question": "What are the MBA MoUs in MKCE?", "answer": "MBA MoUs include EKARUP, IIMBx, NSE, PUPA, VANAPRASTHA, RJS, and EPC."},
    {"question": "What is KOLOZ in MKCE?", "answer": "KOLOZ is the technical magazine of the MCA department."},
    {"question": "What are JANANAM and IPSUM?", "answer": "JANANAM and IPSUM are annual management meets conducted by the MBA department."},
    {"question": "Can students pursue Ph.D. at MKCE?", "answer": "Yes. Six departments are recognized as Anna University research centres."},
    {"question": "What is the Ph.D. fellowship amount at MKCE?", "answer": "INR 10000 per month for full-time scholars."},
    {"question": "How can I pay fees in MKCE?", "answer": "Fees can be paid through Axis Bank EasyPay links for new and existing students."},
    {"question": "How do I check exam results in MKCE?", "answer": "Use CAMS portal: http://www.camsmkce.in"},
    {"question": "How do I verify my certificate from MKCE?", "answer": "Use https://mkce.directverify.in/student/index.html"},
    {"question": "How do I apply for admission in MKCE?", "answer": "Apply via https://forms.gle/EGoB193DkB9tu3ts8 or contact admission helpline numbers."},
    {"question": "What sports facilities are available in MKCE?", "answer": "Basketball, tennis, volleyball courts, and 3 fitness centres are available."},
    {"question": "Is hostel facility available at MKCE?", "answer": "Yes. Hostel portal: http://hostel.mkce.ac.in/"},
    {"question": "Is bus transport available in MKCE?", "answer": "Yes, city-wide bus transport is available. Route file: https://www.mkce.ac.in/hostel/bus_route.pdf"},
    {"question": "How can I raise a grievance in MKCE?", "answer": "Use the online grievance redressal form available on the MKCE website."},
    {"question": "Which professional bodies are active in ECE?", "answer": "Eminence Association, IEEE ComSoc, and IETE."},
    {"question": "Which professional bodies are active in EEE?", "answer": "ISTE and IEEE Student Chapter."},
    {"question": "Which professional bodies are active in Civil Engineering?", "answer": "IV, IE, IEEE, and ISTE."},
    {"question": "What is CSE NBA status in MKCE?", "answer": "CSE is NBA accredited under Engineering Tier-I and Washington Accord."},
    {"question": "Did MKCE receive a teaching award?", "answer": "Yes. CSE received the Staffordshire University Teaching Award in Engineering in 2015."},
    {"question": "What are MSME grants received by MKCE?", "answer": "MSME grants include INR 28 lakh for 2023-24 and INR 48 lakh for 2024-25."},
    {"question": "What is the MKCE admission email?", "answer": "admission@mkce.ac.in"},
    {"question": "What is the MKCE placement email?", "answer": "placement@mkce.ac.in"},
    {"question": "What is the MKCE administration phone number?", "answer": "04324-272155 / 04324-270755"},
    {"question": "What is the full name of MKCE?", "answer": "The full name is M. Kumarasamy College of Engineering."},
    {"question": "What is the MKCE website?", "answer": "https://www.mkce.ac.in"},
    {"question": "What is the MKCE tagline?", "answer": "The Best Engineering College With 25 Years of Excellence."},
    {"question": "Where is MKCE located?", "answer": "MKCE is located in Karur, Tamil Nadu, India."},
    {"question": "Where is RK block in MKCE?", "answer": "RK block refers to Dr. S. Radhakrishnan Block in MKCE. It has Civil Engineering on the Ground Floor, Mechanical Engineering and MBA on the First Floor, IT on the Second Floor, and AIDS and AIML on the Third Floor."},
    {"question": "Where is Dr. S. Radhakrishnan Block?", "answer": "Dr. S. Radhakrishnan Block is one of the main academic blocks in MKCE campus and hosts Civil Engineering, Mechanical Engineering, MBA, IT, AIDS, and AIML across its floors."},
    {"question": "What departments are in APJ Block?", "answer": "Dr. APJ Abdul Kalam Block has CSE on the Ground Floor, EEE on the First Floor, ECE on the Second Floor, and CSBS on the Third Floor."},
    {"question": "What departments are in RK Block?", "answer": "Dr. S. Radhakrishnan Block has Civil Engineering on the Ground Floor, Mechanical Engineering and MBA on the First Floor, IT on the Second Floor, and AIDS and AIML on the Third Floor."},
    {"question": "Where is ECE department in MKCE?", "answer": "ECE department is on the Second Floor of Dr. APJ Abdul Kalam Block."},
    {"question": "Where are the ECE classrooms?", "answer": "ECE classrooms are in Rooms 202, 203, 204, 208, 209, 210, 211, 213, 214, 215, 222, 224, 225, 229, and 232, along with the associated ECE sections in the Second Floor of Dr. APJ Abdul Kalam Block."},
    {"question": "Where is ECE Staff Room 1?", "answer": "ECE Staff Room 1 is in Room 205."},
    {"question": "Where is ECE Staff Room 2?", "answer": "ECE Staff Room 2 is in Room 212."},
    {"question": "Where is ECE Staff Room 3?", "answer": "ECE Staff Room 3 is in Room 230."},
    {"question": "Where is the ECE HOD cabin?", "answer": "The ECE HOD Cabin is in Room 239. The HOD is Mr. Mahendran."},
    {"question": "Where is the Optical and Microwave Lab?", "answer": "The Optical and Microwave Lab is in Room 201. In-charge: Mrs. Revathi, 9965569714, revathig.ece@mkce.ac.in."},
    {"question": "Where is the Embedded System Design Lab?", "answer": "The Embedded System Design Lab is in Room 207. In-charge: Mr. Mohanraj, 9976775159, mohanrajs.ece@mkce.ac.in."},
    {"question": "Where is the DSP Lab?", "answer": "The DSP Lab is in Room 217. In-charge: Mr. JeyaKumar P, 9994723025, jeyakumarp.ece@mkce.ac.in."},
    {"question": "Where is III ECE A section?", "answer": "III ECE A section is in Room 210 and Room 225 in the Second Floor of Dr. APJ Abdul Kalam Block."},
    {"question": "Where is III ECE B section?", "answer": "III ECE B section is in Room 211 and Room 224 in the Second Floor of Dr. APJ Abdul Kalam Block."},
    {"question": "Where is III ECE C section?", "answer": "III ECE C section is in Room 213 in the Second Floor of Dr. APJ Abdul Kalam Block."},
    {"question": "Where is III ECE D section?", "answer": "III ECE D section is in Room 214 in the Second Floor of Dr. APJ Abdul Kalam Block."},
    {"question": "Where is the ECE Library?", "answer": "The ECE Library is in Room 237. Staff: Mr. Sundarapandi."},
    {"question": "Where is the Women Empowerment Cell in ECE?", "answer": "The Women Empowerment Cell is in Room 216. Staff: Mrs. Pushpalatha, Mrs. Rakha Sudha, and Mrs. Vaidegi."},
    {"question": "Where is the RO drinking water in ECE?", "answer": "RO drinking water is available opposite Room 209 and opposite Room 232."},
    {"question": "Is a lift available near ECE?", "answer": "Yes. A lift is available opposite Room 202."},
    {"question": "Where is the ECE board room?", "answer": "The ECE Board Room is in Room 218."},
    {"question": "What are the UG programmes in MKCE?", "answer": "UG programmes include B.E./B.Tech in AI and DS, CSE, CSE AI and ML, Civil, CSBS, EEE, ECE, IT, Mechanical, VLSI, and CSE Cyber Security."},
    {"question": "What are the PG programmes in MKCE?", "answer": "PG programmes include MBA, MCA, M.E. CSE, M.E. Communication Systems, M.E. Power Systems Engineering, and M.E. Manufacturing Engineering."},
    {"question": "How many seats are available in B.Tech AI and DS?", "answer": "180 seats."},
    {"question": "How many seats are available in B.E. CSE?", "answer": "180 seats."},
    {"question": "How many seats are available in B.E. ECE?", "answer": "300 seats."},
    {"question": "How many seats are available in B.Tech IT?", "answer": "120 seats."},
    {"question": "How many seats are available in MBA?", "answer": "120 seats."},
    {"question": "How many seats are available in MCA?", "answer": "60 seats."},
    {"question": "What is KR Connect portal URL?", "answer": "http://krconnect.mkce.ac.in/"},
    {"question": "What is CAMS portal URL?", "answer": "http://www.camsmkce.in"},
    {"question": "What is MKCE Smart Hostel portal URL?", "answer": "http://hostel.mkce.ac.in/"},
    {"question": "What is MKCE Teaching Learning Centre URL?", "answer": "http://tlc.krgi.in"},
    {"question": "What is the MKCE library OPAC URL?", "answer": "http://10.0.7.150/impreserp/OPAC/Default.aspx"},
    {"question": "What is the MKCE alumni portal URL?", "answer": "http://alumni.mkce.ac.in/"},
    {"question": "What are major recruiters for MKCE placements?", "answer": "Recruiters include Infosys, LTIMindtree, Hexaware, Zoho, TCS, Capgemini, Accenture, Wipro, IBM, CTS, and several Japan-based companies."},
    {"question": "Does MKCE support Japan placements?", "answer": "Yes. Students are placed in Japanese companies and also pursue higher studies through Sakura Science pathways."},
]


def _normalize(text):
    return (text or "").strip().lower()


def upsert_faq(question, answer):
    normalized_question = _normalize(question)
    existing = FAQ.query.filter(db.func.lower(FAQ.question) == normalized_question).first()

    if existing:
        existing.answer = answer.strip()
        return "updated"

    db.session.add(FAQ(question=question.strip(), answer=answer.strip()))
    return "inserted"


def upsert_document(title, content):
    normalized_title = _normalize(title)
    existing = Document.query.filter(db.func.lower(Document.title) == normalized_title).first()

    if existing:
        existing.content = content.strip()
        return "updated"

    db.session.add(Document(title=title.strip(), content=content.strip()))
    return "inserted"


def train_mkce_chapter_dataset():
    with app.app_context():
        faq_inserted = 0
        faq_updated = 0
        doc_inserted = 0
        doc_updated = 0

        for item in CHAPTER_DOCUMENTS:
            action = upsert_document(item["title"], item["content"])
            if action == "inserted":
                doc_inserted += 1
            else:
                doc_updated += 1

        for item in FAQ_BANK:
            action = upsert_faq(item["question"], item["answer"])
            if action == "inserted":
                faq_inserted += 1
            else:
                faq_updated += 1

        db.session.commit()

        print("MKCE chapter dataset training completed.")
        print(f"FAQ inserted: {faq_inserted}")
        print(f"FAQ updated: {faq_updated}")
        print(f"Document inserted: {doc_inserted}")
        print(f"Document updated: {doc_updated}")
        print(f"Total FAQs in DB: {FAQ.query.count()}")
        print(f"Total Documents in DB: {Document.query.count()}")


if __name__ == "__main__":
    train_mkce_chapter_dataset()
