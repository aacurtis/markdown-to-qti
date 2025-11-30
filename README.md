# markdown-to-qti

Converts Markdown Exam Files to QTI format for Canvas LMS Import.

## Overview

This Python tool converts multiple-choice exam files written in Markdown format to QTI (Question and Test Interoperability) format, specifically QTI 1.2 compatible with Canvas LMS. It supports code blocks (with syntax highlighting) in both question stems and answer choices.

## Installation

```bash
pip install -e .
```

Or for development:

```bash
pip install -e ".[dev]"
```

## Usage

### Command Line

Convert a Markdown exam file to a QTI package (ZIP file):

```bash
markdown-to-qti exam.md -o exam_qti.zip
```

Options:
- `-o, --output`: Path for the output QTI package (defaults to input filename with .zip extension)
- `-t, --title`: Title for the assessment (default: "Assessment")
- `--xml-only`: Output only the QTI XML to stdout instead of creating a ZIP package

### Markdown Format

The expected Markdown format for questions is:

````markdown
1. Question text here.
This can span multiple lines.
   
```python
# Code blocks are supported
def example():
    return "Hello"
```
   
a. First choice
b. Second choice
*c. Correct answer (marked with asterisk)
d. Fourth choice

2. Another question?
*a. Correct answer
b. Wrong answer
c. Another wrong answer
d. Another wrong answer
````

Key formatting rules:
- Questions start with a number followed by a period (e.g., `1.`)
- Answer choices start with a letter followed by a period (e.g., `a.`, `b.`)
- Mark the correct answer with an asterisk before the letter (e.g., `*c.`)
- Code blocks use standard Markdown fencing (triple backticks)
- Inline code uses single backticks

### Example

See the `examples/sample_quiz.md` file for a complete example.

```bash
markdown-to-qti examples/sample_quiz.md -t "Python Quiz" -o python_quiz.zip
```

### Importing into Canvas

1. Generate the QTI package using this tool
2. In Canvas, go to Settings > Import Course Content
3. Select "QTI .zip file" as the content type
4. Upload the generated ZIP file
5. Click "Import"

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Project Structure

```
markdown-to-qti/
├── src/
│   └── markdown_to_qti/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       ├── parser.py       # Markdown parsing logic
│       └── qti_generator.py # QTI XML generation
├── tests/
│   ├── test_cli.py
│   ├── test_parser.py
│   └── test_qti_generator.py
├── examples/
│   └── sample_quiz.md
├── pyproject.toml
└── README.md
```

## License

MIT License
