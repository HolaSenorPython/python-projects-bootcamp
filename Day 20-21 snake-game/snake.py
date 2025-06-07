import turtle as t
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:

    def __init__(self):
        self.FULL_SNAKE = []
        self.make_snake()
        self.head = self.FULL_SNAKE[0]

    def make_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        snake_segment = t.Turtle()
        snake_segment.penup()
        snake_segment.color("royal blue")
        snake_segment.shape("square")
        snake_segment.setpos(position)
        self.FULL_SNAKE.append(snake_segment)

    def reset(self):
        for segment in self.FULL_SNAKE:
            segment.hideturtle()
        self.FULL_SNAKE.clear()
        self.make_snake()
        self.head = self.FULL_SNAKE[0]

    def grow(self):
        """ADD NEW SEGMENT TO SNAKE"""
        self.add_segment(self.FULL_SNAKE[-1].position())

    def move(self):
        for segment in range(len(self.FULL_SNAKE) - 1, 0, -1):
            new_x = self.FULL_SNAKE[segment - 1].xcor()
            new_y = self.FULL_SNAKE[segment - 1].ycor()
            self.FULL_SNAKE[segment].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.seth(UP)
    def down(self):
        if self.head.heading() != UP:
            self.head.seth(DOWN)
    def left(self):
        if self.head.heading() != RIGHT:
            self.head.seth(LEFT)
    def right(self):
        if self.head.heading() != LEFT:
            self.head.seth(RIGHT)