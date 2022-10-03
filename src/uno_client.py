'''
Backend client script for UNO.
Handles all client side operations like selection and communication.

[TODO] Needs cleanup.
'''

from src import config
from src.bridge import Network
from src import uno_module as uno
from src import clientConfig as cc

import subprocess, sys, os
import threading

class Client:

    def __init__(self, address, port):
        '''
        Initializes the Client.
        '''

        self.net = Network(address, port)
        self.choice = 0
        self.colour = '0'
        self.event = ['0', 'regular', 'no_cards', '+4/+2', 'reverse', 'skip', 'wild']
        self.playerName = cc.playerName
        self.playerList = []

    @staticmethod
    def parse(data):
        '''
        Decodes received data from server

        Data form: "topCard: playerHand: responseID: cardList: playerTurn: winner: chosenColour"
        [TODO]: what's going on in the game unrelated to the player aka Broadcasting
        '''
        print(f'{data=}')                #DEBUGGING

        if ':' not in data and not cc.receivedPlayerList:
            # playerList received
            try:
                print(f"Player list retrived: {data}")
                cc.receivedPlayerList = True
                return data.split(',') if ',' in data else [data,]

            except ValueError or TypeError or IndexError:
                print("ERROR RETRIEVING DATA FROM SERVER!")
                return 0
        else:
            # game data received
            try:
                top_card = uno.Card()
                top_card.generate(data.split(':')[0][-1], data.split(':')[0][:-1])

                player_hand = uno.Stack()
                for i in list(data.split(':')[1].split(',')):
                    try:
                        sample = uno.Card()
                        sample.generate(i[-1], i[:-1])
                        player_hand.add(sample)
                    except:
                        print("ERROR")
                        print(data)

                eventID = int(data.split(':')[2])

                drawn_cards = uno.Stack()
                for i in list(data.split(':')[3].split(',')):
                    sample = uno.Card()
                    sample.generate(i[-1], i[:-1])
                    drawn_cards.add(sample)

                playerTurn = data.split(':')[4]

                players = {}
                for player in data.split(':')[5].split(','):
                    players[player.split('=')[0]] = player.split('=')[1]
                    
                if not cc.old_card_dict:
                    cc.old_card_dict = players.copy()

                winner = data.split(':')[6]

                chosenColour = data.split(':')[7]

                return (top_card, 
                        player_hand, 
                        eventID, 
                        drawn_cards, 
                        playerTurn, 
                        players, 
                        winner, 
                        chosenColour)

            except ValueError or TypeError or IndexError:
                print ("ERROR RETRIEVING DATA FROM SERVER!")
                print (data)
                return 0, 0, 0, 0, 0

    def send_recv(self, oneTime=False):
        '''
        Sends data to server and returns reply.

        oneTime: If True, exchanges playerName with playerList.
        '''

        if oneTime:
            reply = self.net.communicate(self.playerName)
            return reply
        else:
            data = (str(self.net.id) + ':' + 
                    str(self.choice) + ',' + 
                    str(self.colour))
            reply = self.net.communicate(data)
            return reply


def display(addrPort):
    address, port = addrPort.split(':')

    try:
        client = Client(address, port)
    except Exception as e:
        print(e)
        cc.page = 0
    oldData = 'NEW'

    # Retrieve playerList (one time data)
    client.playerList = client.parse(client.send_recv(oneTime=True))
    cc.playerList = client.playerList.copy()
    cc.playerCount = len(cc.playerList)
    
    while cc.playerList[-1] != cc.playerName:
        cc.playerList.append(cc.playerList.pop(0))

    while True:
        try:
            data = client.send_recv()

            # so the client won't refresh always
            if oldData == data:
                continue
            else:
                oldData = data

            # # data received
            (cc.top_card, 
             cc.player_hand, 
             cc.eventID, 
             cc.drawn_cards, 
             cc.playerTurn, 
             cc.players, 
             cc.winner, 
             cc.chosenColour) = client.parse(data)

            # winner/loser
            if cc.winner == client.playerName:
                print("\nYOU ARE THE WINNER!!\n")
                break

            elif cc.winner != 'NONE':
                print(f"\nWinner is {cc.winner}\n")
                break

            cc.event = ''

            # # prints top card
            # print("\n+" + "-"*(13+len(top_card.show())) + "+")
            print("|" + f" Top card = {cc.top_card.show()} " + "|")
            # print("+" + "-"*(13+len(top_card.show())) + "+")
            
            print(f"Your cards: {cc.player_hand.show()}")
            
            if cc.playerTurn == cc.playerName:

                if client.event[cc.eventID] == 'regular':
                    played_card = 0
                    fake_hand = uno.Stack()
                    fake_hand.add(cc.player_hand.stack)
                    cc.playable_cards = uno.isPlayable(cc.top_card, fake_hand, cc.chosenColour)

                    while True:
                        # Traps the user until input is received
                        if cc.currentChoice is not None:
                            # find cc.currentChoice in playable cards
                            for i in range(len(cc.playable_cards.stack)):
                                if cc.currentChoice == cc.playable_cards.stack[i]:
                                    played_card = i+1
                            cc.currentChoice = None
                        else:
                            continue

                        if played_card > 0 and played_card <= len(cc.playable_cards.stack):
                            print(f'pc: {played_card}')
                            # print(f"Card played: {cc.playable_cards.stack[played_card-1].show()}")
                            if cc.playable_cards.stack[played_card-1].card['colour'] == 'X':
                                cc.colourChange = 0
                                cc.event = 'colour_change'

                                while True:
                                    if cc.colourChange in ['R','B','G','Y']:
                                        client.colour = cc.colourChange
                                        cc.colourChange = None
                                        break

                                client.choice = played_card
                            else:
                                client.choice = played_card
                                client.colour = '0'
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(cc.playable_cards.stack)}")

                    cc.playable_cards = None
                elif client.event[cc.eventID] == 'no_cards':
                    print(f"Your turn {client.playerName}:")
                    print("You have no playable cards")
                    cc.event = 'no_cards'

                    cc.okPrompt = 0
                    while True:
                        if cc.okPrompt == 1:
                            cc.okPrompt = None
                            break

                    client.choice = '0'
                    client.colour = 'N'

                elif client.event[cc.eventID] == '+4/+2':
                    print(f"+{len(cc.drawn_cards.stack)} was used on you")
                    print(f"Cards drawn: {cc.drawn_cards.show()}")
                    cc.event = f'+{len(cc.drawn_cards.stack)}'

                    cc.okPrompt = 0
                    while True:
                        if cc.okPrompt == 1:
                            cc.okPrompt = None
                            break

                    client.choice = '0'
                    client.colour = 'N'

                elif client.event[cc.eventID] == 'skip':
                    print("Your turn was skipped.")
                    cc.event = 'skip'

                    cc.okPrompt = 0
                    while True:
                        if cc.okPrompt == 1:
                            cc.okPrompt = None
                            break

                    client.choice = '0'
                    client.colour = 'N'
            else:
                client.colour = '0'
                client.choice = '0'
                print("not my turn")

        except ValueError as e:
            print("BAD VALUE")
            print(e)
            print(f'{data=}')


def start():
    if cc.host is True:
        if config.platform == 'Windows':
            subprocess.Popen([sys.executable, f'src/uno_server.py', f'{cc.settings}'],
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
        # else:
            # subprocess.Popen(['python3.10', f'src/uno_server.py', f'{config.settings}'],
            #                 shell=False)
            # os.system(f'python3 src/uno_server.py {config.settings}')

        # print("before exec")
        threading.Thread(target=display, args=('localhost:5555',)).start()
        # print("exec")
        
    elif cc.host is False:
        threading.Thread(target=display, args=(cc.settings,)).start()