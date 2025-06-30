import json
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# Set a secret key for session management.
# In a production environment, use a strong, randomly generated key from environment variables.
app.secret_key = 'your_super_secret_key_here'

# Path to your quiz questions JSON file
# Make sure 'Quiz.json' is in the same directory as this 'app.py' file,
# or provide the full path if it's elsewhere.
QUIZ_FILE = 'Quizques.json'

def load_quiz_questions():
    """Loads quiz questions from the JSON file."""
    try:
        with open(QUIZ_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Assuming the structure is intents -> first intent -> questions
            return data['intents'][0]['questions']
    except FileNotFoundError:
        print(f"Error: {QUIZ_FILE} not found. Please ensure it's in the correct directory.")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing {QUIZ_FILE}: {e}. Please check the JSON format.")
        return []

@app.route('/')
def index():
    """
    Handles the home page, initializes or restarts the quiz.
    """
    questions = load_quiz_questions()
    if not questions:
        return "Error: Quiz questions could not be loaded. Please check Quiz.json."

    # Shuffle questions and reset quiz state in session
    session['questions'] = random.sample(questions, len(questions)) # Use random.sample for a new shuffled list
    session['current_question_index'] = 0
    session['score'] = 0
    session['total_questions'] = len(session['questions'])

    # Redirect to the quiz route to display the first question
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    Handles displaying questions and processing answers.
    """
    questions = session.get('questions')
    current_index = session.get('current_question_index', 0)
    score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)

    # If no questions or index is out of bounds, redirect to results or home
    if not questions or current_index >= total_questions:
        return redirect(url_for('results'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        current_question = questions[current_index]

        if user_answer and user_answer.strip().upper() == current_question['answer'].strip().upper():
            session['score'] = score + 1
            
        session['current_question_index'] = current_index + 1

        # Check if there are more questions
        if session['current_question_index'] < total_questions:
            return redirect(url_for('quiz'))
        else:
            # No more questions, show results
            return redirect(url_for('results'))

    # GET request: display the current question
    current_question = questions[current_index]
    return render_template('Quizindex.html',
                           question=current_question['question'],
                           options=current_question['options'],
                           current_q_num=current_index + 1,
                           total_q_num=total_questions)

@app.route('/results')
def results():
    """
    Displays the final quiz results.
    """
    final_score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)
    return render_template('quizresult.html', score=final_score, total=total_questions)

if __name__ == '__main__':
    # To run: python app.py
    # Then open your browser to http://127.0.0.1:5000/
    app.run(debug=True) # debug=True enables auto-reloading and better error messages
