from graphics2 import *
import random
from constants import *

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.face_up = False
        self.card_name = self.rank + "_" + self.suit
        

    def isFlipped(self):
        return self.face_up

    def flip(self,win):
        if self.face_up == False:
            self.face_up = not self.face_up
        self._updateVisual(win) 

    def back(self,win):
        if self.face_up == True:
            self.face_up = not self.face_up
        self._updateVisual(win)
        
    def draw(self, win, x, y):
        if self.face_up:
            self.card = Image(Point(x, y), "PNG-cards-1.3/" + self.card_name  + ".png")
            self.card.scale(0.3)
            self.card.draw(win)

        else:
            self.card = Image(Point(x, y), "PNG-cards-1.3/back.png")
            self.card.scale(0.09)
            self.card.draw(win)

    def cardValue(self):
        return self.card_name
    
    def _updateVisual(self, win):
        if self.face_up:
            self.card.undraw()
            self.card = Image(self.card.getCenter(), "PNG-cards-1.3/" + self.card_name  + ".png")
            self.card.scale(0.13)
            self.card.draw(win)
        else:
            self.card.undraw()
            self.card = Image(self.card.getCenter(), "PNG-cards-1.3/back.png")
            self.card.scale(0.09)
            self.card.draw(win) 

    
    def isClicked(self, click_point):
        if click_point is None:
            return False
        else:
            x_min = self.card.getCenter().getX() - 20 
            x_max = self.card.getCenter().getX() + 20 
            y_min = self.card.getCenter().getY() - 40
            y_max = self.card.getCenter().getY() + 40

        return x_min <= click_point.getX() <= x_max and y_min <= click_point.getY() <= y_max
    
    def __str__(self):  
        return f"{self.rank} of {self.suit} is face up: {self.face_up}" 