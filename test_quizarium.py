import unittest
from quizarium import *


class TestIsNewQuestion(unittest.TestCase):
    def test_new_question(self):
        message = '''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]'''
        actual = is_new_question(message)
        self.assertTrue(actual)

    def test_not_new_question1(self):
        message = '''Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
Hint:  _ _ _ _ _ _ _
[••••   ○       ○        ]'''
        actual = is_new_question(message)
        self.assertFalse(actual)

    def test_not_new_question2(self):
        message = '''🐱🚀🌕 We (Quizarium devs) released a new iOS and Android puzzle game Catomic where cats go to space and colonize Mars. Check it out!
 🍏 App Store | 🤖 Google Play | 📲 catomic.on-5.com'''
        actual = is_new_question(message)
        self.assertFalse(actual)

    def test_not_new_question3(self):
        message = '''✅ Yes, Hollies!

🏅 Hui Wen Wong +1

📢 Share the wisdom:  FB | TW
⚖ Rate this question:   👍 /good  or   👎 /bad ?'''
        actual = is_new_question(message)
        self.assertFalse(actual)


class TestIsGameFinished(unittest.TestCase):
    def test_game_finished1(self):
        message = '''🏁 And the winners are:
  🏆 Jiayu   40 points (answers: 10)


If you enjoy the game please rate our bot: https://telegram.me/storebot?start=QuizariumBot'''
        finished = is_game_finished(message)
        self.assertTrue(finished)

    def test_game_finished2(self):
        message = '''🏁 Weirdly, nobody won. On the bright side, nobody lost either!

If you enjoy the game please rate our bot: https://telegram.me/storebot?start=QuizariumBot'''
        finished = is_game_finished(message)
        self.assertTrue(finished)

    def test_not_game_finished1(self):
        message = '''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]'''
        finished = is_game_finished(message)
        self.assertFalse(finished)

    def test_not_game_finished2(self):
        message = '''Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
Hint:  _ _ _ _ _ _ _
[••••   ○       ○        ]'''
        finished = is_game_finished(message)
        self.assertFalse(finished)

    def test_not_game_finished3(self):
        message = '''🐱🚀🌕 We (Quizarium devs) released a new iOS and Android puzzle game Catomic where cats go to space and colonize Mars. Check it out!
 🍏 App Store | 🤖 Google Play | 📲 catomic.on-5.com'''
        finished = is_game_finished(message)
        self.assertFalse(finished)

    def test_not_game_finished4(self):
        message = '''✅ Yes, Hollies!

🏅 Hui Wen Wong +1

📢 Share the wisdom:  FB | TW
⚖ Rate this question:   👍 /good  or   👎 /bad ?'''
        finished = is_game_finished(message)
        self.assertFalse(finished)


class TestGetQuestion(unittest.TestCase):
    def test_when_question_first_appears(self):
        message = '''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]'''
        expected = 'Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?'
        actual = get_question(message)
        self.assertEqual(expected, actual)

    def test_when_question_first_appears_without_round(self):
        message = '''▶️ QUESTION  [music]
What composer was working on his 10th symphony at the time of his death?
[   ○   ○       ○        ]'''
        expected = 'What composer was working on his 10th symphony at the time of his death?'
        actual = get_question(message)
        self.assertEqual(expected, actual)


class TestGetHint(unittest.TestCase):
    def test_when_hint_not_given_yet(self):
        message = '''Round 7/10
▶️ QUESTION  [Music Bands]
Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
[   ○   ○       ○        ]'''
        expected = None
        actual = get_hint(message)
        self.assertEqual(expected, actual)

    def test_when_hint_given1(self):
        message = '''Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
Hint:  _ _ _ _ _ _ _
[••••   ○       ○        ]'''
        expected = '_ _ _ _ _ _ _'
        actual = get_hint(message)
        self.assertEqual(expected, actual)

    def test_when_hint_given2(self):
        message = '''Name the 60s band from Manchester who had a hit with a song called "Jennifer Eccles"?
Hint:  H _ _ l _ _ _
[••••••••       ○        ]'''
        expected = 'H _ _ l _ _ _'
        actual = get_hint(message)
        self.assertEqual(expected, actual)

    def test_when_no_hint(self):
        message = '''🐱🚀🌕 We (Quizarium devs) released a new iOS and Android puzzle game Catomic where cats go to space and colonize Mars. Check it out!
 🍏 App Store | 🤖 Google Play | 📲 catomic.on-5.com'''
        expected = None
        actual = get_hint(message)
        self.assertEqual(expected, actual)


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
