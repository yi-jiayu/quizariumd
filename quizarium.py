import re

hint_regex = re.compile(r'^Hint:  (.+)$', re.MULTILINE)
answer_regex = re.compile(r'^(?:⛔️ Nobody guessed\. The correct answer was ([\w ]+)|✅ Yes, ([\w ]+)!)')


def is_new_question(message):
    return '▶️' in message


def is_game_finished(message: str):
    return message.startswith('🏁')


def get_question(message):
    return message.split('\n')[2]


def get_hint(message):
    match = hint_regex.search(message)
    if match:
        return match.group(1)


def get_answer(message):
    match = answer_regex.search(message)
    if match:
        first, second = match.groups()
        return first or second
