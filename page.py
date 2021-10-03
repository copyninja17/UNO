import pygame
from src import button
import subprocess, sys
import pygame_textinput
from src import config

pygame.init()

#create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
TEXTBOX_WIDTH = 272
TEXTBOX_HEIGHT = 35
bPOsX = SCREEN_WIDTH/2
bPosY = SCREEN_HEIGHT/2

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO')

#load button images
sample_button = pygame.image.load('assets/textures/2.png').convert_alpha()
enterRoomSize_ = pygame.image.load('assets/textures/roomsize.png').convert_alpha()

enterRoomSize = button.Button(SCREEN_WIDTH/2-(enterRoomSize_.get_width()/2*0.4), SCREEN_HEIGHT/5, enterRoomSize_, 0.4)

roomSizeButtons = [[] for _ in range(3)]
roomSizeButtonsFinal = [[] for _ in range(3)]
roomSizeNames = [[] for _ in range(3)]

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

#game loop
run = True
config.waitQuit = 0

while run:

    screen.fill((202, 228, 241))
    events = pygame.event.get()

    for i in range(3):
        for j in range(3):
            if roomSizeButtons[i][j].draw(screen):
                roomSizeButtons[i][j] = roomSizeButtonsFinal[i][j]
                selectedButton = roomSizeNames[i][j]
                print(selectedButton)
                config.waitQuit += 1

    enterRoomSize.draw(screen)

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
