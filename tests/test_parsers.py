import pytest
from pathlib import Path
from sme_clone.parsers.pdf_parser import parse_pdf
from sme_clone.parsers.email_parser import parse_email_archive
from sme_clone.parsers.slack_parser import parse_slack_export
from sme_clone.parsers.docx_parser import parse_docx
from sme_clone.parsers.pptx_parser import parse_pptx
from sme_clone.parsers.xlsx_parser import parse_xlsx
from sme_clone.setup import dispatch_file, _parse_passthrough, _parse_code

# Setup test constants
REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_EXAMPLE_DIR = REPO_ROOT / "test-example"
SME_EMAIL = "departing-sme@example.com"

@pytest.fixture
def temp_output_dir(tmp_path):
    """Provides a temporary directory for parser output."""
    d = tmp_path / "parsed"
    d.mkdir()
    return d

def test_pdf_parser(temp_output_dir):
    pdf_path = TEST_EXAMPLE_DIR / "sample_design_doc.pdf"
    assert pdf_path.exists(), f"Missing fixture: {pdf_path}"
    
    output_path = parse_pdf(pdf_path, temp_output_dir)
    
    assert output_path.exists()
    assert output_path.suffix == ".md"
    content = output_path.read_text(encoding="utf-8")
    assert "# Sample Design Doc" in content
    assert "Parsed from `sample_design_doc.pdf`" in content
    # Check that some text was extracted (even if it's minimal)
    assert len(content) > 100

def test_email_parser_mbox(temp_output_dir):
    mbox_path = TEST_EXAMPLE_DIR / "sample_emails.mbox"
    assert mbox_path.exists(), f"Missing fixture: {mbox_path}"
    
    # We use a dummy email that we expect to find in the sample (or it will include all if no match)
    output_files = parse_email_archive(mbox_path, temp_output_dir, SME_EMAIL)
    
    assert len(output_files) > 0
    for out_file in output_files:
        assert out_file.exists()
        assert out_file.suffix == ".md"
        content = out_file.read_text(encoding="utf-8")
        assert "# " in content  # Should have a subject as H1

def test_slack_parser_zip(temp_output_dir):
    zip_path = TEST_EXAMPLE_DIR / "sample_slack_export.zip"
    assert zip_path.exists(), f"Missing fixture: {zip_path}"
    
    # The sample zip might require a specific email to find messages.
    # In our sample_slack_export.zip, the user is likely 'alice@example.com' or similar.
    # We'll use a generic email and the parser should return all if no match found.
    output_files = parse_slack_export(zip_path, temp_output_dir, "alice@example.com")
    
    assert len(output_files) > 0
    for out_file in output_files:
        assert out_file.exists()
        assert out_file.suffix == ".md"
        content = out_file.read_text(encoding="utf-8")
        assert "# #" in content  # Slack channels start with # in the header

def test_docx_parser(temp_output_dir):
    docx_path = TEST_EXAMPLE_DIR / "sample_doc.docx"
    assert docx_path.exists(), f"Missing fixture: {docx_path}"
    
    output_path = parse_docx(docx_path, temp_output_dir)
    
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Sample Word Doc" in content

def test_pptx_parser(temp_output_dir):
    pptx_path = TEST_EXAMPLE_DIR / "sample_slides.pptx"
    assert pptx_path.exists(), f"Missing fixture: {pptx_path}"
    
    output_path = parse_pptx(pptx_path, temp_output_dir)
    
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Sample Presentation" in content

def test_xlsx_parser(temp_output_dir):
    xlsx_path = TEST_EXAMPLE_DIR / "sample_data.xlsx"
    assert xlsx_path.exists(), f"Missing fixture: {xlsx_path}"
    
    output_path = parse_xlsx(xlsx_path, temp_output_dir)
    
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "Header 1" in content
    assert "Data 1" in content

def test_passthrough_parser(temp_output_dir):
    # Test with a .txt file
    txt_path = TEST_EXAMPLE_DIR / "README.md" # Using README.md as a test file
    output_path = _parse_passthrough(txt_path, temp_output_dir)
    
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "offboarding-sme-clone" in content

def test_code_parser(temp_output_dir):
    # Test with a .py file (the script itself)
    py_path = REPO_ROOT / "sme_clone" / "setup.py"
    output_path = _parse_code(py_path, temp_output_dir)
    
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "```python" in content
    assert "setup.py" in content

def test_dispatch_file(temp_output_dir):
    pdf_path = TEST_EXAMPLE_DIR / "sample_design_doc.pdf"
    
    output_paths = dispatch_file(pdf_path, temp_output_dir, SME_EMAIL)
    
    assert len(output_paths) == 1
    assert output_paths[0].exists()
    assert "docs" in str(output_paths[0])
