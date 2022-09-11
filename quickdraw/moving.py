import tkinter as tk      # for python 2, replace with import Tkinter as tk
import random


class Ball:

    def __init__(self):
        self.xpos = random.randint(0, 254)
        self.ypos = random.randint(0, 310)
        self.xspeed = random.randint(1, 5)
        self.yspeed = random.randint(1, 5)


class MyCanvas(tk.Canvas):

    def __init__(self, master):

        super().__init__(master, width=254, height=310, bg="snow2", bd=0, highlightthickness=0, relief="ridge")
        self.pack()

        self.balls = []   # keeps track of Ball objects
        self.bs = []      # keeps track of Ball objects representation on the Canvas
        for _ in range(25):
            ball = Ball()
            self.balls.append(ball)
            self.bs.append(self.create_oval(ball.xpos - 10, ball.ypos - 10, ball.xpos + 10, ball.ypos + 10, fill="saddle brown"))
        self.run()

    def run(self):
        for b, ball in zip(self.bs, self.balls):
            self.move(b, ball.xspeed, ball.yspeed)
            pos = self.coords(b)
            if pos[3] >= 310 or pos[1] <= 0:
                ball.yspeed = - ball.yspeed
            if pos[2] >= 254 or pos[0] <= 0:
                ball.xspeed = - ball.xspeed
        self.after(10, self.run)


if __name__ == '__main__':

    shop_window = tk.Tk()
    shop_window.geometry("254x310")
    c = MyCanvas(shop_window)

    shop_window.mainloop()