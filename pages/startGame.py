from src import config, clientData
from src import clientConfig as cc
from src import button

R = 'red'
B = 'blue'
G = 'green'
Y = 'yellow'
X = 'X'
colours = [R,B,G,Y,X]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def cardDisplay(screen, cardsList, currCard, x=-1, y=-1):

    col = currCard.card['colour']
    if currCard.card['val'] == '+4':
        val = 0
    elif currCard.card['val'] == 'wild':
        val = 1
    elif currCard.card['val'] == '+2':
        val = 10
    elif currCard.card['val'] == 'reverse':
        val = 11
    elif currCard.card['val'] == 'skip':
        val = 12
    else:
        val = int(currCard.card['val'])
    
    if x == -1:
        x,y = SCREEN_WIDTH/2-cardsList['R'][0].get_width()/2*0.4, SCREEN_HEIGHT/4+cardsList['R'][0].get_height()*0.4
    # find the image
    if button.Button(x,y,cardsList[col][val], 0.4).draw(screen):
        cc.currentChoice = currCard

    # make a new button

def printHand(screen,cardsList):
    numCards = len(cc.player_hand.stack)
    for i in range(numCards):
        cardDisplay(screen, cardsList, cc.player_hand.stack[i], x=(10 + cardsList['R'][0].get_width()*0.4)*(i+1), y=SCREEN_HEIGHT-100)
        


def display(screen, tableButton, cardsList):
    tableButton.draw(screen)
    cardDisplay(screen, cardsList, cc.top_card)
    printHand(screen, cardsList)
    