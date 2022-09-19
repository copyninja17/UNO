'''
Holds global variables for all scripts to access
'''

try:
    from src import uno_module as uno
except:
    import uno_module as uno

#-----------------------------------
# Backend
#----------------------------------- 

platform = None

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


#-----------------------------------
# GUI
#----------------------------------- 

host = None

settings = None

buttonUpdate = 0

Page = 0

lastPage = None

waitingTime = 0

buttonFlip = 1

counter = 0
