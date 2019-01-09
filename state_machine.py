import logging
import quizarium
import random
import search
from dataclasses import dataclass, field
from telethon.errors import ChatWriteForbiddenError
from typing import Dict, List, Set


def get_id(peer):
    """Returns the integer ID of a Telethon peer."""
    if hasattr(peer, 'chat_id'):
        return peer.chat_id
    elif hasattr(peer, 'channel_id'):
        return peer.channel_id
    elif hasattr(peer, 'user_id'):
        return peer.user_id
    else:
        raise ValueError('invalid peer:', peer)


@dataclass
class ChatState:
    question: str
    search_results: List[str] = field(default_factory=list)
    answer_attempts: Set[str] = field(default_factory=set)
    skip_question: bool = False


class StateMachine:
    def __init__(self, test_bank=None, try_answer_probability=1.0, use_test_bank_probability=1.0,
                 use_candidate_answer_probability=1.0, random=random.random):
        self._search = search

        self.chat_states: Dict[int, ChatState] = {}
        self.test_bank = test_bank

        self.try_answer_probability = try_answer_probability
        self.use_test_bank_probability = use_test_bank_probability
        self.use_candidate_answer_probability = use_candidate_answer_probability

        self.random = random

    async def handle(self, event):
        message = event.message.message
        if not message:
            return
        chat_id = get_id(event.to_id)
        answer = self._handle(chat_id, message)
        if answer:
            try:
                await event.respond(answer)
            except ChatWriteForbiddenError:
                logging.info('CHAT_ID=%s chat write forbidden', chat_id)

    def _handle_new_question(self, chat_id, question):
        logging.info('CHAT_ID=%s got question: %s', chat_id, question)
        try_answer = self.random() < self.try_answer_probability
        if not try_answer:
            self.chat_states[chat_id] = ChatState(question, skip_question=True)
            return

        if self.test_bank:
            use_test_bank = self.random() < self.use_test_bank_probability
            if use_test_bank:
                answer = self.test_bank.get_answer(question)
                if answer:
                    logging.info('CHAT_ID=%s responding with answer from test bank: %s', chat_id, answer)
                    return answer

        search_results = self._search.get_search_results(question)
        self.chat_states[chat_id] = ChatState(question, search_results=search_results)
        return

    def _handle_answer(self, chat_id, chat_state, answer):
        logging.info('CHAT_ID=%s got answer: Q: %s A: %s', chat_id, chat_state.question, answer)
        if self.test_bank:
            self.test_bank.add_question(chat_state.question, answer)
        return

    def _handle_hint(self, chat_id, chat_state, hint):
        logging.info('CHAT_ID=%s got hint: %s', chat_id, hint)
        candidates = self._search.evaluate_candidate_answers(chat_state.search_results, hint,
                                                             question=chat_state.question,
                                                             additional_stopwords=chat_state.answer_attempts)
        logging.info('CHAT_ID=%s got candidate answers: %s', chat_id, candidates)
        if not candidates:
            return

        answer = self._search.get_best_match(candidates)
        use_candidate_answer = self.random() < self.use_candidate_answer_probability
        if answer and use_candidate_answer:
            chat_state.answer_attempts.add(answer)
            logging.info('CHAT_ID=%s replying with answer: %s', chat_id, answer)
            return answer.capitalize()

    def _handle(self, chat_id, message):
        if quizarium.is_new_question(message):
            question = quizarium.get_question(message)
            return self._handle_new_question(chat_id, question)

        chat_state = self.chat_states.get(chat_id, None)
        if not chat_state:
            return

        answer = quizarium.get_answer(message)
        if answer:
            return self._handle_answer(chat_id, chat_state, answer)

        if chat_state.skip_question:
            return

        hint = quizarium.get_hint(message)
        if hint:
            return self._handle_hint(chat_id, chat_state, hint)
