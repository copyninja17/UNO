from src import config, clientData
from src import clientConfig as cc

R = 'red'
B = 'blue'
G = 'green'
Y = 'yellow'
X = 'X'
colours = [R,B,G,Y,X]

def topCardDisplay(screen, tableButton, cardButtons):
    tableButton.draw(screen)

    col = cc.top_card.card['colour']
    if cc.top_card.card['val'] == '+4':
        val = 0
    elif cc.top_card.card['val'] == 'wild':
        val = 1
    elif cc.top_card.card['val'] == '+2':
        val = 10
    elif cc.top_card.card['val'] == 'reverse':
        val = 11
    elif cc.top_card.card['val'] == 'skip':
        val = 12
    else:
        val = int(cc.top_card.card['val'])

    cardButtons[col][val].draw(screen)

def display(screen, tableButton, cardButtons):
    topCardDisplay(screen, tableButton, cardButtons)
    