import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.crm import extract_lead

def test_extract_lead():
    text = "Hi, My name is John Doe. Contact john@doe.com, 1234567890"
    lead = extract_lead(text)
    assert lead["email"] == "john@doe.com"
    assert lead["phone"] == "1234567890"
    assert lead["name"] == "John Doe"