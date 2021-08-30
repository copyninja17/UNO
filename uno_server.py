import uno_module as uno
import os
import uno_ai as ai
import time
import socket
from _thread import *


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

# declarations
currentId = "0"
playerList = []
sample_data = "4R:6B,3G,8Y,9R:3:0:0"


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
                    reply = sample_data
                else:  # if client requests playerList
                    playerList.append(reply)
                    name = reply

                    while True:
                        if len(playerList) == roomSize:
                            reply = ",".join(playerList)
                            prepare()
                            print(f"Sending to : " + reply)
                            break

                        elif len(playerList) != roomSize:
                            os.system('cls')
                            print(f"players joined({roomSize-len(playerList)}/{roomSize})")
                            print("Waiting...")

            conn.sendall(str.encode(reply))
        except:
            print("break from threaded_client")
            break

    print("Connection Closed")
    conn.close()


def prepare():
    print("preparing")

    global deck
    deck = uno.Deck()
    deck.shuffle()

    for i in range(roomSize):
        stack = uno.Stack()
        stack.add(deck.deal(7))
        # playerList[i]['hand'] = stack

    while True:
        if deck.deck[0].card['val'] == '+4':
            deck.shuffle()
        else:
            break
    global discard_pile
    discard_pile = uno.Stack()
    discard_pile.add(deck.deal(1))
    print("preparations complete")


def Deal(n):  # deals cards to players whenever required
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


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))

    try:
        if len(playerList[0]['hand'].stack) == 0:
            print(f"Winner is {playerList[0]['name']}!!")
            match = False
            break
        # if data is received from client
        #     discard_pile.add(playable_cards.deal(0, played_card-1))
        #     print(f"Card played: {discard_pile.stack[-1].show()}")
        #     players[0]['hand'].add(playable_cards.stack)

    except:
        print("not yet started")
        continue
