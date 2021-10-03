import pygame
from src import button
import subprocess, sys
import pygame_textinput

pygame.init()

# create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
TEXTBOX_WIDTH = 272
TEXTBOX_HEIGHT = 35

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO')

#load button images
createRoom = pygame.image.load('assets/textures/createroom.png').convert_alpha()
joinRoom = pygame.image.load('assets/textures/joinroom.png').convert_alpha()

#create button instances
createButton = button.Button(100, 200, createRoom, 0.4)
joinButton = button.Button(450, 200, joinRoom, 0.4)

#game loop
run = True

while run:

	screen.fill((202, 228, 241))
	events = pygame.event.get()

	if createButton.draw(screen):
		print('CREATE SCRIPT')
		subprocess.Popen([sys.executable, 'src/uno_client.py', '1'],
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)

	if joinButton.draw(screen):
		print('JOIN SCRIPT HERE')
		subprocess.Popen([sys.executable, 'src/uno_client.py', '0'],
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)

	for event in events:
		# quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()
	clock.tick(60)

pygame.quit()