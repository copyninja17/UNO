import uno_module as uno
from os import system

game = True
players = []

while game:
    n = uno.Input("Enter the number of players: ", int)
    for i in range(n):
        sample_dict = {'name':0, 'hand':0}
        p = input("Enter the name of player " + str(i+1) +  ": ")
        sample_dict['name'] = p
        players.append(sample_dict)

    system('cls')

    print("--------------------------------GAME STARTS------------------------------------")

    deck = uno.Deck()
    deck.shuffle()


    for i in range(n):
        stack = uno.Stack()
        stack.add(deck.deal(7))
        players[i]['hand'] = stack


    discard_pile = uno.Stack()
    discard_pile.add(deck.deal(1))

    assumed_colour = 'None'
    
    match = True
    while match:
        print("+" + "-"*(13+len(discard_pile.stack[-1].show())) + "+")
        print("|" + f" Top card = {discard_pile.stack[-1].show()} " + "|")
        print("+" + "-"*(13+len(discard_pile.stack[-1].show())) + "+")
        # print(f"DEBUG LINE: {assumed_colour}")
    

        print(f"Your turn {players[0]['name']}: {players[0]['hand'].show()}")
        
        playable_cards = uno.isplayable(discard_pile.stack[-1], players[0]['hand'], assumed_colour)

        if playable_cards != 'None':
            print(f"Playable cards: {playable_cards.show()}")
            q = True
            while q:
                played_card = uno.Input("Play a card: ", int)

                if played_card > 0 and played_card <= len(playable_cards.stack):
                    discard_pile.add(playable_cards.deal(0, played_card-1))
                    print(f"Card played: {discard_pile.stack[-1].show()}")

                    players[0]['hand'].add(playable_cards.stack)
                    q = False
                else:
                    print(f"Please enter a number between 1 and {len(playable_cards.stack)}")
            
        else:
            print("You have no playable cards")
            players[0]['hand'].add(deck.deal(1))
            print(f"Card drawn: {players[0]['hand'].stack[-1].show()}")
            players.append(players.pop(0))
            continue

        # game ends
        if len(players[0]['hand'].stack) == 0:
            print(f"Winner is {players[0]['name']}!!")
            match = False
            break

        # [order control code] keep these at end
        if uno.isaction(discard_pile.stack[-1]) == 'rev':
            players.reverse()
            print("Order reversed!")
        elif uno.isaction(discard_pile.stack[-1]) == 'skp':
            players.append(players.pop(0))
            players.append(players.pop(0))
            print(f"{players[-1]['name']}'s turn was skipped!")
        elif uno.isaction(discard_pile.stack[-1]) == '+2':
            players.append(players.pop(0))
            players.append(players.pop(0))
            players[-1]['hand'].add(deck.deal(2))
            print(f"{players[-1]['name']} drew 2 cards!")
        elif uno.isaction(discard_pile.stack[-1]) == '+4':
            assumed_colour = uno.colour_switch()
            print(f"Colour has been changed to {assumed_colour}!")
            players.append(players.pop(0))
            players.append(players.pop(0))
            players[-1]['hand'].add(deck.deal(4))
            print(f"{players[-1]['name']} drew 4 cards!")
        elif uno.isaction(discard_pile.stack[-1]) == 'wld':
            assumed_colour = uno.colour_switch()
            print(f"Colour has been changed to {assumed_colour}!")
            players.append(players.pop(0))

        else:
            players.append(players.pop(0))
        

    game = False