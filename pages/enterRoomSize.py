import sys
from src import config, button

def display(screen, roomSizeButtons, roomSizeButtonsFinal, roomSizeNames):
    for i in range(3):
        for j in range(3):
            if roomSizeButtons[i][j].draw(screen):
                # roomSizeButtons[i][j] = 
                roomSizeButtonsFinal[i][j].draw(screen)
                selectedButton = roomSizeNames[i][j]
                print(selectedButton)
                config.buttonUpdate += 1