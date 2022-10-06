'''
Multithreaded Server for UNO.

Handles all transactions and calculations related to players and cards.
'''

# try:
from src import uno_module as uno
from src import config as c
# except:
#     import uno_module as uno
#     import config as c

import socket
from _thread import *
import threading
import sys
import os
import logging
from datetime import datetime
from pathlib import Path as PATH



def main(roomSize=None):
    #############################
    # Logging
    #############################

    try:
        os.mkdir(f"{PATH(__file__).parent.absolute()}/logs")
    except:
        pass

    d1 = (f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}")
    i = 0
    while True:
        if f'server_{d1}_{i}.log' in os.listdir(f"{PATH(__file__).parent.absolute()}/logs"):
            i+=1
        else:
            logname = f'{PATH(__file__).parent.absolute()}/logs/server_{d1}_{i}.log'
            break

    logging.basicConfig(filename=logname,
                        filemode='a',
                        format="[ {asctime} ][ {levelname} ] {message}",
                        level=logging.DEBUG,
                        style='{')


    #############################
    # Networking setup
    #############################

    c.currentId = '0'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server = 'localhost'
    port = 5555

    server_ip = socket.gethostbyname(server)

    try:
        s.bind((server, port))

    except socket.error as e:
        logging.error(str(e))

    s.listen(roomSize)
    logging.info("Waiting for a connection")


    #############################
    # Helper functions
    #############################

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
                str(dct['players']) + ':' + 
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

        # creating 'playername=handsize' string once
        players = []
        for player in c.myPlayers:
            player = [player['name'], str(player['hand'].size())]
            players.append('='.join(player))
        
        players = ','.join(players) # reusing the same variable

        dct = {}
        for i in range(len(c.myPlayers)):
            if name != c.myPlayers[i]['name']:
                eventID = 0
                drawnCards = '00'
            dct[c.myPlayers[i]['name']] = {'topCard': c.myDiscard_pile.stack[-1].conv(),
                                                'hand': c.myPlayers[i]['hand'].conv(),
                                                'eventID': eventID,
                                                'playerTurn': name,
                                                'drawnCards': drawnCards,
                                                'players': players,
                                                'winner': c.Winner,
                                                'chosenColour': c.assumedColour}
        return dct


    @run_once
    def prepare():
        '''
        preapares stuff before starting server
        '''
        logging.info("Preparing cards")

        for i in range(roomSize):
            sample_dict = {'name': 0, 'hand': 0}
            sample_dict['name'] = c.myPlayerList[i]
            stack = uno.Stack()
            stack.add(c.myDeck.deal(7))
            sample_dict['hand'] = stack
            c.myPlayers.append(sample_dict)
        logging.info("c.myPlayers ready")

        # doesn't allow +4 on first turn
        while True:
            if c.myDeck.deck[0].card['colour'] == 'X':
                c.myDeck.shuffle()
            else:
                break
        
        c.myDiscard_pile.add(c.myDeck.deal(1))
        
        # creating c.myReplies
        for i in c.myPlayerList:
            sample_dict = {'choice': '0', 'colour': '0'}
            c.myReplies[i] = sample_dict
        logging.info("c.myReplies ready")

        c.myStorage = database()

        c.myPreparations_complete = True
        logging.info("Preparations complete")


    def Deal(n):
        '''
        Deals cards to players from deck.
        Also refills deck from discard pile.
        '''
        dealt_cards = []
        rem = n
        if len(c.myDeck.deck) < n:
            dealt_cards += c.myDeck.deck
            rem = n - len(dealt_cards)
            c.myDeck.deck = list(c.myDiscard_pile.stack)
            c.myDiscard_pile.stack.clear()
            c.myDiscard_pile.stack.append(c.myDeck.deck.pop())
            c.myDeck.shuffle()
        return c.myDeck.deal(rem) + dealt_cards


    #############################
    # Logic Segment
    #############################

    def threaded_server():
        '''
        starts server in a separate thread
        '''
        while True:
            try:
                if roomSize == len(c.myPlayerList):    prepare()
                else:                                       continue

                logging.info(f"It's {c.myPlayers[0]['name']} turn")

                if c.actionEffect == False:
                    copied_hand = uno.Stack()
                    lst = list(c.myPlayers[0]['hand'].stack)
                    copied_hand.add(lst)

                    playable_cards = uno.isPlayable(
                        c.myDiscard_pile.stack[-1], copied_hand, c.assumedColour)

                    if playable_cards != 'None':
                        logging.info(f"{c.myPlayers[0]['name']} has playable cards")
                        c.myStorage = database(c.myPlayers[0]['name'], 1)
                        while True:
                            # trapping until input is recieved
                            choice = int(
                                c.myReplies[c.myPlayers[0]['name']]['choice'])
                            if choice != 0:
                                logging.info(f"{c.myPlayers[0]['name']} has chosen a card")
                                c.assumedColour = c.myReplies[c.myPlayers[0]
                                                                        ['name']]['colour']
                                played_card = choice-1
                                c.myDiscard_pile.add(
                                    playable_cards.deal(0, played_card))
                                copied_hand.add(playable_cards.stack)
                                c.myPlayers[0]['hand'].clear()

                                # at this point we have successfully played the card
                                c.myPlayers[0]['hand'].add(copied_hand.stack)
                                logging.info(f"remaining hand: {c.myPlayers[0]['hand'].show()}")
                                logging.info(f"hand length = {len(c.myPlayers[0]['hand'].stack)}")

                                if (uno.isAction(c.myDiscard_pile.stack[-1]) != 'None' and 
                                    c.myDiscard_pile.stack[-1].card['val'] != 'wild'):
                                    c.actionEffect = True

                                if len(c.myPlayers[0]['hand'].stack) == 0:
                                    logging.info(f"Winner is {c.myPlayers[0]['name']}!!")
                                    c.Winner = str(c.myPlayers[0]['name'])
                                    # c.SERVER_EXIT = True
                                    c.myPlayers[0]['hand'].add(c.myDiscard_pile.deal(0,0))
                                break

                        if uno.isAction(c.myDiscard_pile.stack[-1]) == 'rev':
                            c.actionEffect = False
                            c.myPlayers.reverse()
                            continue

                    else:
                        # no cards situation
                        logging.info(f"{c.myPlayers[0]['name']} has NO playable cards")
                        c.myPlayers[0]['hand'].add(Deal(1))

                        c.myStorage = database(c.myPlayers[0]['name'], 2, 
                                                    c.myPlayers[0]['hand'].stack[-1].conv())

                        while True:
                            # trapping until input is recieved
                            colour = c.myReplies[c.myPlayers[0]['name']]['colour']
                            if colour == 'N':  # N = Nil[client has received data]
                                logging.info(f"{c.myPlayers[0]['name']} has received his card")
                                break

                    c.myPlayers.append(c.myPlayers.pop(0))

                else:
                    logging.info(f"{c.myPlayers[0]['name']} is facing an action situation")

                    # write action code
                    if uno.isAction(c.myDiscard_pile.stack[-1]) == 'skp':
                        c.actionEffect = False
                        c.myStorage = database(c.myPlayers[0]['name'], 5)

                        while True:
                            # trapping until input is recieved
                            colour = c.myReplies[c.myPlayers[0]['name']]['colour']
                            if colour == 'N':  # N = Nil[client has received data]
                                logging.info(f"{c.myPlayers[0]['name']} has agreed")
                                break
                        c.myPlayers.append(c.myPlayers.pop(0))

                    elif uno.isAction(c.myDiscard_pile.stack[-1]) == '+2':
                        c.actionEffect = False
                        c.myPlayers[0]['hand'].add(Deal(2))
                        drawn_cards = (c.myPlayers[0]['hand'].stack[-1].conv() + "," + 
                                    c.myPlayers[0]['hand'].stack[-2].conv())
                        c.myStorage = database(c.myPlayers[0]['name'], 3, 
                                                    drawn_cards)
                        while True:
                            # trapping until input is recieved
                            colour = c.myReplies[c.myPlayers[0]['name']]['colour']
                            if colour == 'N':  # N = Nil[client has received data]
                                logging.info(f"{c.myPlayers[0]['name']} has received 2 cards")
                                break
                        c.myPlayers.append(c.myPlayers.pop(0))

                    elif uno.isAction(c.myDiscard_pile.stack[-1]) == '+4':
                        c.actionEffect = False
                        c.myPlayers[0]['hand'].add(Deal(4))
                        drawn_cards = (c.myPlayers[0]['hand'].stack[-1].conv() + "," + 
                                    c.myPlayers[0]['hand'].stack[-2].conv() + "," + 
                                    c.myPlayers[0]['hand'].stack[-3].conv() + "," + 
                                    c.myPlayers[0]['hand'].stack[-4].conv())
                        c.myStorage = database(
                            c.myPlayers[0]['name'], 3, drawn_cards)
                        while True:
                            # trapping until input is recieved
                            colour = c.myReplies[c.myPlayers[0]
                                                    ['name']]['colour']
                            if colour == 'N':  # N = Nil[client has received data]
                                logging.info(f"{c.myPlayers[0]['name']} has received four cards")
                                break
                        c.myPlayers.append(c.myPlayers.pop(0))

                # if c.SERVER_EXIT:
                #     print("Game ends\nThank you for playing!")
                #     break

            except KeyboardInterrupt:
                c.SERVER_EXIT = True
                break
            except Exception as e:
                raise


    th = threading.Thread(target=threaded_server)
    th.start()


    #############################
    # Client-comm handler
    #############################

    def threaded_client(conn):
        '''
        runs new threads for new clients
        '''
        conn.send(str.encode(c.currentId))
        c.currentId = str(int(c.currentId) + 1)
        reply = ''
        name = f"player-{c.currentId}"
        while True:
            # if c.SERVER_EXIT:  break

            try:
                data = conn.recv(2048)
                reply = data.decode('utf-8')
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    if ":" in reply:  # if client requests game data
                        # print(name)
                        c.myReplies[name]['choice'], c.myReplies[name]['colour'] = parse(
                            reply)
                        if c.myReplies[name]['choice'] != '0':
                            c.myStorage[name]['playerTurn'] = '0'
                            c.myStorage[name]['eventID'] = '0'
                            reply = encode(c.myStorage[name])
                            logging.info(f"Data sent to name: {reply}")
                        else:
                            reply = encode(c.myStorage[name])

                    else:  # if client requests c.myPlayerList
                        c.myPlayerList.append(reply)
                        name = reply
                        while True:  # trap until all Players join
                            if ((len(c.myPlayerList) == roomSize) and 
                                c.myPreparations_complete):
                                reply = ','.join(c.myPlayerList)
                                logging.info(f"Sending playerList: {reply}")
                                break
                            elif len(c.myPlayerList) != c.playerCount:
                                logging.info(
                                    f"c.myPlayers joined({len(c.myPlayerList)}/{roomSize})")
                                logging.info("Waiting...")
                                c.playerCount = len(c.myPlayerList)
                                
                        logging.info(f"Sending to {name}: {reply}")

                    conn.sendall(str.encode(reply))

            except KeyboardInterrupt:
                c.SERVER_EXIT = True
                break
            except Exception as e:
                logging.error("Break from threaded_client")
                logging.error(e)
                raise

        logging.warning(f"Connection Closed for {name}")
        conn.close()


    while True:
        '''
        manages new players
        '''
        try:
            conn, addr = s.accept()
            logging.info(f"Connected to: {addr}")
            start_new_thread(threaded_client, (conn,))
        except KeyboardInterrupt:
            logging.info("server closed")
            c.SERVER_EXIT = True
            break

if __name__ == '__main__':
    roomSize = int(input("Enter room size: "))
    main(roomSize)