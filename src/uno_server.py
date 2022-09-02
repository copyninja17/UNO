'''
Multithreaded Server for UNO.

Handles all transactions and calculations related to players and cards.
'''

import uno_module as uno
import config

import socket
from _thread import *
import threading
import sys


# local declarations
currentId = "0"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

roomSize = int(sys.argv[1])

s.listen(roomSize)
print("Waiting for a connection")


def parse(message):
    '''
    decodes messages from clients
    '''
    id = message.split(":")[0]
    choice = message.split(":")[1].split(",")[0]
    colour = message.split(":")[1].split(",")[1]
    return choice, colour


def encode(dct):
    '''
    converts dct into sendable string
    '''
    string = (str(dct['topCard']) + ":" + 
              str(dct['hand']) + ":" + 
              str(dct['eventID']) + ":" + 
              str(dct['drawnCards']) + ":" + 
              str(dct['playerTurn']) + ":" + 
              str(dct['winner']) + ":" + 
              str(dct['chosenColour']))
    return string


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


def database(name='0', eventID=0, drawnCards='00'):
    '''
    stores data for all clients to take from
    '''
    dct = {}
    for i in range(len(config.myPlayers)):
        playerTurn = 0
        if name == config.myPlayers[i]['name']:
            playerTurn = 1
        else:
            eventID = 0
            drawnCards = '00'
        dct[config.myPlayers[i]['name']] = {'topCard': config.myDiscard_pile.stack[-1].conv(),
                                            'hand': config.myPlayers[i]['hand'].conv(),
                                            'eventID': eventID,
                                            'playerTurn': playerTurn,
                                            'drawnCards': drawnCards,
                                            'winner': config.Winner,
                                            'chosenColour': config.assumedColour}
    return dct


@run_once
def prepare():
    '''
    preapares stuff before starting server
    '''
    print("preparing")

    for i in range(roomSize):
        sample_dict = {'name': 0, 'hand': 0}
        sample_dict['name'] = config.myPlayerList[i]
        stack = uno.Stack()
        stack.add(config.myDeck.deal(7))
        sample_dict['hand'] = stack
        config.myPlayers.append(sample_dict)
    print("config.myPlayers ready")

    # doesn't allow +4 on first turn
    while True:
        if config.myDeck.deck[0].card['colour'] == 'X':
            config.myDeck.shuffle()
        else:
            break
    print("wild clause")

    # creating config.myReplies
    for i in config.myPlayerList:
        sample_dict = {'choice': '0', 'colour': '0'}
        config.myReplies[i] = sample_dict
    print("config.myReplies ready")

    config.myStorage = database()

    config.myPreparations_complete = True
    print("preparations complete")


def Deal(n):
    '''
    deals cards to players from deck
    '''
    dealt_cards = []
    rem = n
    if len(config.myDeck.deck) < n:
        dealt_cards += config.myDeck.deck
        rem = n - len(dealt_cards)
        config.myDeck.deck = list(config.myDiscard_pile.stack)
        config.myDiscard_pile.stack.clear()
        config.myDiscard_pile.stack.append(config.myDeck.deck.pop())
        config.myDeck.shuffle()
    return config.myDeck.deal(rem) + dealt_cards


def threaded_server():
    '''
    starts server in a separate thread
    '''
    while True:
        if roomSize == len(config.myPlayerList):
            prepare()
        else:
            continue

        print(f"it's {config.myPlayers[0]['name']} turn")
        if config.actionEffect == False:
            copied_hand = uno.Stack()
            lst = list(config.myPlayers[0]['hand'].stack)
            copied_hand.add(lst)

            playable_cards = uno.isPlayable(
                config.myDiscard_pile.stack[-1], copied_hand, config.assumedColour)

            if playable_cards != 'None':
                print(f"{config.myPlayers[0]['name']} has playable cards")
                config.myStorage = database(config.myPlayers[0]['name'], 1)
                while True:
                    # trapping until input is recieved
                    choice = int(
                        config.myReplies[config.myPlayers[0]['name']]['choice'])
                    if choice != 0:
                        print(f"{config.myPlayers[0]['name']} HAS CHOSEN")
                        config.assumedColour = config.myReplies[config.myPlayers[0]
                                                                ['name']]['colour']
                        played_card = choice-1
                        config.myDiscard_pile.add(
                            playable_cards.deal(0, played_card))
                        copied_hand.add(playable_cards.stack)
                        config.myPlayers[0]['hand'].clear()
                        # at this point we have successfully played the card
                        config.myPlayers[0]['hand'].add(copied_hand.stack)
                        print(
                            f"remaining hand: {config.myPlayers[0]['hand'].show()}")
                        print(
                            f"hand length = {len(config.myPlayers[0]['hand'].stack)}")

                        if (uno.isAction(config.myDiscard_pile.stack[-1]) != 'None' and 
                            config.myDiscard_pile.stack[-1].card['val'] != 'wild'):
                            config.actionEffect = True

                        if len(config.myPlayers[0]['hand'].stack) == 0:
                            print(f"Winner is {config.myPlayers[0]['name']}!!")
                            config.Winner = str(config.myPlayers[0]['name'])
                            config.myPlayers[0]['hand'].add(
                                config.myDiscard_pile.deal(0, 0))
                        break

            else:
                # no cards situation
                print(f"{config.myPlayers[0]['name']} has NO playable cards")
                config.myPlayers[0]['hand'].add(Deal(1))

                config.myStorage = database(config.myPlayers[0]['name'], 2, 
                                            config.myPlayers[0]['hand'].stack[-1].conv())

                while True:
                    # trapping until input is recieved
                    colour = config.myReplies[config.myPlayers[0]['name']]['colour']
                    if colour == 'N':  # N = Nil[client has received data]
                        print(f"{config.myPlayers[0]['name']} HAS RECEIVED")
                        break

            if uno.isAction(config.myDiscard_pile.stack[-1]) == 'rev':
                config.actionEffect = False
                config.myPlayers.reverse()
                continue

            config.myPlayers.append(config.myPlayers.pop(0))

        else:
            print(
                f"{config.myPlayers[0]['name']} is facing an action situation")

            # write action code
            if uno.isAction(config.myDiscard_pile.stack[-1]) == 'skp':
                config.actionEffect = False
                config.myStorage = database(config.myPlayers[0]['name'], 5)

                while True:
                    # trapping until input is recieved
                    colour = config.myReplies[config.myPlayers[0]['name']]['colour']
                    if colour == 'N':  # N = Nil[client has received data]
                        print(f"{config.myPlayers[0]['name']} HAS RECEIVED")
                        break
                config.myPlayers.append(config.myPlayers.pop(0))

            elif uno.isAction(config.myDiscard_pile.stack[-1]) == '+2':
                config.actionEffect = False
                config.myPlayers[0]['hand'].add(Deal(2))
                drawn_cards = (config.myPlayers[0]['hand'].stack[-1].conv() + "," + 
                               config.myPlayers[0]['hand'].stack[-2].conv())
                config.myStorage = database(config.myPlayers[0]['name'], 3, 
                                            drawn_cards)
                while True:
                    # trapping until input is recieved
                    colour = config.myReplies[config.myPlayers[0]['name']]['colour']
                    if colour == 'N':  # N = Nil[client has received data]
                        print(f"{config.myPlayers[0]['name']} HAS RECEIVED")
                        break
                config.myPlayers.append(config.myPlayers.pop(0))

            elif uno.isAction(config.myDiscard_pile.stack[-1]) == '+4':
                config.actionEffect = False
                config.myPlayers[0]['hand'].add(Deal(4))
                drawn_cards = (config.myPlayers[0]['hand'].stack[-1].conv() + "," + 
                               config.myPlayers[0]['hand'].stack[-2].conv() + "," + 
                               config.myPlayers[0]['hand'].stack[-3].conv() + "," + 
                               config.myPlayers[0]['hand'].stack[-4].conv())
                config.myStorage = database(
                    config.myPlayers[0]['name'], 3, drawn_cards)
                while True:
                    # trapping until input is recieved
                    colour = config.myReplies[config.myPlayers[0]
                                              ['name']]['colour']
                    if colour == 'N':  # N = Nil[client has received data]
                        print(f"{config.myPlayers[0]['name']} HAS RECEIVED")
                        break
                config.myPlayers.append(config.myPlayers.pop(0))


th = threading.Thread(target=threaded_server)
th.start()


def threaded_client(conn):
    '''
    runs new threads for new clients
    '''
    global currentId
    conn.send(str.encode(currentId))
    currentId = str(int(currentId) + 1)
    reply = ''
    name = f"player-{currentId}"
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                if ":" in reply:  # if client requests game data
                    print(name)
                    config.myReplies[name]['choice'], config.myReplies[name]['colour'] = parse(
                        reply)
                    if config.myReplies[name]['choice'] != '0':
                        config.myStorage[name]['playerTurn'] = '0'
                        config.myStorage[name]['eventID'] = '0'
                        reply = encode(config.myStorage[name])
                        print(f"Latest reply = {reply}")
                    else:
                        reply = encode(config.myStorage[name])

                else:  # if client requests config.myPlayerList
                    config.myPlayerList.append(reply)
                    name = reply
                    while True:  # trap until all Players join
                        if ((len(config.myPlayerList) == roomSize) and 
                            config.myPreparations_complete):
                            reply = ",".join(config.myPlayerList)
                            print(f"Sending to : " + reply)
                            break
                        else:
                            print(
                                f"config.myPlayers joined({len(config.myPlayerList)}/{roomSize})")
                            print("Waiting...")
                    print(f"Sending to {name}: {reply}")

                conn.sendall(str.encode(reply))
        except:
            print("break from threaded_client")
            raise

    print("Connection Closed")
    conn.close()


while True:
    '''
    manages new players
    '''
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))
