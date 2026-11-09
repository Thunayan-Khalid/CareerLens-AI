from analyzer.resume_parser import extract_pdf_text

def test_invalid_pdf_raises_value_error():
    try:
        extract_pdf_text(b"not a pdf")
        assert False, "Expected ValueError"
    except ValueError:
        assert True
