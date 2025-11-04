from crm import get_leads

def print_leads():
    leads = get_leads()
    for lead in leads:
        print(f"ID: {lead[0]}, Name: {lead[1]}, Email: {lead[2]}, Phone: {lead[3]}, Source: {lead[4]}")