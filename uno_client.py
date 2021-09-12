import os
from bridge import Network
import uno_module as uno
import time

'''
Missing features: Are you host?: add in a run file maybe
'''

address, port = input("Enter Server Address: ").split(":")
# address, port = "localhost", "5555"

class Client():

    def __init__(self):
        self.net = Network(address, port)
        self.choice = 0
        self.colour = '0'
        self.event = ['0', 'regular', 'no_cards', '+4/+2', 'reverse', 'skip']
        self.playerName = uno.Input("Enter your name: ", str, 3)
        self.playerList = []

    @staticmethod
    def parse(data):
        '''
        decodes received data
        data form: "topCard:playerHand:responseID:cardList:playerTurn"
        [TODO]: what's going on in the game unrelated to the player
        '''
        if ':' not in data:
            try:
                print(f"Player list retrived: {data}")
                return data

            except ValueError or TypeError or IndexError:
                print("ERROR RETRIEVING DATA FROM SERVER!")
                return 0
        else:
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

                return top_card, player_hand, eventID, drawn_cards, playerTurn, winner

            except ValueError or TypeError or IndexError:
                print("ERROR RETRIEVING DATA FROM SERVER!")
                return 0, 0, 0, 0, 0

    def send_recv(self, oneTime=False):
        '''
        sends data and returns reply
        '''
        if oneTime:
            reply = self.net.communicate(self.playerName)
            return reply
        else:
            data = str(self.net.id) + ":" + str(self.choice) + "," + str(self.colour)
            reply = self.net.communicate(data)
            return reply


client = Client()
temp = 'NEW'

# one time data
client.playerList = client.parse(client.send_recv(oneTime=True))
while True:
    data = client.send_recv()

    # so the client won't refresh always
    if temp == data:
        continue
    else:
        temp = data

    top_card, player_hand, eventID, drawn_cards, playerTurn, winner = client.parse(data)

    # winner/loser
    if winner == client.playerName:
        print("\nYOU ARE THE WINNER!!\n")
        print("Press 'enter' to continue")
        while True:
            x = input()
            if x == '':
                break
        break
    elif winner != 'NONE':
        print(f"\nWinner is {winner}\n")
        print("Press 'enter' to continue")
        while True:
            x = input()
            if x == '':
                break
        break

    os.system('cls')
    # print(data)
    print("\n+" + "-"*(13+len(top_card.show())) + "+")
    print("|" + f" Top card = {top_card.show()} " + "|")
    print("+" + "-"*(13+len(top_card.show())) + "+")
    
    print(f"Your cards: {player_hand.show()}")
    
    if playerTurn is True:

        if client.event[eventID] == 'regular':
            print(f"Your turn {client.playerName}: ")
            playable_cards = uno.isplayable(top_card, player_hand)
            try:
                print(f"Playable cards: {playable_cards.show()}")
            except:
                print(f"Playable cards: {playable_cards}")

            while True:
                played_card = uno.Input("Play a card: ", int)

                if played_card > 0 and played_card <= len(playable_cards.stack):
                    print(f"Card played: {playable_cards.stack[played_card-1].show()}")
                    if playable_cards.stack[played_card-1].card['colour'] == 'None':
                        client.colour = uno.colour_switch()
                        client.choice = played_card
                    else:
                        client.choice = played_card
                        client.colour = '0'
                    break
                else:
                    print(f"Please enter a number between 1 and {len(playable_cards.stack)}")

        elif client.event[eventID] == 'no_cards':
            print(f"Your turn {client.playerName}:")
            print("You have no playable cards")
            print(f"Card drawn: {drawn_cards.show()}")
            print("Press 'enter' to continue")
            while True:
                x = input()
                if x == '':
                    break
            client.choice = '0'
            client.colour = 'N'

        elif client.event[eventID] == '+4/+2':
            print(f"+{len(drawn_cards.stack)} was used on you")
            print(f"Cards drawn: {drawn_cards.show()}")
            print("Press 'enter' to continue")
            while True:
                x = input()
                if x == '':
                    break
            client.choice = '0'
            client.colour = 'N'

        elif client.event[eventID] == 'skip':
            print("Your turn was skipped.")
            print("Press 'enter' to continue")
            while True:
                x = input()
                if x == '':
                    break
            client.choice = '0'
            client.colour = 'N'
    else:
        client.colour = '0'
        client.choice = '0'
        print("not my turn")