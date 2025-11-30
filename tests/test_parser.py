"""
Tests for the markdown parser module.
"""
import pytest
from markdown_to_qti.parser import parse_markdown_exam, Question, Choice


class TestParseMarkdownExam:
    """Tests for parse_markdown_exam function."""
    
    def test_single_question_with_correct_answer(self):
        """Test parsing a single question with marked correct answer."""
        markdown = """
1. What is 2 + 2?
   a. 3
   *b. 4
   c. 5
   d. 6
"""
        questions = parse_markdown_exam(markdown)
        
        assert len(questions) == 1
        assert questions[0].number == 1
        assert questions[0].stem == "What is 2 + 2?"
        assert len(questions[0].choices) == 4
        assert questions[0].correct_answer == "b"
        
        # Check choices
        assert questions[0].choices[0].letter == "a"
        assert questions[0].choices[0].text == "3"
        assert not questions[0].choices[0].is_correct
        
        assert questions[0].choices[1].letter == "b"
        assert questions[0].choices[1].text == "4"
        assert questions[0].choices[1].is_correct

    def test_multiple_questions(self):
        """Test parsing multiple questions."""
        markdown = """
1. Question one
   a. A
   *b. B

2. Question two
   *a. A
   b. B
"""
        questions = parse_markdown_exam(markdown)
        
        assert len(questions) == 2
        assert questions[0].number == 1
        assert questions[0].correct_answer == "b"
        assert questions[1].number == 2
        assert questions[1].correct_answer == "a"

    def test_question_with_code_block_in_stem(self):
        """Test parsing a question with a code block in the stem."""
        markdown = """
1. What is the output of the following code?

   ```python
   print("Hello")
   ```

   a. Hello
   *b. "Hello"
   c. Error
"""
        questions = parse_markdown_exam(markdown)
        
        assert len(questions) == 1
        assert "```python" in questions[0].stem
        assert 'print("Hello")' in questions[0].stem
        assert "```" in questions[0].stem
        assert len(questions[0].choices) == 3

    def test_question_with_code_block_in_choice(self):
        """Test parsing a question with code blocks in choices."""
        markdown = """
1. Which function prints to stdout?

   a. Using echo
      ```python
      echo("text")
      ```
   *b. Using print
       ```python
       print("text")
       ```
   c. log("text")
"""
        questions = parse_markdown_exam(markdown)
        
        assert len(questions) == 1
        assert len(questions[0].choices) == 3
        assert "echo" in questions[0].choices[0].text
        assert questions[0].choices[1].is_correct

    def test_question_with_inline_code(self):
        """Test parsing a question with inline code."""
        markdown = """
1. What does `len([1,2,3])` return?
   *a. 3
   b. 6
   c. None
"""
        questions = parse_markdown_exam(markdown)
        
        assert len(questions) == 1
        assert "`len([1,2,3])`" in questions[0].stem

    def test_multiline_question_stem(self):
        """Test parsing a question with a multiline stem."""
        markdown = """
1. Consider the following scenario:
   A user wants to sort a list.
   What method should they use?
   a. list.sort()
   *b. sorted(list)
   c. list.order()
"""
        questions = parse_markdown_exam(markdown)
        
        assert len(questions) == 1
        assert "Consider the following scenario:" in questions[0].stem
        assert "A user wants to sort a list." in questions[0].stem

    def test_no_correct_answer_marked(self):
        """Test parsing when no correct answer is marked."""
        markdown = """
1. A question
   a. Option A
   b. Option B
"""
        questions = parse_markdown_exam(markdown)
        
        assert len(questions) == 1
        assert questions[0].correct_answer is None

    def test_empty_input(self):
        """Test parsing empty input."""
        questions = parse_markdown_exam("")
        assert len(questions) == 0

    def test_no_questions_found(self):
        """Test input without properly formatted questions."""
        markdown = "This is just some text without any questions."
        questions = parse_markdown_exam(markdown)
        assert len(questions) == 0


class TestQuestionDataclass:
    """Tests for the Question dataclass."""
    
    def test_question_creation(self):
        """Test creating a Question object."""
        choices = [
            Choice(letter="a", text="Option A", is_correct=False),
            Choice(letter="b", text="Option B", is_correct=True),
        ]
        question = Question(
            number=1,
            stem="What is the answer?",
            choices=choices,
            correct_answer="b"
        )
        
        assert question.number == 1
        assert question.stem == "What is the answer?"
        assert len(question.choices) == 2
        assert question.correct_answer == "b"


class TestChoiceDataclass:
    """Tests for the Choice dataclass."""
    
    def test_choice_creation(self):
        """Test creating a Choice object."""
        choice = Choice(letter="a", text="Some option", is_correct=True)
        
        assert choice.letter == "a"
        assert choice.text == "Some option"
        assert choice.is_correct is True
    
    def test_choice_default_is_correct(self):
        """Test that is_correct defaults to False."""
        choice = Choice(letter="b", text="Another option")
        
        assert choice.is_correct is False
