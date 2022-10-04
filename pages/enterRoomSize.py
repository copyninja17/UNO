from src import clientConfig as cc
import logging

logging.getLogger("client")

def display(screen, roomSizeButtons, roomSizeButtonsFinal, roomSizeNames):
    for i in range(3):
        for j in range(3):
            if roomSizeButtons[i][j].draw(screen):
                roomSizeButtonsFinal[i][j].draw(screen)
                cc.roomSize = roomSizeNames[i][j]
                print(f"roomsize: {cc.roomSize}")
                cc.buttonUpdate += 1