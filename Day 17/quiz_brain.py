class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.list = q_list

    def still_has_questions(self):
        if self.question_number == 12:
            return False
        return True

    def next_question(self):
        question = self.list[self.question_number]
        self.question_number += 1
        answer = input(f"Q.{self.question_number}: {question.text} (True/False)?: ").title()
        self.check_answer(answer, question.answer)

    def check_answer(self, answer, correct_answer):
        if answer == correct_answer:
            self.score += 1
            print("You got it right!👍✅")
        elif answer != correct_answer:
            print("You got it wrong.👎❌")
        print(f"The correct answer was: {correct_answer}.")
        print(f"Your current score: {self.score}/{self.question_number}")
        print("\n")

