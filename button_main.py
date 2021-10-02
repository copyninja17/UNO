import pygame
import button
import subprocess, sys	

#create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO')

#load button images
start_img = pygame.image.load('createroom.png').convert_alpha()
exit_img = pygame.image.load('joinroom.png').convert_alpha()

#create button instances
createButton = button.Button(100, 200, start_img, 0.4)
joinButton = button.Button(450, 200, exit_img, 0.4)

#game loop
run = True

while run:

	screen.fill((202, 228, 241))

	if createButton.draw(screen):
		print('CREATE SCRIPT')
		subprocess.Popen([sys.executable, 'uno_client.py', '1'],
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
		
	if joinButton.draw(screen):
		print('JOIN SCRIPT HERE')
		subprocess.Popen([sys.executable, 'uno_client.py', '0'],
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()