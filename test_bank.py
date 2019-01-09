import sqlite3


class TestBank:
    __test__ = False  # prevent this class from being treated as test (since it starts with Test*)

    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        with self.conn as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS questions (question text, answer text)''')
            cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS questions_question_index ON questions(question)')

    def add_question(self, question, answer):
        with self.conn as cursor:
            cursor.execute('INSERT OR IGNORE INTO questions VALUES (?, ?)', (question, answer))

    def get_answer(self, question):
        cursor = self.conn.cursor()
        cursor.execute('select answer from questions where question = ?', (question,))
        result = cursor.fetchone()
        if result:
            return result[0]
