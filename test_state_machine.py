import asyncio
from state_machine import StateMachine, ChatState
from telethon.errors import ChatWriteForbiddenError
from test_bank import TestBank
from unittest.mock import Mock, MagicMock
from unittest import TestCase


# solution from https://stackoverflow.com/a/51399767¬
# monkey patch MagicMock
async def async_magic():
    pass


MagicMock.__await__ = lambda x: async_magic().__await__()


def mock_event(message):
    event = MagicMock()
    event.to_id.chat_id = 0
    event.message.message = message
    return event


class TestStateMachine(TestCase):
    def test_use_answer_from_test_bank(self):
        event = mock_event('''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]''')
        test_bank = Mock()
        test_bank.get_answer.return_value = 'Hollies'

        state_machine = StateMachine(test_bank=test_bank)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(state_machine.handle(event))
        event.respond.assert_called_with('Hollies')

    def test_save_answer_to_test_bank(self):
        question = 'Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?'
        event = mock_event('''✅ Yes, Hollies!

🏅 Hui Wen Wong +1

📢 Share the wisdom:  FB | TW
⚖ Rate this question:   👍 /good  or   👎 /bad ?''')
        test_bank = Mock()

        state_machine = StateMachine(test_bank=test_bank)
        state_machine.chat_states[0] = ChatState(question, None)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(state_machine.handle(event))
        test_bank.add_question.assert_called_with(question, 'Hollies')

    def test_handle_chat_write_forbidden_error_when_responding_from_test_bank(self):
        event = mock_event('''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]''')
        event.respond.side_effect = ChatWriteForbiddenError(event)
        test_bank = Mock(spec=TestBank)
        test_bank.get_answer.return_value = 'Hollies'

        state_machine = StateMachine(test_bank=test_bank)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(state_machine.handle(event))
