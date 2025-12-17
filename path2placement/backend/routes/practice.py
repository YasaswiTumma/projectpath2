from flask import Blueprint, request, jsonify
from models.question import Question, UserResult
from middleware.auth import token_required
import random

practice_bp = Blueprint('practice', __name__)

# Sample aptitude questions
SAMPLE_APTITUDE_QUESTIONS = [
    {
        'subject': 'aptitude',
        'topic': 'quantitative',
        'question_text': 'If a train travels 120 km in 2 hours, what is its speed in km/h?',
        'options': ['60', '50', '40', '30'],
        'correct_answer': 0,
        'difficulty': 'easy',
        'explanation': 'Speed = Distance/Time = 120 km / 2 hours = 60 km/h'
    },
    {
        'subject': 'aptitude',
        'topic': 'logical',
        'question_text': 'Find the next number in the sequence: 2, 4, 8, 16, ?',
        'options': ['24', '32', '28', '20'],
        'correct_answer': 1,
        'difficulty': 'easy',
        'explanation': 'Each number is double the previous: 2×2=4, 4×2=8, 8×2=16, 16×2=32'
    },
    {
        'subject': 'aptitude',
        'topic': 'verbal',
        'question_text': 'Choose the synonym of "Benevolent":',
        'options': ['Kind', 'Angry', 'Sad', 'Tired'],
        'correct_answer': 0,
        'difficulty': 'medium',
        'explanation': 'Benevolent means well-meaning and kind, which is closest to "Kind"'
    }
]

SAMPLE_TECHNICAL_QUESTIONS = [
    {
        'subject': 'technical',
        'topic': 'python',
        'question_text': 'What is the output of: print(2 ** 3)',
        'options': ['6', '8', '9', '16'],
        'correct_answer': 1,
        'difficulty': 'easy',
        'explanation': '** is the exponentiation operator in Python: 2^3 = 8'
    },
    {
        'subject': 'technical',
        'topic': 'java',
        'question_text': 'Which keyword is used to define a class in Java?',
        'options': ['function', 'class', 'def', 'void'],
        'correct_answer': 1,
        'difficulty': 'easy',
        'explanation': 'In Java, classes are defined using the "class" keyword'
    }
]

@practice_bp.route('/questions/<subject>', methods=['GET'])
@token_required
def get_questions(current_user, subject):
    topic = request.args.get('topic')
    limit = int(request.args.get('limit', 10))

    if subject == 'aptitude':
        questions = SAMPLE_APTITUDE_QUESTIONS
    elif subject == 'technical':
        questions = SAMPLE_TECHNICAL_QUESTIONS
    else:
        return jsonify({'message': 'Invalid subject'}), 400

    if topic:
        questions = [q for q in questions if q['topic'] == topic]

    # Shuffle and limit questions
    random.shuffle(questions)
    questions = questions[:limit]

    return jsonify({'questions': questions})

@practice_bp.route('/submit-result', methods=['POST'])
@token_required
def submit_result(current_user):
    data = request.get_json()
    subject = data.get('subject')
    topic = data.get('topic', '')
    score = data.get('score')
    total_questions = data.get('total_questions')
    time_taken = data.get('time_taken')
    answers = data.get('answers', [])

    if not all([subject, score is not None, total_questions]):
        return jsonify({'message': 'Missing required fields'}), 400

    result = UserResult(
        user_id=current_user['_id'],
        subject=subject,
        topic=topic,
        score=score,
        total_questions=total_questions,
        time_taken=time_taken,
        answers=answers
    )
    result.save()

    return jsonify({'message': 'Result saved successfully'})

@practice_bp.route('/leaderboard', methods=['GET'])
@token_required
def get_leaderboard(current_user):
    # Mock leaderboard data - in real app, this would aggregate from UserResult
    leaderboard = [
        {'name': 'Alice Johnson', 'score': 85, 'rank': 1},
        {'name': 'Bob Smith', 'score': 82, 'rank': 2},
        {'name': 'Charlie Brown', 'score': 78, 'rank': 3},
        {'name': 'Diana Prince', 'score': 75, 'rank': 4},
        {'name': 'Eve Wilson', 'score': 72, 'rank': 5}
    ]
    return jsonify({'leaderboard': leaderboard})

@practice_bp.route('/user-stats', methods=['GET'])
@token_required
def get_user_stats(current_user):
    # Mock user statistics - in real app, this would calculate from UserResult
    stats = {
        'total_tests': 12,
        'average_score': 78,
        'best_score': 95,
        'total_time': 3600,  # seconds
        'subject_breakdown': {
            'aptitude': {'attempted': 8, 'average': 82},
            'technical': {'attempted': 4, 'average': 70}
        }
    }
    return jsonify({'stats': stats})
