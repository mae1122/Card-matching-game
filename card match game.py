from graphics2 import *
import random
from constants import * 
from cards import Card
from button import Button
import time

def displayOpeningScreenAndGetSettings():
    win = GraphWin("Card Match Game", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("green")
    background = Image(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "PNG-cards-1.3/background.png")
    background.scale(2.2)
    background.draw(win)
    
    instruction = Text(Point(WINDOW_WIDTH//2,200),"press start button to start the game")
    instruction.setSize(20)
    instruction.draw(win)

    cardsEntry = Entry(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT-260),4)
    cardsEntry.setText(5)
    cardsEntry.setSize(15)
    cardsEntry.draw(win)

    directions = Text(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT-300), "Enter the number of cards(1 - 5):")
    directions.setSize(15)
    directions.draw(win)
    
    startButton = Button(Point(WINDOW_WIDTH//2, 400),80, 50,"Start")
    startButton.draw(win)
    startButton.activate()

    win.getMouse()
    win.close()
    return int(cardsEntry.getText())




def createCards(numCards):
    cards = []

    # Create two of each card for matching
    for i in range(numCards):
        suit = random.choice(SUITS)
        rank = random.choice(RANKS)
        
        card = Card(suit, rank)
        cards.append(card)
        
        card = Card(suit, rank)
        cards.append(card)
    return cards

def getClickedCard(win, cards):
    while True:
        clickPoint = win.getMouse()
        for card in cards:
            if card.isClicked(clickPoint):
                 return card
            
def hasUnflippedCards(cards):
    return any(not card.isFlipped() for card in cards)
            

def play(numCards):

    cards = createCards(numCards)
    random.shuffle(cards)


    win = GraphWin("Card Match Game", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("green")
    background = Image(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "PNG-cards-1.3/background.png")
    background.scale(2.0)
    background.draw(win)

    while hasUnflippedCards(cards):
        
        card_positions = []
        for i in range(len(cards)):
            x = (i % 5) * 100 + 300
            y = (i // 5) * 150 + 300
            if not cards[i].isFlipped():
                cards[i].draw(win, x, y)
            card_positions.append((x, y))

        firstCard = getClickedCard(win, cards)
        firstCard.flip(win)

        secondCard = getClickedCard(win, cards)
        secondCard.flip(win)

        if firstCard.cardValue() == secondCard.cardValue():
            print("hello")
        else:
            time.sleep(1)
            firstCard.flip(win)
            secondCard.flip(win)

    win.getMouse()
    win.close()
    
    return True

def main():
    numCards = displayOpeningScreenAndGetSettings()
    playAgain = play(numCards)

main()