from test_bank import *
from unittest import TestCase


class TestTestBank(TestCase):
    def test_add_and_get_question(self):
        test_bank = TestBank(':memory:')
        test_bank.add_question('Pigs can become what – like humans', 'Alcoholics')
        expected = 'Alcoholics'
        actual = test_bank.get_answer('Pigs can become what – like humans')
        self.assertEqual(expected, actual)

    def test_add_same_question(self):
        test_bank = TestBank(':memory:')
        test_bank.add_question('Pigs can become what – like humans', 'Alcoholics')
        test_bank.add_question('Pigs can become what – like humans', 'Alcoholics')

    def test_get_nonexistent_answer(self):
        test_bank = TestBank(':memory:')
        answer = test_bank.get_answer('Pigs can become what – like humans')
        self.assertIsNone(answer)
