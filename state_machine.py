import logging
import quizarium
import search
from telethon.tl.types import PeerChat, PeerChannel, PeerUser
from typing import Dict


def get_id(peer):
    if isinstance(peer, PeerChat):
        return peer.chat_id
    elif isinstance(peer, PeerChannel):
        return peer.channel_id
    elif isinstance(peer, PeerUser):
        return peer.user_id
    else:
        raise ValueError('invalid peer:', peer)


class ChatState:
    def __init__(self, question, search_results):
        self.question = question
        self.search_results = search_results
        self.answer_attempts = set()


class StateMachine:
    def __init__(self, additional_stopwords=None):
        self.chat_states: Dict[int, ChatState] = {}
        self.additional_stopwords: set = additional_stopwords or set()

    async def handle(self, event):
        message = event.message.message
        if not message:
            return
        chat_id = get_id(event.to_id)

        if quizarium.is_new_question(message):
            question = quizarium.get_question(message)
            logging.info('CHAT_ID=%s getting search results for question: %s', chat_id, question)
            search_results = search.get_search_results(question)
            self.chat_states[chat_id] = ChatState(question, search_results)
            return

        if chat_id not in self.chat_states:
            return
        chat_state = self.chat_states[chat_id]
        hint = quizarium.get_hint(message)
        if not hint:
            return
        logging.info('CHAT_ID=%s got hint: %s', chat_id, hint)
        stopwords = self.additional_stopwords | chat_state.answer_attempts

        candidates = search.evaluate_candidate_answers(chat_state.search_results, hint,
                                                       question=chat_state.question,
                                                       additional_stopwords=stopwords)
        if not candidates:
            return
        logging.info('CHAT_ID=%s got candidate answers: %s', chat_id, candidates)

        answer = search.get_best_match(candidates)
        if answer:
            chat_state.answer_attempts.add(answer)
            logging.info('CHAT_ID=%s replying with answer: %s', chat_id, answer)
            await event.respond(answer.capitalize())
