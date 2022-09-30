from src import clientConfig as cc
from src import button

import math


R = 'red'
B = 'blue'
G = 'green'
Y = 'yellow'
X = 'X'
colours = [R,B,G,Y,X]
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600 #450
CARD_SIZE = 1.0

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
        x = SCREEN_WIDTH/2 - cardsList['R'][0].get_width()/2*CARD_SIZE
        y = SCREEN_HEIGHT/2 - cardsList['R'][0].get_height()/2*CARD_SIZE
        
        if val in [0,1] and cc.chosenColour in ['R', 'B', 'G', 'Y']:
            col = cc.chosenColour
            val = 13 if val == 0 else 14

    if button.Button(x,y,cardsList[col][val], CARD_SIZE).draw(screen):
        cc.currentChoice = currCard


def printHand(screen,cardsList):
    try:
        if cc.winner == cc.playerName:
            return
            
        n = len(cc.player_hand.stack)
        for i in range(n):
            # x = vertical pos of cards
            if n > 9:
                x = (SCREEN_WIDTH * 0.9) * i / n 
            else:
                card_gap = 10
                offset_x = card_gap + cardsList['R'][0].get_width() * CARD_SIZE
                x =  + (offset_x * i)

            x += SCREEN_WIDTH / 20
            y  = SCREEN_HEIGHT - cardsList['R'][0].get_height() - 10
            
            cardDisplay(screen, cardsList, cc.player_hand.stack[i], x, y)
    except Exception as e:
        print(e)


def uno_back_coords(baseAngle ,tables, cardsList, index):
    angle = math.radians(index * cc.playerAngle + baseAngle)
    
    x = (SCREEN_WIDTH/2 - tables[0].get_width()/2*1) * math.cos(angle) + SCREEN_WIDTH/2 - cardsList['unoBack'].get_width()/2
    y = SCREEN_HEIGHT/2 - (tables[0].get_height()/2*1) * math.sin(angle) - cardsList['unoBack'].get_height()

    return (x,y)


def printPlayers(screen, cardsList, myFont, tables):
    if cc.playerCount == 2:
        baseAngle = 0
        cc.playerAngle = 90
    
    elif cc.playerCount == 3:
        baseAngle = -90
        cc.playerAngle = 120

    elif cc.playerCount == 4:
        baseAngle = -90
        cc.playerAngle = 90        

    elif cc.playerCount > 4:
        cc.playerAngle = 240/(cc.playerCount - 2)
        baseAngle = -30 - cc.playerAngle
    
    else:
        return
    
    for i, player in enumerate(cc.playerList[:-1]):
        card_coords = uno_back_coords(baseAngle, tables, cardsList, i+1)
        if player == cc.playerTurn:
            card_coords = (card_coords[0], card_coords[1] + math.sin(cc.cardAnimationAngle)*5)
            cc.cardAnimationAngle += 1 * 0.15
        screen.blit(cardsList['unoBack'],card_coords)

        LIGHT_RED = (255,204,203)
        LIGHT_GREEN = (144,238,144)

        bg_color = LIGHT_GREEN if player == cc.playerTurn else LIGHT_RED

        playerLabel = myFont[1].render(f' {player} : {cc.players[player]} ', 1, (0,0,0), bg_color)
        x = card_coords[0] + cardsList['unoBack'].get_width()/2 - playerLabel.get_width()/2
        y = card_coords[1] + cardsList['unoBack'].get_height() + 2
        screen.blit(playerLabel, (x,y))


def display(screen, tables, cardsList, gameplayImg,myFont):
    if cc.winner !='NONE':
        winnerName = f"YOU ARE THE WINNER!!" if cc.winner == cc.playerName else f"WINNER IS {cc.winner}!"
        winnerLabel = myFont[2].render(winnerName, 1, (0,0,0))

        x = SCREEN_WIDTH/2 - winnerLabel.get_width()/2
        y = SCREEN_HEIGHT/2 - winnerLabel.get_height()/2
        screen.blit(winnerLabel, (x,y))
        return

    # flip table on screen
    if cc.playerCount <= 2:
        cc.table_direction = 0

    elif ((cc.top_card.card['val'] == 'reverse') and 
        (cc.players != cc.old_card_dict) and 
        (sum(list(map(int, cc.players.values()))) <= sum(list(map(int, cc.old_card_dict.values()))))):
        print("reversed table!")
        cc.table_direction *= -1

    screen.blit(tables[cc.table_direction], (SCREEN_WIDTH/2 - tables[0].get_width()/2*1,
                            SCREEN_HEIGHT/2 - tables[0].get_height()/2*1))

    cc.old_card_dict = cc.players

    # display cards on table
    printPlayers(screen, cardsList, myFont, tables)
    cardDisplay(screen, cardsList, cc.top_card)
    printHand(screen, cardsList)

    if cc.playerTurn == cc.playerName:
        button.Button(10, 10, gameplayImg['yourTurn'], 0.2).draw(screen)
    else:
        button.Button(10, 10, gameplayImg['notYourTurn'], 0.2).draw(screen)

    if cc.okPrompt == 0:
        if button.Button(SCREEN_WIDTH-gameplayImg['ok'].get_width()*0.25 -10,
                         SCREEN_HEIGHT/2-gameplayImg['ok'].get_height()/2*0.25,
                         gameplayImg['ok'], 0.25).draw(screen):
            cc.okPrompt = 1

    if cc.colourChange == 0:
        if button.Button(SCREEN_WIDTH-2*gameplayImg['pick']['red'].get_width()*0.4 -10,
                         SCREEN_HEIGHT/2-gameplayImg['pick']['red'].get_height()/2*0.4,
                         gameplayImg['pick']['red'], 0.4).draw(screen):
            cc.colourChange = 'R'
        elif button.Button(SCREEN_WIDTH-gameplayImg['pick']['blue'].get_width()*0.4 -10, 
                           SCREEN_HEIGHT/2-gameplayImg['pick']['blue'].get_height()/2*0.4, 
                           gameplayImg['pick']['blue'], 0.4).draw(screen):
            cc.colourChange = 'B'
        elif button.Button(SCREEN_WIDTH-2*gameplayImg['pick']['yellow'].get_width()*0.4 -10, 
                           SCREEN_HEIGHT/2+gameplayImg['pick']['yellow'].get_height()/2*0.4, 
                           gameplayImg['pick']['yellow'], 0.4).draw(screen):
            cc.colourChange = 'Y'
        elif button.Button(SCREEN_WIDTH-gameplayImg['pick']['green'].get_width()*0.4 -10, 
                           SCREEN_HEIGHT/2+gameplayImg['pick']['green'].get_height()/2*0.4, 
                           gameplayImg['pick']['green'], 0.4).draw(screen):
            cc.colourChange = 'G'
