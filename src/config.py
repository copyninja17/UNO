try:
    from src import uno_module as uno
except:
    import uno_module as uno

'''
Holds global variables for all scripts to access
'''
#-----------------------------------
# Backend
#----------------------------------- 

myDeck = uno.Deck()
myDeck.shuffle()

myPreparations_complete = False

myDiscard_pile = uno.Stack()
myDiscard_pile.add(myDeck.deal(1))

myStorage = 0

myPlayerList = []

myPlayers = []

myReplies={}

actionEffect = False

assumedColour = '0'

Winner = 'NONE'


#-----------------------------------
# GUI
#----------------------------------- 

host = None

settings = None

playerName = ''

buttonUpdate = 0

Page = 0

lastPage = None

waitingTime = 0

buttonFlip = 1

counter = 0