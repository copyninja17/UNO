import uno_module as uno
import os
import uno_ai as ai
import time
import socket
from _thread import *
import threading
from config import *

# globals
deck = myDeck
discard_pile = myDiscard_pile
storage = myStorage
preparations_complete = myPreparations_complete
playerList = myPlayerList
players = myPlayers
replies = myReplies

# local declarations
currentId = "0"
# sample_data = "4R:6B,3G,8Y,9R:3:0:0"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

roomSize = 2  # will actually come from host client

s.listen(roomSize)
print("Waiting for a connection")


def parse(message):
    id = message.split(":")[0]
    choice = int(message.split(":")[1].split(",")[0])
    colour = message.split(":")[1].split(",")[1]
    return choice, colour

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def prepare():
    print("preparing")

    # creating deck
    # global deck
    # deck = uno.Deck()
    # deck.shuffle()
    # print("deck generated")

    # generate name: hand: dict pairs(update players)
    for i in range(roomSize):
        sample_dict = {'name': 0, 'hand': 0}
        sample_dict['name'] = playerList[i]
        stack = uno.Stack()
        stack.add(deck.deal(7))
        sample_dict['hand'] = stack
        players.append(sample_dict)
    print("players ready")

    # doesn't allow +4 on irst turn
    while True:
        if deck.deck[0].card['val'] == '+4':
            deck.shuffle()
        else:
            break
    print("+4 clause")

    # creating discard pile
    # global discard_pile
    # discard_pile = uno.Stack()
    # discard_pile.add(deck.deal(1))
    # print("discard pile generated")

    # creating replies
    for i in playerList:
        sample_dict = {'choice':0, 'colour':0}
        replies[i] = sample_dict
    print("replies ready")

    preparations_complete = True
    print("preparations complete")


def Deal(n):  # deals cards to players from deck
    dealt_cards = []
    rem = n
    if len(deck.deck) < n:
        dealt_cards += deck.deck
        rem = n - len(dealt_cards)
        deck.deck = list(discard_pile.stack)
        discard_pile.stack.clear()
        discard_pile.stack.append(deck.deck.pop())
        deck.shuffle()
    return deck.deal(rem) + dealt_cards


def database(name, eventID, drawn_cards=0):
    '''
    stores data for all clients to take from
    '''
    lst = {}
    for i in range(len(players)):
        playerTurn = 0
        print(f"players = {players[i]}")
        if name == players[i]['name']:
            playerTurn = 1
        else:
            eventID = 0
            drawn_cards = 0
        lst[players[i]['name']] = discard_pile.stack[-1].conv() + ":" + players[i]['hand'].conv() + ":" + str(eventID) + ":" + str(drawn_cards) + ":" + str(playerTurn)
    return lst

def threaded_server():
    # global storage
    while True:
        if roomSize == len(playerList):
            prepare()
        else:
            continue

        if len(players[0]['hand'].stack) == 0:
            print(f"Winner is {playerList[0]['name']}!!")
            break

        if uno.isaction(discard_pile.stack[-1]) == 'none':
            # write normal code
            playable_cards = uno.isplayable(discard_pile.stack[-1], players[0]['hand'])
            if playable_cards != 'None':
                storage = database(players[0]['name'], 1)
                while True:                    
                    # trapping until input is recieved
                    choice = replies[players[0]['name']]['choice']

                    if choice != 0:
                        played_card = playable_cards.stack[choice-1]
                        discard_pile.add(playable_cards.deal(0, played_card-1))
                        players[0]['hand'].add(playable_cards.stack)  # at this point we have successfully played the card
                        break
            else:
                # no cards situation
                players[0]['hand'].add(Deal(1))
                storage = database(players[0]['name'], 2, [players[0]['hand'].stack[-1].conv()])

        # elif uno.isaction(discard_pile.stack[-1]) == 'wld':
        #     # write wild card code here
        #     # [TODO] YOU WERE SUPPOSED TO CHOOSE A COLOUR, YET YOU CHOSE AN EASIER PATH
        #     pass
        
        else:
            # write action code
            if uno.isaction(discard_pile.stack[-1]) == 'skp':
                storage = database(players[0]['name'], 5)

            elif uno.isaction(discard_pile.stack[-1]) == '+2':
                players[0]['hand'].add(Deal(2))
                drawn_cards = [players[0]['hand'].stack[-1].conv(), players[0]['hand'].stack[-2].conv()]
                storage = database(players[0]['name'], 3, drawn_cards)

            elif uno.isaction(discard_pile.stack[-1]) == 'rev':
                storage = database(players[0]['name'], 4)
                players.reverse()
                players.append(players.pop(0))

        players.append(players.pop(0))


th = threading.Thread(target=threaded_server)
th.start()


def threaded_client(conn):
    global currentId
    conn.send(str.encode(currentId))
    currentId = str(int(currentId) + 1)
    reply = ''
    name = f"player-{currentId}"
    while True:
        try:
            print(f"hi my name is: {name}")
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                if ":" in reply:  # if client requests game data
                    replies[name]['choice'], replies[name]['colour'] = parse(reply)
                    reply = storage[name]
                    conn.sendall(str.encode(reply))
                    storage = database(0,0)

                else:  # if client requests playerList
                    playerList.append(reply)
                    name = reply

                    while True:  # trap until all players join
                        if (len(playerList) == roomSize):# and (preparations_complete == True):
                            reply = ",".join(playerList)
                            print(f"Sending to : " + reply)
                            time.sleep(5)
                            break

                        else:
                            # os.system('cls')
                            print(f"players joined({len(playerList)}/{roomSize})")
                            print("Waiting...")
                            time.sleep(5)
                    conn.sendall(str.encode(reply))
            # conn.sendall(str.encode(reply))
        except:
            print("break from threaded_client")
            raise
            # break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))





















# while True:
#     try:
#         conn, addr = s.accept()
#         print("Connected to: ", addr)
#         start_new_thread(threaded_client, (conn,))

#         if roomSize == len(playerList):
#             prepare()

#         if len(playerList[0]['hand'].stack) == 0:
#             print(f"Winner is {playerList[0]['name']}!!")
#             break

#         storage = database(players[0]['name'], 1)  # exchange data here / update database

#         # check if player can play
#         if playable_cards is not 'None':
#             while True:
#                 choice = replies[players[0]['name']]['choice']
#                 colour = replies[players[0]['name']]['colour']
#                 playable_cards = uno.isplayable(discard_pile.stack[-1], players[0]['hand'])
                
#                 if playable_cards is not 'None':
#                     while True:
                    
#                         if choice != 0:
#                             played_card = playable_cards.stack[choice-1]
#                             discard_pile.add(playable_cards.deal(0, played_card-1))
#                             players[0]['hand'].add(playable_cards.stack)  # at this point we have successfully played the card

#                             break
#                         else:
#                             break

#         # calculate(change the order too?)

#     except:
#         print("not yet started")
#         continue
