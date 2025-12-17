from config.db import get_db_compat

class Question:
    def __init__(self, subject, topic, question_text, options, correct_answer, difficulty='medium', explanation=''):
        self.subject = subject  # 'aptitude', 'technical'
        self.topic = topic
        self.question_text = question_text
        self.options = options  # list of 4 options
        self.correct_answer = correct_answer  # index of correct option (0-3)
        self.difficulty = difficulty  # 'easy', 'medium', 'hard'
        self.explanation = explanation

    def save(self):
        db = get_db_compat()
        question_data = {
            'subject': self.subject,
            'topic': self.topic,
            'question_text': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'difficulty': self.difficulty,
            'explanation': self.explanation
        }
        result = db.users.insert_one(question_data)  # Using users collection for simplicity
        return str(result.inserted_id)

    @staticmethod
    def find_by_subject_topic(subject, topic, limit=10):
        db = get_db_compat()
        return list(db.users.find({'subject': subject, 'topic': topic}).limit(limit))

    @staticmethod
    def find_by_subject(subject, limit=10):
        db = get_db_compat()
        return list(db.users.find({'subject': subject}).limit(limit))

class UserResult:
    def __init__(self, user_id, subject, topic, score, total_questions, time_taken, answers):
        self.user_id = user_id
        self.subject = subject
        self.topic = topic
        self.score = score
        self.total_questions = total_questions
        self.time_taken = time_taken
        self.answers = answers  # list of user's answers

    def save(self):
        db = get_db_compat()
        result_data = {
            'user_id': self.user_id,
            'subject': self.subject,
            'topic': self.topic,
            'score': self.score,
            'total_questions': self.total_questions,
            'time_taken': self.time_taken,
            'answers': self.answers,
            'timestamp': '2025-01-01T00:00:00Z'  # placeholder
        }
        result = db.users.insert_one(result_data)
        return str(result.inserted_id)
