import pygame
from src import button
import subprocess, sys
import pygame_textinput
from src import config
import hostPrompt, enterRoomSize

pygame.init()

# create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
TEXTBOX_WIDTH = 272
TEXTBOX_HEIGHT = 35
bPOsX = SCREEN_WIDTH/2
bPosY = SCREEN_HEIGHT/2

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO')


#-----------------------------------
# Host Prompt
#-----------------------------------
createRoom = pygame.image.load('assets/textures/createroom.png').convert_alpha()
joinRoom = pygame.image.load('assets/textures/joinroom.png').convert_alpha()

createButton = button.Button(100, 200, createRoom, 0.4)
joinButton = button.Button(450, 200, joinRoom, 0.4)


#-----------------------------------
# Room size
#-----------------------------------

# loading images
sample_button = pygame.image.load('assets/textures/2.png').convert_alpha()
enterRoomSize_ = pygame.image.load('assets/textures/roomsize.png').convert_alpha()

# Creating butttons
enterRoomSizeHeader = button.Button(SCREEN_WIDTH/2-(enterRoomSize_.get_width()/2*0.4), SCREEN_HEIGHT/5, enterRoomSize_, 0.4)

roomSizeButtons = [[] for _ in range(3)]
roomSizeButtonsFinal = [[] for _ in range(3)]
roomSizeNames = [[] for _ in range(3)]


# making room buttons
count = 2
for i in range(3):
    for j in range(3):
        roomSizeButtons[i].append(pygame.image.load(f'assets/textures/{count}.png').convert_alpha())
        roomSizeButtonsFinal[i].append(pygame.image.load(f'assets/textures/{count}final.png').convert_alpha())
        roomSizeNames[i].append(str(count))
        count+=1

w,h = -1.5*sample_button.get_width()*0.45,0

for i in range(3):
    for j in range(3):
        roomSizeButtons[i][j] = button.Button(bPOsX + w, bPosY + h, roomSizeButtons[i][j], 0.4)
        roomSizeButtonsFinal[i][j] = button.Button(bPOsX + w, bPosY + h, roomSizeButtonsFinal[i][j], 0.4)
        w += sample_button.get_width()*0.45
    w=-1.5*sample_button.get_width()*0.45
    h += sample_button.get_height()*0.45



#-----------------------------------
# Game Loop
#-----------------------------------
run = True
config.waitQuit = 0

while run:

    screen.fill((202, 228, 241))
    events = pygame.event.get()

    if config.Page == 0:
        hostPrompt.display(screen, createButton, joinButton)
    elif config.Page == 1:
        enterRoomSizeHeader.draw(screen)
        enterRoomSize.display(screen, roomSizeButtons, roomSizeButtonsFinal, roomSizeNames)

    for event in events:
        # quit game
        if event.type == pygame.QUIT:
            run = False
        if config.waitQuit == 2:
            pygame.time.wait(1000)
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()