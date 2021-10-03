import subprocess, sys
from src import config

def hostPrompt(screen, createButton, joinButton):
    if createButton.draw(screen):
            print('CREATE SCRIPT')
            # subprocess.Popen([sys.executable, 'src/uno_client.py', '1'],
            #                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            config.Page = 1

    if joinButton.draw(screen):
        print('JOIN SCRIPT HERE')
        # subprocess.Popen([sys.executable, 'src/uno_client.py', '0'],
        #                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
        config.Page = 2

def enterRoomSize(screen, roomSizeButtons, roomSizeButtonsFinal, roomSizeNames):
    for i in range(3):
        for j in range(3):
            if roomSizeButtons[i][j].draw(screen):
                roomSizeButtons[i][j] = roomSizeButtonsFinal[i][j]
                selectedButton = roomSizeNames[i][j]
                print(selectedButton)
                config.waitQuit += 1