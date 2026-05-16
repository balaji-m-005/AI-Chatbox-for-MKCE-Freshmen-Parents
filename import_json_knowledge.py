import json
from app import app
from models import db, FAQ, Document

def load_data():
    with open('new_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with app.app_context():
        # Clear existing data to avoid conflicts with wrong information
        db.session.query(FAQ).delete()
        db.session.query(Document).delete()
        
        faqs_to_add = []
        
        # 1. Add Sample Queries as FAQs
        for sq in data.get('sample_queries', []):
            faqs_to_add.append(FAQ(question=sq['question'], answer=sq['answer']))
            
        # 2. College Overview FAQ
        c = data.get('college', {})
        college_ans = f"{c.get('name')} ({c.get('short_name')})\n"
        college_ans += f"Tagline: {c.get('tagline')}\n"
        college_ans += f"Location: {c.get('location')}\n"
        college_ans += f"Established: {c.get('established')}\n"
        college_ans += f"Type: {c.get('type')}\n"
        college_ans += f"Affiliation: {c.get('affiliation')}\n"
        college_ans += f"Approval: {c.get('approval')}\n"
        college_ans += f"Website: {c.get('website')}\n"
        college_ans += f"TNEA Code: {c.get('tnea_code')}\n"
        college_ans += f"Principal: {c.get('principal')}\n"
        college_ans += f"Chairman: {c.get('chairman')}\n"
        college_ans += f"Executive Director: {c.get('executive_director')}\n"
        faqs_to_add.append(FAQ(question="Tell me about MKCE college basic information, principal, and chairman", answer=college_ans))
        
        # 3. Contact Details FAQ
        contact = c.get('contact', {})
        contact_ans = f"Admin Phone: {', '.join(contact.get('admin_phone', []))}\n"
        contact_ans += f"Admission Helpline: {', '.join(contact.get('admission_helpline', []))}\n"
        contact_ans += f"Admission Email: {contact.get('admission_email')}\n"
        contact_ans += f"Placement Email: {contact.get('placement_email')}\n"
        faqs_to_add.append(FAQ(question="What are the contact details, phone numbers, and emails for MKCE?", answer=contact_ans))
        
        # 4. Blocks FAQ
        blocks_ans = "Blocks in MKCE:\n"
        for b in data.get('blocks', []):
            blocks_ans += f"- {b.get('name')} ({b.get('block_id')}) with {b.get('floors')} floors.\n"
        faqs_to_add.append(FAQ(question="What are the different blocks in MKCE campus?", answer=blocks_ans))
        
        # 5. Departments FAQ
        dept_ans = "Departments in MKCE:\n"
        for d in data.get('departments', []):
            dept_ans += f"- {d.get('name')} ({d.get('department_id')}): Located in {d.get('block')}, {d.get('floor')}.\n"
        faqs_to_add.append(FAQ(question="Where are the different departments located in MKCE?", answer=dept_ans))
        
        # 6. ECE Specific FAQ
        ece = next((d for d in data.get('departments', []) if d.get('department_id') == 'ECE'), None)
        if ece:
            ece_ans = f"ECE Department is in {ece['block']}, {ece['floor']}.\n"
            ece_ans += f"HOD: {ece['hod']['name']} (Room {ece['hod']['room']})\n\nLabs:\n"
            for lab in ece.get('labs', []):
                ece_ans += f"- {lab['name']} (Room {lab['room_no']}) - Incharge: {lab.get('incharge', 'N/A')}\n"
            faqs_to_add.append(FAQ(question="Tell me about the ECE department, HOD, and labs", answer=ece_ans))
            
        # 7. Hostel & Mess FAQ
        hostel = data.get('hostel', {}).get('boys_mess_timing', {})
        mess_ans = "Boys Mess Timings:\nWorking Days:\n"
        wd = hostel.get('working_days', {})
        for k, v in wd.items(): mess_ans += f"- {k.capitalize()}: {v}\n"
        mess_ans += "Holidays:\n"
        hd = hostel.get('holidays', {})
        for k, v in hd.items(): mess_ans += f"- {k.capitalize()}: {v}\n"
        faqs_to_add.append(FAQ(question="What are the hostel mess timings for boys?", answer=mess_ans))
        
        # 8. Canteen & Cafeteria FAQ
        canteen = data.get('canteen', {})
        cafe = data.get('cafeteria', {})
        food_ans = f"Canteen: {canteen.get('name')}\nPopular Items:\n"
        for item in canteen.get('popular_items', []): food_ans += f"- {item['item']}: ₹{item['price']}\n"
        food_ans += f"\nCafeteria: {cafe.get('name')}\n"
        food_ans += "Milkshakes:\n"
        for item in cafe.get('menu', {}).get('milkshakes', []): food_ans += f"- {item['item']}: ₹{item['price']}\n"
        food_ans += "Fresh Juices:\n"
        for item in cafe.get('menu', {}).get('fresh_juices', []): food_ans += f"- {item['item']}: ₹{item['price']}\n"
        faqs_to_add.append(FAQ(question="What is the canteen and cafeteria menu with prices?", answer=food_ans))
        
        # 9. Portals FAQ
        portals_ans = "MKCE Student Portals:\n"
        for p in data.get('portals', []):
            portals_ans += f"- {p['name']}: {p['url']} ({p.get('purpose', 'Portal')})\n"
        faqs_to_add.append(FAQ(question="What are the college portals, CAMS, and KR Connect links?", answer=portals_ans))
        
        # 10. Bonafide Procedure FAQ
        bp = data.get('bonafide_procedure', {})
        bp_ans = f"To apply for a bonafide certificate, email {bp.get('email')} with the following details:\n"
        for field in bp.get('required_fields', []):
            bp_ans += f"- {field}\n"
        faqs_to_add.append(FAQ(question="How to apply for a bonafide certificate?", answer=bp_ans))
        
        # 11. Facilities & Sports
        fac_ans = "Campus Facilities:\n"
        for f in data.get('campus_facilities', []):
            fac_ans += f"- {f['name']} "
            if 'block' in f: fac_ans += f"({f['block']}, {f['floor']})\n"
            else: fac_ans += f"(Location ID: {f.get('location_id')})\n"
        fac_ans += "\nSports Facilities: " + ", ".join(data.get('sports_facilities', []))
        faqs_to_add.append(FAQ(question="What are the campus and sports facilities available?", answer=fac_ans))

        # Add everything to DB
        db.session.add_all(faqs_to_add)
        
        # Also store the full JSON as a Document for fallback context
        full_doc = Document(title="Complete MKCE JSON Information", content=json.dumps(data, indent=2))
        db.session.add(full_doc)
        
        db.session.commit()
        print(f"Successfully added {len(faqs_to_add)} FAQs and 1 Document to the database.")

if __name__ == '__main__':
    load_data()
