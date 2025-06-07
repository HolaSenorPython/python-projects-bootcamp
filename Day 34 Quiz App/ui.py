from tkinter import *
from quiz_brain import QuizBrain
import pygame
THEME_COLOR = "#375362"

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        # sound
        pygame.mixer.init()
        self.wow = pygame.mixer.Sound("wow.mp3")
        self.nope = pygame.mixer.Sound("nope.mp3")
        #get the quizbrain, score, and answer
        self.quiz = quiz_brain
        # window setup
        self.window = Tk()
        self.window.title("Quizzler!")
        self.window.config(padx=20,pady=20,bg=THEME_COLOR)
        # canvas setup
        self.canvas = Canvas(width=300,height=250)
        self.text = self.canvas.create_text(150,
                                            125,
                                            text="placeholder string",
                                            font=("Arial", 18, "italic"),
                                            fill="green",
                                            width=250,)
        self.canvas.grid(column=0,row=1,columnspan=2,padx=20,pady=50)
        # labels
        self.score_label = Label(text=f"Score: {self.quiz.score}",bg=THEME_COLOR,fg="white",font=("Arial", 12, "bold"))
        self.score_label.grid(column=1,row=0)
        # BUTTONS
        true_img = PhotoImage(file="true.png")
        false_img = PhotoImage(file="false.png")
        self.true_btn = Button(command=self.button_press_true,image=true_img,bg=THEME_COLOR,relief="flat",highlightthickness=0)
        self.true_btn.grid(column=0,row=2)
        self.false_btn = Button(command=self.button_press_fal,image=false_img,bg=THEME_COLOR,relief="flat",highlightthickness=0)
        self.false_btn.grid(column=1,row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.text, text=q_text)
        else:
            self.canvas.config(bg="white")
            self.canvas.itemconfig(self.text, text=f"You've completed the quiz. Your final "
                                                   f"score was {self.quiz.score}/{len(self.quiz.question_list)}.")
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")
            
    def button_press_true(self):
        self.user_feedback(self.quiz.check_answer("True"))

    def button_press_fal(self):
        self.user_feedback(self.quiz.check_answer("False"))

    def user_feedback(self, is_correct):
        if is_correct is True:
            pygame.mixer.Sound.play(self.wow)
            self.canvas.config(bg="lime")
            self.score_label.config(text=f"Score: {self.quiz.score}")
            self.window.after(ms=1000, func=self.question_reset)
        elif is_correct is False:
            pygame.mixer.Sound.play(self.nope)
            self.canvas.config(bg="red")
            self.score_label.config(text=f"Score: {self.quiz.score}")
            self.window.after(ms=1000, func=self.question_reset)

    def question_reset(self):
        self.canvas.config(bg="white")
        self.get_next_question()