from flask import Flask, render_template, request, jsonify
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Storing questions and answers in a dictionary (for simplicity)
custom_qna = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message')
    response = generate_response(user_message)
    return jsonify({'response': response})


def generate_response(user_message):
    greetings = ['hi', 'hello', 'hey']
    if any(greeting in user_message.lower() for greeting in greetings):
        return "Hi student, how can I help you?"

    if re.search(r'\b(what|when|explain)\b', user_message, re.I):
        answer = get_answer_from_external_resource(user_message)
        if answer:
            return answer
        else:
            return "I'm sorry, I couldn't find an answer for that."

    if user_message.lower().startswith('add'):
        parts = user_message.split('\n')
        if len(parts) == 3:
            question = parts[1]
            answer = parts[2]
            add_question_answer(question, answer)
            return "Question and answer added successfully!"
        else:
            return "Invalid format. To add a question and answer, use:\nadd\n<question>\n<answer>"

    return "Tutor will assist you"

def get_answer_from_external_resource(question):
    url = "https://intellipaat.com/blog/interview-question/data-analyst-interview-questions/?US"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    question_elements = soup.find_all("h3")

    for question_element in question_elements[:-1]:
        #Debugg: print(question_element)
        question_text = question_element.text
        question_text = re.sub(r"^\d+:", "", question_text).strip()

        if question.lower() in question_text.lower():
            answer_element = question_element.find_next("p")
            if answer_element:
                return answer_element.get_text().strip()

    return "Answer not found in the external resource"


def add_question_answer(question, answer):
    custom_qna[question] = answer


if __name__ == '__main__':
    app.run(debug=True)
