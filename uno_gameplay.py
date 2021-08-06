import uno_module as uno
from os import system

game = True
players = []

while game:
    n = int(input("Enter the number of players: "))
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
    
    match = True
    while match:
        for i in range(n):
            print(f"----------------Top card = {discard_pile.stack[-1].show()}---------------------")

            print(f"Your turn {players[i]['name']}: {players[i]['hand'].show()}")

            playable_cards = uno.compare(discard_pile.stack[-1], players[i]['hand'])

            if playable_cards != 'None':
                print(f"Playable cards: {playable_cards.show()}")
                q = True
                while q:
                    played_card = int(input("Play a card:"))

                    if played_card > 0 and played_card <= len(playable_cards.stack):
                        discard_pile.add(playable_cards.deal(0, played_card-1))
                        print(f"Card played: {discard_pile.stack[-1].show()}")

                        players[i]['hand'].add(playable_cards.stack)
                        q = False
                    else:
                        print(f"Please enter a number between 0 and {len(playable_cards.stack)}")
                
            else:
                print("You have no playable cards")
                players[i]['hand'].add(deck.deal(1))
                print(f"Card drawn: {players[i]['hand'].stack[-1].show()}")
            
            if len(players[i]['hand'].stack) == 0:
                print(f"Winner is {players[i]['name']}!!")
                match = False
                break
        

    game = False