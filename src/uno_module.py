'''
A module designed to help with the development of UNO Card game.

Classes
-------
    Card: designed to handle Card objects.
    Deck: designed to handle Deck objects.
    Stack: designed to handle Stack objects.

Functions
---------
    isPlayable: Returns a list of playable cards.
    isAction: Returns the nature of card.
    Input: Custom Input function.
    colourSwitch: Prompts the user to choose a colour.
    pressEnterKey: Prompts the user to press 'Enter' key.
    isAI: [TODO]

'''

import random
import sys

class Card:

    def __init__(self):
        '''
        Creates a Card object.
        '''

        self.card = {'colour':0, 'val':0}
        self = self.card

    def generate(self, colour, value):
        '''
        Generats a 'Card' object.

        colour: colour of card
        value: face of card
        '''

        self.card['colour'] = str(colour)
        self.card['val'] = str(value)

    def show(self):
        '''
        Returns Card in a human readable format.
        '''

        string = str(self.card['val']) + " of " + str(self.card['colour'])
        return string

    def conv(self):
        string = str(self.card['val']) + str(self.card['colour'])
        return string



class Deck:
    
    def __init__(self):
        '''
        Creates a Deck object.
        '''

        self.colours = ['B', 'G', 'R', 'Y']
        self.values = ['1', '2', '3', '4', '5', '6', '7', '8' ,'9', 'skip', 'reverse', '+2']
        self.special = ['wild', '+4']
        self.extras = ['0']
        self.deck = []
        self.build_deck()
        self = self.deck


    def build_deck(self):
        '''
        Builds the deck according to values & colours.
        '''

        for _ in range(2):
            for c in self.colours:
                for v in self.values:
                    sample = Card()
                    sample.generate(c,v)
                    self.deck.append(sample)
        for c in self.colours:
            sample = Card()
            sample.generate(c, self.extras[0])
            self.deck.append(sample)
        for _ in range(4):
            for s in self.special:
                sample = Card()
                sample.generate('X', s)
                self.deck.append(sample)

    def show(self):
        '''
        Returns the Deck in a human readable format.
        '''

        lst = []
        for i in range(len(self.deck)):
            string = self.deck[i].show()
            lst.append(string)
        return lst

    def deal(self, n):
        '''
        Returns dealt cards from Deck.

        n: Number of cards to deal
        '''

        dealt_cards = []
        for _ in range(n):
            dealt_cards.append(self.deck.pop(0))
        return dealt_cards
    
    def add(self, lst):
        '''
        Adds cards to deck.

        lst: single card or list of cards to be added
        '''

        if isinstance(lst, Card):
            self.deck.append(lst)
        else:
            self.deck += lst

    def clear(self):
        '''
        Empties the Deck.
        '''

        self.deck.clear()
    
    def shuffle(self):
        '''
        Shuffles the Deck.
        '''

        random.shuffle(self.deck)



class Stack:

    def __init__(self):
        '''
        Creates an empty Stack object.
        '''
        self.stack = []
        self = self.stack

    def show(self):
        '''
        Returns the Stack in a human readable format.
        '''

        lst = []
        for i in range(len(self.stack)):
            string = self.stack[i].show()
            lst.append(string)
        return lst

    def deal(self, numOfCards, cardPos=0):
        '''
        Returns dealt cards from Stack.

        n: Number of cards to deal
        '''

        new_stack = []
        if numOfCards!=0:
            for _ in range(numOfCards):
                new_stack.append(self.stack.pop(0))
        else:
            new_stack.append(self.stack.pop(cardPos))

        return new_stack

    def add(self, lst):
        '''
        Adds cards to Stack.

        lst: single card or list of cards to be added
        '''

        if isinstance(lst, Card):
            self.stack.append(lst)
        else:
            self.stack += lst

    def clear(self):
        '''
        Empties the Stack.
        '''

        self.stack.clear()

    def conv(self):
        '''
        Returns a shorter format of Stack.
        '''

        lst = []
        for i in self.stack:
            lst.append(i.conv())
        return ','.join(lst)



def isPlayable(base_card, lst, assumed_colour='0'):
    '''
    Returns a Stack of playable cards based on top card and player's hand. If none, returns 'None'.

    base_card: top card
    lst: player's hand
    assumed_colour: chosen colour is case of a wild card
    '''

    playable = Stack()
    i=0
    while i!=len(lst.stack):
        if ((lst.stack[i].card['colour'] in [base_card.card['colour'], 'X']) or 
            (lst.stack[i].card['val'] in [base_card.card['val'], '+4', 'wild']) or 
            (lst.stack[i].card['colour'] == assumed_colour and base_card.card['colour']=='X')):
            playable.add(lst.deal(0, i))
        else:
            i+=1

    if len(playable.stack):
        return playable
    else:
        return 'None'


def isAction(CARD):
    '''
    Returns the nature of card. If not an action card, returns 'None'.

    CARD: a card object
    '''

    if CARD.card['val'] == 'reverse':
        return 'rev'
    elif CARD.card['val'] == 'skip':
        return 'skp'
    elif CARD.card['val'] == '+2':
        return '+2'
    elif CARD.card['val'] == '+4':
        return '+4'
    elif CARD.card['val'] == 'wild':
        return 'wld'
    else:
        return 'None'

def Input(msg, input_type=str, min_len=1):
    '''
    Custom input function with configurations.

    msg: message to be printed before input
    input_type: type of input
    min_len: minimum length of input
    '''
    
    while True:
        try:
            inp = input_type(input(msg))
            if len(str(inp))>=min_len:
                return inp
            else:
                BufferError
        except ValueError:
            print("Invalid input")
        except BufferError:
            print(f"Input should be atleast {min_len} characters long")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

def colourSwitch():
    '''
    Prompts the user to choose colour after playing a wild card. Returns R/B/G/Y.
    '''
    
    while True: 
        c = Input("Enter a colour: ", str)

        try:
            if c[0].upper() in ['R', 'B', 'G', 'Y']:
                return c[0].upper()
            else:
                raise ValueError
        except ValueError:
            print("Invalid input")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

def pressEnterKey():
    '''
    Press Enter Key to continue.
    '''

    print("Press 'Enter' to continue")
    while True:
        x = input()
        if x == '':
            break

# [TODO] Modify for use in current(GUI) version
def isAI():
    while True: 
        c = Input("Is this player computer? (Y/N): ", str)

        try:
            if c[0].upper() == 'Y':
                return True
            elif c[0].upper() == 'N':
                return False
            else:
                raise ValueError
        except ValueError:
            print("Invalid input")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

