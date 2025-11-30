"""
Tests for the CLI module.
"""
import os
import sys
import tempfile
import pytest
from unittest.mock import patch

from markdown_to_qti.cli import main


class TestCli:
    """Tests for the command-line interface."""
    
    def test_help_option(self):
        """Test that --help works."""
        with patch.object(sys, 'argv', ['markdown-to-qti', '--help']):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 0
    
    def test_missing_input_file(self):
        """Test error handling for missing input file."""
        with patch.object(sys, 'argv', ['markdown-to-qti', 'nonexistent.md']):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 1
    
    def test_converts_markdown_to_qti_package(self):
        """Test converting a markdown file to QTI package."""
        markdown_content = """
1. What is 2 + 2?
   a. 3
   *b. 4
   c. 5
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "test.md")
            output_path = os.path.join(tmpdir, "test.zip")
            
            with open(input_path, 'w') as f:
                f.write(markdown_content)
            
            with patch.object(sys, 'argv', ['markdown-to-qti', input_path, '-o', output_path]):
                main()
            
            assert os.path.exists(output_path)
    
    def test_xml_only_option(self, capsys):
        """Test the --xml-only option."""
        markdown_content = """
1. Test question
   *a. Correct
   b. Wrong
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "test.md")
            
            with open(input_path, 'w') as f:
                f.write(markdown_content)
            
            with patch.object(sys, 'argv', ['markdown-to-qti', input_path, '--xml-only']):
                main()
            
            captured = capsys.readouterr()
            assert '<?xml' in captured.out
            assert 'questestinterop' in captured.out
    
    def test_custom_title(self):
        """Test setting a custom assessment title."""
        markdown_content = """
1. Q1
   *a. A
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "test.md")
            
            with open(input_path, 'w') as f:
                f.write(markdown_content)
            
            with patch.object(sys, 'argv', ['markdown-to-qti', input_path, '--xml-only', '-t', 'My Custom Title']):
                main()
                # If we get here without error, the title option worked
    
    def test_no_questions_error(self, capsys):
        """Test error when no questions are found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "test.md")
            
            with open(input_path, 'w') as f:
                f.write("No questions here")
            
            with patch.object(sys, 'argv', ['markdown-to-qti', input_path]):
                with pytest.raises(SystemExit) as excinfo:
                    main()
                assert excinfo.value.code == 1
