import uno_module as uno

myDeck = uno.Deck()
myDeck.shuffle()

myPreparations_complete = False

myDiscard_pile = uno.Stack()
myDiscard_pile.add(myDeck.deal(1))

myStorage = 0

myPlayerList = []

myPlayers = []

myReplies={}

Winner = 'NONE'