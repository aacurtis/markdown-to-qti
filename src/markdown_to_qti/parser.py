"""
Parser module for converting Markdown exam questions to structured data.
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Choice:
    """Represents a single answer choice."""
    letter: str
    text: str
    is_correct: bool = False


@dataclass
class Question:
    """Represents a single multiple-choice question."""
    number: int
    stem: str
    choices: List[Choice] = field(default_factory=list)
    correct_answer: Optional[str] = None


def _update_code_block_state(text: str, in_code_block: bool) -> bool:
    """
    Update the code block state based on fence markers in the text.
    
    Args:
        text: The text to check for fence markers.
        in_code_block: Current code block state.
        
    Returns:
        Updated code block state (True if inside a code block).
    """
    # Count fence markers in the text
    fence_count = text.count('```')
    # Each pair of markers toggles in and out, so odd count means state changes
    if fence_count % 2 == 1:
        return not in_code_block
    return in_code_block


def parse_markdown_exam(markdown_content: str) -> List[Question]:
    """
    Parse a markdown exam file and extract questions.
    
    Expected format:
    1. Question text here
       May span multiple lines and include code blocks.
       
       ```python
       def example():
           pass
       ```
       
       a. Choice A text
       b. Choice B text
       *c. Correct choice (marked with asterisk)
       d. Choice D text
    
    Args:
        markdown_content: The markdown content to parse.
        
    Returns:
        A list of Question objects.
    """
    questions = []
    
    # Split content into question blocks
    # Questions start with a number followed by a period
    question_pattern = r'(?:^|\n)(\d+)\.\s+'
    
    # Find all question starts
    matches = list(re.finditer(question_pattern, markdown_content))
    
    for i, match in enumerate(matches):
        question_num = int(match.group(1))
        start_pos = match.end()
        
        # Find end of this question (start of next question or end of content)
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(markdown_content)
        
        question_text = markdown_content[start_pos:end_pos].strip()
        
        # Parse the question
        question = _parse_question_block(question_num, question_text)
        if question:
            questions.append(question)
    
    return questions


def _parse_question_block(question_num: int, text: str) -> Optional[Question]:
    """
    Parse a single question block into a Question object.
    
    Args:
        question_num: The question number.
        text: The text content of the question (stem + choices).
        
    Returns:
        A Question object or None if parsing fails.
    """
    # Pattern to match answer choices (a., b., c., etc. or *a., *b., etc.)
    # Must handle multi-line choices that may contain code blocks
    # Allows optional leading whitespace
    # Uses (?:\s+|$) to match either whitespace after period or end-of-line,
    # enabling choices like "*a.\n```python" where code block is on next line
    choice_pattern = r'^\s*(\*?)([a-zA-Z])\.(?:\s+|$)'
    
    lines = text.split('\n')
    stem_lines = []
    choices = []
    current_choice = None
    current_choice_lines = []
    in_code_block = False
    
    for line in lines:
        # Check if this line starts a new choice (only when not in code block)
        choice_match = re.match(choice_pattern, line) if not in_code_block else None
        
        if choice_match:
            # Save previous choice if any
            if current_choice is not None:
                choice_text = '\n'.join(current_choice_lines).strip()
                choices.append(Choice(
                    letter=current_choice[0],
                    text=choice_text,
                    is_correct=current_choice[1]
                ))
            
            # Start new choice
            is_correct = choice_match.group(1) == '*'
            letter = choice_match.group(2).lower()
            remainder = line[choice_match.end():].strip()
            current_choice = (letter, is_correct)
            current_choice_lines = [remainder] if remainder else []
            
            # Update code block state based on fence markers in remainder
            in_code_block = _update_code_block_state(remainder, in_code_block)
        elif current_choice is not None:
            # Continue current choice
            current_choice_lines.append(line)
            # Track code blocks in choice content
            in_code_block = _update_code_block_state(line, in_code_block)
        else:
            # Still in question stem
            stem_lines.append(line)
            # Track code blocks in stem
            in_code_block = _update_code_block_state(line, in_code_block)
    
    # Don't forget the last choice
    if current_choice is not None:
        choice_text = '\n'.join(current_choice_lines).strip()
        choices.append(Choice(
            letter=current_choice[0],
            text=choice_text,
            is_correct=current_choice[1]
        ))
    
    if not choices:
        return None
    
    # Find correct answer
    correct_answer = None
    for choice in choices:
        if choice.is_correct:
            correct_answer = choice.letter
            break
    
    return Question(
        number=question_num,
        stem='\n'.join(stem_lines).strip(),
        choices=choices,
        correct_answer=correct_answer
    )
