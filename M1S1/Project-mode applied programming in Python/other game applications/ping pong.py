import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 400
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
BALL_SIZE = 15
BALL_SPEED = 5
PADDLE_SPEED = 10

class Pong(tk.Tk):
    def __init__(self):
        super().__init__()

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.paddle1 = self.canvas.create_rectangle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                                    50 + PADDLE_WIDTH, HEIGHT // 2 + PADDLE_HEIGHT // 2,
                                                    fill='white')
        self.paddle2 = self.canvas.create_rectangle(WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                                    WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 + PADDLE_HEIGHT // 2,
                                                    fill='white')

        self.ball = self.canvas.create_oval(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2,
                                            WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2,
                                            fill='white')

        self.ball_dx = 0
        self.ball_dy = 0

        self.bind('<KeyPress-Up>', self.move_paddle)
        self.bind('<KeyPress-Down>', self.move_paddle)
        self.bind('<KeyPress-w>', self.move_paddle)
        self.bind('<KeyPress-s>', self.move_paddle)
        self.bind('<space>', self.start_game)

        self.started = False

        self.score1 = 0
        self.score2 = 0
        self.score_display = self.canvas.create_text(WIDTH // 2, 30, text="Press Space to Start",
                                                     fill='white', font=('Arial', 20))

        self.update()

    def move_paddle(self, event):
        if self.started:
            if event.keysym == 'Up' and self.canvas.coords(self.paddle2)[1] > 0:
                self.canvas.move(self.paddle2, 0, -PADDLE_SPEED)
            elif event.keysym == 'Down' and self.canvas.coords(self.paddle2)[3] < HEIGHT:
                self.canvas.move(self.paddle2, 0, PADDLE_SPEED)
            elif event.keysym == 'w' and self.canvas.coords(self.paddle1)[1] > 0:
                self.canvas.move(self.paddle1, 0, -PADDLE_SPEED)
            elif event.keysym == 's' and self.canvas.coords(self.paddle1)[3] < HEIGHT:
                self.canvas.move(self.paddle1, 0, PADDLE_SPEED)

    def start_game(self, event):
        self.started = True
        self.ball_dx = BALL_SPEED * random.choice([-1, 1])
        self.ball_dy = BALL_SPEED * random.choice([-1, 1])
        self.canvas.itemconfig(self.score_display, text=f"{self.score1} - {self.score2}")

    def update(self):
        if self.started:
            self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
            ball_pos = self.canvas.coords(self.ball)

            if ball_pos[1] <= 0 or ball_pos[3] >= HEIGHT:
                self.ball_dy *= -1

            if ball_pos[0] <= 0:
                self.score2 += 1
                self.canvas.itemconfig(self.score_display, text=f"{self.score1} - {self.score2}")
                self.reset_ball()
            elif ball_pos[2] >= WIDTH:
                self.score1 += 1
                self.canvas.itemconfig(self.score_display, text=f"{self.score1} - {self.score2}")
                self.reset_ball()

            paddles = self.canvas.find_overlapping(*ball_pos)
            if self.paddle1 in paddles or self.paddle2 in paddles:
                self.ball_dx *= -1

        self.after(20, self.update)

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2,
                           WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2)
        self.started = False
        self.ball_dx = 0
        self.ball_dy = 0

if __name__ == "__main__":
    game = Pong()
    game.title("Pong Game")
    game.mainloop()