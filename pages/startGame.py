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
    try:
        numCards = len(cc.player_hand.stack)
        for i in range(numCards):
            cardDisplay(screen, cardsList, cc.player_hand.stack[i], x=(10 + cardsList['R'][0].get_width()*0.4)*(i+1), y=SCREEN_HEIGHT-100)
    except:
        pass



def display(screen, tableButton, cardsList, gameplayImg):
    tableButton.draw(screen)
    # if cc.winner == 'None':
    cardDisplay(screen, cardsList, cc.top_card)
    printHand(screen, cardsList)
    if cc.playerTurn is True:
        button.Button(10, 10, gameplayImg['yourTurn'], 0.4).draw(screen)
    else:
        button.Button(10, 10, gameplayImg['notYourTurn'], 0.4).draw(screen)

    if cc.okPrompt == 0:
        if button.Button(SCREEN_WIDTH-gameplayImg['ok'].get_width()*0.25 -10, SCREEN_HEIGHT/2-gameplayImg['ok'].get_height()/2*0.25, gameplayImg['ok'], 0.25).draw(screen):
            cc.okPrompt = 1

    if cc.colourChange == 0:
        if button.Button(SCREEN_WIDTH-2*gameplayImg['pick']['red'].get_width()*0.4 -10, SCREEN_HEIGHT/2-gameplayImg['pick']['red'].get_height()/2*0.4, gameplayImg['pick']['red'], 0.4).draw(screen):
            cc.colourChange = 'R'
        elif button.Button(SCREEN_WIDTH-gameplayImg['pick']['blue'].get_width()*0.4 -10, SCREEN_HEIGHT/2-gameplayImg['pick']['blue'].get_height()/2*0.4, gameplayImg['pick']['blue'], 0.4).draw(screen):
            cc.colourChange = 'B'
        elif button.Button(SCREEN_WIDTH-2*gameplayImg['pick']['yellow'].get_width()*0.4 -10, SCREEN_HEIGHT/2+gameplayImg['pick']['yellow'].get_height()/2*0.4, gameplayImg['pick']['yellow'], 0.4).draw(screen):
            cc.colourChange = 'Y'
        elif button.Button(SCREEN_WIDTH-gameplayImg['pick']['green'].get_width()*0.4 -10, SCREEN_HEIGHT/2+gameplayImg['pick']['green'].get_height()/2*0.4, gameplayImg['pick']['green'], 0.4).draw(screen):
            cc.colourChange = 'G'
