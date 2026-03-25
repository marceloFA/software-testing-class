import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# New tests below:

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_choice_with_empty_text_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)

def test_choice_with_long_text_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

def test_multiple_selections_are_allowed():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', True)
    question.add_choice('c', False)
    assert [
        choice.is_correct for choice in question.choices
        ] == [True, True, False]

def test_above_max_selections_raises_exception():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', True)
    question.add_choice('c', True)
    with pytest.raises(Exception):
        question.correct_selected_choices([1, 2, 3])

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', True)
    question.add_choice('c', False)
    assert question.correct_selected_choices([1, 2]) == [1, 2]
    assert question.correct_selected_choices([1]) == [1]
    assert question.correct_selected_choices([3]) == []

def test_invalid_choice_id_raises_exception():
    question = Question(title='q1')
    choice = question.add_choice('a', True)
    with pytest.raises(Exception):
        question.remove_choice_by_id(choice.id + 999)

def test_remove_choice():
    question = Question(title='q1')
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    question.remove_choice_by_id(choice1.id)
    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_remove_choices_on_an_empty_question():
    question = Question(title='q1')
    question.remove_all_choices()
    assert len(question.choices) == 0
