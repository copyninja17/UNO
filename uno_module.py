# import pydealer as pd
import random

class Card():

    def __init__(self):
        self.card = {'colour':0, 'val':0}
        self = self.card

    def generate(self, colour, value):
        self.card['colour'] = colour
        self.card['val'] = value

    def show(self):
        string = str(self.card['val']) + " of " + str(self.card['colour'])
        return string



class Deck():
    
    def __init__(self):
        self.colours = ['B', 'G', 'R', 'Y']
        self.values = ['1', '2', '3', '4', '5', '6', '7', '8' ,'9', 'skip', 'reverse', '+2']
        # self.special = ['wild', 'draw 4']
        # self.extras = ['0']
        self.deck = []
        self.build_deck()
        self = self.deck


    def build_deck(self):
        for c in self.colours:
            for v in self.values:
                sample = Card()
                sample.generate(c,v)
                self.deck.append(sample)

    def show(self):
        lst = []
        for i in range(len(self.deck)):
            string = self.deck[i].show()
            lst.append(string)
        return lst

    def deal(self, n):
        dealt_cards = []
        for _ in range(n):
            dealt_cards.append(self.deck.pop(0))
        return dealt_cards
    
    def shuffle(self):
        random.shuffle(self.deck)



class Stack():

    def __init__(self):
        self.stack = []
        self = self.stack

    def show(self):
        lst = []
        for i in range(len(self.stack)):
            string = self.stack[i].show()
            lst.append(string)
        return lst

    def deal(self, n, pos=0):
        new_stack = []
        if n!=0:
            for _ in range(n):
                new_stack.append(self.stack.pop(0))
        else:
            new_stack.append(self.stack.pop(pos))

        return new_stack
    
    def add(self, lst):
        if isinstance(lst, Card):
            self.stack.append(lst)
        # elif type(lst) == Card():
        else:
            self.stack += lst



def compare(card, lst):
    playable = Stack()
    i=0
    while i!=len(lst.stack):
        if lst.stack[i].card['colour'] == card.card['colour']:
            playable.add(lst.deal(0, i)) #lst.deal(1, i)
        elif lst.stack[i].card['val'] == card.card['val']:
            playable.add(lst.deal(0, i))
        else:
            i+=1

    if len(playable.stack):
        return playable
    else:
        return 'None'




#--------------------------------------------------------------------------------
# Testing
#--------------------------------------------------------------------------------
# uno=UNO()
# uno.build_deck()
# stack = uno.deal(uno.deck, 7)
# uno.print_deck(stack)
# print("################")
# uno.print_deck(uno.deck)