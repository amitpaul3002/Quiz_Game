# Quiz_Game
Flask Quiz Game

A simple web-based quiz application built using Flask (Python).
The app loads multiple-choice questions from a JSON file, presents them randomly to the user, tracks the score, and displays the final result.

Features

Loads quiz questions dynamically from Quizques.json

Shuffles questions on every new quiz session

Simple multiple-choice interface

Tracks score during the quiz

Displays results at the end

Project Structure
project_folder/
│
├─ app.py               # Main Flask application
├─ Quizques.json        # Quiz questions file
└─ templates/
   ├─ Quizindex.html     # Template to display quiz questions
   └─ results.html       # Template to display results

Requirements

Python 3.8 or higher

Flask

Install dependencies using:

pip install flask

How to Run

Clone or download this repository

Place Quizques.json in the same folder as app.py

Make sure your templates folder contains Quizindex.html and results.html

Start the Flask app:

python app.py


Open your browser and visit:

http://127.0.0.1:5000/

Quiz Questions JSON Format

The JSON file must have this structure:

{
    "intents": [
        {
            "questions": [
                {
                    "question": "What is 2 + 2?",
                    "options": ["1", "2", "3", "4"],
                    "answer": "4"
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Earth", "Mars", "Jupiter", "Saturn"],
                    "answer": "Mars"
                }
            ]
        }
    ]
}

Future Enhancements

Add user authentication (login/signup)

Store scores in a database (SQLite or MongoDB)

Add a timer for each question

Enhance UI with CSS and animations

Deploy to Heroku, Render, or PythonAnywhere

Author

Amit Paul
Built with ❤️ using Python and Flask.
