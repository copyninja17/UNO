from src import config, button

def display(screen, roomSizeButtons, roomSizeButtonsFinal, roomSizeNames):
    for i in range(3):
        for j in range(3):
            if roomSizeButtons[i][j].draw(screen):
                # roomSizeButtons[i][j] = 
                roomSizeButtonsFinal[i][j].draw(screen)
                config.settings = roomSizeNames[i][j]
                print(f"roomsize: {config.settings}")
                config.buttonUpdate += 1