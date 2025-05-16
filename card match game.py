'''
Card Match Game
This is a simple card matching game where players can play against each other or alone
I used chat gpt to generate a method to print the cards in a specific position everything else is my own work.
'''
from graphics2 import *
import random
from constants import * 
from cards import Card
from button import Button
import time

def randomColor():
    return random.choice(["red", "blue", "green", "yellow", "purple", "orange"])
def validateInput(input, win):
    if input < 4 or input > 10:
        instruction = Text(Point(WINDOW_WIDTH//2, 100), "Please enter a number between 4 and 10")
        instruction.setSize(20)
        instruction.draw(win)
        instruction.setFill(randomColor())
        return False
    return True

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

    directions = Text(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT-300), "Enter the number of cards(4 - 10)")
    directions.setSize(15)
    directions.draw(win)
    
    singlePlayerButton = Button(Point(WINDOW_WIDTH//2, 400),150, 50,"single player")
    singlePlayerButton.draw(win)

    multiPlayerButton = Button(Point(WINDOW_WIDTH//2, 300),150, 50,"multiplayer")
    multiPlayerButton.draw(win)

    clickPt = win.getMouse()
    cards =  int(cardsEntry.getText())
    readySingle = singlePlayerButton.isClicked(clickPt)
    readyMulti = multiPlayerButton.isClicked(clickPt)
    
    while not (readySingle or readyMulti) or not validateInput(cards, win):
        clickPt = win.getMouse()
        cards =  int(cardsEntry.getText())
        
        readySingle = singlePlayerButton.isClicked(clickPt)
        readyMulti = multiPlayerButton.isClicked(clickPt)
        
    if  readySingle:
        win.close()
        return int(cardsEntry.getText()), "single"
    
    elif readyMulti:
        win.close()
        return int(cardsEntry.getText()), "multi"
    

def createCards(numCards):
    cards = []

    for i in range(numCards):
        suit = random.choice(SUITS)
        rank = random.choice(RANKS)
        
        card = Card(suit, rank)
        for i in cards:
            while card.cardValue() == i.cardValue():
                suit = random.choice(SUITS)
                rank = random.choice(RANKS)
                card = Card(suit, rank)
        
        cards.append(card)
        
        card = Card(suit, rank)
        cards.append(card)
    return cards

def getClickedCard(win, cards):
    clickPoint = win.getMouse()
    for card in cards:
        if card.isClicked(clickPoint) and card.isFlipped() == False:
            return card
            
def hasUnflippedCards(cards):
    return any(not card.isFlipped() for card in cards)
            

def playSingle(numCards):

    cards = createCards(numCards)
    random.shuffle(cards)
    score = 0


    win = GraphWin("Card Match Game", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("green")
    
    background = Image(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "PNG-cards-1.3/background.png")
    background.scale(2.2)
    background.draw(win)
    
    score_current = Text(Point(WINDOW_WIDTH//2, 50), f"Score: {score}")
    score_current.setSize(20)
    score_current.draw(win)

    while hasUnflippedCards(cards):
        
        card_positions = []
        for i in range(len(cards)):
            x = (i % 7) * 100 + 250
            y = (i // 7) * 150 + 200
            if not cards[i].isFlipped():
                cards[i].draw(win, x, y)
            card_positions.append((x, y))

        firstCard = getClickedCard(win, cards)
        while firstCard == None:
            firstCard = getClickedCard(win, cards)
        firstCard.flip(win)

        secondCard = getClickedCard(win, cards)
        while secondCard == None:
            secondCard = getClickedCard(win, cards)    
        secondCard.flip(win)

        if firstCard.cardValue() == secondCard.cardValue():
            score += 1
        else:
            time.sleep(1)
            firstCard.back(win)
            secondCard.back(win)
            if score > 0:
                score -= 1
        score_current.setText(f"Score: {score}")
    
    winner = Text(Point(WINDOW_WIDTH//2, 600), f"completed with {score} score.")
    winner.setFill(randomColor())
    winner.setSize(50)
    winner.draw(win)
    time.sleep(2)
    win.close()
    
    return score

def playMulti(numCards):
    cards = createCards(numCards)
    random.shuffle(cards)
    score_P1 = 0
    score_P2 = 0


    win = GraphWin("Card Match Game", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("green")
    
    background = Image(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "PNG-cards-1.3/background.png")
    background.scale(2.2)
    background.draw(win)
    
    scoreP1Text = Text(Point(WINDOW_WIDTH//5, 70), f"player one: {score_P1}")
    scoreP1Text.setFill(randomColor())
    scoreP1Text.setSize(18)
    scoreP1Text.draw(win)

    scoreP2Text = Text(Point(WINDOW_WIDTH//5, 120), f"player two: {score_P2}")
    scoreP2Text.setSize(18)
    scoreP2Text.setFill(randomColor())
    scoreP2Text.draw(win)

    player = 1

    turn = Text(Point(WINDOW_WIDTH//2, 100), "Player 1 turn")
    turn.setSize(20)
    turn.draw(win)

    while hasUnflippedCards(cards):
        
        card_positions = []
        for i in range(len(cards)):
            x = (i % 7) * 100 + 250
            y = (i // 7) * 150 + 200
            if not cards[i].isFlipped():
                cards[i].draw(win, x, y)
            card_positions.append((x, y))


        if player%2 == 1:
            turn.setText(f"Player 1 turn")
            scoreP1Text.setText(f"player one: {score_P1}")
        else:
            turn.setText(f"Player 2 turn")
            scoreP2Text.setText(f"player two: {score_P2}")

        firstCard = getClickedCard(win, cards)

        while firstCard == None:
            firstCard = getClickedCard(win, cards)
            
        firstCard.flip(win)

        secondCard = getClickedCard(win, cards)
        while secondCard == None:
            secondCard = getClickedCard(win, cards)
            
        secondCard.flip(win)


        if firstCard.cardValue() == secondCard.cardValue():
            if player == 1:
                player = 2
                score_P1 +=1
            else:
                player = 1
                score_P2 +=1
        else:
            time.sleep(1)
            firstCard.back(win)
            secondCard.back(win)

        if player == 1:
            player = 2
        else:
            player = 1

    if score_P1 > score_P2:
        winner = Text(Point(WINDOW_WIDTH//2, 600), "Player 1 wins.")
        winner_score = score_P1
    elif score_P1 < score_P2:
        winner = Text(Point(WINDOW_WIDTH//2, 600), "Player 2 wins.")
        winner_score = score_P2
    else:
        winner = Text(Point(WINDOW_WIDTH//2, 600), "It's a tie.")
        winner_score = 0    
   
    winner.setFill(randomColor())
    winner.setSize(50)
    winner.draw(win)
    time.sleep(2)
    win.close()
    
    return winner.getText(), winner_score

def main():
    continueGame = True

    while continueGame:
        numCards, game = displayOpeningScreenAndGetSettings()
        
        if game == "single":
            score = playSingle(numCards)
            win = GraphWin("game over", WINDOW_WIDTH, WINDOW_HEIGHT)
            win.setBackground("green")
        
            background = Image(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "PNG-cards-1.3/background.png")
            background.scale(2.2)
            background.draw(win)

            winner = Text(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), f"completed with {score} score.")
            winner.setSize(50)
        elif game == "multi":
            winner, score = playMulti(numCards)
            win = GraphWin("game over", WINDOW_WIDTH, WINDOW_HEIGHT)
            win.setBackground("green")
        
            background = Image(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), "PNG-cards-1.3/background.png")
            background.scale(2.2)
            background.draw(win)

            winner = Text(Point(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), f"{winner} with {score} score.")
            winner.setSize(50)
        
        winner.setFill(randomColor())
        winner.draw(win)
        playAgainButton = Button(Point(200, 500),150, 50,"play again")
        playAgainButton.draw(win)

        quitButton = Button(Point(800, 500),150, 50,"quit")
        quitButton.draw(win)

        clickPt = win.getMouse()

        quit = quitButton.isClicked(clickPt)
        play = playAgainButton.isClicked(clickPt)
        
        while not (quit or play):
            clickPt = win.getMouse()

            quit = quitButton.isClicked(clickPt)
            play = playAgainButton.isClicked(clickPt)
        
        if  quit:
            continueGame = False
        
        elif play:
            continueGame = True
        win.close()
   
    win.close()
    print("Thanks for playing")
        
main()