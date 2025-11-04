from src import crm
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src import crm  # This assumes crm is a package with __init__.py, or adjust to from src.crm import ...

# Add your test code here

def test_db():
    crm.init_db("db/test_crm.db")
    crm.add_lead("Test User", "test@user.com", "1234567890", "test", db_path="db/test_crm.db")
    leads = crm.get_leads(db_path="db/test_crm.db")
    assert leads[-1][1] == "Test User"