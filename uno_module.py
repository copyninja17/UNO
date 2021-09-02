import random
import sys

class Card():

    def __init__(self):
        self.card = {'colour':0, 'val':0}
        self = self.card

    def generate(self, colour, value):
        self.card['colour'] = str(colour)
        self.card['val'] = str(value)

    def show(self):
        string = str(self.card['val']) + " of " + str(self.card['colour'])
        return string

    def conv(self):
        string = str(self.card['val']) + str(self.card['colour'])
        return string



class Deck():

    def __init__(self):
        self.colours = ['B', 'G', 'R', 'Y']
        self.values = ['1', '2', '3', '4', '5', '6', '7', '8' ,'9', 'skip', 'reverse', '+2']
        # self.special = ['wild', '+4']
        self.extras = ['0']
        self.deck = []
        self.build_deck()
        self = self.deck


    def build_deck(self):
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
        # for _ in range(4):
        #     for s in self.special:
        #         sample = Card()
        #         sample.generate('None', s)
        #         self.deck.append(sample)

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
    
    def add(self, lst):
        if isinstance(lst, Card):
            self.deck.append(lst)
        else:
            self.deck += lst

    def clear(self):
        self.deck.clear()
    
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
        else:
            self.stack += lst

    def clear(self):
        self.stack.clear()

    def conv(self):
        lst = []
        for i in self.stack:
            lst.append(i.conv())
        return ','.join(lst)



def isplayable(base_card, lst, assumed_colour='0'):
    playable = Stack()
    i=0
    while i!=len(lst.stack):
        if (lst.stack[i].card['colour'] in [base_card.card['colour'], 'None']) or (lst.stack[i].card['val'] in [base_card.card['val'], '+4', 'wild']) or (lst.stack[i].card['colour'] == assumed_colour and base_card.card['colour']=='None'):
            playable.add(lst.deal(0, i))
        else:
            i+=1

    if len(playable.stack):
        return playable
    else:
        return 'None'


def isaction(CARD):
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
        return 'none'

def Input(msg, input_type=str, min_len=1):
    while True:
        try:
            inp = input_type(input(msg))
            if len(inp)>min_len:
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

def colour_switch():
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

