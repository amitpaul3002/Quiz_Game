import json
import random
from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'

QUIZ_FILE = os.path.join(os.path.dirname(__file__), 'Quizques.json')

def load_quiz_questions():
    try:
        with open(QUIZ_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['intents'][0]['questions']
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return []

@app.route('/')
def index():
    """Welcome page."""
    return render_template('index.html')

@app.route('/start-quiz')
def start_quiz():
    """Start a new quiz (Play Again also calls this)."""
    # Clear any previous session data
    session.clear()  # This ensures previous results are completely removed

    questions = load_quiz_questions()
    if not questions:
        return "Error: Quiz questions could not be loaded."

    # Shuffle questions and save to session
    session['questions'] = random.sample(questions, len(questions))
    session['current_question_index'] = 0
    session['score'] = 0
    session['total_questions'] = len(questions)

    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = session.get('questions')
    current_index = session.get('current_question_index', 0)
    score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)

    if not questions or current_index >= total_questions:
        return redirect(url_for('results'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        current_question = questions[current_index]

        if user_answer and user_answer.strip().upper() == current_question['answer'].strip().upper():
            session['score'] = score + 1

        session['current_question_index'] = current_index + 1

        if session['current_question_index'] < total_questions:
            return redirect(url_for('quiz'))
        else:
            return redirect(url_for('results'))

    current_question = questions[current_index]
    return render_template(
        'quizmain.html',
        question=current_question['question'],
        options=current_question['options'],
        current_q_num=current_index + 1,
        total_q_num=total_questions
    )

@app.route('/results')
def results():
    final_score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)
    return render_template(
        'quizresult.html',
        score=final_score,
        total=total_questions
    )

if __name__ == '__main__':
    app.run(debug=True)
