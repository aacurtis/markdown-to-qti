"""
Command-line interface for markdown-to-qti converter.
"""
import argparse
import sys
from pathlib import Path

from .parser import parse_markdown_exam
from .qti_generator import create_qti_package, generate_qti_assessment


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown exam files to QTI format for Canvas LMS import.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example markdown format:
  1. What is the output of the following code?
     
     ```python
     print("Hello, World!")
     ```
     
     a. Hello
     b. World
     *c. Hello, World!
     d. Error

  2. Which of these is a Python keyword?
     a. function
     *b. def
     c. method
     d. procedure

Note: Mark the correct answer with an asterisk (*) before the choice letter.
"""
    )
    
    parser.add_argument(
        'input',
        type=str,
        help='Path to the input Markdown file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Path for the output QTI package (ZIP file). Defaults to input filename with .zip extension.'
    )
    
    parser.add_argument(
        '-t', '--title',
        type=str,
        default='Assessment',
        help='Title for the assessment (default: Assessment)'
    )
    
    parser.add_argument(
        '--xml-only',
        action='store_true',
        help='Output only the QTI XML to stdout instead of creating a ZIP package'
    )
    
    args = parser.parse_args()
    
    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except IOError as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse markdown
    questions = parse_markdown_exam(markdown_content)
    
    if not questions:
        print("Error: No questions found in the input file.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(questions)} question(s).", file=sys.stderr)
    
    # Generate output
    if args.xml_only:
        xml_output = generate_qti_assessment(questions, args.title)
        print(xml_output)
    else:
        # Determine output path
        if args.output:
            output_path = args.output
        else:
            output_path = str(input_path.with_suffix('.zip'))
        
        try:
            result_path = create_qti_package(questions, output_path, args.title)
            print(f"QTI package created: {result_path}", file=sys.stderr)
        except IOError as e:
            print(f"Error creating output file: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
