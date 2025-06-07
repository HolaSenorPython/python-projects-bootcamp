from question_model import Question
from quiz_brain import QuizBrain
from data import question_data
from ui import QuizInterface
import pygame

question_text = None
question_bank = []
for question in question_data["results"]:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

pygame.mixer.init()
pygame.mixer.music.load("jeopardy.mp3")  # just the filename, assuming it's in the same folder
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)


