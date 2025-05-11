from graphics2 import *
import random

win = GraphWin("Card Match Game", 500, 500)
win.setBackground("green")

card = Image(Point(0, 0), "PNG-cards-1.3/back.png")
card.draw(win)

win.getMouse()