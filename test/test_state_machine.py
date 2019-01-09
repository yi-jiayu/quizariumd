import pytest
from state_machine import StateMachine
from test_bank import TestBank
from unittest.mock import Mock

question = 'Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?'
answer = 'Hollies'
hint = '_ _ _ _ _ _ _'
new_question_message = '''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]'''
hint_message = '''Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
Hint:  _ _ _ _ _ _ _
[••••   ○       ○        ]'''
answer_message = '''✅ Yes, Hollies!

🏅 Hui Wen Wong +1

📢 Share the wisdom:  FB | TW
⚖ Rate this question:   👍 /good  or   👎 /bad ?'''


class TestHandleNewQuestion:
    def test_without_test_bank(self):
        state_machine = StateMachine()
        search = Mock()
        state_machine._search = search

        response = state_machine._handle(0, new_question_message)

        assert response is None
        search.get_search_results.assert_called_with(question)

    def test_using_answer_from_test_bank(self):
        test_bank = Mock(spec=TestBank)
        test_bank.get_answer.return_value = 'Hollies'
        search = Mock()
        state_machine = StateMachine(test_bank=test_bank)
        state_machine._search = search

        response = state_machine._handle(0, new_question_message)

        assert response == 'Hollies'
        search.get_search_results.assert_not_called()
        test_bank.get_answer.assert_called_with(question)

    @pytest.mark.parametrize('random_value', [0, 0.999])
    def test_try_answer_probability_one(self, random_value):
        """When test_bank is None and try_answer_probability is set to 1, _search.get_search_results should be called
        no matter the value returned by random."""
        search = Mock()
        random = Mock(return_value=random_value)
        state_machine = StateMachine(try_answer_probability=1, random=random)
        state_machine._search = search

        response = state_machine._handle(0, new_question_message)

        assert response is None
        search.get_search_results.assert_called_with(question)

    @pytest.mark.parametrize('random_value', [0, 0.999])
    def test_try_answer_probability_zero(self, random_value):
        """When test_bank is None and try_answer_probability is set to 0, _search.get_search_results should not be
        called no matter the value returned by random."""
        search = Mock()
        random = Mock(return_value=random_value)
        state_machine = StateMachine(try_answer_probability=0, random=random)
        state_machine._search = search

        response = state_machine._handle(0, new_question_message)

        assert response is None
        search.get_search_results.assert_not_called()

    @pytest.mark.parametrize('random_value', [0, 0.999])
    def test_use_test_bank_probability_one(self, random_value):
        """When answer is available in test bank and use_test_bank_probability is set to 1, the answer should be looked
        up and returned from the test bank and no search request should be made no matter the value returned
        by random."""
        search = Mock()
        test_bank = Mock(TestBank)
        test_bank.get_answer.return_value = answer
        random = Mock(return_value=random_value)
        state_machine = StateMachine(test_bank=test_bank, use_test_bank_probability=1, random=random)
        state_machine._search = search

        response = state_machine._handle(0, new_question_message)

        assert response == answer
        search.get_search_results.assert_not_called()
        test_bank.get_answer.assert_called_with(question)

    @pytest.mark.parametrize('random_value', [0, 0.999])
    def test_use_test_bank_probability_zero(self, random_value):
        """When answer is available in test bank but use_test_bank_probability is set to 0, the answer should not be
        looked up from the test bank and a search request should still be made no matter the value returned
        by random."""
        search = Mock()
        test_bank = Mock(TestBank)
        test_bank.get_answer.return_value = answer
        random = Mock(return_value=random_value)
        state_machine = StateMachine(test_bank=test_bank, use_test_bank_probability=0, random=random)
        state_machine._search = search

        response = state_machine._handle(0, new_question_message)

        assert response is None
        test_bank.get_answer.assert_not_called()
        search.get_search_results.assert_called_with(question)


class TestHandleAnswer:
    def test_handle_answer_before_question(self):
        """When have not encountered any question but receive a message containing an answer, we should do nothing."""
        search = Mock()
        test_bank = Mock(TestBank)
        state_machine = StateMachine(test_bank=test_bank)
        state_machine._search = search

        response = state_machine._handle(0, answer_message)

        assert response is None
        search.get_search_results.assert_not_called()
        test_bank.get_answer.assert_not_called()
        test_bank.add_question.assert_not_called()

    def test_handle_answer_after_question(self):
        """When we have previously received a new question and then receive a message containing an answer, we should
        add the question and answer to the test bank."""
        search = Mock()
        test_bank = Mock(TestBank)
        test_bank.get_answer.return_value = None
        state_machine = StateMachine(test_bank=test_bank)
        state_machine._search = search

        state_machine._handle(0, new_question_message)
        response = state_machine._handle(0, answer_message)

        assert response is None
        test_bank.add_question.assert_called_with(question, answer)


class TestHandleHintMessage:
    def test_handle_hint_before_question(self):
        """If we encounter a question with a hint without receiving the question as a new question,
        we should ignore it."""
        search = Mock()
        state_machine = StateMachine()
        state_machine._search = search

        response = state_machine._handle(0, hint_message)

        assert response is None
        search.evaluate_candidate_answers.assert_not_called()
        search.get_best_batch.assert_not_called()

    def test_handle_hint_after_question(self):
        """If we encounter a question with a hint after receiving the question as a new question,
        we should try to evaluate and choose the best candidate answer.."""
        search = Mock()
        search.get_best_match.return_value = 'Poppies'
        state_machine = StateMachine()
        state_machine._search = search

        state_machine._handle(0, new_question_message)
        response = state_machine._handle(0, hint_message)

        assert response == 'Poppies'

    @pytest.mark.parametrize('random_value', [0, 0.999])
    def test_handle_hint_try_answer_probability_zero(self, random_value):
        """When try_answer_probability is zero, we should not try to answer at all."""
        random = Mock(return_value=random_value)
        search = Mock()
        search.get_best_match.return_value = 'Poppies'
        state_machine = StateMachine(try_answer_probability=0, random=random)
        state_machine._search = search

        state_machine._handle(0, new_question_message)
        response = state_machine._handle(0, hint_message)

        assert response is None

    @pytest.mark.parametrize('random_value', [0, 0.999])
    def test_handle_hint_try_answer_probability_one(self, random_value):
        """When try_answer_probability is one, we should always answer when we have a best candidate answer."""
        random = Mock(return_value=random_value)
        search = Mock()
        search.get_best_match.return_value = 'Poppies'
        state_machine = StateMachine(try_answer_probability=1, random=random)
        state_machine._search = search

        state_machine._handle(0, new_question_message)
        response = state_machine._handle(0, hint_message)

        assert response == 'Poppies'
