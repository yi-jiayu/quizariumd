import re

hint_regex = re.compile(r'^Hint:  (.+)$', re.MULTILINE)


def get_question(message):
    return message.split('\n')[2]


def get_hint(message):
    match = hint_regex.search(message)
    if match:
        return match.group(1)
