import asyncio
from state_machine import StateMachine, ChatState
from telethon.errors import ChatWriteForbiddenError
from test_bank import TestBank
from unittest import TestCase
from unittest.mock import Mock


class TestStateMachine(TestCase):
    def test_use_answer_from_test_bank(self):
        message = '''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]'''
        test_bank = Mock()
        test_bank.get_answer.return_value = 'Hollies'

        state_machine = StateMachine(test_bank=test_bank)

        expected = 'Hollies'
        actual = state_machine._handle(message, 0)
        self.assertEqual(expected, actual)

    def test_save_answer_to_test_bank(self):
        question = 'Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?'
        message = '''✅ Yes, Hollies!

🏅 Hui Wen Wong +1

📢 Share the wisdom:  FB | TW
⚖ Rate this question:   👍 /good  or   👎 /bad ?'''
        test_bank = Mock()

        state_machine = StateMachine(test_bank=test_bank)
        state_machine.chat_states[0] = ChatState(question, None)

        state_machine._handle(message, 0)
        test_bank.add_question.assert_called_with(question, 'Hollies')

    def test_handle_chat_write_forbidden_error_when_responding_from_test_bank(self):
        event = Mock()
        event.message.message = '''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]'''
        f = asyncio.Future()
        f.set_result(None)
        event.respond.return_value = f
        event.respond.side_effect = ChatWriteForbiddenError(event)
        test_bank = Mock(spec=TestBank)
        test_bank.get_answer.return_value = 'Hollies'

        state_machine = StateMachine(test_bank=test_bank)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(state_machine.handle(event))
