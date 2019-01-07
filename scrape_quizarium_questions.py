import asyncio
import quizarium
import toml
from telethon import TelegramClient
from test_bank import TestBank

QUIZARIUM_USER_ID = 155670507
CHECKPOINT_FILE = '.scrape_offset'

# use your own values here
target_chat_id = 0
test_bank_file = 'questions.sqlite'
config_file = 'quizarium.toml'

test_bank = TestBank(test_bank_file)

config = toml.load(config_file)

telegram_config = config['telegram']
session = telegram_config['session_file'] or telegram_config['username']
api_id = telegram_config['api_id']
api_hash = telegram_config['api_hash']
phone = telegram_config['phone']
password = telegram_config['password']


def get_last_offset():
    try:
        with open(CHECKPOINT_FILE) as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


def save_offset(offset):
    with open(CHECKPOINT_FILE, 'w') as f:
        print(offset, file=f)


async def main():
    question = None
    async with TelegramClient(session, api_id, api_hash) as client:
        offset = get_last_offset()
        count = 0
        it = client.iter_messages(target_chat_id,
                                  limit=None,
                                  offset_id=offset,
                                  from_user=QUIZARIUM_USER_ID,
                                  reverse=True)
        async for message in it:
            text = message.message
            if not text:
                continue

            if quizarium.is_new_question(text):
                question = quizarium.get_question(text)
            elif quizarium.is_game_finished(text):
                question = None
            else:
                answer = quizarium.get_answer(text)
                if question and answer:
                    print(f'{count}\t{message.id}\tQ: {question} A: {answer}')
                    test_bank.add_question(question, answer)

            if count % 100 == 0:
                save_offset(message.id)
                print('---\nSaved offset\n---')
            count += 1


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
