from pages.startGame import printHand
from src import config
from src.bridge import Network
from src import uno_module as uno
import os, subprocess, sys
import multiprocessing as mp
import threading
from src import clientConfig as cc

class Client:

    def __init__(self, address, port):
        '''
        Initializes the Client.
        '''

        self.net = Network(address, port)
        self.choice = 0
        self.colour = '0'
        self.event = ['0', 'regular', 'no_cards', '+4/+2', 'reverse', 'skip', 'wild']
        self.playerName = config.playerName
        self.playerList = []

    @staticmethod
    def parse(data):
        '''
        Decodes received data from server

        Data form: "topCard: playerHand: responseID: cardList: playerTurn: winner: chosenColour"
        [TODO]: what's going on in the game unrelated to the player
        '''

        if ':' not in data:
            # playerList received
            try:
                print(f"Player list retrived: {data}")
                return data

            except ValueError or TypeError or IndexError:
                print("ERROR RETRIEVING DATA FROM SERVER!")
                return 0
        else:
            # game data received
            try:
                top_card = uno.Card()
                top_card.generate(data.split(":")[0][-1], data.split(":")[0][:-1])

                player_hand = uno.Stack()
                for i in list(data.split(":")[1].split(",")):
                    sample = uno.Card()
                    sample.generate(i[-1], i[:-1])
                    player_hand.add(sample)

                eventID = int(data.split(":")[2])

                drawn_cards = uno.Stack()
                for i in list(data.split(":")[3].split(",")):
                    sample = uno.Card()
                    sample.generate(i[-1], i[:-1])
                    drawn_cards.add(sample)

                playerTurn = bool(int(data.split(":")[4]))

                winner = data.split(":")[5]

                chosenColour = data.split(":")[6]

                # return cc.top_card, cc.player_hand, cc.eventID, cc.drawn_cards, cc.playerTurn, cc.winner, cc.chosenColour
                return top_card, player_hand, eventID, drawn_cards, playerTurn, winner, chosenColour

            except ValueError or TypeError or IndexError:
                print("ERROR RETRIEVING DATA FROM SERVER!")
                return 0, 0, 0, 0, 0

    def send_recv(self, oneTime=False):
        '''
        Sends data to server and returns reply.

        ontTime: If True, exchanges playerName with playerList.
        '''

        if oneTime:
            reply = self.net.communicate(self.playerName)
            return reply
        else:
            data = str(self.net.id) + ":" + str(self.choice) + "," + str(self.colour)
            reply = self.net.communicate(data)
            return reply


def run_once(f):
    '''
    lets a function run only once
    '''
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


# @run_once
def display(addrPort):
    address, port = addrPort.split(':')

    client = Client(address, port)
    oldData = 'NEW'

    # Retrieve playerList (one time data)
    client.playerList = client.parse(client.send_recv(oneTime=True))

    while True:
        data = client.send_recv()

        # so the client won't refresh always
        if oldData == data:
            continue
        else:
            oldData = data

        # # data received
        # top_card, player_hand, eventID, drawn_cards, playerTurn, winner, chosenColour = client.parse(data)
        cc.top_card, cc.player_hand, cc.eventID, cc.drawn_cards, cc.playerTurn, cc.winner, cc.chosenColour = client.parse(data)

        # winner/loser
        if cc.winner == client.playerName:
            print("\nYOU ARE THE WINNER!!\n")

        elif cc.winner != 'NONE':
            print(f"\nWinner is {cc.winner}\n")
        # os.system('cls')

        # # prints top card
        # print("\n+" + "-"*(13+len(top_card.show())) + "+")
        print("|" + f" Top card = {cc.top_card.show()} " + "|")
        # print("+" + "-"*(13+len(top_card.show())) + "+")
        
        print(f"Your cards: {cc.player_hand.show()}")
        
        if cc.playerTurn is True:
            if client.event[cc.eventID] == 'regular':
        #         print(f"\nYour turn {client.playerName}:\n")
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
                            client.colour = uno.colourSwitch()
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
                # print(f"Card drawn: {cc.drawn_cards.show()}")

                # print("Press 'enter' to continue")
                # while True:
                #     # convert into a separate 'ENTER' function [FIXME]
                #     x = input()
                #     if x == '':
                        # break
                client.choice = '0'
                client.colour = 'N'

            elif client.event[cc.eventID] == '+4/+2':
                print(f"+{len(cc.drawn_cards.stack)} was used on you")
                print(f"Cards drawn: {cc.drawn_cards.show()}")

                print("Press 'enter' to continue")
                # while True:
                #     # convert into a separate 'ENTER' function [FIXME]
                #     x = input()
                #     if x == '':
                #         break
                client.choice = '0'
                client.colour = 'N'

            elif client.event[cc.eventID] == 'skip':
                print("Your turn was skipped.")

                print("Press 'enter' to continue")
                # while True:
                #     # convert into a separate 'ENTER' function [FIXME]
                #     x = input()
                #     if x == '':
                #         break
                client.choice = '0'
                client.colour = 'N'
        else:
            client.colour = '0'
            client.choice = '0'
            print("not my turn")


def start():
    if config.host is True:
        subprocess.Popen([sys.executable, f'src/uno_server.py', f'{config.settings}'],
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("before exec")
        threading.Thread(target=display, args=('localhost:5555',)).start()
        print("exec")
        
    elif config.host is False:
        threading.Thread(target=display, args=(config.settings,)).start()