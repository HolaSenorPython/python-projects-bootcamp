### THIS WAS DAY 17!!!! ###
from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
import random

question_bank = []
quiz_pool = random.sample(question_data, 12)
for item in quiz_pool:
    new_question = Question(item["text"], item["answer"])
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("🥳You've completed the quiz🥳")
print(f"Your final score: {quiz.score}/{quiz.question_number}")
