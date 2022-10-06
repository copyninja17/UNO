'''
Holds global variables for all scripts to access
'''

from src import uno_module as uno

#-----------------------------------
# Backend
#----------------------------------- 

myDeck = uno.Deck()
myDeck.shuffle()

myPreparations_complete = False

myDiscard_pile = uno.Stack()

myStorage = 0

myPlayerList = []

playerCount = 0

myPlayers = []

myReplies={}

actionEffect = False

assumedColour = '0'

Winner = 'NONE'

SERVER_EXIT = False

currentId = '0'