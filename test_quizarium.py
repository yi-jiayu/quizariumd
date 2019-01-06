import unittest
from quizarium import *


class TestGetAnswer(unittest.TestCase):
    def test_when_guessed_correctly(self):
        message = '''✅ Yes, Hollies!

🏅 Hui Wen Wong +1

📢 Share the wisdom:  FB | TW
⚖ Rate this question:   👍 /good  or   👎 /bad ?'''
        expected = 'Hollies'
        actual = get_answer(message)
        self.assertEqual(expected, actual)

    def test_when_nobody_guessed(self):
        message = '''⛔️ Nobody guessed. The correct answer was Vietnam

📢 Share the wisdom:  FB (https://www.facebook.com/dialog/feed?app_id=444837735034&display=popup&link=https%3A%2F%2Ftelegram.me%2FQuizariumBot&name=%40QuizariumBot%20on%20Telegram&description=Coq%20Bang%20can%20be%20found%20in%20which%20country%20%E2%80%94%20Vietnam.%20Learn%20this%20and%20more%20with%20Telegram%20QuizariumBot!&picture=https%3A%2F%2Fs3.amazonaws.com%2Fon5%2Fqz%2FQ_avatar__.png) | TW (http://twitter.com/share?text=Coq%20Bang%20can%20be%20found%20in%20which%20country%20%E2%80%94%20Vietnam&url=https%3A%2F%2Ftelegram.me%2FQuizariumBot)
⚖️ Rate this question:   👍 /good  or   👎 /bad ?'''
        expected = 'Vietnam'
        actual = get_answer(message)
        self.assertEqual(expected, actual)

    def test_not_an_answer(self):
        message = '''Round 9/10
▶️ QUESTION  [myth]
Agrippa poisoned her husband/uncle who was he
[   ○   ○       ○        ]'''
        expected = None
        actual = get_answer(message)
        self.assertEqual(expected, actual)
