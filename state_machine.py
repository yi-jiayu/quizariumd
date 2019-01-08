import logging
import quizarium
import search
from telethon.errors import ChatWriteForbiddenError
from typing import Dict


def get_id(peer):
    if hasattr(peer, 'chat_id'):
        return peer.chat_id
    elif hasattr(peer, 'channel_id'):
        return peer.channel_id
    elif hasattr(peer, 'user_id'):
        return peer.user_id
    else:
        raise ValueError('invalid peer:', peer)


class ChatState:
    def __init__(self, question, search_results):
        self.question = question
        self.search_results = search_results
        self.answer_attempts = set()


class StateMachine:
    def __init__(self, test_bank=None):
        self.chat_states: Dict[int, ChatState] = {}
        self.test_bank = test_bank

    async def handle(self, event):
        message = event.message.message
        if not message:
            return
        chat_id = get_id(event.to_id)
        try:
            await self._handle(event, message, chat_id)
        except ChatWriteForbiddenError:
            logging.info('CHAT_ID=%s chat write forbidden', chat_id)

    async def _handle(self, event, message, chat_id):
        if quizarium.is_new_question(message):
            question = quizarium.get_question(message)
            logging.info('CHAT_ID=%s got question: %s', chat_id, question)

            if self.test_bank:
                answer = self.test_bank.get_answer(question)
                if answer:
                    logging.info('CHAT_ID=%s responding with answer from test bank: %s', chat_id, answer)
                    return await event.respond(answer)

            search_results = search.get_search_results(question)
            self.chat_states[chat_id] = ChatState(question, search_results)
            return

        if chat_id not in self.chat_states:
            return
        chat_state = self.chat_states[chat_id]

        hint = quizarium.get_hint(message)
        if hint:
            logging.info('CHAT_ID=%s got hint: %s', chat_id, hint)
            candidates = search.evaluate_candidate_answers(chat_state.search_results, hint,
                                                           question=chat_state.question,
                                                           additional_stopwords=chat_state.answer_attempts)
            logging.info('CHAT_ID=%s got candidate answers: %s', chat_id, candidates)
            if not candidates:
                return

            answer = search.get_best_match(candidates)
            if answer:
                chat_state.answer_attempts.add(answer)
                logging.info('CHAT_ID=%s replying with answer: %s', chat_id, answer)
                return await event.respond(answer.capitalize())
            return

        answer = quizarium.get_answer(message)
        if answer:
            logging.info('CHAT_ID=%s got answer: Q: %s A: %s', chat_id, chat_state.question, answer)
            if self.test_bank:
                self.test_bank.add_question(chat_state.question, answer)
