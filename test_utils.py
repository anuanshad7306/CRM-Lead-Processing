from src.utils import clean_text

def test_clean_text():
    assert clean_text(" Hello\nWorld\r ") == "Hello World "