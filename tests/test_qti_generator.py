"""
Tests for the QTI generator module.
"""
import os
import tempfile
import zipfile
import pytest
from xml.etree import ElementTree

from markdown_to_qti.parser import Question, Choice
from markdown_to_qti.qti_generator import (
    generate_qti_assessment,
    generate_qti_manifest,
    create_qti_package,
    _markdown_to_html,
)


class TestMarkdownToHtml:
    """Tests for _markdown_to_html function."""
    
    def test_plain_text(self):
        """Test converting plain text."""
        result = _markdown_to_html("Simple text")
        assert "Simple text" in result
    
    def test_html_escaping(self):
        """Test that HTML special characters are escaped."""
        result = _markdown_to_html("1 < 2 && 3 > 2")
        assert "&lt;" in result
        assert "&gt;" in result
        assert "&amp;" in result
    
    def test_code_block_conversion(self):
        """Test converting code blocks to HTML."""
        markdown = """Here is code:

```python
def hello():
    print("Hello")
```"""
        result = _markdown_to_html(markdown)
        
        assert "<pre><code" in result
        assert "language-python" in result
        assert "def hello():" in result
    
    def test_code_block_preserves_content(self):
        """Test that code block content is preserved."""
        markdown = """```
x = 1
y = 2
```"""
        result = _markdown_to_html(markdown)
        
        assert "x = 1" in result
        assert "y = 2" in result
    
    def test_inline_code(self):
        """Test converting inline code."""
        result = _markdown_to_html("Use `print()` function")
        assert "<code>print()</code>" in result
    
    def test_newlines_converted(self):
        """Test that newlines are converted to <br/> tags."""
        result = _markdown_to_html("Line 1\nLine 2")
        assert "<br/>" in result


class TestGenerateQtiAssessment:
    """Tests for generate_qti_assessment function."""
    
    def test_generates_valid_xml(self):
        """Test that valid XML is generated."""
        questions = [
            Question(
                number=1,
                stem="What is 1+1?",
                choices=[
                    Choice(letter="a", text="1", is_correct=False),
                    Choice(letter="b", text="2", is_correct=True),
                ],
                correct_answer="b"
            )
        ]
        
        xml_output = generate_qti_assessment(questions, "Test Assessment")
        
        # Should be valid XML
        root = ElementTree.fromstring(xml_output)
        # Check that it's a questestinterop element (may have namespace prefix)
        assert 'questestinterop' in root.tag
    
    def test_contains_assessment_title(self):
        """Test that the assessment title is included."""
        questions = [
            Question(
                number=1,
                stem="Q1",
                choices=[Choice(letter="a", text="A", is_correct=True)],
                correct_answer="a"
            )
        ]
        
        xml_output = generate_qti_assessment(questions, "My Quiz")
        root = ElementTree.fromstring(xml_output)
        
        assessment = root.find('.//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}assessment')
        assert assessment is not None
        assert assessment.get('title') == "My Quiz"
    
    def test_contains_all_questions(self):
        """Test that all questions are included."""
        questions = [
            Question(
                number=i,
                stem=f"Question {i}",
                choices=[Choice(letter="a", text="A", is_correct=True)],
                correct_answer="a"
            )
            for i in range(1, 4)
        ]
        
        xml_output = generate_qti_assessment(questions, "Test")
        root = ElementTree.fromstring(xml_output)
        
        items = root.findall('.//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}item')
        assert len(items) == 3
    
    def test_contains_question_text(self):
        """Test that question text is included."""
        questions = [
            Question(
                number=1,
                stem="What color is the sky?",
                choices=[
                    Choice(letter="a", text="Blue", is_correct=True),
                    Choice(letter="b", text="Green", is_correct=False),
                ],
                correct_answer="a"
            )
        ]
        
        xml_output = generate_qti_assessment(questions, "Test")
        
        assert "What color is the sky?" in xml_output
        assert "Blue" in xml_output
        assert "Green" in xml_output
    
    def test_code_blocks_converted_to_html(self):
        """Test that code blocks are converted to HTML."""
        questions = [
            Question(
                number=1,
                stem="```python\nprint('hi')\n```",
                choices=[Choice(letter="a", text="A", is_correct=True)],
                correct_answer="a"
            )
        ]
        
        xml_output = generate_qti_assessment(questions, "Test")
        
        # The HTML is entity-encoded in the XML, so look for the encoded version
        assert "&lt;pre&gt;" in xml_output or "<pre>" in xml_output
        assert "&lt;code" in xml_output or "<code" in xml_output


class TestGenerateQtiManifest:
    """Tests for generate_qti_manifest function."""
    
    def test_generates_valid_xml(self):
        """Test that valid manifest XML is generated."""
        manifest_xml = generate_qti_manifest("test_id", "Test Assessment")
        
        root = ElementTree.fromstring(manifest_xml)
        # Check that it's a manifest element (may have namespace prefix)
        assert 'manifest' in root.tag
    
    def test_contains_resource_reference(self):
        """Test that the manifest references the assessment resource."""
        manifest_xml = generate_qti_manifest("test_id", "Test Assessment")
        
        assert "test_id" in manifest_xml


class TestCreateQtiPackage:
    """Tests for create_qti_package function."""
    
    def test_creates_zip_file(self):
        """Test that a ZIP file is created."""
        questions = [
            Question(
                number=1,
                stem="Q1",
                choices=[Choice(letter="a", text="A", is_correct=True)],
                correct_answer="a"
            )
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output.zip")
            result_path = create_qti_package(questions, output_path, "Test")
            
            assert os.path.exists(result_path)
            assert result_path.endswith('.zip')
    
    def test_zip_contains_manifest(self):
        """Test that the ZIP file contains imsmanifest.xml."""
        questions = [
            Question(
                number=1,
                stem="Q1",
                choices=[Choice(letter="a", text="A", is_correct=True)],
                correct_answer="a"
            )
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output.zip")
            result_path = create_qti_package(questions, output_path, "Test")
            
            with zipfile.ZipFile(result_path, 'r') as zf:
                names = zf.namelist()
                assert 'imsmanifest.xml' in names
    
    def test_zip_contains_assessment_xml(self):
        """Test that the ZIP file contains the assessment XML."""
        questions = [
            Question(
                number=1,
                stem="Q1",
                choices=[Choice(letter="a", text="A", is_correct=True)],
                correct_answer="a"
            )
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output.zip")
            result_path = create_qti_package(questions, output_path, "Test")
            
            with zipfile.ZipFile(result_path, 'r') as zf:
                names = zf.namelist()
                # Should have at least one XML file in a subdirectory
                xml_files = [n for n in names if n.endswith('.xml') and n != 'imsmanifest.xml']
                assert len(xml_files) >= 1
    
    def test_adds_zip_extension_if_missing(self):
        """Test that .zip extension is added if not provided."""
        questions = [
            Question(
                number=1,
                stem="Q1",
                choices=[Choice(letter="a", text="A", is_correct=True)],
                correct_answer="a"
            )
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output")  # No extension
            result_path = create_qti_package(questions, output_path, "Test")
            
            assert result_path.endswith('.zip')
            assert os.path.exists(result_path)
